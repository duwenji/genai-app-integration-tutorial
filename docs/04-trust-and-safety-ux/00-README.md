# 04. Trust & Safety UX - 信頼と安全性のUX設計

生成AIは、もっともらしく見えて実は誤った情報を返すことがあります（この現象を「ハルシネーション」と呼びます）。
また、ユーザー入力に紛れ込んだ悪意ある指示文（プロンプトインジェクション）で、意図しない出力を引き出されることもあります。
さらに、AIが何を記憶し、何を記録しているかが不透明だと、ユーザーは安心して使えません。
このカテゴリでは、こうした失敗からユーザーを守るための設計を、6つの教材に分けて学びます。
具体的には、AIの提案をユーザーに確認させるUI設計、事実とAI考察の分離、ガードレールと免責事項、プロンプトインジェクション対策、処理経過の開示、そして記憶・プライバシーへの配慮を扱います。

## 学習目標

- 確認ステップ（Verificationパターン）を実装できる
- 事実とAI考察を分離できる
- ガードレールと免責事項を実装できる
- プロンプトインジェクション対策（列挙値制約・ホワイトリスト化）を実装できる
- AIの処理経過・実行計画を開示し、ユーザーが制御できるUXを設計できる
- AIが何を記憶・記録するかを設計し、プライバシーに配慮したUXを実装できる

## 教材一覧

| # | 教材 | 内容 | 防ぐ失敗例 |
|---|------|------|------------|
| 01 | [確認ステップ（Verificationパターン）](01-verification-checkpoint.md) | AIの解釈結果を確認させてから適用する設計 | AIの誤解釈が気づかれずに実データへ反映される |
| 02 | [事実とAI考察の分離](02-fact-and-opinion-separation.md) | 計算はプログラム、考察はAIという役割分担 | AIが誤った数値をもっともらしく生成する（ハルシネーション） |
| 03 | [ガードレールと免責事項](03-guardrails-and-disclaimers.md) | 禁止事項の明示と機械的な注記付与 | 出力が越えてはいけない境界（投資助言化等）を越える |
| 04 | [プロンプトインジェクション対策](04-prompt-injection-defense.md) | 列挙値制約・ホワイトリスト化による攻撃面の縮小 | 入力に紛れた指示文でLLMの役割が書き換えられる |
| 05 | [透明性と制御](05-transparency-and-control.md) | 実行前後のAI処理をユーザーに開示・制御させる設計 | 何が実行されたか分からず、ユーザーが不安・不信になる |
| 06 | [記憶・プライバシー・来歴](06-memory-privacy-and-provenance.md) | AIの記憶・記録とプライバシー配慮の設計 | 何が記憶・記録されているか不透明で、プライバシー上の懸念が残る |

## 外部パターン対応

[Shape of AI](https://www.shapeof.ai/)は、生成AI UXの確立されたパターン集を公開しているサイトです。
「Governors」はAIの挙動をユーザーが把握・制御できるようにするパターン群、「Trust Builders」はAIへの信頼を築くためのパターン群を指します。
Governors（13パターン）・Trust Builders（7パターン）の全20パターンが、本章6教材のいずれかに対応します。

| Shape of AIカテゴリ | パターン | 対応教材 |
|---|---|---|
| Governors | [Verification](https://www.shapeof.ai/patterns/verification) | [01-verification-checkpoint.md](01-verification-checkpoint.md) |
| Governors | [Sample response](https://www.shapeof.ai/patterns/sample-response) | [01-verification-checkpoint.md](01-verification-checkpoint.md) |
| Trust Builders | [Caveat](https://www.shapeof.ai/patterns/caveat) | [03-guardrails-and-disclaimers.md](03-guardrails-and-disclaimers.md) |
| Trust Builders | [Disclosure](https://www.shapeof.ai/patterns/disclosure) | [03-guardrails-and-disclaimers.md](03-guardrails-and-disclaimers.md) |
| Governors | Action plan, Branches, Citations, Controls, Cost estimates, Draft mode, References, Stream of Thought, Variations | [05-transparency-and-control.md](05-transparency-and-control.md) |
| Governors | Memory, Shared vision | [06-memory-privacy-and-provenance.md](06-memory-privacy-and-provenance.md) |
| Trust Builders | Consent, Data ownership, Footprints, Incognito Mode, Watermark | [06-memory-privacy-and-provenance.md](06-memory-privacy-and-provenance.md) |

事実とAI考察の分離（02章）・プロンプトインジェクション対策（04章）は、Shape of AIに直接対応するパターン名が無いため対応表から除く。

---

[← 前へ: 03-reliability-and-cost](../03-reliability-and-cost/00-README.md) | [次へ: 05-agentic-workflow-patterns →](../05-agentic-workflow-patterns/00-README.md)
