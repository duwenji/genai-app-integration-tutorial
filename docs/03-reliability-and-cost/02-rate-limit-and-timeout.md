# レート制限・タイムアウト設計

## この教材で身につくこと

- タイムアウトを設定し、応答が返らないLLM呼び出しでアプリ全体が止まるのを防げる
- レート制限・一時的なエラーに対してリトライ/指数バックオフを実装できる
- リトライ対象にすべきエラーとすべきでないエラーを区別できる

## 概要

`app/`の`call_llm`が備える`timeout`引数を入口に、`app/`には実装されていない
リトライ/バックオフを汎用サンプルコードで補って解説します。

## 位置づけ

01（防御的パース）の直後に置く「呼び出し失敗への対処」ファミリーの教材です。
03（キャッシュ）以降の「コスト最適化」ファミリーとは役割が異なります。

## 主要概念・設計判断の解説

### `app/`のタイムアウト実装

`call_llm(prompt, timeout=120)`は`subprocess.run`に`timeout`を渡しています。
タイムアウト時は`subprocess.TimeoutExpired`が呼び出し元に伝播しますが、
現状`call_llm`内ではキャッチされていません。

### なぜタイムアウトが必要か

Streamlitのようなリクエスト応答型アプリでは、応答なしのプロセスが
ユーザー操作をブロックし続けます。タイムアウトを設定することで、
最悪の場合でも一定時間で処理が打ち切られることを保証できます。

### リトライすべきエラー・すべきでないエラー

- **一時的なエラー（リトライ対象）**: レート制限、タイムアウト、
  ネットワーク瞬断。時間を置けば成功する可能性がある
- **恒久的なエラー（リトライ対象外）**: 認証エラー、CLI未検出
  （`ClaudeCLINotFoundError`）。リトライしても解決しない

`app/`の`ClaudeCLIError`は上記の一時的なエラーを一括りにしているため、
レート制限だけを区別してリトライしたい場合は`stderr`文字列の判定が
必要になる、という設計トレードオフがあります。

### 指数バックオフ

失敗のたびに待機時間を倍にすることで、外部サービスへの負荷集中を
避けます。固定間隔でのリトライに比べ、一時的な過負荷からの回復を
妨げにくい設計です。

## 実ソースコード（Python / プロンプト例、出典パス明記）

出典: `ai-stock-investing-tutorial/app/data_api/llm_client.py`

```python
def call_llm(prompt: str, timeout: int = 120) -> str:
    """Claude Code CLIにプロンプトを渡し、応答テキストを取得する。"""
    executable = _resolve_claude_executable()
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

本教材のサンプルコードは`app/`に実装例が無いため、汎用サンプルコードで
解説します。

```python
import time

def call_llm_with_retry(prompt: str, max_retries: int = 3, base_delay: float = 2.0) -> str:
    """一時的なエラーに対して指数バックオフでリトライする。

    ClaudeCLINotFoundError（CLI未検出）はリトライしても解決しないため対象外とし、
    そのまま呼び出し元に伝播させる。
    """
    for attempt in range(max_retries):
        try:
            return call_llm(prompt)
        except ClaudeCLIError:
            if attempt == max_retries - 1:
                raise
            delay = base_delay * (2 ** attempt)
            time.sleep(delay)
    raise RuntimeError("unreachable")  # for文が必ずreturn/raiseするため到達しない
```

```mermaid
flowchart TD
    A["call_llm(prompt)を試行"] --> B{"成功?"}
    B -->|Yes| C["応答を返す"]
    B -->|"No: ClaudeCLINotFoundError"| D["即座に呼び出し元へ伝播（リトライ対象外）"]
    B -->|"No: ClaudeCLIError（一時的エラー）"| E{"最大試行回数に到達?"}
    E -->|Yes| F["例外を呼び出し元へ伝播"]
    E -->|No| G["待機時間 = base_delay * 2^attempt だけスリープ"]
    G --> A
```

## 演習課題

1. `max_retries=3`、`base_delay=2.0`のとき、各試行前の待機時間（秒）を
   計算してください（1回目0秒、2回目2秒、3回目4秒）。
2. `ClaudeCLINotFoundError`を`call_llm_with_retry`でリトライ対象にして
   しまった場合、何が起きるか説明してください。

## 理解度チェック

- [ ] タイムアウトがなぜ必要か説明できる
- [ ] リトライすべきエラーとすべきでないエラーを区別できる
- [ ] 指数バックオフの目的を説明できる

---

[← 前へ: 防御的パースとフォールバック設計](01-defensive-parsing-and-fallback.md) | [次へ: キャッシュ層の設計 →](03-caching-strategy.md)
