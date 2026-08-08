# 事実とAI考察の分離

## この教材で身につくこと

- プログラムで計算した「事実」とAIの「考察」を分離して扱う設計ができる
- LLMに数値計算そのものを任せない理由を説明できる
- 「事実データ」をプロンプトに埋め込む際の書き方を実装できる

## 概要

LLMは数値計算が得意ではなく、誤った値をもっともらしく生成することが
あります（ハルシネーション）。本教材では、`ai-stock-investing-tutorial`の
アプリが一貫して採用している「計算はプログラム、考察はAI」という
役割分担の設計を扱います。

## 位置づけ

01章の確認ステップが「UI上でどう確認させるか」を扱ったのに対し、
本教材は「そもそもLLMに何をさせないか」という設計判断を扱います。

## 主要概念・設計判断の解説

### `app/`の一貫した方針

構成比・リスク指標・テクニカルシグナル等の数値計算は、必ずPython側
（`analyze_portfolio_composition`・`assess_risk`など）で行います。
その結果を「事実データ」としてプロンプトに埋め込んでから、
初めてLLMに渡します。LLM自身には数値計算をさせません。

### プロンプトでの境界の明示

`build_report_prompt`は、「以下はポートフォリオの事実データ
（Python側で計算済み）です」と明示することで、LLMの役割を
「解釈・要約のみ」に限定しています。

## 実ソースコード（Python / プロンプト例、出典パス明記）

出典: `ai-stock-investing-tutorial/app/portfolio_management/review.py`

```python
def generate_portfolio_review(
    holdings, current_prices, price_histories, fundamentals_by_ticker,
    technicals_by_ticker, news_sentiment_by_ticker, names_by_ticker=None,
    call_llm=default_call_llm,
) -> str:
    composition = analyze_portfolio_composition(holdings, current_prices)
    risk = assess_risk(price_histories)
    snapshots = [
        build_holding_snapshot(holding, ...)
        for holding in holdings
    ]

    # LLMに渡す「事実（facts）」として、構成・リスク・銘柄詳細を1つにまとめる。
    facts = {
        "composition": composition,
        "risk": risk,
        "holdings": snapshots,
        "ticker_names": names_by_ticker,
    }
    prompt = build_report_prompt(facts)
    commentary = call_llm(prompt)
    ...
```

出典: `ai-stock-investing-tutorial/app/prompt_patterns/report_generation.py`

```python
def build_report_prompt(facts: dict) -> str:
    # ポートフォリオの数値的事実はPython側で計算済みのため、LLMには解釈・要約のみを依頼する。
    facts_json = json.dumps(facts, ensure_ascii=False, indent=2, default=str)
    return (
        "以下はポートフォリオの事実データ（Python側で計算済み）です。\n\n"
        f"{facts_json}\n\n"
        "このデータを見て、教育的な観察事項（例: 集中度が高い銘柄、"
        "ニュースセンチメントが弱い銘柄、テクニカルシグナルが弱含みの銘柄）を"
        "箇条書きで示してください。\n"
        "売買の推奨・指示・目標株価の提示は行わないでください。\n\n"
        f"{DISCLAIMER_NOTICE}"
    )
```

### 良い例/悪い例

悪い例: LLMに数値計算そのものを依頼するプロンプト。

```text
保有銘柄の損益率を計算して教えてください。
ticker: 7203.T, shares: 100, cost: 2000, current: 2150
```

良い例: 損益率はPython側で計算し、結果の数値をプロンプトに埋め込んで
観察事項の言語化のみを依頼する。

```text
以下はポートフォリオの事実データ（Python側で計算済み）です。
{"ticker": "7203.T", "profit_loss_pct": 7.5}
このデータを見て、教育的な観察事項を箇条書きで示してください。
```

## 演習課題

1. `assess_risk`（`app/portfolio_management/risk.py`）が計算する
   年率ボラティリティ・銘柄間相関のいずれかを1つ挙げ、それをLLMに
   計算させた場合に起こりうる誤りを説明してください。
2. 「事実」と「AI考察」を画面表示上どう視覚的に区別すべきか、
   UIデザインの観点で提案してください。

## 理解度チェック

- [ ] `app/`が数値計算をLLMに任せない理由を説明できる
- [ ] 「事実データ」をプロンプトに埋め込む際の書き方を説明できる
- [ ] 事実とAI考察の分離を自分の機能に適用する方法を説明できる

---

[← 前へ: 確認ステップ（Verificationパターン）](01-verification-checkpoint.md) | [次へ: ガードレールと免責事項 →](03-guardrails-and-disclaimers.md)
