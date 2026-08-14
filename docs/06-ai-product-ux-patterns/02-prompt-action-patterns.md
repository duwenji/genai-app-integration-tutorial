# プロンプト操作アクション

## この教材で身につくこと

- ユーザーがAIに指示する典型的なアクション（開いた入力・対話継続・要約・拡張等）を、目的別に分類できる
- 既存の分析結果を入力として次のAI呼び出しに渡す「Chained action」を実装できる
- `app/`のどの機能がどのPrompt Actionsパターンに対応するか説明できる

## 概要

01教材のWayfindersでユーザーが最初のプロンプトを送った後、次に迷うのが「送信した後、何ができるのか分からない」という問題です。
結果が返ってきても、「もう一度試す」のか「今の結果を膨らませる」のか「別の書き方に直す」のか、選択肢がボタン化されていないとユーザーは毎回プロンプトを一から書き直すしかありません。
これは特にAPI経由でLLMを呼ぶ設計に慣れたエンジニアが見落としがちな観点です。
バックエンド側から見ると「1回のプロンプト→1回の応答」で完結しますが、ユーザー体験としてはその前後に「次に何を押せるか」というUIの選択肢が必要になります。

Shape of AIでは、こうした「送信後にユーザーがAIへ指示する操作」をPrompt Actionsと呼びます。
[Shape of AI](https://www.shapeof.ai/)のPrompt Actionsカテゴリ14パターン（Auto-fill, Chained action, Describe, Expand, Inline Action, Inpainting, Madlibs, Open input, Regenerate, Restructure, Restyle, Summary, Synthesis, Transform）を、`app/`の実装に対応するものと、対応しないものに分けて扱います。

## 位置づけ

06章の2番目の教材です。
01教材（導線）で最初のプロンプトを送った後、ユーザーがAIに対して行う様々な操作アクションを扱います。

## 主要概念・設計判断の解説

### `app/`の実例（7パターン）

| パターン | `app/`での対応 | つまずきやすい点 |
|---|---|---|
| [Open input](https://www.shapeof.ai/patterns/open-input) | AI質問箱の自由記述入力（`qa_tab.py`） | 自由入力ゆえに意図分類（Routing）を誤ることがある |
| [Chained action](https://www.shapeof.ai/patterns/chained-action) | 戦略ビルダーの対話継続（`st.chat_input`で追加発言） | 履歴が長くなるほど毎回のプロンプトが肥大化する |
| [Auto-fill](https://www.shapeof.ai/patterns/auto-fill) | 提案結果を投資アイデア入力欄へ反映（単一フィールド版） | 反映後にユーザーが編集した内容と混同しやすい |
| [Summary](https://www.shapeof.ai/patterns/summary) | バックテスト結果を初心者向けに要約説明 | 数値を丸めすぎると誤解を招く表現になりうる |
| [Expand](https://www.shapeof.ai/patterns/expand) | 既存の解説に追加の検討観点を加える（Prompt Chaining 2段目） | 元の解説と矛盾する観点を出すことがある |
| [Synthesis](https://www.shapeof.ai/patterns/synthesis) | ポートフォリオの事実データから観察事項を箇条書きに整理 | 事実と所感の境界が曖昧になりやすい |
| [Transform](https://www.shapeof.ai/patterns/transform) | ランキング結果（構造化データ）を銘柄ごとの一言コメント（文章）に変換 | 出力形式（JSON）が崩れると後続処理が失敗する |

### `app/`に実装が無い観点（7パターン）

以下7パターンは`app/`に該当する実装がありません。
本教材のサンプルコードは`app/`に実装例が無いため、汎用サンプルコードで解説します。

| パターン | 説明 | つまずきやすい点 |
|---|---|---|
| [Describe](https://www.shapeof.ai/patterns/describe) | 対象を基本要素に分解しプロンプト候補を示す | 分解の粒度が細かすぎるとかえって使いにくい |
| [Inline Action](https://www.shapeof.ai/patterns/inline-action) | 画面上の既存コンテンツを起点にAIへ問い合わせる | 選択範囲の取得にJS連携が必要になりがち |
| [Inpainting](https://www.shapeof.ai/patterns/inpainting) | 結果の一部だけを再生成する | 部分再生成が全体の整合性を崩す場合がある |
| [Madlibs](https://www.shapeof.ai/patterns/madlibs) | 同じ書式のまま繰り返し生成する | 書式が固定されすぎると柔軟な入力ができない |
| [Regenerate](https://www.shapeof.ai/patterns/regenerate) | 追加入力なしで再生成する | 何度も押されるとLLM呼び出しコストが膨らむ |
| [Restructure](https://www.shapeof.ai/patterns/restructure) | 既存コンテンツを起点にプロンプトを組み立てる | 起点コンテンツが長いとプロンプトが肥大化する |
| [Restyle](https://www.shapeof.ai/patterns/restyle) | 構造を変えずスタイルだけ変換する | 「スタイル」の範囲をユーザーに誤解されやすい |

## 実ソースコード（Python / プロンプト例、出典パス明記）

出典: `ai-stock-investing-tutorial/app/app_tabs/qa_tab.py`（Open input）

```python
ticker = st.text_input("銘柄コード（任意）", placeholder="7203.T", key="qa_ticker")
question = st.text_area(
    "質問", placeholder="この銘柄は割安ですか？", key="qa_question"
)
if not st.button("質問する", disabled=not question):
    return
```

出典: `ai-stock-investing-tutorial/app/app_tabs/strategy_builder_tab.py`（Chained action、対話の継続）

```python
user_reply = st.chat_input("AIへの返信を入力", key="strategy_chat_input")
if user_reply:
    history.append({"role": "user", "content": user_reply})
    st.session_state["strategy_chat_history"] = history
    st.rerun()
```

出典: `ai-stock-investing-tutorial/app/prompt_patterns/backtest_explanation.py`（Summary、複雑な数値結果を初心者向けに要約）

```python
return (
    f"以下は{strategy_name}戦略のバックテスト結果です"
    "（Python側でパラメータの近傍グリッドサーチまで計算済みのため再計算は不要です）。\n\n"
    ...
    "この結果を投資初心者にも分かる言葉で説明してください。\n"
)
```

出典: `ai-stock-investing-tutorial/app/prompt_patterns/backtest_explanation.py`（Expand、既存の解説に追加の観点を加える2段目のプロンプト）

```python
def build_improvement_prompt(
    ticker: str, comparison: dict, explanation: str, stability: dict, ...
) -> str:
    # Step1（結果解説）の出力を入力として受け取り、追加で検討すべき観点を
    # 生成させる2段階目のプロンプト（Prompt Chaining）。
    return (
        f"...\n【既存の解説】\n{explanation}\n\n"
        "この解説を踏まえ、投資家が追加で検討する価値がある観点を"
        "日本語で2〜3個、簡潔に提案してください。\n"
    )
```

出典: `ai-stock-investing-tutorial/app/prompt_patterns/report_generation.py`（Synthesis、事実データを観察事項に整理）

```python
return (
    "以下はポートフォリオの事実データ（Python側で計算済み）です。\n\n"
    f"{facts_json}\n\n"
    "このデータを見て、教育的な観察事項（例: 集中度が高い銘柄、"
    "ニュースセンチメントが弱い銘柄、テクニカルシグナルが弱含みの銘柄）を"
    "箇条書きで示してください。\n"
)
```

出典: `ai-stock-investing-tutorial/app/prompt_patterns/backtest_explanation.py`（Transform、構造化ランキングを文章コメントへ変換）

```python
def build_ranking_comment_prompt(ranking_rows: list[dict]) -> str:
    rows_json = json.dumps(rows, ensure_ascii=False)
    return (
        "以下は複数銘柄のバックテスト結果ランキング（リスク調整済みリターン降順）です。"
        "銘柄ごとに投資家向けの一言コメントを日本語で1文ずつ作成してください。"
        '出力形式: {"<ticker>": "<コメント>"} というJSONのみを出力してください。\n\n'
        f"{rows_json}"
    )
```

汎用サンプルコード（`app/`に実装例が無いため、Regenerate・Inline Actionを解説する架空のコード）:

```python
def render_regenerate_and_inline_action(last_prompt: str, selected_text: str | None) -> str | None:
    """同じプロンプトのまま結果だけ再生成する（Regenerate）ボタンと、
    画面上で選択済みのテキストを起点にAIへ問い合わせる（Inline Action）
    ボタンを並べて表示する。
    """
    col1, col2 = st.columns(2)
    with col1:
        if st.button("再生成する（同じ条件で）"):
            return last_prompt
    with col2:
        if selected_text and st.button(f"「{selected_text}」について聞く"):
            return f"次のテキストについて詳しく説明してください: {selected_text}"
    return None
```

汎用サンプルコード（`app/`に実装例が無いため、Describe・Madlibsを解説する架空のコード）:

```python
def render_describe_and_madlibs(ticker: str) -> str | None:
    """対象銘柄を基本要素に分解しプロンプト候補を提示する（Describe）。
    同じ書式のまま銘柄コードだけ差し替えて繰り返し生成できる
    入力欄（Madlibs）も並べて表示する。
    """
    st.caption(f"「{ticker}」について聞けること: 割安性 / 成長性 / リスク")
    madlibs_ticker = st.text_input("銘柄コードを変えて同じ質問を繰り返す", value=ticker)
    if st.button("この銘柄で同じ質問をする"):
        return f"{madlibs_ticker}の割安性について教えてください"
    return None
```

```mermaid
sequenceDiagram
    actor User
    participant UI as app_tabs/*.py
    participant Prompt as prompt_patterns/*.py
    participant LLM as call_llm()

    User->>UI: アクションを選択（質問する/対話継続/要約する等）
    UI->>Prompt: build_*_prompt(...)
    Prompt->>LLM: call_llm(prompt)
    LLM-->>UI: 応答（Summary/Synthesis/Transform等の結果）
    UI->>User: 結果を表示
    User->>UI: さらにアクション（Expand/Chained action）
    UI->>Prompt: build_improvement_prompt(..., explanation)
```

この図が示すように、ユーザーのアクション選択は毎回`prompt_patterns/*.py`の`build_*_prompt`関数を経由してから`call_llm`に渡ります。
アクションの種類が増えても、UI層とプロンプト構築層を分けておくことで、新しいPrompt Actionsパターンを追加する際にUI側の変更だけで済みます。

## 演習課題

1. `build_improvement_prompt`がExpandパターンに対応する理由を、「既存の出力を入力として使う」という観点で説明してください。
2. 自分のアプリの既存出力にPrompt Actionsを追加する設計をしてください。
   1. 対象となる既存出力（画面・機能）を1つ書き出してください。
   2. Regenerate（同条件で再生成）とRestyle（構造は変えずスタイルだけ変更）のどちらが向いているか、上の比較表を参考に判断してください。
   3. 選ばなかった方が向くユースケースも1つ挙げてください。

## 理解度チェック

- [ ] `app/`が実装する7つのPrompt Actionsパターンをそれぞれ説明できる
- [ ] Expand（既存出力を入力にする）とSummary（複雑な結果を要約する）の違いを説明できる
- [ ] Describe・Inline Action・Inpainting・Madlibs・Regenerate・Restructure・Restyleの目的をそれぞれ説明できる
- [ ] 各Prompt Actionsパターンのつまずきやすい点を説明できる

---

[← 前へ: オンボーディングと導線](01-onboarding-and-wayfinding.md) | [次へ: 調整とコンテキスト制御 →](03-tuning-and-context-control.md)
