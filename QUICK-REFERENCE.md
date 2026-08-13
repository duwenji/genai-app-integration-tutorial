# クイックリファレンス

チュートリアル全体で扱う設計パターンの早見表です。詳細は各教材を参照してください。

## 呼び出し方式の比較（01章）

| 方式 | 認証 | 向いているケース |
|------|------|-------------------|
| API直叩き（SDK） | APIキー必須 | サーバー環境、レート制御を自前で持ちたい場合 |
| CLIサブプロセス | ログイン済みCLIに委譲 | 個人利用ツール、鍵管理を省きたい場合（例: `app/data_api/llm_client.py`） |

## 入出力契約のチェックリスト（02章）

- [ ] システムプロンプトで出力形式を限定しているか
- [ ] JSON以外の説明文を出力させない指示があるか
- [ ] 単発呼び出しかバッチ呼び出しかを明示しているか
- [ ] 出力可能なフィールド・値の範囲を限定しているか

## 信頼性・コストのチェックリスト（03章）

| 観点 | 対策 |
|------|------|
| パース失敗 | コードフェンス除去 → `json.loads` → 失敗時フォールバック値 |
| 一時的な失敗 | タイムアウト設定＋指数バックオフでのリトライ（恒久的エラーはリトライ対象外） |
| 重複呼び出し | 日次/TTLベースのキャッシュ |
| 呼び出し回数 | 複数対象を1プロンプトにまとめる（バッチ化） |
| 個別対象の失敗 | 例外を対象単位で捕捉し、他の処理は継続 |
| テスト | `call_llm` 相当の関数はモック化し、外部通信なしで検証 |

## 信頼と安全性のUXチェックリスト（04章）

- [ ] AIの提案をそのまま実行せず、確認ステップを挟んでいるか（Verificationパターン）
- [ ] 事実（プログラムで計算した値）とAIの考察を表示上分離しているか
- [ ] プロンプトで禁止事項（断定的な助言等）を明示しているか
- [ ] 免責事項を出力に必ず付与しているか
- [ ] LLM出力の演算子・フィールドをホワイトリスト化し、eval等の直接評価を避けているか
- [ ] AIの実行計画・処理経過をユーザーに開示しているか（Governors）
- [ ] AIが何を記憶・記録するかを設計し、記録にfacts/ai_outputの区別があるか（Footprints）

## 用語対応表

| 本教材の用語 | 対応する外部の呼称 | 読み方 |
|--------------|----------------------|--------|
| 呼び出し方式とアーキテクチャ選定 | Augmented LLM（Anthropic） | オーグメンテッド・エルエルエム |
| バッチ化・並列化 | Parallelization（Anthropic） | パラレライゼーション |
| 確認ステップ | Verification / Human-in-the-loop（Shape of AI） | ベリフィケーション／ヒューマン・イン・ザ・ループ |
| 事実とAI考察の分離、禁止事項の明示 | Guardrails | ガードレールズ |
| マルチターン対話プロンプト | Stateless Multi-turn Conversation | ステートレス・マルチターン・カンバセーション |
| プロンプトインジェクション対策 | Input/Output Guardrail（二層構造） | インプット・アウトプット・ガードレール |
| Prompt Chaining | Prompt Chaining（Anthropic） | プロンプト・チェイニング |
| Routing | Routing（Anthropic） | ルーティング |
| Orchestrator-Workers | Orchestrator-Workers（Anthropic） | オーケストレーター・ワーカーズ |
| Evaluator-Optimizer | Evaluator-Optimizer（Anthropic） | エバリュエーター・オプティマイザー |
| 自律エージェント | Autonomous Agents（Anthropic） | オートノマス・エージェンツ |
| 事実とAI出力の分離記録 | Footprints（Shape of AI） | フットプリンツ |
| 実行計画・処理経過の開示 | Action plan / Stream of Thought（Shape of AI） | アクションプラン／ストリーム・オブ・ソート |
| テンプレート・提案による初回入力支援 | Templates / Suggestions（Shape of AI） | テンプレーツ／サジェスチョンズ |
| AI解釈結果の確認表示 | Filters（Shape of AI） | フィルターズ |
| 保存済み戦略の再利用 | Saved styles（Shape of AI） | セーブド・スタイルズ |
| LLMプロバイダの切り替え | Model management（Shape of AI） | モデル・マネジメント |

## エージェント型ワークフローの選び方（05章）

| パターン | 向いているケース |
|---|---|
| Prompt Chaining | タスクが明確な固定順序のサブタスクに分解できる |
| Routing | 入力が明確に異なるカテゴリに分類でき、カテゴリごとに個別対応したい |
| Orchestrator-Workers | 必要なサブタスクを事前に予測できず、動的に決めたい |
| Evaluator-Optimizer | 明確な評価基準があり、反復改善で品質が上がる |
| Autonomous Agents | 実行経路を事前にコード化できない開放的な問題 |

## AIプロダクトUXパターンの選び方（07章）

| パターン | 向いているケース |
|---|---|
| Templates / Suggestions | ユーザーが何を入力すればよいか分からない（空白キャンバス） |
| Open input / Chained action | 自由記述の質問や、複数ターンにわたる対話が必要 |
| Filters / Saved styles | AIの解釈結果を確認・再利用したい |
| Model management | 複数のLLMプロバイダを使い分けたい |
