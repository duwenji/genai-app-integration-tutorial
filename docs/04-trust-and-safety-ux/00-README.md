# 04. Trust & Safety UX - 信頼と安全性のUX設計

生成AIの出力は誤りを含みえます。このカテゴリでは、AIの提案をユーザーに
確認させるUI設計、事実とAI考察の分離、そしてガードレールと免責事項の
実装方法を学びます。

## 学習目標

- 確認ステップ（Verificationパターン）を実装できる
- 事実とAI考察を分離できる
- ガードレールと免責事項を実装できる

## 教材一覧

| # | 教材 | 内容 |
|---|------|------|
| 01 | [確認ステップ（Verificationパターン）](01-verification-checkpoint.md) | AIの解釈結果を確認させてから適用する設計 |
| 02 | [事実とAI考察の分離](02-fact-and-opinion-separation.md) | 計算はプログラム、考察はAIという役割分担 |
| 03 | [ガードレールと免責事項](03-guardrails-and-disclaimers.md) | 禁止事項の明示と機械的な注記付与 |

## 外部パターン対応

確認ステップは[Shape of AIのVerificationパターン](https://www.shapeof.ai/patterns/verification)、
事実/考察分離や禁止事項の明示は、Anthropicが言及する「Guardrails」の考え方に対応します。

---

[← 前へ: 03-reliability-and-cost](../03-reliability-and-cost/00-README.md) | [次へ: 05-real-world-case-study →](../05-real-world-case-study/00-README.md)
