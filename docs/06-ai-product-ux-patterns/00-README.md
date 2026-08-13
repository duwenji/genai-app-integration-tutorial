# 06. AI Product UX Patterns - AIプロダクトのUXパターン

01〜05章が「AIをどう呼び出すか」という統合設計を扱うのに対し、本章は
「ユーザーがAI機能をどう使い始め、どう操作し、どう調整するか」という
UI/UXレベルの設計パターンを扱います。

[Shape of AI](https://www.shapeof.ai/)の6カテゴリのうち、04章が扱う
Governors/Trust Builders（信頼・安全性）を除く4カテゴリ（Wayfinders /
Prompt Actions / Tuners / Identifiers、計37パターン）に対応します。

## 学習目標

- 初回プロンプト体験（テンプレート・提案）の空白キャンバス対策を設計できる
- ユーザーがAIに指示するアクション（開いた入力・対話継続等）を設計できる
- フィルタ・保存済みプリセット・モデル選択によるプロンプト調整UXを設計できる
- AIの存在をUI上で識別可能にする表現（命名・トーン等）を設計できる

## 教材一覧

| # | 教材 | 内容 |
|---|------|------|
| 01 | [オンボーディングと導線](01-onboarding-and-wayfinding.md) | 初回プロンプト体験の空白キャンバス対策 |
| 02 | [プロンプト操作アクション](02-prompt-action-patterns.md) | ユーザーがAIに指示する各種アクション |
| 03 | [調整とコンテキスト制御](03-tuning-and-context-control.md) | フィルタ・プリセット・モデル選択によるプロンプト調整 |
| 04 | [AIの識別とブランディング](04-ai-identity-and-branding.md) | AIの存在をUI上で識別可能にする表現 |

## 外部パターン対応

| Shape of AIカテゴリ | パターン | 対応教材 |
|---|---|---|
| [Wayfinders](https://www.shapeof.ai/) | Gallery, Follow up, Initial CTA, Nudges, Prompt details, Randomize, Suggestions, Templates（計8） | [01-onboarding-and-wayfinding.md](01-onboarding-and-wayfinding.md) |
| [Prompt Actions](https://www.shapeof.ai/) | Auto-fill, Chained action, Describe, Expand, Inline Action, Inpainting, Madlibs, Open input, Regenerate, Restructure, Restyle, Summary, Synthesis, Transform（計14） | [02-prompt-action-patterns.md](02-prompt-action-patterns.md) |
| [Tuners](https://www.shapeof.ai/) | Attachments, Connectors, Filters, Model management, Modes, Parameters, Preset styles, Prompt enhancer, Saved styles, Voice and tone（計10） | [03-tuning-and-context-control.md](03-tuning-and-context-control.md) |
| [Identifiers](https://www.shapeof.ai/) | Avatar, Color, Iconography, Name, Personality（計5） | [04-ai-identity-and-branding.md](04-ai-identity-and-branding.md) |

Shape of AIのGovernors/Trust Buildersは[04-trust-and-safety-ux](../04-trust-and-safety-ux/00-README.md)で扱います。

## 章の方針

`app/`に実装がある観点（テンプレート・提案・オープン入力・フィルタ確認・
戦略の保存/読込・LLMプロバイダ切替等）は実ソースコードを引用します。
実装が無い観点（Identifiers全般、Prompt Actionsの一部等）は、その旨を
明記した上で汎用サンプルコードで解説します。

---

[← 前へ: 05-agentic-workflow-patterns](../05-agentic-workflow-patterns/00-README.md) | [次へ: 07-real-world-case-study →](../07-real-world-case-study/00-README.md)
