# マルチターン（対話型）プロンプトの設計

## この教材で身につくこと

- ステートレスな全履歴リプレイ方式でマルチターン対話を設計できる
- 応答を「対話継続（質問・提案）」と「確定出力（構造化データ）」に分岐処理する契約を実装できる
- マルチターン対話がターン数に比例してコストが増える点を理解し、設計時に考慮できる

## 概要

AI戦略ビルダー機能②の対話型スクリーニング条件構築（`strategy_dialogue.py`）を
例に、`app/`の`call_llm`がターン単位のセッション状態を持たないステートレスな
サブプロセス呼び出しであることへの対処法を扱います。

## 位置づけ

02章の最後の教材です。01（構造化出力）・02（単発/バッチ）で学んだ
「呼び出し単位」の設計軸に、3つ目の選択肢「マルチターン対話」を追加します。

## 主要概念・設計判断の解説

### ステートレスLLM呼び出しでの会話継続方法

`call_llm`はCLIサブプロセスを毎回起動する薄いラッパーで、ターン単位の
セッション状態を持ちません（出典: `strategy_dialogue.py`冒頭のdocstring）。
そのため、各ターンで**会話履歴全文をプロンプトに含めて送信**することで
「対話している」ように見せかけます。

### 2段階のペルソナ指示

`_PERSONA_INSTRUCTIONS_TEMPLATE`は、1つのプロンプトに2段階のステップを埋め込みます。

- **ステップ1（アイデアの定量化）**: ユーザーの投資アイデアを具体化する
  質問・提案を1〜2個、短く行う。JSON形式は使わない
- **ステップ2（構造化データの出力）**: ユーザーと条件が合意できたら、
  説明文を含めず```json コードブロックのみで確定出力する

どちらのステップに進むかはLLM自身の判断に委ねられており、アプリ側は
毎ターン同じ指示文（`_PERSONA_INSTRUCTIONS_TEMPLATE`、使用できる関数一覧
`{functions}`だけはターンによらず同じ内容で毎回展開）を送るだけです。
使用できる関数一覧はハードコードではなく、`strategy_builder/pipeline_functions.py`
の`PIPELINE_FUNCTIONS`レジストリから`_format_pipeline_functions_for_prompt`が
毎回組み立てます（05-03章 Orchestrator-Workersで扱うワーカーレジストリと
同じもの）。

### 応答の分岐解析

`parse_dialogue_response`は、LLM応答を次のように判定します。

- JSONとしてパースでき、かつ`strategy_name`と`steps`の両キーを
  含む場合 → `{"kind": "strategy", "strategy": {...}}`（確定出力）
- それ以外（パース失敗、またはキー不足） → `{"kind": "question", "text": raw}`
  （対話継続）

JSONパースに成功しても`strategy_name`が無ければ「question」として扱われる
（`steps`のみで`strategy_name`を欠く場合も同様に「question」扱いになる）
点がポイントです。これにより、ステップ1の途中でLLMが誤って断片的な
JSONらしき文字列を返しても、対話が壊れず継続します。

### コストの考慮

会話が長くなるほど、毎ターンの送信トークン量は履歴の長さに比例して
線形に増えます。10ターン目の呼び出しは、1ターン目の呼び出しよりも
はるかに大きなプロンプトを毎回送信することになります。会話履歴を要約して
圧縮する対策は本教材群のスコープ外とし、将来の拡張候補とします。

## 実ソースコード（Python / プロンプト例、出典パス明記）

出典: `ai-stock-investing-tutorial/app/prompt_patterns/strategy_dialogue.py` 全文

```python
"""AI協調型のスクリーニングロジック構築（AI戦略ビルダー機能②）向けの
対話プロンプト構築・応答解析を行うモジュール。

data_api.llm_client.call_llm はターン単位のセッション状態を持たない
ステートレスなサブプロセス呼び出しのため、対話の各ターンで会話全履歴を
毎回プロンプトに含めて送信する。
"""

import json

from common.json_parsing import strip_code_fence
from strategy_builder.pipeline_functions import PIPELINE_FUNCTIONS


def _format_pipeline_functions_for_prompt() -> str:
    lines = []
    for name, entry in PIPELINE_FUNCTIONS.items():
        params_lines = "\n".join(
            f"    - {param}: {description}"
            for param, description in entry["params_schema"].items()
        )
        lines.append(f"- {name}: {entry['description']}\n  params:\n{params_lines}")
    return "\n".join(lines)


_PERSONA_INSTRUCTIONS_TEMPLATE = """\
あなた（AI）は、ユーザーの投資アイデアを厳密な「株式スクリーニング・パイプライン」へと
昇華させるプロのクオンツ・アナリストです。以下のステップに従ってユーザーをナビゲートしてください。

【ステップ1: アイデアの定量化】
ユーザーから「考え方」が入力されたら、それを歓迎し、以下の要素を具体化するための質問や提案を
1〜2個、短く行ってください。
1. どの関数（複数可）をどの順番で使うか
2. 各関数のパラメータ（戦略名・期間・閾値等）
このステップでは、説明文以外は出力しないでください。JSON形式は使わないでください。

【使用できる関数一覧】
{functions}

【ステップ2: 構造化データの出力】
ユーザーと条件が合意できたら、それ以外の説明文を一切含めず、必ず次のJSON形式のみを
```json コードブロックで返してください。
```json
{{
  "strategy_name": "確定した戦略名",
  "steps": [
    {{"function": "関数名", "params": {{...}}}}
  ]
}}
```
stepsは上記の関数一覧にある関数名のみを使い、必要な順番・組み合わせで並べてください。
"""


def build_dialogue_prompt(history: list[dict], sectors: list[str] | None = None) -> str:
    """会話履歴（[{"role": "user"|"assistant", "content": str}, ...]）から、
    ペルソナ指示と会話全文を含む1回分のLLM呼び出し用プロンプトを組み立てる。
    """
    persona = _PERSONA_INSTRUCTIONS_TEMPLATE.format(
        functions=_format_pipeline_functions_for_prompt()
    )
    transcript_lines = [
        f"{'ユーザー' if turn['role'] == 'user' else 'AI'}: {turn['content']}"
        for turn in history
    ]
    transcript = "\n".join(transcript_lines)
    return (
        f"{persona}"
        f"\n\n【これまでの会話】\n{transcript}\n\n【あなたの次の発言】"
    )


def parse_dialogue_response(raw: str) -> dict:
    """LLM応答を判定する。

    JSONコードブロックとして解析でき、かつ`strategy_name`と`steps`を
    含む場合は `{"kind": "strategy", "strategy": {...}}` を返す。
    それ以外は質問・提案テキストとして `{"kind": "question", "text": raw}` を返す。
    """
    try:
        parsed = json.loads(strip_code_fence(raw))
    except json.JSONDecodeError:
        return {"kind": "question", "text": raw.strip()}

    if (
        isinstance(parsed, dict)
        and "strategy_name" in parsed
        and "steps" in parsed
    ):
        return {"kind": "strategy", "strategy": parsed}
    return {"kind": "question", "text": raw.strip()}
```

使用できる関数一覧（`{functions}`）は、05-03章 Orchestrator-Workersで扱う
`PIPELINE_FUNCTIONS`レジストリの`description`/`params_schema`から動的に
組み立てられます。ハードコードされた財務指標一覧ではなく、レジストリ側の
関数追加・削除に自動で追従する設計です。

`sectors`引数によるSECTOR表記ゆれ吸収は、02-03章「出力範囲の限定と禁止事項」で
学んだ内容と重複するため、本教材では説明を省略します。

```mermaid
sequenceDiagram
    actor User
    participant UI as strategy_builder_tab.py
    participant Dialogue as strategy_dialogue.py

    User->>UI: 投資アイデアを入力
    UI->>Dialogue: build_dialogue_prompt(history)
    Note over Dialogue: 会話履歴全文を毎回プロンプトに含める
    Dialogue->>Dialogue: call_llm(prompt)
    Dialogue->>Dialogue: parse_dialogue_response(raw)
    alt kind == "question"
        Dialogue-->>UI: 質問・提案テキスト
        UI->>User: 追加の質問を表示（対話継続）
    else kind == "strategy"
        Dialogue-->>UI: {"strategy_name": ..., "steps": [...]}
        UI->>User: 確定した戦略パイプラインを表示
    end
```

## 演習課題

1. 3ターン分の会話履歴がある状態で4ターン目を送信する場合、プロンプトに
   含まれる内容がどう変化するか、トークン量の観点で説明してください。
2. `parse_dialogue_response`がJSONパースに成功したが`strategy_name`キーが
   無い場合、なぜ`question`種別として扱われるか、その設計意図を説明してください。

## 理解度チェック

- [ ] ステートレスな呼び出しでマルチターン対話を実現する方法を説明できる
- [ ] 応答の分岐（質問継続/確定出力）をどう判定しているか説明できる
- [ ] マルチターン対話でコストが増える理由を説明できる

---

[← 前へ: 出力範囲の限定と禁止事項](03-prompt-scope-and-constraints.md) | [次へ: 03-reliability-and-cost →](../03-reliability-and-cost/00-README.md)
