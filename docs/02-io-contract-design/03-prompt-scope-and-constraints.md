# 出力範囲の限定と禁止事項

## この教材で身につくこと

- 出力可能なフィールド・値域をプロンプトで限定する設計を実装できる
- ホワイトリスト方式の演算子マッピングがなぜ安全かを説明できる
- プロンプトでの限定とアプリ側の防御を二重化する設計を実装できる

## 概要

LLMに自由なJSONを出力させると、アプリ側が想定していないフィールドや
演算子が返ってくる可能性があります。本教材では、出力可能な範囲を
プロンプトの時点で限定し、さらにアプリ側でも安全に処理する二重の
防御設計を扱います。

## 位置づけ

本教材はカテゴリ02の最終教材です。ここで学ぶ「限定」の考え方は、
03章「Reliability & Cost」で扱う防御的パースの前段にあたります。

## 主要概念・設計判断の解説

### fieldとoperatorの限定

`build_screening_prompt`は、使用可能なfieldを`per`/`pbr`/`dividend_yield_pct`/
`sector`の4つに限定するようプロンプト内で明示しています。`sector`を使う場合の
operatorは`==`のみとし、valueは実在する業種名（`SECTOR_MAP`の値。
`app/screening/sectors.py`で定義された「銘柄コード→東証17業種区分」の対応表）
から選ばせることで表記ゆれを吸収しています。

### プロンプトでの限定だけに頼らない

LLMがプロンプトの指示を無視して範囲外のfieldやoperatorを返す可能性は
ゼロではありません。そのため`app/`は、アプリ側の`apply_filters`でも
ホワイトリスト外の値を無視する二重の防御をしています。

## 実ソースコード（Python / プロンプト例、出典パス明記）

出典: `ai-stock-investing-tutorial/app/prompt_patterns/screening.py`

```python
# LLMが出力する演算子文字列を、実際に比較演算を行う関数へ安全にマッピングする。
# eval等を使わずホワイトリスト化することで、不正な演算子指定を無害化する。
_OPERATORS = {
    "<=": operator.le,
    ">=": operator.ge,
    "<": operator.lt,
    ">": operator.gt,
    "==": operator.eq,
}


def apply_filters(df: pd.DataFrame, filters: list[dict]) -> pd.DataFrame:
    # LLMが生成したフィルタ条件を順に適用する。存在しない列や未知の演算子は
    # 無視してスキップすることで、LLMの出力ゆれがあっても処理全体を落とさない。
    result = df
    for condition in filters:
        field = condition.get("field")
        op_symbol = condition.get("operator")
        value = condition.get("value")
        if field not in result.columns or op_symbol not in _OPERATORS:
            continue
        op_func = _OPERATORS[op_symbol]
        mask = result[field].notna() & op_func(result[field], value)
        result = result[mask]
    return result
```

### 良い例/悪い例

悪い例: 文字列演算子を直接評価する（インジェクションのリスク）。

```python
# 悪い例: LLMが返した演算子文字列をevalでそのまま実行する
mask = eval(f"df['{field}'] {op_symbol} {value}")
```

良い例: `_OPERATORS`辞書によるホワイトリスト化（存在しない演算子は`in`チェックで弾かれる）。

```python
# 良い例: ホワイトリストに無い演算子はスキップされ、evalは一切使わない
if op_symbol not in _OPERATORS:
    continue
op_func = _OPERATORS[op_symbol]
```

## 演習課題

1. 新しいfield（例: `market_cap`）をスクリーニング条件に追加する場合、
   `build_screening_prompt`と`_OPERATORS`のどちらを、どう変更する必要があるか
   書いてください。
2. 悪い例（`eval`を使った実装）が実際に踏まれるとどんな入力で問題が起きるか、
   具体的な`condition_text`の例を1つ考えてください。

## 理解度チェック

- [ ] プロンプトでfieldを限定する目的を説明できる
- [ ] ホワイトリスト方式のoperatorマッピングがなぜ`eval`より安全か説明できる
- [ ] 自分の機能でLLMに渡す出力範囲をどう限定するか設計できる

---

[← 前へ: 単発呼び出し vs バッチ呼び出し](02-single-vs-batch-prompting.md) | [次へ: マルチターン（対話型）プロンプトの設計 →](04-multi-turn-dialogue-prompting.md)
