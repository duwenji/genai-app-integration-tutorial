# 生成AIアプリケーション統合パターン教材 設計書

## 1. 背景・目的

[ai-stock-investing-tutorial](https://github.com/duwenji/ai-stock-investing-tutorial/blob/master/README.md) の
完成版アプリ（`app/`）は、生成AI（Claude Code CLI）を9箇所で活用しており、
バッチ処理・構造化出力＋防御的パース・キャッシュ・確認ステップ・
事実とAI考察の分離など、複数のカテゴリにまたがる設計パターンを
実践している。しかし、これらは既存教材（01-fundamentals〜06-real-world-examples）
に分散しており、横断的にまとめた教材は存在しない。

また、既存の `docs/03-data-api/02-llm-api-integration.md` は
Anthropic/OpenAIの**SDK + APIキー**方式のみを扱っており、`app/`が
採用している**CLIサブプロセス方式**（APIキー不要）は未解説である。

本教材は、これらのギャップを埋めるとともに、特定ドメイン（株投資）に
依存しない**汎用の生成AI統合設計パターン教材**として独立させる。
ai-stock-investing-tutorialの`app/`はケーススタディとして参照するのみで、
本教材自体はどのアプリケーションにも応用できる原則を主軸に据える。

## 2. 対象読者・前提

- Pythonでの開発経験があり、アプリに生成AI機能を組み込みたいエンジニア
- LLM APIの最小コードは書けるが、本番品質（信頼性・コスト・安全性）の
  設計判断に自信がない層
- ai-stock-investing-tutorial受講者（未受講でも進行可能な自己完結構成にする）

## 3. 外部知見との対応づけ（章立ての裏付け）

Web調査により、以下の確立された呼称・分類に対応づけて章立てを設計した。

| 本教材のカテゴリ | 対応する外部の呼称・出典 |
|---|---|
| 01. Invocation & Architecture | Augmented LLM（[Anthropic “Building Effective Agents”](https://www.anthropic.com/research/building-effective-agents)） |
| 02. I/O Contract Design | 構造化出力バリデーション（[LLM Deployment Best Practices 2026](https://futureagi.com/blog/llm-deployment-best-practices-2026/), [MLflow LLM Application Architecture](https://mlflow.org/articles/llm-application-architecture-a-2026-engineers-guide/)） |
| 03. Reliability & Cost | Parallelizationパターン（Anthropic）／キャッシュ層パターン（GPTCache等の実務記事） |
| 04. Trust & Safety UX | Verification / Human-in-the-loopパターン（[Shape of AI](https://www.shapeof.ai/patterns/verification), [Zapier: Human-in-the-loop](https://zapier.com/blog/human-in-the-loop/)）／Guardrails（Anthropic） |
| 05. Real World Case Study | css-tutorialの `05-real-world-examples` に相当する総仕上げカテゴリ |

各カテゴリの `00-README.md` には、対応する外部呼称と出典リンクを明記する。

## 4. リポジトリ構成

`css-tutorial` を参考に、ルート直下に独立した教材リポジトリを作成する
（`ai-stock-investing-tutorial` とは別のgitリポジトリ）。

```
genai-app-integration-tutorial/
  README.md
  00_STYLE_GUIDE.md
  MASTER-INDEX.md
  QUICK-REFERENCE.md
  ROADMAP.md
  CONTRIBUTING.md
  LICENSE
  .gitignore / .gitattributes
  docs/
    00-COVER.md
    01-invocation-and-architecture/
    02-io-contract-design/
    03-reliability-and-cost/
    04-trust-and-safety-ux/
    05-real-world-case-study/
    superpowers/specs/   # 本設計書の格納先
```

上記のうち、ルート直下ファイル・`docs/00-COVER.md` は本設計書と同時に
scaffold済み（後述5節参照）。`docs/0X-*/` 配下の教材本文は、本設計書の
承認後、別途 `writing-plans` スキルで実装計画を立てて作成する。

## 5. 教材一覧と学習目標

### 01. Invocation & Architecture（呼び出し方式とアーキテクチャ選定）

| # | ファイル | 学習目標 | 主な参照ソース |
|---|----------|----------|-----------------|
| 01 | `01-augmented-llm-building-block.md` | LLM単体呼び出しを拡張する「Augmented LLM」という基本単位を理解し、ワークフロー/エージェントとの違いを説明できる | Anthropic記事（外部） |
| 02 | `02-api-sdk-vs-cli-subprocess.md` | API直叩き/SDK/CLIサブプロセスの3方式を比較し、鍵管理要否・実行環境に応じて選定できる | `app/data_api/llm_client.py`、既存教材`03-data-api/02-llm-api-integration.md`（対比） |
| 03 | `03-system-prompt-and-io-boundary.md` | システムプロンプトで出力形式を制御し、認証・鍵管理の設計判断を説明できる | `app/data_api/llm_client.py` の `_SYSTEM_PROMPT` |

### 02. I/O Contract Design（入出力契約の設計）

| # | ファイル | 学習目標 | 主な参照ソース |
|---|----------|----------|-----------------|
| 01 | `01-structured-output-json-contract.md` | JSON構造化出力を指示し、コードフェンス除去からパースまでの契約を設計できる | `app/common/json_parsing.py`、`app/prompt_patterns/screening.py` |
| 02 | `02-single-vs-batch-prompting.md` | 単発呼び出しとバッチ呼び出しの使い分け基準を説明できる | `app/analysis_agents/news_research_agent.py`、`app/stock_detail/detail.py`（対比） |
| 03 | `03-prompt-scope-and-constraints.md` | 出力可能なフィールド・値域をプロンプトで限定する設計を実装できる | `app/prompt_patterns/screening.py::build_screening_prompt` |

### 03. Reliability & Cost（信頼性・コスト最適化）

| # | ファイル | 学習目標 | 主な参照ソース |
|---|----------|----------|-----------------|
| 01 | `01-defensive-parsing-and-fallback.md` | パース失敗時のフォールバック設計（機能ごとの安全な既定値）を実装できる | `app/prompt_patterns/screening.py`、`app/portfolio_management/review.py` |
| 02 | `02-caching-strategy.md` | 日次/TTLベースのキャッシュ層を設計し、再計算コストを削減できる | `app/common/cache.py`、`app/app_tabs/shared.py` |
| 03 | `03-batching-and-parallelization.md` | 複数対象の処理をバッチ化・並列化し、呼び出しオーバーヘッドを削減できる（Parallelizationパターン） | `app/common/concurrency.py::map_concurrently` |
| 04 | `04-testing-llm-integrations.md` | 非決定的なLLM呼び出しをモック化し、外部通信なしでテストできる | `app/tests/test_llm_client.py` |

### 04. Trust & Safety UX（信頼と安全性のUX設計）

| # | ファイル | 学習目標 | 主な参照ソース |
|---|----------|----------|-----------------|
| 01 | `01-verification-checkpoint.md` | AIの解釈結果をユーザーに確認させてから適用するUI設計ができる（Verificationパターン） | `app/app_tabs/screening_tab.py`（`st.json`確認ステップ） |
| 02 | `02-fact-and-opinion-separation.md` | プログラムで計算した「事実」とAIの「考察」を表示上分離する設計ができる | `app/portfolio_management/review.py`、`app/prompt_patterns/report_generation.py` |
| 03 | `03-guardrails-and-disclaimers.md` | プロンプトでの禁止事項明示と免責事項の必須表示を実装できる | `app/common/disclaimer.py`、各`prompt_patterns/*.py` |

### 05. Real World Case Study（実践：既存アプリの統合パターン横断分析）

| # | ファイル | 学習目標 | 主な参照ソース |
|---|----------|----------|-----------------|
| 01 | `01-case-study-map.md` | `app/`内9箇所の生成AI活用箇所を01〜04の観点でマッピングした一覧表を読み解ける | `app/docs/app-design.md`（既存設計書） |
| 02 | `02-exercise-apply-to-your-app.md` | 01〜04で学んだ設計判断を、自分のアプリの新機能に適用する演習に取り組める | （演習、実装なし） |

## 6. 執筆方針

- 各教材ファイルは `00_STYLE_GUIDE.md` の7見出し構成
  （身につくこと/概要/位置づけ/主要概念/実ソースコード/演習課題/理解度チェック）に従う
- 実ソースコード欄は `app/` からの引用に必ず出典パスを明記する
  （新規に架空のコード例を書く場合は「サンプル」であることを明示する）
- 外部の確立されたパターン名を各教材の「概要」または「主要概念」で
  必ず1回は明示し、独自用語だけで説明を終わらせない
- 01〜04は汎用原則、05はそれを実アプリで確認するケーススタディという
  役割分担を崩さない（05に新しい原則を持ち込まない）
- 図（アーキテクチャ比較・処理フロー）は`00_STYLE_GUIDE.md`の
  「6. 図表ルール」に従い、すべてMermaid形式で記載する（画像化しない）

### 6.1 図解計画

| ファイル | 図の種類 | 内容 |
|----------|----------|------|
| `01-02-api-sdk-vs-cli-subprocess.md` | `flowchart` | API直叩き/SDK/CLIサブプロセスの3方式のコンポーネント関係比較 |
| `01-03-system-prompt-and-io-boundary.md` | `sequenceDiagram` | システムプロンプト付与からLLM応答取得までの流れ |
| `02-01-structured-output-json-contract.md` | `sequenceDiagram` | プロンプト送信→JSON応答→コードフェンス除去→パースの流れ |
| `03-01-defensive-parsing-and-fallback.md` | `flowchart` | パース成功/失敗の分岐とフォールバック先 |
| `03-02-caching-strategy.md` | `sequenceDiagram` | キャッシュヒット/ミス判定の流れ（`app/common/cache.py`ベース） |
| `03-03-batching-and-parallelization.md` | `sequenceDiagram` | `map_concurrently`による並列取得の流れ |
| `04-01-verification-checkpoint.md` | `sequenceDiagram` | AI解釈→ユーザー確認→適用の流れ（`app_tabs/screening_tab.py`ベース） |
| `05-01-case-study-map.md` | `flowchart` | `app/`内9箇所の生成AI活用箇所と01〜04カテゴリの対応関係の俯瞰図 |

上記以外の教材は表・箇条書きで十分伝わる内容のため、図は必須としない
（教材執筆時に必要と判断すれば追加してよい）。

## 7. 完了条件・レビュー観点

- MASTER-INDEXの全リンクが実在するファイルを指している
- 各教材が対応する外部パターン名を明記している
- `app/`引用箇所の出典パスが実在し、内容と矛盾しない
- スタイルガイドのレビュー用チェックリスト（8節）を満たす
- 6.1節で図解計画のある教材にMermaidコードブロックが存在し、
  記法エラーがない（コードブロック言語指定 `mermaid` を確認）
- 05章のケーススタディが投資助言と誤解されない表現になっている
  （該当箇所は[ai-stock-investing-tutorialの免責事項](https://github.com/duwenji/ai-stock-investing-tutorial/blob/master/DISCLAIMER.md)にリンク）

## 8. スコープ外（本設計書では扱わない）

- エージェント型ワークフロー（Routing/Orchestrator-Workers/Evaluator-Optimizer）の解説
  → ROADMAP.mdの中期計画に記載済み、別設計書で扱う
- RAG（検索拡張生成）
  → ROADMAP.mdの長期計画に記載済み、別設計書で扱う
- 評価ゲート・プロンプトのバージョン管理の詳細実装
  → ROADMAP.mdの長期計画に記載済み、別設計書で扱う
