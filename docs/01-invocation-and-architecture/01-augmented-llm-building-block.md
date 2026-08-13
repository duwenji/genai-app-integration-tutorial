# Augmented LLMという基本単位

## この教材で身につくこと

- LLM単体呼び出しを拡張する「Augmented LLM」という基本単位を説明できる
- ワークフロー（predefined code paths）とエージェントの違いを説明できる
- 実アプリの生成AI機能が、なぜ最も単純な形（Augmented LLM）で十分なのかを判断できる

## 概要

生成AIをアプリに組み込むとき、いきなり「自律的に動くエージェント」を
作ろうとするのは失敗のもとです。Anthropicが公開している
[Building Effective Agents](https://www.anthropic.com/research/building-effective-agents)
では、最も基本的な構成要素として「Augmented LLM」という単位を定義しています。
本教材では、この基本単位を理解し、より複雑なワークフロー・エージェントとの
違いを整理します。

## 位置づけ

本教材はカテゴリ01の1番目です。ここで理解する「Augmented LLM」という単位は、
02のCLIサブプロセス方式・03のシステムプロンプト設計の前提となります。

## 主要概念・設計判断の解説

### Augmented LLMとは

Anthropicの定義では、Augmented LLMとは検索（retrieval）・ツール（tools）・
メモリ（memory）などで拡張したLLM呼び出しの基本単位です。1回のプロンプト送信
とその応答受け取りが最小構成であり、必要に応じて外部ツール呼び出しや
検索結果の埋め込みを組み合わせます。

### ワークフローとエージェントの違い

| 分類 | 特徴 |
|------|------|
| ワークフロー（Prompt Chaining / Routing / Parallelization / Orchestrator-Workers / Evaluator-Optimizer） | あらかじめ決めたコード経路をたどる。次に何をするかは開発者が決める |
| エージェント（Autonomous Agents） | 実行中に次の行動をLLM自身が決める。ループの終了条件も動的 |

### 実アプリの生成AI機能はどこに位置するか

ai-stock-investing-tutorialの`app/`は、生成AIを11箇所で活用しています。
このうち8箇所は「1回（またはバッチ）のAugmented LLM呼び出し（必要な事実
データをプロンプトに埋め込み、1〜数文の考察を得る）」で、ワークフローの
中でも最も単純な形にとどまっています。残る3箇所（バックテスト解説・
AI協調型戦略対話・AI投資質問箱）は、単一のAugmented LLM呼び出しでは
表現しづらい構造に対応するため、05章で扱うPrompt Chaining/
Orchestrator-Workers/Evaluator-Optimizer/Routingパターンへ発展しています
（詳細は[05章](../05-agentic-workflow-patterns/00-README.md)と
[07章の横断マッピング](../07-real-world-case-study/01-case-study-map.md)を
参照）。エージェント（実行中にLLM自身が次の行動を決める構成）は、
`app/`のどの機能でも使っていません。

これはAnthropicが原則として掲げる「まず単純な構成から始め、効果が実証された
場合のみ複雑さを足す」を体現した設計です。株価分析コメントの生成の大半に
複雑なワークフローは不要で、事実データ→1回のLLM呼び出し→表示、という
単純な構成で十分に価値が出せています。一方、固定順の2段階処理や動的な
ワーカー選定が必要になった一部の機能だけ、必要になった分だけ複雑さを
足しています。

## 実ソースコード（Python / プロンプト例、出典パス明記）

出典: `ai-stock-investing-tutorial/app/data_api/llm_client.py`

```python
def call_llm(prompt: str, timeout: int = 120) -> str:
    """設定されたLLMプロバイダにプロンプトを渡し、応答テキストを取得する。

    各分析エージェントやコメント生成処理から共通のLLM呼び出し口として利用される。
    """
    provider = _get_provider()
    if provider == "claude_cli":
        return _call_claude_cli(prompt, timeout)
    elif provider == "openai":
        return _call_openai(prompt, timeout)
    else:
        raise ValueError(f"未対応のllm_providerです: {provider}")


def _call_claude_cli(prompt: str, timeout: int) -> str:
    """Claude Code CLIにプロンプトを渡し、応答テキストを取得する。"""
    executable = _resolve_claude_executable()
    with log_duration(logger, f"Claude CLI呼び出し（prompt長={len(prompt)}）"):
        result = subprocess.run(
            [executable, "--system-prompt", _SYSTEM_PROMPT, "-p"],
            input=prompt,
            capture_output=True,
            text=True,
            encoding="utf-8",
            timeout=timeout,
        )
        if result.returncode != 0:
            raise ClaudeCLIError(f"Claude Code CLIの実行に失敗しました: {result.stderr.strip()}")
    return result.stdout.strip()
```

この`call_llm`が、`app/`内すべての生成AI機能が呼び出す唯一の入口です。
`llm_provider`設定（`.streamlit/secrets.toml`）で`_call_claude_cli`（Claude Code
CLIをサブプロセス実行）と`_call_openai`（OpenAI Chat Completions APIをSDK経由で
直接呼び出す）を切り替えられ、現在の設定は`_call_openai`（SDK方式）です
（`llm_provider`未設定時のコード側フォールバック既定値は`_call_claude_cli`）。
どちらの経路でも検索やツール呼び出しは行わず、プロンプト文字列を渡して応答文字列を
受け取るだけの最小構成のAugmented LLM呼び出しである点は変わりません
（方式選択の詳細は[02章](02-api-sdk-vs-cli-subprocess.md)で扱います）。

## 演習課題

1. `ai-stock-investing-tutorial/app/`から`call_llm`を呼び出している箇所を3つ探し
   （`analysis_agents/`, `prompt_patterns/`, `portfolio_management/`, `stock_detail/`
   配下を探すとよい）、それぞれ「単発呼び出し」か「バッチ呼び出し」かを分類してください。
2. `app/`のAI協調型戦略対話は、単一のAugmented LLM呼び出しでは足りず
   Orchestrator-Workersパターン（05-03章）へ発展しています。なぜ他の
   8箇所は単純なAugmented LLM呼び出しのままで十分なのか、この機能との
   違いを理由とともに説明してください。

## 理解度チェック

- [ ] Augmented LLMとワークフロー、エージェントの違いを説明できる
- [ ] `app/`の大半のLLM呼び出しが単純なAugmented LLM呼び出しにとどまる理由と、
      一部だけワークフローパターンへ発展した理由を説明できる
- [ ] 「まず単純な構成から始める」という原則を自分の言葉で説明できる

---

[← 前へ: 00-README](00-README.md) | [次へ: SDK方式 vs CLIサブプロセス方式 →](02-api-sdk-vs-cli-subprocess.md)
