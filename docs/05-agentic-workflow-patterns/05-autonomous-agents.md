# Autonomous Agents

## この教材で身につくこと

- ワークフロー（固定コード経路）と自律エージェント（動的なツール選択ループ）
  の違いを説明できる
- 最小限のツール呼び出しループを実装できる
- ワークフローと自律エージェントのどちらを採用すべきか判断基準を持てる

## 概要

銘柄情報の取得・回答をLLM自身がツール呼び出しの要否を判断しながら
繰り返す、最小限の自律エージェントループを解説します。

## 位置づけ

05章の最後の教材です。01〜04で扱ったワークフロー（あらかじめ決めた
コード経路）に対し、本教材は「次に何をするか」をLLM自身が決める点で
質的に異なります。章全体の締めくくりとして、ワークフローとエージェントの
使い分け判断基準を示します。

## 主要概念・設計判断の解説

### 自律エージェントの定義

LLMが環境からのフィードバックに基づき、ツールをループで使用します
（出典: [Anthropic "Building Effective Agents"](https://www.anthropic.com/research/building-effective-agents)）。
実行経路を事前にコード化できない開放的な問題に向きます。

### ワークフローとの違い

ワークフロー（Prompt Chaining〜Evaluator-Optimizer）は「次に何を呼ぶか」が
コードで決まっていますが、自律エージェントは「次に何をするか」をLLMの
応答自体が決めます。

### Anthropicの推奨

「まず単純な構成（ワークフロー）から始め、効果が実証された場合のみ
自律エージェントの複雑さを足す」。`app/`が採用していない理由（01章と
接続）は、用途がシンプルなAugmented LLM呼び出しで十分なためです。

### 終了条件の設計

`max_steps`による上限、および`"finish"`という明示的な終了アクションの
両方を用意し、無限ループを防ぎます。

## 実ソースコード（Python / プロンプト例、出典パス明記）

本教材のサンプルコードは`app/`に実装例が無いため、汎用サンプルコードで
解説します。

```python
import json

from common.json_parsing import strip_code_fence

_TOOLS = {
    "get_price": lambda args: get_price(args["ticker"]),
    "get_news": lambda args: get_news(args["ticker"]),
}


def build_agent_prompt(history: list[dict], tools: list[str]) -> str:
    transcript = "\n".join(f"{turn['role']}: {turn['content']}" for turn in history)
    return (
        f"利用できるツール: {tools}\n"
        '次のいずれかのJSON形式で次の行動を1つだけ出力してください。\n'
        '{"type": "tool_call", "tool": "<ツール名>", "args": {...}}\n'
        '{"type": "finish", "answer": "<最終回答>"}\n\n'
        f"【これまでの履歴】\n{transcript}"
    )


def run_agent_loop(user_request: str, max_steps: int = 5) -> str:
    history = [{"role": "user", "content": user_request}]
    for _ in range(max_steps):
        raw = call_llm(build_agent_prompt(history, tools=list(_TOOLS)))
        action = json.loads(strip_code_fence(raw))
        if action["type"] == "finish":
            return action["answer"]
        tool_result = _TOOLS[action["tool"]](action["args"])
        history.append({"role": "assistant", "content": raw})
        history.append({"role": "tool", "content": json.dumps(tool_result, ensure_ascii=False)})
    return "ステップ上限に達したため終了しました。"
```

## 演習課題

1. `get_price`/`get_news`ツールに加え、第3のツール（例:
   `get_technical_indicators`）を追加する場合、`_TOOLS`辞書と
   `build_agent_prompt`のどちらを、どう変更する必要があるか書いてください。
2. `app/`にこのパターンを追加するとしたら、Anthropicの「まず単純な構成
   から始める」原則に照らして、どんな条件が揃えば自律エージェント化を
   検討すべきか考えてください。

## 理解度チェック

- [ ] ワークフローと自律エージェントの違いを説明できる
- [ ] ツール呼び出しループの終了条件をどう設計しているか説明できる
- [ ] ワークフローと自律エージェントのどちらを採用すべきか判断基準を説明できる

---

[← 前へ: Evaluator-Optimizer](04-evaluator-optimizer.md) | [次へ: 06-ai-product-ux-patterns →](../06-ai-product-ux-patterns/00-README.md)
