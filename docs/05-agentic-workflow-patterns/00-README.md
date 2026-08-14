# 05. Agentic Workflow Patterns - エージェント型ワークフローパターン

01〜04章で学んだのは、1回のLLM呼び出し（Augmented LLM呼び出し）を安全・高品質にする方法でした。
しかし、タスクによっては1回の呼び出しだけでは対応しきれない場合があります。
たとえば「複数の手順を順番にこなす必要がある」「入力の種類によって扱いを変えたい」「生成した結果を自分で評価し、基準を満たすまで改善したい」といったケースです。

「複数のLLM呼び出しをどう組み合わせるか」という、単一呼び出し（01〜04章）の先にあるアーキテクチャ選択肢を学びます。
本章で登場する用語を先に整理します。

| 用語 | 意味 |
|---|---|
| ワークフロー | あらかじめ決めた経路（コード）で複数のLLM呼び出しを組み合わせる設計 |
| オーケストレーター | 他のLLM呼び出しや処理（ワーカー）に指示を出す中央の役割を持つLLM |
| ワーカー | オーケストレーターから委譲され、個別のサブタスクを担当するLLM呼び出しや関数 |
| 評価者ループ | 生成結果を別のLLM呼び出しが評価し、基準を満たすまで再生成を繰り返す仕組み |
| 自律エージェント | 次に何をするかをLLM自身が都度判断しながらツールを使うループ |

`app/`の生成AI活用11箇所のうち3箇所（バックテスト解説・AI質問箱・AI戦略ビルダーの確定フロー）は、本章で扱うPrompt Chaining/Routing/Evaluator-Optimizerパターンをそれぞれ実際に採用しています。
さらにAI戦略ビルダーの確定フローは、対話LLMがスクリーニング/ランキング関数を動的に選んで実行順を決めるOrchestrator-Workersパターンも同時に採用しています（Evaluator-Optimizerは確定候補への自動評価・改善ループ、Orchestrator-Workersは候補生成自体のワーカー選定という別の局面で組み合わさっています）。
残る8箇所は「1回のAugmented LLM呼び出し」（01章）のままです。
用途が単一銘柄・単一レポート単位の考察生成にとどまる機能では、Anthropicが推奨する「まず単純な構成から始める」原則のとおり、ワークフロー/エージェントの複雑さを必要としないためです。
本章のPrompt Chaining/Routing/Orchestrator-Workers/Evaluator-Optimizerの4教材は`app/`の実ソースコードを引用して解説し、Autonomous Agentsの1教材のみ`app/`に実装例が無いため汎用サンプルコードで解説します。

## 学習目標

- Prompt Chainingでタスクを固定順序のLLM呼び出しに分解できる
- Routingで入力を分類し専用処理へ振り分けられる
- Orchestrator-Workersで中央LLMが動的にサブタスクを委譲する設計を説明できる
- Evaluator-Optimizerで生成→評価→改善のループを実装できる
- ワークフローと自律エージェントの違いを説明し、採用判断基準を持てる

## 教材一覧

| # | 教材 | 内容 |
|---|------|------|
| 01 | [Prompt Chaining](01-prompt-chaining.md) | タスクを固定順序の複数LLM呼び出しに分解する |
| 02 | [Routing](02-routing.md) | 入力を分類し専用処理へ振り分ける |
| 03 | [Orchestrator-Workers](03-orchestrator-workers.md) | 中央LLMが動的にサブタスクを委譲する |
| 04 | [Evaluator-Optimizer](04-evaluator-optimizer.md) | 生成→評価→改善のループを設計する |
| 05 | [Autonomous Agents](05-autonomous-agents.md) | ワークフローと自律エージェントの違いと判断基準 |

5パターンの違いは初学者には混同しやすいため、次の早見表で整理します。
各教材の「主要概念・設計判断の解説」でも、直前のパターンとの違いを表で詳しく比較します。

| パターン | トリガー条件 | 制御フロー | 向いている場面 | つまずきやすい点 |
|---|---|---|---|---|
| Prompt Chaining | タスクが固定順序のサブタスクに分解できる | コードが決めた順序で逐次呼び出す | 精度重視で、各ステップの検証（gate）が有効 | ステップ数が増えるとレイテンシ・コストが線形に増える |
| Routing | 入力の意図・カテゴリが明確に分かれる | コードが分類結果で1つの経路に分岐する | カテゴリごとに専用処理する方が精度が上がる | 誤分類や未知ラベルへのフォールバック設計が必須 |
| Orchestrator-Workers | サブタスクの数・組み合わせを事前に予測できない | 中央LLMが動的にサブタスクを決定し委譲する | 対話ごとに必要な処理の組み合わせが変わる | 中央LLMの出力が壊れた場合の防御的処理が必須 |
| Evaluator-Optimizer | 出力に明確な評価基準があり反復改善が効く | 生成→評価→（不合格なら）改善のループ | 品質基準を明文化できるタスク | 終了条件を設計しないと無限ループ・コスト増になる |
| Autonomous Agents | 実行経路を事前にコード化できない開放的な問題 | LLM自身が次の行動を都度判断する | 探索的なタスク、対話的なツール利用 | 予測可能性・コストが下がるため採用は慎重に判断する |

## 外部パターン対応

本章の全5パターンは、[Anthropic "Building Effective Agents"](https://www.anthropic.com/research/building-effective-agents)の呼称に対応します。
同記事が挙げる6パターンのうちParallelizationは既に03章[バッチ化・並列化](../03-reliability-and-cost/04-batching-and-parallelization.md)で扱っているため、本章では対象外とします。

## 章の方針

各教材末尾の演習課題には、実アプリとの接点を保つ問いを必ず1問加えます。
`app/`に実装がある4パターン（Prompt Chaining/Routing/Orchestrator-Workers/Evaluator-Optimizer）では実装の設計判断を掘り下げる問いを、実装が無いAutonomous Agentsでは「このパターンを`app/`に追加するならどこに使えそうか」という思考演習を扱います。

---

[← 前へ: 04-trust-and-safety-ux](../04-trust-and-safety-ux/00-README.md) | [次へ: 06-ai-product-ux-patterns →](../06-ai-product-ux-patterns/00-README.md)
