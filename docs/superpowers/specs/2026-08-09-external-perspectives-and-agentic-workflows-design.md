# 外部視点の取り込みとエージェント型ワークフロー章の新設 設計書

## 1. 背景・目的

`genai-app-integration-tutorial`は01〜05カテゴリの執筆が完了しているが、
以下の2つのギャップがある。

1. **外部の設計パターン視点の反映が薄い**。各教材は外部の確立された
   呼称を1回引用する程度に留まっており（例: 01章がAnthropic
   「Building Effective Agents」の"Augmented LLM"のみを引用）、
   同記事が定義する他のワークフローパターンや、OpenAI Agents SDK・
   プロダクション運用記事など他の情報源の視点が体系的に取り込まれて
   いない。
2. **参照アプリ`app/`の新機能が未反映**。ケーススタディ
   （`05-real-world-case-study/01-case-study-map.md`）が棚卸しする
   「生成AI活用9箇所」に、AI戦略ビルダー機能の対話型条件構築
   （`app/prompt_patterns/strategy_dialogue.py`）が含まれていない。
   これはステートレスな全履歴リプレイ方式のマルチターン対話という、
   現行02章（単発/バッチのみ）でも扱っていない設計パターンである。

本設計書は、Web調査で収集した外部視点を章立てに反映しつつ、上記の
実装ギャップを埋める改訂を行う。既存教材の全面書き換えは行わず、
**新規教材の追加・一部教材の並び替え・索引類の更新**に限定する。

## 2. 外部視点マッピング（今回の調査結果）

| 情報源 | 観点 | 本教材との対応 |
|---|---|---|
| Anthropic [Building Effective Agents](https://www.anthropic.com/research/building-effective-agents) | ワークフロー5パターン（Prompt Chaining/Routing/Parallelization/Orchestrator-Workers/Evaluator-Optimizer）+ 自律エージェント | Parallelizationは03章で対応済み。残る4パターン+自律エージェントを新設05章で扱う |
| OpenAI [Agents SDK](https://openai.github.io/openai-agents-python/agents/) | Handoff（会話全体を引き継ぐ制御移譲）、型付きGuardrail、Session/トレース | 05章のOrchestrator-Workers教材で「Anthropic版との違い」として補足引用に留める（別カテゴリは起こさない） |
| [Shape of AI](https://www.shapeof.ai/) | UXパターン集（Verification等） | 既存04章で引用済み。今回は追加引用なし |
| プロンプトインジェクション対策記事（[arXiv:2506.08837](https://arxiv.org/pdf/2506.08837) 等） | 入力フィルタ・system prompt防御・dual-LLM・型付きツール呼び出し | 新設`04-prompt-injection-defense.md`で扱う。`app/prompt_patterns/screening.py`の演算子/フィールドのホワイトリスト化が実例に相当 |
| LLM運用記事（[MLflow 2026 Guide](https://mlflow.org/articles/llm-application-architecture-a-2026-engineers-guide/) 等） | レート制限・タイムアウト設計、ガードレールの入力/出力二層構造 | 新設`03-rate-limit-and-timeout.md`、既存`04-03-guardrails-and-disclaimers.md`冒頭に二層構造の説明を追加 |
| ステートレスLLM会話設計記事 | 会話履歴を毎ターン全送信する設計、コストがターン数に比例して増える点 | 新設`02-04-multi-turn-dialogue-prompting.md`で扱う。`app/prompt_patterns/strategy_dialogue.py`が実例 |

各行の対応先教材には、該当する情報源へのリンクを「主要概念・設計判断の解説」内で明記する（`00_STYLE_GUIDE.md`の出典明記ルールに従う）。

## 3. 章立ての変更

```
01. Invocation & Architecture          （変更なし、3教材）
02. I/O Contract Design                （+1教材 → 4教材）
03. Reliability & Cost                 （+1教材、並び替え → 5教材）
04. Trust & Safety UX                  （+1教材 → 4教材）
05. Agentic Workflow Patterns  【新設】 （5教材）
06. Real World Case Study      （旧05を繰り下げ、内容更新）
```

新設05章はAnthropicのワークフロー5パターンのうちParallelization以外
（Prompt Chaining/Routing/Orchestrator-Workers/Evaluator-Optimizer）と、
自律エージェント（Autonomous Agents）を扱う。`app/`に実装例が無いため、
**汎用サンプルコード**（架空だが動作する最小コード）で解説する。

### 3.1 設計原則の改訂

`docs/00-COVER.md`の特徴3「実例として`ai-stock-investing-tutorial`の
完成版アプリ（`app/`）の実ソースコードを引用し、抽象論で終わらせない」を
以下に改訂する。

> 実例として、`app/`に実装があるものは実ソースコードを優先して引用する。
> `app/`に実装例が無いパターン（05章が該当）は、その旨を明記した上で
> 汎用サンプルコードで解説する。

`00_STYLE_GUIDE.md`の「2. 見出しの標準順序」補足と「8. レビュー用
チェックリスト」の出典明記ルールに、上記の例外規定を追記する。

## 4. 教材一覧（追加・変更分のみ）

### 02. I/O Contract Design（追加1教材）

| # | ファイル | 学習目標 | 主な参照ソース |
|---|----------|----------|-----------------|
| 04 | `04-multi-turn-dialogue-prompting.md` | ステートレスな全履歴リプレイ方式のマルチターン対話を設計でき、応答を「対話継続」と「確定出力」で分岐処理する契約を実装できる | `app/prompt_patterns/strategy_dialogue.py`、`app/app_tabs/strategy_builder_tab.py` |

### 03. Reliability & Cost（追加1教材、並び替え）

| # | ファイル（新番号） | 変更 |
|---|----------|------|
| 01 | `01-defensive-parsing-and-fallback.md` | 変更なし |
| 02 | `02-rate-limit-and-timeout.md`（新規） | レート制限エラー・タイムアウトへのリトライ/バックオフ設計。ROADMAP短期予定項目 |
| 03 | `03-caching-strategy.md`（旧02から改番） | 内容変更なし |
| 04 | `04-batching-and-parallelization.md`（旧03から改番） | 内容変更なし |
| 05 | `05-testing-llm-integrations.md`（旧04から改番） | 内容変更なし |

新規教材の主な参照ソース: `app/data_api/llm_client.py::call_llm`の
`timeout`引数（実例）を「タイムアウト設計」の入口として引用する。
`app/`にはリトライ/バックオフの実装が無いため、「レート制限時の
リトライ・指数バックオフ」の解説は汎用サンプルコードで補う
（その旨を明記する）。

### 04. Trust & Safety UX（追加1教材）

| # | ファイル | 学習目標 | 主な参照ソース |
|---|----------|----------|-----------------|
| 04 | `04-prompt-injection-defense.md` | 列挙値制約・ホワイトリスト化による攻撃面の縮小を実装でき、プロンプト内指示だけに頼る対策の限界を説明できる | `app/prompt_patterns/screening.py`（`_OPERATORS`ホワイトリスト、`eval`不使用） |

既存`03-guardrails-and-disclaimers.md`の「概要」直後に、入力側
（プロンプトインジェクション・PII等）/出力側（ポリシー違反・機密情報等）
の二層ガードレール構造を1段落で導入し、新設04教材への橋渡しとする。

### 05. Agentic Workflow Patterns（新設、5教材）

| # | ファイル | 学習目標 | 参照ソース |
|---|----------|----------|-----------|
| 00 | `00-README.md` | 章の位置づけと、`app/`に実装例が無い理由を理解する | Anthropic記事 |
| 01 | `01-prompt-chaining.md` | タスクを固定順序のLLM呼び出しに分解する設計を実装できる | 汎用サンプル |
| 02 | `02-routing.md` | 入力を分類し専用処理へ振り分ける設計を実装できる | 汎用サンプル |
| 03 | `03-orchestrator-workers.md` | 中央LLMが動的にサブタスクを分解・委譲する設計を説明できる（OpenAI Handoffとの違いを補足） | 汎用サンプル、OpenAI Agents SDK（補足引用） |
| 04 | `04-evaluator-optimizer.md` | 生成→評価→改善のループ設計を実装できる | 汎用サンプル |
| 05 | `05-autonomous-agents.md` | ワークフローと自律エージェントの違いを説明し、採用判断基準を持てる | Anthropic記事 |

各教材末尾の演習課題に「このパターンを`app/`に追加するならどこに
使えそうか」という思考演習を1問加え、実アプリとの接点を保つ
（実装は行わない）。

### 06. Real World Case Study（旧05、内容更新）

- `01-case-study-map.md`のマッピング表に10番目の項目
  「AI協調型戦略対話（`strategy_dialogue.py`）」を追加
  （呼び出し単位: マルチターン対話／フォールバック: 質問継続へのフォールバック／
  確認ステップ: なし）
- Mermaid図（`flowchart TB`）に02章のマルチターン対話ブロックを追加
- 「全9箇所に共通する設計」を「全10箇所に共通する設計」に更新
- 末尾に「エージェント型ワークフローパターン（05章）は本アプリでは
  未使用」という一文を追加し、05章との役割分担を明示
- `02-exercise-apply-to-your-app.md`の演習1（10番目の機能を追加する
  としたら、という設問）を、実装済みとなった10番目の機能を踏まえて
  11番目の機能を想定する設問に更新

## 5. 索引・参照ファイルの更新

- `README.md` / `MASTER-INDEX.md` / `docs/00-COVER.md`:
  カテゴリ数を5→6に、学習の流れ図（STEP 1-5→STEP 1-6）を更新
- `ROADMAP.md`: 短期予定2項目（レート制限・タイムアウト、
  プロンプトインジェクション対策）を完了に移動。中期予定から
  「エージェント型ワークフロー」の記載を削除（05章で対応済みのため）
- `QUICK-REFERENCE.md`の「用語対応表」に以下を追加

  | 本教材の用語 | 対応する外部の呼称 |
  |---|---|
  | マルチターン対話プロンプト | Stateless Multi-turn Conversation |
  | Prompt Chaining / Routing / Orchestrator-Workers / Evaluator-Optimizer | 同名（Anthropic） |
  | 自律エージェント | Autonomous Agents（Anthropic） |
  | プロンプトインジェクション対策 | Input/Output Guardrail（二層構造） |

- `00_STYLE_GUIDE.md`: 3.1節の設計原則改訂を反映

## 6. 執筆方針・図解計画

既存の`2026-08-08-genai-app-integration-design.md`の6節の方針
（7見出し構成、Mermaid形式、出典明記）を踏襲する。追加分の図解計画:

| ファイル | 図の種類 | 内容 |
|----------|----------|------|
| `02-04-multi-turn-dialogue-prompting.md` | `sequenceDiagram` | 各ターンで全履歴を再送する対話フローと分岐（質問継続/確定JSON） |
| `03-02-rate-limit-and-timeout.md` | `flowchart` | リトライ/バックオフの分岐フロー |
| `04-04-prompt-injection-defense.md` | `flowchart` | ホワイトリスト判定による安全な演算子適用の分岐 |
| `05-01-prompt-chaining.md` | `sequenceDiagram` | 固定順序の複数LLM呼び出しの流れ |
| `05-02-routing.md` | `flowchart` | 分類→専用処理への振り分け |
| `05-03-orchestrator-workers.md` | `flowchart` | 中央LLMによる動的なサブタスク委譲 |
| `05-04-evaluator-optimizer.md` | `sequenceDiagram` | 生成→評価→改善のループ |
| `06-01-case-study-map.md` | `flowchart`（既存図を更新） | 10箇所目のブロック追加 |

## 7. 完了条件・レビュー観点

- MASTER-INDEXの全リンクが実在するファイルを指している
  （改番したファイルの旧パスへのリンク切れが無いこと）
- 新設05章の各教材が「`app/`に実装例が無い」旨を明記している
- 06章のケーススタディ表が10箇所すべてを正しくマッピングしている
- `04-prompt-injection-defense.md`が引用する`screening.py`の
  コードが実際のリポジトリ内容と一致する
- QUICK-REFERENCE.mdの用語対応表に今回追加した全パターンが載っている
- `00_STYLE_GUIDE.md`8節のレビュー用チェックリストを満たす

## 8. スコープ外（本設計書では扱わない）

- RAG（検索拡張生成） → ROADMAP.md長期計画のまま、別設計書で扱う
- 評価ゲート・プロンプトのバージョン管理 → 同上
- `app/`（`ai-stock-investing-tutorial`側）への新機能実装
  → 今回は既存実装の教材化のみ。新パターンの実装例を追加する場合は
    別リポジトリ・別設計書で扱う
- トークン最適化（プロンプト圧縮・会話サマライズ）の独立教材化
  → `02-04-multi-turn-dialogue-prompting.md`内で「コストがターン数に
    比例して増える」点に触れるに留め、独立教材は次サイクルに送る
