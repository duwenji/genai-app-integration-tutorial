# 01. Invocation & Architecture - 呼び出し方式とアーキテクチャ選定

アプリに生成AI機能を組み込む最初の設計判断は、「LLMをどう呼び出すか」です。
このカテゴリでは、LLM呼び出しの基本単位（Augmented LLM）を理解したうえで、
API直叩き/SDK方式とCLIサブプロセス方式を比較し、システムプロンプトによる
出力制御・認証設計まで学びます。

## 学習目標

- LLM単体呼び出しを拡張する「Augmented LLM」という基本単位を説明できる
- API直叩き/SDK方式とCLIサブプロセス方式を比較し、選定基準を説明できる
- システムプロンプトによる出力制御と、認証・鍵管理の設計判断を説明できる

## 教材一覧

| # | 教材 | 内容 |
|---|------|------|
| 01 | [Augmented LLMという基本単位](01-augmented-llm-building-block.md) | LLM呼び出しの基本単位とワークフロー/エージェントとの違い |
| 02 | [SDK方式 vs CLIサブプロセス方式](02-api-sdk-vs-cli-subprocess.md) | 2つの呼び出し方式の比較と選定基準 |
| 03 | [システムプロンプトと入出力の境界](03-system-prompt-and-io-boundary.md) | 出力制御の仕組みと認証設計 |

## 外部パターン対応

「Augmented LLM」は、Anthropicの
[Building Effective Agents](https://www.anthropic.com/research/building-effective-agents)
で使われている呼称です。本カテゴリの内容はこの記事の分類に沿っています。

---

[← 前へ: 00-COVER](../00-COVER.md) | [次へ: 02-io-contract-design →](../02-io-contract-design/00-README.md)
