# 06. AI Product UX Patterns - AIプロダクトのUXパターン

バックエンドを主に書いてきたエンジニアがAI機能のUIを実装すると、次のような場面でよくつまずきます。

- ユーザーが画面を開いても、何を入力すればいいか分からず離脱する
- ボタンを押すとLLM呼び出しが発生するのか、事前に判断できない
- 表示された文章が、AIの発言なのか人間が書いた文章なのか分からない

これらはAPIの呼び出し方（01〜05章）を正しく実装するだけでは解決しません。
ユーザーが画面上でAI機能を「見つけ・操作し・信頼する」体験そのものを設計する必要があるからです。
この体験設計を、本教材ではUI/UXパターンと呼びます。

01〜05章が「AIをどう呼び出すか」という統合設計を扱うのに対し、本章は「ユーザーがAI機能をどう使い始め、どう操作し、どう調整するか」というUI/UXレベルの設計パターンを扱います。

[Shape of AI](https://www.shapeof.ai/)は、こうしたAI UXパターンを6カテゴリ・57パターンに整理した外部カタログです。
本章はそのうち、04章が扱うGovernors/Trust Builders（信頼・安全性に関わるパターン群）を除く4カテゴリ（Wayfinders / Prompt Actions / Tuners / Identifiers、計37パターン）に対応します。

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

各カテゴリが「ユーザーのどんな困りごとに答えるか」を先に押さえると、個別パターン名が覚えやすくなります。

| Shape of AIカテゴリ | ひとことで言うと | パターン | 対応教材 |
|---|---|---|---|
| [Wayfinders](https://www.shapeof.ai/) | 最初の一歩をどう案内するか | Gallery, Follow up, Initial CTA, Nudges, Prompt details, Randomize, Suggestions, Templates（計8） | [01-onboarding-and-wayfinding.md](01-onboarding-and-wayfinding.md) |
| [Prompt Actions](https://www.shapeof.ai/) | 入力後にどんな操作を提供するか | Auto-fill, Chained action, Describe, Expand, Inline Action, Inpainting, Madlibs, Open input, Regenerate, Restructure, Restyle, Summary, Synthesis, Transform（計14） | [02-prompt-action-patterns.md](02-prompt-action-patterns.md) |
| [Tuners](https://www.shapeof.ai/) | 生成の前後で何を調整できるか | Attachments, Connectors, Filters, Model management, Modes, Parameters, Preset styles, Prompt enhancer, Saved styles, Voice and tone（計10） | [03-tuning-and-context-control.md](03-tuning-and-context-control.md) |
| [Identifiers](https://www.shapeof.ai/) | AIの発言だと一目で分かるか | Avatar, Color, Iconography, Name, Personality（計5） | [04-ai-identity-and-branding.md](04-ai-identity-and-branding.md) |

Shape of AIのGovernors（実行の透明性・制御）とTrust Builders（信頼性の補強）は、AI出力の「正しさ・安全性」寄りのパターン群です。
これらは[04-trust-and-safety-ux](../04-trust-and-safety-ux/00-README.md)で扱います。

## 章の方針

`app/`に実装がある観点（テンプレート・提案・オープン入力・フィルタ確認・戦略の保存/読込・LLMプロバイダ切替等）は実ソースコードを引用します。
実装が無い観点（Identifiers全般、Prompt Actionsの一部等）は、その旨を明記した上で汎用サンプルコードで解説します。
汎用サンプルコードは「実装すればこうなる」という設計イメージを示すためのものであり、`app/`に実在するコードではありません。
各教材の該当箇所で必ずその旨を明記します。

---

[← 前へ: 05-agentic-workflow-patterns](../05-agentic-workflow-patterns/00-README.md) | [次へ: 07-real-world-case-study →](../07-real-world-case-study/00-README.md)
