# 生成AIをアプリケーションに統合する設計パターン

アプリケーションに生成AI（LLM）機能を組み込む際の**設計判断**を、
呼び出し方式の選定から入出力契約・信頼性・安全性のUXまで
体系的に学ぶ、エンジニア向け教材です。

特定ドメインに依存しない一般原則を中心に扱い、実例として
[ai-stock-investing-tutorial](https://github.com/duwenji/ai-stock-investing-tutorial/blob/master/README.md) の
完成版アプリ（`app/`）を随所でケーススタディとして参照します。

**📢 更新状況**: ✅ 01〜07カテゴリ執筆完了

- 全体索引: [MASTER-INDEX.md](MASTER-INDEX.md)
- スタイルガイド: [00_STYLE_GUIDE.md](00_STYLE_GUIDE.md)
- クイック参照: [QUICK-REFERENCE.md](QUICK-REFERENCE.md)
- 学習拡張計画: [ROADMAP.md](ROADMAP.md)

---

## 学習の進め方

1. [docs/00-COVER.md](docs/00-COVER.md) で全体像と学習目標を把握する
2. [docs/01-invocation-and-architecture/00-README.md](docs/01-invocation-and-architecture/00-README.md) で呼び出し方式とアーキテクチャ選定を学ぶ
3. [docs/02-io-contract-design/00-README.md](docs/02-io-contract-design/00-README.md) で入出力契約の設計を学ぶ
4. [docs/03-reliability-and-cost/00-README.md](docs/03-reliability-and-cost/00-README.md) で信頼性・コスト最適化の設計を学ぶ
5. [docs/04-trust-and-safety-ux/00-README.md](docs/04-trust-and-safety-ux/00-README.md) で信頼と安全性のUX設計を学ぶ
6. [docs/05-agentic-workflow-patterns/00-README.md](docs/05-agentic-workflow-patterns/00-README.md) で複数LLM呼び出しの組み合わせパターンを学ぶ
7. [docs/06-ai-product-ux-patterns/00-README.md](docs/06-ai-product-ux-patterns/00-README.md) でAIプロダクトのUXパターン（Shape of AI準拠）を学ぶ
8. [docs/07-real-world-case-study/00-README.md](docs/07-real-world-case-study/00-README.md) で実践ケーススタディに取り組む

---

## カテゴリ入口

- [docs/00-COVER.md](docs/00-COVER.md)
- [docs/01-invocation-and-architecture/00-README.md](docs/01-invocation-and-architecture/00-README.md)
- [docs/02-io-contract-design/00-README.md](docs/02-io-contract-design/00-README.md)
- [docs/03-reliability-and-cost/00-README.md](docs/03-reliability-and-cost/00-README.md)
- [docs/04-trust-and-safety-ux/00-README.md](docs/04-trust-and-safety-ux/00-README.md)
- [docs/05-agentic-workflow-patterns/00-README.md](docs/05-agentic-workflow-patterns/00-README.md)
- [docs/06-ai-product-ux-patterns/00-README.md](docs/06-ai-product-ux-patterns/00-README.md)
- [docs/07-real-world-case-study/00-README.md](docs/07-real-world-case-study/00-README.md)

## 関連教材

- [ai-stock-investing-tutorial](https://github.com/duwenji/ai-stock-investing-tutorial/blob/master/README.md) — 本教材でケーススタディとして参照する完成版アプリの元教材。プロンプト設計・分析エージェントの基礎はこちらで学べます。
