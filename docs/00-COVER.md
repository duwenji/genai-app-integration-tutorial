# 生成AIをアプリケーションに統合する設計パターン - 全体像

生成AI（テキストを入力すると応答テキストを返すAIモデル。以下LLMと呼びます。Large Language Modelの略）を1回呼び出すだけなら、数行のコードで動きます。
しかし実際のアプリに組み込むとなると、呼び出し方式の選び方・失敗時の挙動・コストの制御・ユーザーへの見せ方など、公式ドキュメントや入門記事だけでは学びにくい設計判断が次々に出てきます。
本チュートリアルは、こうした「動くコードの次」に必要な設計判断を体系立てて学ぶための教材です。

| 情報源 | 主な内容 | 本チュートリアルとの違い |
|---|---|---|
| 公式SDK/APIドキュメント | 1回の呼び出し方法・パラメータ仕様 | 呼び出し後の設計判断（信頼性・コスト・UX）は扱わない |
| 一般的なLLM入門記事 | プロンプトの書き方・モデル比較 | 実アプリへの組み込み設計（例外処理・キャッシュ等）は扱わない |
| 本チュートリアル | 実アプリ（`app/`）の設計判断を汎用パターン化して解説 | 「動くコード」だけでなく「なぜその設計か」に焦点を当てる |

## このチュートリアルで身につくこと

- API直叩き/SDK/CLIサブプロセスという呼び出し方式の選定基準
- システムプロンプト・構造化出力（JSON）による入出力契約の設計力
- 防御的パース・キャッシュ・バッチ化によるコスト最適化の実装力
- 確認ステップ・事実とAI考察の分離によるユーザー向け安全性設計力
- 既存アプリの生成AI活用箇所を、設計パターンの観点で分析する力
- 複数LLM呼び出しの組み合わせパターン（Prompt Chaining/Routing/Orchestrator-Workers/Evaluator-Optimizer）を理解し、単発呼び出しとの使い分けを判断する力

## 対象読者

- Pythonでの開発経験があり、アプリに生成AI機能を組み込みたいエンジニア
- LLM APIの最小コードは書けるが、本番品質（信頼性・コスト・安全性）の設計判断に自信がない方
- [ai-stock-investing-tutorial](https://github.com/duwenji/ai-stock-investing-tutorial/blob/master/README.md) を一通り終え、完成版アプリ（`app/`）の設計意図を体系的に理解したい方

## 学習の流れ

```
STEP 1 ──→ Invocation & Architecture（3教材）
             Augmented LLMという基本単位・呼び出し方式の選定・
             システムプロンプトによる出力制御

STEP 2 ──→ I/O Contract Design（4教材）
             構造化出力の契約設計・単発/バッチ呼び出し・出力範囲の限定・
             マルチターン（対話型）プロンプトの設計

STEP 3 ──→ Reliability & Cost（5教材）
             防御的パース・レート制限とタイムアウト・キャッシュ層・
             バッチ化/並列化・テスト（モック化）

STEP 4 ──→ Trust & Safety UX（4教材）
             確認ステップ（Verification）・事実とAI考察の分離・
             ガードレールと免責事項・プロンプトインジェクション対策

STEP 5 ──→ Agentic Workflow Patterns（5教材）
             Prompt Chaining・Routing・Orchestrator-Workers・
             Evaluator-Optimizer・Autonomous Agents

STEP 6 ──→ AI Product UX Patterns（4教材）
             Shape of AIの残り4カテゴリ（Wayfinders/Prompt Actions/
             Tuners/Identifiers）に対応するUI/UXレベルの設計パターン

STEP 7 ──→ Real World Case Study（2教材）
             既存アプリ11箇所の統合パターン横断分析・自分のアプリへの適用演習・
             01〜06すべての設計判断を一括点検する運用移行前チェックリスト
```

## 前提知識

「LLM APIの最小呼び出し経験」とは、`anthropic`や`openai`のSDK、またはWeb上のプレイグラウンドで、プロンプト文字列を送って応答文字列を受け取るだけの1回限りのコードを書いたことがある、という程度の経験を指します。
未経験でも、02章の実ソースコードを見ながら進行できます。

| 知識 | 要否 |
|------|------|
| Python基本文法（関数・クラス・パッケージ管理） | ✅ 必須 |
| REST API・JSONの基本理解 | ✅ 必須 |
| LLM APIの最小呼び出し経験（`anthropic`/`openai` SDK等） | 🔶 推奨 |
| [ai-stock-investing-tutorial](https://github.com/duwenji/ai-stock-investing-tutorial/blob/master/README.md) の受講経験 | 🔶 推奨（未受講でも進行可） |

## 本チュートリアルの特徴

1. 特定ドメインに依存しない**一般的な設計パターン**を軸に構成する
2. 各パターンは、Anthropicの公開資料や実務記事など**外部の確立された呼称**に対応づける
3. 実例として、`app/`に実装があるものは実ソースコードを優先して引用する。`app/`に実装例が無いパターン（05章・06章の一部が該当）は、その旨を明記した上で汎用サンプルコードで解説し、抽象論で終わらせない
4. 最終章では、既存アプリの生成AI活用箇所を横断的に棚卸しし、自分のアプリへの適用演習に取り組む

---
