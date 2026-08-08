# 単発呼び出し vs バッチ呼び出し

## この教材で身につくこと

- 単発呼び出しとバッチ呼び出しの使い分け基準を説明できる
- バッチ化がAPIコストではなく何を削減しているかを説明できる
- バッチ結果の一部が欠けた場合の対処法を実装できる

## 概要

複数の対象（銘柄・ペアなど）にLLMでコメントを付けたいとき、
1件ずつ呼び出すか、まとめて1回で呼び出すかは重要な設計判断です。
本教材では、`ai-stock-investing-tutorial`のアプリが採用している
バッチ化の方針と、単発呼び出しが適切なケースを対比して整理します。

## 位置づけ

01章で学んだJSON契約は、単発・バッチのどちらでも同じ形で使えます。
本教材は「何件分をまとめてプロンプトに詰め込むか」という設計軸を追加します。

## 主要概念・設計判断の解説

### `app/`の原則

アプリの設計書（`app/docs/app-design.md`）には次のように明記されています。

> 複数対象に対する処理（ニュースセンチメント・スクリーニングコメント・
> ランキングコメント・セクターローテーションコメント）は個別呼び出しではなく
> 必ず1回のプロンプトにまとめてバッチ処理する（サブプロセス起動オーバーヘッドの
> 削減）。唯一の例外は銘柄詳細ダイアログのAIコメントで、こちらは性質上
> つねに単一銘柄分だけを都度呼び出す。

### バッチ化する理由は「APIコスト」ではない

一般的なSDK方式のLLM統合では、バッチ化はAPI課金の削減が主目的になりがちです。
しかし`app/`はCLIサブプロセス方式（01章）を採用しているため、
削減対象は**サブプロセス起動オーバーヘッド**（CLIプロセスの起動・終了に
かかる時間）です。呼び出し方式が変われば、バッチ化のモチベーションも変わる
ことを理解しておくと、自分のアプリでの判断がぶれません。

### 単発呼び出しが妥当なケース

銘柄詳細ダイアログは、ユーザー操作のたびに対象が1件に決まり、
その場ですぐ結果を表示する必要があります。他の対象とまとめて
待たせる理由がないため、単発呼び出しのままで問題ありません。

## 実ソースコード（Python / プロンプト例、出典パス明記）

バッチの例。出典: `ai-stock-investing-tutorial/app/analysis_agents/news_research_agent.py`

```python
def build_news_sentiment_prompt(news_by_ticker: dict[str, list[dict]]) -> str:
    # 全銘柄分のニュース見出しを1つのプロンプトにまとめてバッチ処理し、
    # 後段でticker単位にパースできるようJSON形式での出力を指示する。
    lines = [
        "以下は銘柄ごとの直近ニュース見出しです。",
        "各銘柄のニュースセンチメントを判定してください。",
        "出力は次の形式のJSONのみとしてください（説明文・コードブロック記法は不要です）。",
        '{"<ticker>": {"sentiment": "ポジティブ|ニュートラル|ネガティブ", "confidence": 0.0〜1.0}}',
        "",
    ]
    for ticker, items in news_by_ticker.items():
        titles = "\n".join(f"- {item['title']}" for item in items) or "- (ニュースなし)"
        lines.append(f"## {ticker}\n{titles}\n")
    return "\n".join(lines)


def research_news_batch(
    news_by_ticker: dict[str, list[dict]], call_llm=default_call_llm
) -> dict[str, dict]:
    prompt = build_news_sentiment_prompt(news_by_ticker)
    raw = call_llm(prompt)
    try:
        result = json.loads(strip_code_fence(raw))
    except json.JSONDecodeError:
        result = {}

    # LLMが一部の銘柄について結果を返さなかった場合でも、
    # 呼び出し元が全銘柄分のキーを期待できるようNoneで埋めて補完する。
    return {
        ticker: result.get(ticker, {"sentiment": None, "confidence": None})
        for ticker in news_by_ticker
    }
```

単発の例。出典: `ai-stock-investing-tutorial/app/prompt_patterns/stock_detail.py`

```python
def build_stock_detail_prompt(
    ticker: str, name: str | None, fundamentals: dict, technical: dict, news: list[dict]
) -> str:
    # 1銘柄のみを扱う。呼び出しごとに単一銘柄分の総合分析コメントを生成する。
    ...
```

## 演習課題

1. `news_research_agent.py`の`research_news_batch`を、銘柄ごとに個別呼び出しする
   実装に書き換えた場合、呼び出し回数がどう変わるか、保有銘柄5件のケースで
   試算してください。
2. 「バッチ化すべきだが現状は単発呼び出しになっている」機能が`app/`にあるか
   調べ、無ければ「無い」という結論とその理由を書いてください。

## 理解度チェック

- [ ] `app/`がバッチ化する理由を「APIコスト」ではなく正しい言葉で説明できる
- [ ] バッチ呼び出しで一部の対象だけ結果が欠けた場合の対処法を説明できる
- [ ] 単発呼び出しが妥当なケースの条件を説明できる

---

[← 前へ: 構造化出力（JSON）の契約設計](01-structured-output-json-contract.md) | [次へ: 出力範囲の限定と禁止事項 →](03-prompt-scope-and-constraints.md)
