# 生成AIをアプリケーションに統合する設計パターン教材 - 全体像

## このチュートリアルで身につくこと

- API直叩き/SDK/CLIサブプロセスという呼び出し方式の選定基準
- システムプロンプト・構造化出力（JSON）による入出力契約の設計力
- 防御的パース・キャッシュ・バッチ化によるコスト最適化の実装力
- 確認ステップ・事実とAI考察の分離によるユーザー向け安全性設計力
- 既存アプリの生成AI活用箇所を、設計パターンの観点で分析する力

## 対象読者

- Pythonでの開発経験があり、アプリに生成AI機能を組み込みたいエンジニア
- LLM APIの最小コードは書けるが、本番品質（信頼性・コスト・安全性）の
  設計判断に自信がない方
- [ai-stock-investing-tutorial](../../ai-stock-investing-tutorial/README.md) を
  一通り終え、完成版アプリ（`app/`）の設計意図を体系的に理解したい方

## 学習の流れ

```
STEP 1 ──→ Invocation & Architecture（3教材）
             Augmented LLMという基本単位・呼び出し方式の選定・
             システムプロンプトによる出力制御

STEP 2 ──→ I/O Contract Design（3教材）
             構造化出力の契約設計・単発/バッチ呼び出し・出力範囲の限定

STEP 3 ──→ Reliability & Cost（4教材）
             防御的パース・キャッシュ層・バッチ化/並列化・テスト（モック化）

STEP 4 ──→ Trust & Safety UX（3教材）
             確認ステップ（Verification）・事実とAI考察の分離・
             ガードレールと免責事項

STEP 5 ──→ Real World Case Study（2教材）
             既存アプリ9箇所の統合パターン横断分析・自分のアプリへの適用演習
```

## 前提知識

| 知識 | 要否 |
|------|------|
| Python基本文法（関数・クラス・パッケージ管理） | ✅ 必須 |
| REST API・JSONの基本理解 | ✅ 必須 |
| LLM APIの最小呼び出し経験（`anthropic`/`openai` SDK等） | 🔶 推奨 |
| [ai-stock-investing-tutorial](../../ai-stock-investing-tutorial/README.md) の受講経験 | 🔶 推奨（未受講でも進行可） |

## 本チュートリアルの特徴

1. 特定ドメインに依存しない**一般的な設計パターン**を軸に構成する
2. 各パターンは、Anthropicの公開資料や実務記事など**外部の確立された呼称**に対応づける
3. 実例として [ai-stock-investing-tutorial](../../ai-stock-investing-tutorial/README.md) の
   完成版アプリ（`app/`）の実ソースコードを引用し、抽象論で終わらせない
4. 最終章では、既存アプリの生成AI活用箇所を横断的に棚卸しし、
   自分のアプリへの適用演習に取り組む

---
