# MASTER INDEX

**📢 対応状況**: ✅ 01〜07カテゴリ執筆完了

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
- [docs/02-io-contract-design/04-multi-turn-dialogue-prompting.md](docs/02-io-contract-design/04-multi-turn-dialogue-prompting.md) - マルチターン（対話型）プロンプトの設計

## 03. Reliability & Cost
- [docs/03-reliability-and-cost/00-README.md](docs/03-reliability-and-cost/00-README.md)
- [docs/03-reliability-and-cost/01-defensive-parsing-and-fallback.md](docs/03-reliability-and-cost/01-defensive-parsing-and-fallback.md) - 防御的パースとフォールバック設計
- [docs/03-reliability-and-cost/02-rate-limit-and-timeout.md](docs/03-reliability-and-cost/02-rate-limit-and-timeout.md) - レート制限・タイムアウト設計
- [docs/03-reliability-and-cost/03-caching-strategy.md](docs/03-reliability-and-cost/03-caching-strategy.md) - キャッシュ層の設計
- [docs/03-reliability-and-cost/04-batching-and-parallelization.md](docs/03-reliability-and-cost/04-batching-and-parallelization.md) - バッチ化・並列化によるコスト最適化
- [docs/03-reliability-and-cost/05-testing-llm-integrations.md](docs/03-reliability-and-cost/05-testing-llm-integrations.md) - LLM呼び出しのテスト（モック化）

## 04. Trust & Safety UX
- [docs/04-trust-and-safety-ux/00-README.md](docs/04-trust-and-safety-ux/00-README.md)
- [docs/04-trust-and-safety-ux/01-verification-checkpoint.md](docs/04-trust-and-safety-ux/01-verification-checkpoint.md) - 確認ステップ（Verificationパターン）
- [docs/04-trust-and-safety-ux/02-fact-and-opinion-separation.md](docs/04-trust-and-safety-ux/02-fact-and-opinion-separation.md) - 事実とAI考察の分離
- [docs/04-trust-and-safety-ux/03-guardrails-and-disclaimers.md](docs/04-trust-and-safety-ux/03-guardrails-and-disclaimers.md) - ガードレールと免責事項
- [docs/04-trust-and-safety-ux/04-prompt-injection-defense.md](docs/04-trust-and-safety-ux/04-prompt-injection-defense.md) - プロンプトインジェクション対策
- [docs/04-trust-and-safety-ux/05-transparency-and-control.md](docs/04-trust-and-safety-ux/05-transparency-and-control.md) - AIの処理経過・実行計画をユーザーに開示・制御させる設計
- [docs/04-trust-and-safety-ux/06-memory-privacy-and-provenance.md](docs/04-trust-and-safety-ux/06-memory-privacy-and-provenance.md) - AIの記憶・記録とプライバシー配慮の設計

## 05. Agentic Workflow Patterns
- [docs/05-agentic-workflow-patterns/00-README.md](docs/05-agentic-workflow-patterns/00-README.md)
- [docs/05-agentic-workflow-patterns/01-prompt-chaining.md](docs/05-agentic-workflow-patterns/01-prompt-chaining.md) - タスクを固定順序の複数LLM呼び出しに分解する
- [docs/05-agentic-workflow-patterns/02-routing.md](docs/05-agentic-workflow-patterns/02-routing.md) - 入力を分類し専用処理へ振り分ける
- [docs/05-agentic-workflow-patterns/03-orchestrator-workers.md](docs/05-agentic-workflow-patterns/03-orchestrator-workers.md) - 中央LLMが動的にサブタスクを委譲する
- [docs/05-agentic-workflow-patterns/04-evaluator-optimizer.md](docs/05-agentic-workflow-patterns/04-evaluator-optimizer.md) - 生成→評価→改善のループを設計する
- [docs/05-agentic-workflow-patterns/05-autonomous-agents.md](docs/05-agentic-workflow-patterns/05-autonomous-agents.md) - ワークフローと自律エージェントの違いと判断基準

## 06. AI Product UX Patterns
- [docs/06-ai-product-ux-patterns/00-README.md](docs/06-ai-product-ux-patterns/00-README.md)
- [docs/06-ai-product-ux-patterns/01-onboarding-and-wayfinding.md](docs/06-ai-product-ux-patterns/01-onboarding-and-wayfinding.md) - 初回プロンプト体験の空白キャンバス対策
- [docs/06-ai-product-ux-patterns/02-prompt-action-patterns.md](docs/06-ai-product-ux-patterns/02-prompt-action-patterns.md) - ユーザーがAIに指示する各種アクション
- [docs/06-ai-product-ux-patterns/03-tuning-and-context-control.md](docs/06-ai-product-ux-patterns/03-tuning-and-context-control.md) - フィルタ・プリセット・モデル選択によるプロンプト調整
- [docs/06-ai-product-ux-patterns/04-ai-identity-and-branding.md](docs/06-ai-product-ux-patterns/04-ai-identity-and-branding.md) - AIの存在をUI上で識別可能にする表現

## 07. Real World Case Study
- [docs/07-real-world-case-study/00-README.md](docs/07-real-world-case-study/00-README.md)
- [docs/07-real-world-case-study/01-case-study-map.md](docs/07-real-world-case-study/01-case-study-map.md) - 既存アプリ11箇所の統合パターン横断マッピング
- [docs/07-real-world-case-study/02-exercise-apply-to-your-app.md](docs/07-real-world-case-study/02-exercise-apply-to-your-app.md) - 自分のアプリへの適用演習
- [docs/07-real-world-case-study/03-operations-checklist.md](docs/07-real-world-case-study/03-operations-checklist.md) - 運用移行前チェックリスト
