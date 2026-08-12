# SDK方式 vs CLIサブプロセス方式

## この教材で身につくこと

- API直叩き（SDK）方式とCLIサブプロセス方式を比較できる
- それぞれの認証・依存関係の違いを説明できる
- 実行環境に応じてどちらの方式を選ぶべきか判断できる

## 概要

LLMを呼び出す方法は「SDKでAPIを直接叩く」だけではありません。
本教材では、`ai-stock-investing-tutorial`の完成版アプリが実装として備えている
「ログイン済みのCLIをサブプロセスとして呼び出す」方式を、
一般的なSDK方式と比較しながら解説します（`app/`自体は`llm_provider`設定で
どちらの方式も使え、現在の設定はSDK方式です。詳細は後述）。

## 位置づけ

01-augmented-llm-building-block.mdで学んだAugmented LLM呼び出しを、
実際にどう実装するかという選択肢を扱います。次の03では、
CLIサブプロセス方式特有の入出力設計をさらに掘り下げます。

## 主要概念・設計判断の解説

### 2方式の比較

| 項目 | SDK + APIキー方式 | CLIサブプロセス方式 |
|---|---|---|
| 認証 | `ANTHROPIC_API_KEY`などを環境変数で管理 | ログイン済みCLIセッションに委譲（アプリ側で鍵を持たない） |
| 依存 | `anthropic`/`openai`等のSDKパッケージ | `claude`コマンドがPATH上にあること |
| 向いているケース | サーバー環境、複数ユーザー、レート制御を自前で持ちたい場合 | 個人利用ツール、開発者本人のログイン済み環境で動かす場合 |
| 呼び出し方法 | `client.messages.create(...)` | `subprocess.run([...], input=prompt)` |

### なぜCLIサブプロセス方式が選ばれたか

`ai-stock-investing-tutorial`には、SDK方式を教える既存教材
`ai-stock-investing-tutorial/docs/03-data-api/02-llm-api-integration.md`が
あります。一方、完成版アプリ`app/`はCLIサブプロセス方式を実装として備えており、
コード側のフォールバック既定値（`llm_provider`未設定時）もCLIサブプロセス方式です。
アプリの設計書（`app/docs/app-design.md`）には次のように書かれています。

> 個人利用向けのStreamlit Webアプリであり、ログイン済みのClaude Code CLI
> （`claude -p`）をサブプロセスとして実行する方式を採る。

つまり、個人利用ツールでAPIキー管理そのものをアプリの外に出すという
明確な設計判断です。サーバーで複数ユーザーに提供するアプリであれば、
SDK方式の方が適しています。

### `app/`における2方式の共存

`llm_client.py`の`call_llm`は`llm_provider`という設定値
（`.streamlit/secrets.toml`の`llm_provider = "claude_cli"`または`"openai"`）で
実装を切り替える構造になっています。現在の`secrets.toml`の設定はSDK方式
（`"openai"`）で、`openai`パッケージの`client.chat.completions.create(...)`を
直接呼び出しています（`ANTHROPIC_API_KEY`ではなく`openai_api_key`を
`secrets.toml`で管理）。`llm_provider`を`"claude_cli"`に戻せばCLIサブプロセス
方式に切り替わります（コード側のフォールバック既定値、つまり`llm_provider`
自体が未設定の場合の値もCLIサブプロセス方式のままです）。つまり`app/`は
「CLIサブプロセス方式のみ」ではなく、1つの入口関数の中で両方式を実装し、
設定で選べるようにしている実例です。

## 実ソースコード（Python / プロンプト例、出典パス明記）

出典: `ai-stock-investing-tutorial/app/data_api/llm_client.py`

```python
def _resolve_claude_executable() -> str:
    """`claude`実行ファイルのパスを解決する。未インストール時は分かりやすい例外に変換する。"""
    executable = shutil.which("claude")
    if executable is None:
        raise ClaudeCLINotFoundError(
            "Claude Code CLI（`claude`コマンド）が見つかりません。"
            "インストールとログインを確認してください。"
        )
    return executable
```

`app/`自身のSDK方式実装（出典は同じ`llm_client.py`）:

```python
def _call_openai(prompt: str, timeout: int) -> str:
    """OpenAI Chat Completions APIにプロンプトを渡し、応答テキストを取得する。"""
    api_key = _get_secret("openai_api_key")
    model = _get_secret("openai_model", "gpt-5")
    client = openai.OpenAI(api_key=api_key)
    completion = client.chat.completions.create(
        model=model,
        messages=[
            {"role": "system", "content": _SYSTEM_PROMPT},
            {"role": "user", "content": prompt},
        ],
        timeout=timeout,
    )
    return completion.choices[0].message.content.strip()
```

さらに対比として、既存教材のSDK方式（出典:
`ai-stock-investing-tutorial/docs/03-data-api/02-llm-api-integration.md`、
Anthropic公式SDKによる最小構成の例）も示します。
どちらも正しい実装であり、優劣ではなく方式の違いです。

```python
import os
import anthropic


def call_llm(prompt: str) -> str:
    client = anthropic.Anthropic(api_key=os.environ["ANTHROPIC_API_KEY"])
    response = client.messages.create(
        model="claude-sonnet-5",
        max_tokens=1024,
        messages=[{"role": "user", "content": prompt}],
    )
    return response.content[0].text
```

```mermaid
flowchart LR
    subgraph sdk["方式A: SDK + APIキー"]
        appA["アプリコード"] -->|"ANTHROPIC_API_KEY"| clientA["anthropic.Anthropic()"]
        clientA -->|"HTTPS"| apiA["Anthropic API"]
    end
    subgraph cli["方式B: CLIサブプロセス"]
        appB["アプリコード"] -->|"subprocess.run"| cliB["claude CLI"]
        cliB -->|"ログイン済みセッション"| apiB["Anthropic API"]
    end
```

## 演習課題

1. `app/data_api/llm_client.py`の`call_llm`をSDK方式（`anthropic`パッケージ使用）に
   書き換えるとしたら、`_resolve_claude_executable`・`ClaudeCLINotFoundError`・
   `ClaudeCLIError`をそれぞれ何に置き換えるか対応表を作ってください。
2. CLIサブプロセス方式のデメリットを1つ挙げ（`llm_client.py`のコメントに
   Windows環境での引数展開の実例があります）、対策を説明してください。

## 理解度チェック

- [ ] SDK方式とCLIサブプロセス方式それぞれの認証の違いを説明できる
- [ ] `app/`がCLIサブプロセス方式を選んだ理由を説明できる
- [ ] 自分のアプリではどちらが向いているか、理由とともに判断できる

---

[← 前へ: Augmented LLMという基本単位](01-augmented-llm-building-block.md) | [次へ: システムプロンプトと入出力の境界 →](03-system-prompt-and-io-boundary.md)
