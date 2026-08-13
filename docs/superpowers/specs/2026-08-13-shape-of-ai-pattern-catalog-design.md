# Shape of AI 全パターンの体系的統合 設計書

## 1. 背景・目的

[Shape of AI](https://www.shapeof.ai/)（Emily Campbell氏によるAI UXパターン集、
6カテゴリ・全57パターン）は、本教材の04章で"Verification"パターンを
1件引用済みだが、それ以外の56パターンは未整理のまま残っている。

本設計書は、Shape of AIの全57パターンを次の2グループに分類し、
既存の教材構成に体系的に統合する。

1. **本教材が既に扱う設計判断と対応するパターン**（Governors 13 /
   Trust Builders 7 = 20パターン）: `04-trust-and-safety-ux`
   カテゴリの既存4教材＋新設2教材で対応づける
2. **本教材が未着手の、プロンプト構築〜AI識別のUXパターン**
   （Wayfinders 8 / Prompt Actions 14 / Tuners 10 / Identifiers 5
   = 37パターン）: 新設`07-ai-product-ux-patterns`カテゴリ（4教材）
   で新規に教材化する

既存教材の全面書き換えは行わない。**新規教材の追加・既存カテゴリの
「外部パターン対応」節の拡充・索引類の更新**に限定する。

## 2. Shape of AI 全パターンマッピング

### 2.1 Governors / Trust Builders → 04章（既存4教材＋新設2教材）

| Shape of AIカテゴリ | パターン | 対応先教材 | 状態 |
|---|---|---|---|
| Governors | Verification | `01-verification-checkpoint.md` | 対応済み（既存） |
| Governors | Sample response | `01-verification-checkpoint.md`（補足） | 今回追記 |
| Trust Builders | Caveat | `03-guardrails-and-disclaimers.md` | 今回追記 |
| Trust Builders | Disclosure | `03-guardrails-and-disclaimers.md` | 今回追記 |
| Governors | Action plan | `05-transparency-and-control.md`（新設） | 今回新規 |
| Governors | Branches | `05-transparency-and-control.md`（新設） | 今回新規 |
| Governors | Citations | `05-transparency-and-control.md`（新設） | 今回新規 |
| Governors | Controls | `05-transparency-and-control.md`（新設） | 今回新規 |
| Governors | Cost estimates | `05-transparency-and-control.md`（新設） | 今回新規 |
| Governors | Draft mode | `05-transparency-and-control.md`（新設） | 今回新規 |
| Governors | References | `05-transparency-and-control.md`（新設） | 今回新規 |
| Governors | Stream of Thought | `05-transparency-and-control.md`（新設） | 今回新規 |
| Governors | Variations | `05-transparency-and-control.md`（新設） | 今回新規 |
| Governors | Memory | `06-memory-privacy-and-provenance.md`（新設） | 今回新規 |
| Governors | Shared vision | `06-memory-privacy-and-provenance.md`（新設） | 今回新規 |
| Trust Builders | Consent | `06-memory-privacy-and-provenance.md`（新設） | 今回新規 |
| Trust Builders | Data ownership | `06-memory-privacy-and-provenance.md`（新設） | 今回新規 |
| Trust Builders | Footprints | `06-memory-privacy-and-provenance.md`（新設） | 今回新規 |
| Trust Builders | Incognito Mode | `06-memory-privacy-and-provenance.md`（新設） | 今回新規 |
| Trust Builders | Watermark | `06-memory-privacy-and-provenance.md`（新設） | 今回新規 |

既存`02-fact-and-opinion-separation.md`・`04-prompt-injection-defense.md`は
Shape of AIに直接対応するパターン名が無いため、追記対象としない
（現状のまま）。

### 2.2 Wayfinders / Prompt Actions / Tuners / Identifiers → 07章（新設4教材）

| Shape of AIカテゴリ | パターン | 対応先教材 |
|---|---|---|
| Wayfinders | Gallery, Follow up, Initial CTA, Nudges, Prompt details, Randomize, Suggestions, Templates（計8） | `01-onboarding-and-wayfinding.md` |
| Prompt Actions | Auto-fill, Chained action, Describe, Expand, Inline Action, Inpainting, Madlibs, Open input, Regenerate, Restructure, Restyle, Summary, Synthesis, Transform（計14） | `02-prompt-action-patterns.md` |
| Tuners | Attachments, Connectors, Filters, Model management, Modes, Parameters, Preset styles, Prompt enhancer, Saved styles, Voice and tone（計10） | `03-tuning-and-context-control.md` |
| Identifiers | Avatar, Color, Iconography, Name, Personality（計5） | `04-ai-identity-and-branding.md` |

以上で57パターン全件が既存4教材＋新設6教材のいずれかに対応づけられる。

## 3. 章立ての変更

```
01. Invocation & Architecture          （変更なし、3教材）
02. I/O Contract Design                （変更なし、4教材）
03. Reliability & Cost                 （変更なし、5教材）
04. Trust & Safety UX                  （+2教材 → 6教材）
05. Agentic Workflow Patterns          （変更なし、5教材）
06. Real World Case Study              （変更なし、2教材）
07. AI Product UX Patterns    【新設】 （4教材）
```

## 4. 教材一覧（追加分）

### 04. Trust & Safety UX（追加2教材）

| # | ファイル | 学習目標 | 主な参照ソース |
|---|----------|----------|-----------------|
| 05 | `05-transparency-and-control.md` | AIの実行計画・処理経過・複数候補をユーザーに開示し、途中で制御できるUXを設計できる | `strategy_builder_tab.py`のパイプライン実行トレース（`st.caption(" → ".join(trace))`）を部分的な実例として引用し、対応する実装が無い観点（Cost estimates, Draft mode, Variations等）は汎用サンプルコードで補う |
| 06 | `06-memory-privacy-and-provenance.md` | AIが何を記憶し、何を証跡として残すかを設計し、プライバシー配慮のUXを実装できる | `common/ai_generation_log.py`（`facts`/`ai_output`分離記録、`session_id`単位の追跡）をFootprintsの実例として引用。Memory/Consent/Data ownership/Incognito Mode/Watermarkは`app/`に実装例が無いため汎用サンプルコードで補う |

`00-README.md`の「外部パターン対応」節を拡充し、上表2.1の全対応関係を
表形式で追記する。

### 07. AI Product UX Patterns（新設、4教材）

| # | ファイル | 学習目標 | 主な参照ソース |
|---|----------|----------|-----------------|
| 00 | `00-README.md` | 章の位置づけと、Shape of AI 4カテゴリとの対応を理解する | Shape of AI |
| 01 | `01-onboarding-and-wayfinding.md` | 初回プロンプト体験（テンプレート・提案・空白キャンバス対策）を設計できる | `strategy_builder_tab.py`の`_TEMPLATES`（Templates）、業種ローテーション提案（Suggestions）、投資アイデア入力欄（Initial CTA） |
| 02 | `02-prompt-action-patterns.md` | ユーザーがAIに指示するアクション（開いた入力・対話継続等）を設計できる | `qa_tab.py`のOpen input、`strategy_builder_tab.py`の対話継続（Chained action相当） |
| 03 | `03-tuning-and-context-control.md` | フィルタ・保存済みプリセット・モデル選択によるプロンプト調整UXを設計できる | `screening_tab.py`のFilters（AI解釈条件の`st.json`確認）、`strategy_builder/storage.py`のSaved styles相当（戦略の保存/読込）、`data_api/llm_client.py`のModel management相当（`llm_provider`設定） |
| 04 | `04-ai-identity-and-branding.md` | AIの存在をUI上で識別可能にする表現（命名・トーン等）を設計できる | `app/`に実装例が無いため汎用サンプルコードで解説 |

各教材は`00_STYLE_GUIDE.md`所定の見出し順
（身につくこと→概要→位置づけ→主要概念・設計判断→実ソースコード→
演習課題→理解度チェック）に従う。`app/`に実装例が無い観点は、既存の
例外規定（`00_STYLE_GUIDE.md` 2節補足）に従い「本教材のサンプルコードは
`app/`に実装例が無いため、汎用サンプルコードで解説します。」と明記する。

## 5. 索引・参照ファイルの更新

- `README.md` / `MASTER-INDEX.md` / `docs/00-COVER.md`: カテゴリ数を
  6→7に、学習の流れ図（STEP 1-6→STEP 1-7）を更新
- `ROADMAP.md`: ステータス表に07行を追加、04行の教材数を4→6に更新
- `QUICK-REFERENCE.md`:
  - 「信頼と安全性のUXチェックリスト（04章）」に05・06教材分の
    観点を追加
  - 「用語対応表」にShape of AI全57パターン中、今回追記・新設した
    パターン名（Sample response, Caveat, Disclosure, Action plan,
    Branches, Citations, Controls, Cost estimates, Draft mode,
    References, Stream of Thought, Variations, Memory, Shared vision,
    Consent, Data ownership, Footprints, Incognito Mode, Watermark,
    および07章の37パターン）を追加
  - 新節「AIプロダクトUXパターンの選び方（07章）」を追加

## 6. 執筆方針・図解計画

既存の`2026-08-08-genai-app-integration-design.md`・
`2026-08-09-external-perspectives-and-agentic-workflows-design.md`の
方針（7見出し構成、Mermaid形式、出典明記、良い例/悪い例対比）を踏襲する。

| ファイル | 図の種類 | 内容 |
|----------|----------|------|
| `04-05-transparency-and-control.md` | `flowchart` | 実行計画の提示→処理経過の開示→ユーザーによる途中制御の分岐 |
| `04-06-memory-privacy-and-provenance.md` | `flowchart` | 記録対象（facts/ai_output）とアクセス範囲（誰が何を見られるか）の分岐 |
| `07-01-onboarding-and-wayfinding.md` | `flowchart` | 空白キャンバス→テンプレート/提案→初回プロンプト送信までの導線 |
| `07-02-prompt-action-patterns.md` | `sequenceDiagram` | ユーザーのアクション選択→プロンプト構築→再生成/継続の流れ |
| `07-03-tuning-and-context-control.md` | `flowchart` | フィルタ解釈の確認→適用、プリセット保存/読込の分岐 |
| `07-04-ai-identity-and-branding.md` | `flowchart` | AI識別要素（名前・アイコン・トーン）がUIのどこに現れるかの対応図 |

## 7. 完了条件・レビュー観点

- Shape of AI全57パターンが、本設計書の対応表（2.1・2.2）のいずれかに
  過不足なく対応づけられている
- MASTER-INDEXの全リンクが実在するファイルを指している
- 07章の各教材が「Shape of AIのどのカテゴリ・パターンに対応するか」を
  本文中で明記している
- `app/`に実装例が無い観点は、その旨を明記した上で汎用サンプルコードで
  解説している（実装が無いのに実ソースを装う記述が無い）
- `04-transparency-and-control.md`が引用する`strategy_builder_tab.py`・
  `04-memory-privacy-and-provenance.md`が引用する`ai_generation_log.py`の
  コードが実際のリポジトリ内容と一致する
- QUICK-REFERENCE.mdの用語対応表に今回追加した全パターンが載っている
- `00_STYLE_GUIDE.md` 8節のレビュー用チェックリストを満たす

## 8. スコープ外（本設計書では扱わない）

- `app/`（`ai-stock-investing-tutorial`側）への新機能実装
  → 今回は既存実装の教材化・汎用サンプルコードでの解説のみ。
    Cost estimates・Variations・Watermark等、実装が無いパターンを
    実際に`app/`へ追加する提案は別リポジトリ・別設計書で扱う
- RAG・評価ゲート・プロンプトのバージョン管理・トークン最適化
  → ROADMAP.md長期計画のまま、別設計書で扱う
- 05章（Agentic Workflow Patterns）・06章（Real World Case Study）の
  内容変更 → 今回のスコープはShape of AIパターンの統合のみ
