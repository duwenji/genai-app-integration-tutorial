# 03. Reliability & Cost - 信頼性・コスト最適化

LLM呼び出しは失敗する・重複する・遅い、という前提で設計する必要があります。
このカテゴリでは、防御的パース＋フォールバック、キャッシュ層、
バッチ化・並列化、そしてLLM呼び出しのテスト方法を学びます。

## 学習目標

- 防御的パース＋フォールバックを実装できる
- キャッシュ層を設計できる
- バッチ化・並列化でコストを最適化できる
- LLM呼び出しをモック化してテストできる

## 教材一覧

| # | 教材 | 内容 |
|---|------|------|
| 01 | [防御的パースとフォールバック設計](01-defensive-parsing-and-fallback.md) | パース失敗時の機能ごとの安全な既定値 |
| 02 | [キャッシュ層の設計](02-caching-strategy.md) | 日次ファイルキャッシュによる再計算コスト削減 |
| 03 | [バッチ化・並列化](03-batching-and-parallelization.md) | 複数対象の並列処理と部分失敗への対処 |
| 04 | [LLM呼び出しのテスト](04-testing-llm-integrations.md) | 非決定的な呼び出しのモック化 |

## 外部パターン対応

並列化は、Anthropicの
[Building Effective Agents](https://www.anthropic.com/research/building-effective-agents)
が挙げる「Parallelization」パターンに対応します。

---

[← 前へ: 02-io-contract-design](../02-io-contract-design/00-README.md) | [次へ: 04-trust-and-safety-ux →](../04-trust-and-safety-ux/00-README.md)
