# 05. Agentic Workflow Patterns - エージェント型ワークフローパターン

「複数のLLM呼び出しをどう組み合わせるか」という、単一呼び出し（01〜04章）
の先にあるアーキテクチャ選択肢を学びます。

`app/`の生成AI活用11箇所のうち3箇所（バックテスト解説・AI質問箱・AI戦略
ビルダーの確定フロー）は、本章で扱うPrompt Chaining/Routing/
Evaluator-Optimizerパターンをそれぞれ実際に採用しています。残る8箇所は
「1回のAugmented LLM呼び出し」（01章）のままです。用途が単一銘柄・
単一レポート単位の考察生成にとどまる機能では、Anthropicが推奨する
「まず単純な構成から始める」原則のとおり、ワークフロー/エージェントの
複雑さを必要としないためです。本章のPrompt Chaining/Routing/
Evaluator-Optimizerの3教材は`app/`の実ソースコードを引用して解説し、
Orchestrator-WorkersとAutonomous Agentsの2教材は`app/`に実装例が
無いため汎用サンプルコードで解説します。

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

## 外部パターン対応

本章の全5パターンは、
[Anthropic "Building Effective Agents"](https://www.anthropic.com/research/building-effective-agents)
の呼称に対応します。同記事が挙げる6パターンのうちParallelizationは
既に03章[バッチ化・並列化](../03-reliability-and-cost/04-batching-and-parallelization.md)で
扱っているため、本章では対象外とします。

## 章の方針

各教材末尾の演習課題には、実アプリとの接点を保つ問いを必ず1問加えます。
`app/`に実装がある3パターン（Prompt Chaining/Routing/Evaluator-Optimizer）
では実装の設計判断を掘り下げる問いを、実装が無い2パターン
（Orchestrator-Workers/Autonomous Agents）では「このパターンを`app/`に
追加するならどこに使えそうか」という思考演習を扱います。

---

[← 前へ: 04-trust-and-safety-ux](../04-trust-and-safety-ux/00-README.md) | [次へ: 06-real-world-case-study →](../06-real-world-case-study/00-README.md)
