# 調整とコンテキスト制御

## この教材で身につくこと

- AIが解釈した条件をユーザーに確認させながら適用するFilters設計を実装できる
- ユーザー固有の設定（保存済み戦略、LLMプロバイダ選択）を永続化する
  Saved styles・Model managementを実装できる
- Attachments・Modes・Preset styles・Prompt enhancer・Voice and toneの
  目的を説明できる

## 概要

[Shape of AI](https://www.shapeof.ai/)のTunersカテゴリ10パターン
（Attachments, Connectors, Filters, Model management, Modes, Parameters,
Preset styles, Prompt enhancer, Saved styles, Voice and tone）を扱います。
共通するテーマは「プロンプトそのものではなく、その前後の設定・文脈を
調整する」ことです。

## 位置づけ

07章の3番目の教材です。02教材（プロンプト操作アクション）が「1回の
やり取りの中でのアクション」を扱うのに対し、本教材は「やり取りの
前提となる設定・文脈」を扱います。

## 主要概念・設計判断の解説

### `app/`の実例（5パターン）

| パターン | `app/`での対応 |
|---|---|
| [Filters](https://www.shapeof.ai/patterns/filters) | AIが解釈した絞り込み条件を`st.json`で確認してから適用 |
| [Parameters](https://www.shapeof.ai/patterns/parameters) | 分析期間（`st.selectbox(["1y", "2y"])`）等の制約付きパラメータ |
| [Connectors](https://www.shapeof.ai/patterns/connectors) | 質問カテゴリに応じて外部データ（株価・ニュース）をプロンプトに接続 |
| [Saved styles](https://www.shapeof.ai/patterns/saved-styles) | ユーザーが確定した戦略条件をDBに保存し再利用 |
| [Model management](https://www.shapeof.ai/patterns/model-management) | `llm_provider`設定でClaude CLI/OpenAI APIを切り替え |

### `app/`に実装が無い観点（5パターン）

[Attachments](https://www.shapeof.ai/patterns/attachments)（ファイル等を
添付してAIの参照材料にする）・[Modes](https://www.shapeof.ai/patterns/modes)
（用途に応じてAIの制約・ペルソナを切り替える）・
[Preset styles](https://www.shapeof.ai/patterns/preset-styles)（生成物の
質感・トーンの既定オプション）・[Prompt enhancer](https://www.shapeof.ai/patterns/prompt-enhancer)
（ユーザーのプロンプトをAIが補強する）・
[Voice and tone](https://www.shapeof.ai/patterns/voice-and-tone)（出力の
声・トーンを一貫させる）は、`app/`に該当する実装がありません。本教材の
サンプルコードは`app/`に実装例が無いため、汎用サンプルコードで解説します。

## 実ソースコード（Python / プロンプト例、出典パス明記）

出典: `ai-stock-investing-tutorial/app/app_tabs/screening_tab.py`（Filters）

```python
st.subheader("AIが解釈した条件（適用前に確認してください）")
st.json(filters)
if st.button("この条件で絞り込む"):
    result_df = apply_filters(universe_df, filters)
```

出典: `ai-stock-investing-tutorial/app/app_tabs/strategy_builder_tab.py`
（Parameters、制約付き選択肢）

```python
sector_period = st.selectbox(
    "分析期間", ["1y", "2y"], key="strategy_sector_period"
)
band_choice = st.selectbox(
    "周期帯",
    ["すべて（自動選択）", "短期", "中期", "長期"],
    key="strategy_watchlist_band",
)
```

出典: `ai-stock-investing-tutorial/app/app_tabs/qa_tab.py`（Connectors、
質問カテゴリに応じた外部データの接続）

```python
if category == "technical":
    history = cached_fetch_price_history(ticker, "6mo")
    technical = analyze_technical(history)
    prompt = build_technical_answer_prompt(question, technical)
elif category == "news":
    news = cached_fetch_news(ticker)
    prompt = build_news_answer_prompt(question, news)
```

出典: `ai-stock-investing-tutorial/app/strategy_builder/storage.py`
（Saved styles）

```python
def load_strategies(user_id: int, session_factory=SessionLocal) -> list[dict]:
    with session_factory() as session:
        rows = (
            session.query(Strategy)
            .filter_by(user_id=user_id)
            .order_by(Strategy.id)
            .all()
        )
        return [json.loads(row.strategy_json) for row in rows]


def save_strategy(user_id: int, strategy: dict, session_factory=SessionLocal) -> None:
    name = strategy.get("strategy_name")
    with session_factory() as session:
        session.query(Strategy).filter_by(user_id=user_id, strategy_name=name).delete()
        session.add(
            Strategy(
                user_id=user_id,
                strategy_name=name,
                strategy_json=json.dumps(strategy, ensure_ascii=False),
            )
        )
        session.commit()
```

出典: `ai-stock-investing-tutorial/app/data_api/llm_client.py`（Model
management）

```python
def _get_provider() -> str:
    return (_get_secret("llm_provider", "claude_cli") or "claude_cli").strip().lower()


def call_llm(prompt: str, timeout: int = 120) -> str:
    provider = _get_provider()
    if provider == "claude_cli":
        return _call_claude_cli(prompt, timeout)
    elif provider == "openai":
        return _call_openai(prompt, timeout)
    else:
        raise ValueError(f"未対応のllm_providerです: {provider}")
```

汎用サンプルコード（`app/`に実装例が無いため、Modes・Voice and toneを
解説する架空のコード）:

```python
def build_prompt_with_mode(user_message: str, mode: str) -> str:
    """用途（Modes）に応じてAIのペルソナ・制約・声のトーン
    （Voice and tone）を切り替える。
    """
    mode_instructions = {
        "初心者向け": "専門用語を避け、やさしい言葉で丁寧に説明してください。",
        "専門家向け": "専門用語を積極的に使い、簡潔に要点だけ述べてください。",
    }
    instruction = mode_instructions.get(mode, mode_instructions["初心者向け"])
    return f"{instruction}\n\n{user_message}"
```

```mermaid
flowchart TD
    A["ユーザーの入力"] --> B["Parameters\n選択肢で制約"]
    B --> C["Connectors\n外部データを接続"]
    C --> D["プロンプト構築"]
    D --> E["call_llm"]
    E --> F["Filters\n解釈結果を確認"]
    F --> G{"適用する?"}
    G -->|Yes| H["Saved styles\n確定結果を保存"]
    G -->|No| A
    H --> I["Model management\nどのLLMで実行したか記録"]
```

## 演習課題

1. `save_strategy`が同名戦略を「削除→追加」で上書きしている理由を、
   Saved stylesが目指す「再利用しやすさ」の観点で説明してください。
2. 自分のアプリにModel management（複数LLMプロバイダの切り替え）を
   追加するとしたら、`llm_client.py`の`_get_provider`をどう拡張するか
   考えてください。

## 理解度チェック

- [ ] `app/`が実装する5つのTunersパターンをそれぞれ説明できる
- [ ] FiltersとVerification（04章）の違いを説明できる
- [ ] Attachments・Modes・Preset styles・Prompt enhancer・Voice and toneの
      目的をそれぞれ説明できる

---

[← 前へ: プロンプト操作アクション](02-prompt-action-patterns.md) | [次へ: AIの識別とブランディング →](04-ai-identity-and-branding.md)
