# 02. I/O Contract Design - 入出力契約の設計

LLM呼び出しの方式（01章）を決めたら、次は「LLMに何を渡し、
何を返させるか」という入出力契約の設計です。このカテゴリでは、
構造化出力（JSON）の契約設計、単発/バッチ呼び出しの使い分け、
出力範囲の限定方法を学びます。

## 学習目標

- JSON構造化出力の契約を設計できる
- 単発呼び出しとバッチ呼び出しを使い分けられる
- 出力範囲（フィールド・値域）をプロンプトで限定できる
- マルチターン（対話型）プロンプトを設計できる

## 教材一覧

| # | 教材 | 内容 |
|---|------|------|
| 01 | [構造化出力（JSON）の契約設計](01-structured-output-json-contract.md) | JSON出力の指示とパースの二段構え |
| 02 | [単発呼び出し vs バッチ呼び出し](02-single-vs-batch-prompting.md) | 使い分けの基準とコストの考え方 |
| 03 | [出力範囲の限定と禁止事項](03-prompt-scope-and-constraints.md) | フィールド・値域を限定する設計 |
| 04 | [マルチターン（対話型）プロンプトの設計](04-multi-turn-dialogue-prompting.md) | ステートレスな全履歴リプレイ方式の対話設計 |

---

[← 前へ: 01-invocation-and-architecture](../01-invocation-and-architecture/00-README.md) | [次へ: 03-reliability-and-cost →](../03-reliability-and-cost/00-README.md)
