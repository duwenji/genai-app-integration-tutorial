# MASTER INDEX

**📢 対応状況**: ✅ 01〜05カテゴリ執筆完了

## Top Level
- [README.md](README.md)
- [00_STYLE_GUIDE.md](00_STYLE_GUIDE.md)
- [QUICK-REFERENCE.md](QUICK-REFERENCE.md)
- [ROADMAP.md](ROADMAP.md)

## Cover
- [docs/00-COVER.md](docs/00-COVER.md)

## 01. Invocation & Architecture
- [docs/01-invocation-and-architecture/00-README.md](docs/01-invocation-and-architecture/00-README.md)
- [docs/01-invocation-and-architecture/01-augmented-llm-building-block.md](docs/01-invocation-and-architecture/01-augmented-llm-building-block.md) - Augmented LLMという基本単位とワークフロー/エージェントの違い
- [docs/01-invocation-and-architecture/02-api-sdk-vs-cli-subprocess.md](docs/01-invocation-and-architecture/02-api-sdk-vs-cli-subprocess.md) - API直叩き/SDK/CLIサブプロセス方式の比較と選定基準
- [docs/01-invocation-and-architecture/03-system-prompt-and-io-boundary.md](docs/01-invocation-and-architecture/03-system-prompt-and-io-boundary.md) - システムプロンプトによる出力制御と認証・鍵管理

## 02. I/O Contract Design
- [docs/02-io-contract-design/00-README.md](docs/02-io-contract-design/00-README.md)
- [docs/02-io-contract-design/01-structured-output-json-contract.md](docs/02-io-contract-design/01-structured-output-json-contract.md) - JSON構造化出力の契約設計
- [docs/02-io-contract-design/02-single-vs-batch-prompting.md](docs/02-io-contract-design/02-single-vs-batch-prompting.md) - 単発/バッチ呼び出しの設計
- [docs/02-io-contract-design/03-prompt-scope-and-constraints.md](docs/02-io-contract-design/03-prompt-scope-and-constraints.md) - 出力範囲の限定と禁止事項の明示

## 03. Reliability & Cost
- [docs/03-reliability-and-cost/00-README.md](docs/03-reliability-and-cost/00-README.md)
- [docs/03-reliability-and-cost/01-defensive-parsing-and-fallback.md](docs/03-reliability-and-cost/01-defensive-parsing-and-fallback.md) - 防御的パースとフォールバック設計
- [docs/03-reliability-and-cost/02-caching-strategy.md](docs/03-reliability-and-cost/02-caching-strategy.md) - キャッシュ層の設計
- [docs/03-reliability-and-cost/03-batching-and-parallelization.md](docs/03-reliability-and-cost/03-batching-and-parallelization.md) - バッチ化・並列化によるコスト最適化
- [docs/03-reliability-and-cost/04-testing-llm-integrations.md](docs/03-reliability-and-cost/04-testing-llm-integrations.md) - LLM呼び出しのテスト（モック化）

## 04. Trust & Safety UX
- [docs/04-trust-and-safety-ux/00-README.md](docs/04-trust-and-safety-ux/00-README.md)
- [docs/04-trust-and-safety-ux/01-verification-checkpoint.md](docs/04-trust-and-safety-ux/01-verification-checkpoint.md) - 確認ステップ（Verificationパターン）
- [docs/04-trust-and-safety-ux/02-fact-and-opinion-separation.md](docs/04-trust-and-safety-ux/02-fact-and-opinion-separation.md) - 事実とAI考察の分離
- [docs/04-trust-and-safety-ux/03-guardrails-and-disclaimers.md](docs/04-trust-and-safety-ux/03-guardrails-and-disclaimers.md) - ガードレールと免責事項

## 05. Real World Case Study
- [docs/05-real-world-case-study/00-README.md](docs/05-real-world-case-study/00-README.md)
- [docs/05-real-world-case-study/01-case-study-map.md](docs/05-real-world-case-study/01-case-study-map.md) - 既存アプリ9箇所の統合パターン横断マッピング
- [docs/05-real-world-case-study/02-exercise-apply-to-your-app.md](docs/05-real-world-case-study/02-exercise-apply-to-your-app.md) - 自分のアプリへの適用演習
