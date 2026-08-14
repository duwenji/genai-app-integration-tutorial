# LLM呼び出しのテスト

## この教材で身につくこと

- 非決定的なLLM呼び出しをモック化し、外部通信・CLI起動なしにテストできる
- 正常系・異常系の両方をテストする設計ができる
- `call_llm`を差し替え可能にする引数デフォルトパターンを理解できる

## 概要

自動テストは、同じ入力に対して常に同じ結果を期待します。
しかしLLMは**非決定的**（同じ入力でも毎回微妙に違う応答を返しうる）です。
本物のLLMをそのままテストで呼び出すと、テストが成功したり失敗したりして信頼できません。
また、CLIプロセスの起動やネットワーク通信を伴うため実行に数秒〜数十秒かかり、テストスイート全体が遅くなります。
**モック化**とは、本物の代わりに、あらかじめ決めた値を返すだけの「偽物」に処理を差し替えるテスト手法です。
本教材では、`ai-stock-investing-tutorial`のアプリがどのように`call_llm`をモック化してテストしているかを扱います。

## 位置づけ

本教材はカテゴリ03の最終教材です。
これまでに学んだキャッシュ・並列化・フォールバックの実装は、いずれもこの教材で学ぶモック化の手法でテスト可能です。

## 主要概念・設計判断の解説

### pytestのfixtureと`monkeypatch`の仕組み

`test_call_llm_returns_stdout_on_success(monkeypatch)`のように、テスト関数の引数に`monkeypatch`と書くだけで使えています。
これはpytestの**fixture**という仕組みによるものです。
テスト関数の引数名がfixture名と一致すると、pytestが該当する値を自動的に注入してくれます（importは不要）。
`monkeypatch`はpytestが標準で提供しているfixtureの1つで、「実行中のオブジェクト・属性・環境変数を一時的に差し替え、テスト終了後は自動的に元へ戻す」役割を持ちます。

コード中には2種類の書き方が出てきます。

```python
monkeypatch.setattr("shutil.which", lambda name: "claude-executable")
monkeypatch.setattr(subprocess, "run", fake_run)
```

どちらも`setattr(対象, 属性名, 差し替え後の値)`という同じ操作ですが、対象の指定方法が異なります。
前者は`"モジュール名.属性名"`という文字列で対象を指定し、後者は`subprocess`モジュールオブジェクトと属性名`"run"`を分けて渡しています。
挙動は同じで、後者の書き方ではimport済みのオブジェクトをそのまま渡せます。

`monkeypatch.setattr`が`unittest.mock.patch`と違い`with`文や`try/finally`を書かずに済むのは、fixtureの後始末（テアダウン）機構がテスト終了時に自動で元の状態へ戻してくれるためです。

### モック化する2箇所

`call_llm`はサブプロセス呼び出しの境界が明確なため、`shutil.which`（CLIパスの解決）と`subprocess.run`（実際の実行）の2箇所だけを差し替えれば、CLIやネットワークに一切触れずにテストできます。

### モック化の粒度: サブプロセス境界 vs 関数引数の注入

`app/`には、モック化の粒度が異なる2つのやり方が併存しています。
何をテストしたいかによって使い分けます。


| モック化の方法 | 差し替える対象 | 向いている場面 | つまずきやすい点 |
|---|---|---|---|
| サブプロセス境界のモック化 | `shutil.which`と`subprocess.run` | `call_llm`自体（CLI引数の組み立て・エラー変換）を検証したいとき | モック関数の引数（`args`, `input`等）を実装のシグネチャに合わせないと、`fake_run`が呼ばれず失敗する |
| 関数引数のフェイク注入（`call_llm=default_call_llm`） | `call_llm`そのもの | `research_news_batch`等、`call_llm`を使う側の挙動を検証したいとき | 引数デフォルトを用意していない既存関数には後から使えない（設計時点で組み込む必要がある） |

### 正常系・異常系の両方をテストする

- 正常系: `subprocess.run`が終了コード0でstdoutを返すケース
- 異常系1: CLIが見つからない（`shutil.which`が`None`）
- 異常系2: `subprocess.run`が非0終了コードを返す

### `call_llm`をモック化したテストを書く手順

サブプロセス境界のモック化を例に、テスト作成の手順を示します。

1. `monkeypatch.setattr("shutil.which", lambda name: "claude-executable")`でCLI検出を差し替える。
   - つまずきやすい点: これを忘れると、テスト環境に`claude`コマンドが無い場合`ClaudeCLINotFoundError`で落ちる。
2. `fake_run`関数を定義し、期待する引数の形（`args`, `input`等）を`assert`する。
   - つまずきやすい点: 実装側の`subprocess.run`呼び出しの引数名・順序が変わると、このassertが壊れる（実装とテストの結合度が高い）。
3. `monkeypatch.setattr(subprocess, "run", fake_run)`で実際の実行を差し替える。
4. `call_llm(...)`を呼び出し、戻り値または送出される例外を検証する。
   - つまずきやすい点: 正常系だけでなく、`returncode != 0`のケースも忘れずにテストする。

### ログ出力の検証

リクエスト内容は成功・失敗にかかわらず常にログに出しますが、レスポンス内容は成功時のみログに出し、失敗時は出さない設計になっています。
これは、失敗時のレスポンスに機密情報が含まれる可能性を考慮した意図的な設計です。
テストでも`caplog`を使ってこの挙動を確認しています。

## 実ソースコード（Python / プロンプト例、出典パス明記）

出典: `ai-stock-investing-tutorial/app/tests/test_llm_client.py`

```python
def test_call_llm_returns_stdout_on_success(monkeypatch):
    monkeypatch.setattr("shutil.which", lambda name: "claude-executable")

    def fake_run(args, input, capture_output, text, encoding, timeout):
        assert args[0] == "claude-executable"
        assert args[-1] == "-p"
        assert "--system-prompt" in args
        assert input == "hello"
        return subprocess.CompletedProcess(args, 0, stdout="response text\n", stderr="")

    monkeypatch.setattr(subprocess, "run", fake_run)
    assert call_llm("hello") == "response text"


def test_call_llm_raises_on_nonzero_exit(monkeypatch):
    monkeypatch.setattr("shutil.which", lambda name: "claude-executable")

    def fake_run(args, input, capture_output, text, encoding, timeout):
        return subprocess.CompletedProcess(args, 1, stdout="", stderr="boom")

    monkeypatch.setattr(subprocess, "run", fake_run)
    with pytest.raises(ClaudeCLIError):
        call_llm("hello")
```

前述の「レスポンス内容は失敗時にログへ出さない」設計を検証するテストです。
`caplog`はpytestが提供する、ログ出力を検証するためのfixtureです（`monkeypatch`と同様、引数名で自動的に注入されます）。

出典: `ai-stock-investing-tutorial/app/tests/test_llm_client.py`

```python
def test_call_llm_does_not_log_response_on_failure(monkeypatch, caplog):
    monkeypatch.setattr(st, "secrets", {})
    monkeypatch.setattr("shutil.which", lambda name: "claude-executable")

    def fake_run(args, input, capture_output, text, encoding, timeout):
        return subprocess.CompletedProcess(
            args, 1, stdout="should not be logged", stderr="boom"
        )

    monkeypatch.setattr(subprocess, "run", fake_run)
    with caplog.at_level(logging.INFO, logger="data_api.llm_client"):
        with pytest.raises(ClaudeCLIError):
            call_llm("prompt")

    assert "Claude CLIリクエスト: prompt" in caplog.text
    assert "Claude CLIレスポンス" not in caplog.text
```

`caplog.text`に対する`assert`が2つある点がポイントです。
「リクエストは出ている」ことと「レスポンスは出ていない」ことの両方を検証しないと、ログ出力漏れに気づけません。

呼び出し元の関数を差し替え可能にするパターン（出典: `ai-stock-investing-tutorial/app/analysis_agents/news_research_agent.py`）:

```python
def research_news_batch(
    news_by_ticker: dict[str, list[dict]], call_llm=default_call_llm
) -> dict[str, dict]:
    ...
```

このように`call_llm=default_call_llm`という引数デフォルトを持たせておくと、テスト側は`research_news_batch(news_by_ticker, call_llm=fake_call_llm)`のようにフェイク関数を注入でき、`test_llm_client.py`のようなサブプロセスレベルのモックすら不要になります。

## 演習課題

1. `research_news_batch`（`news_research_agent.py`）に対するテストを、`call_llm`をモック関数として注入する形で1つ書いてください。
2. `call_llm`がタイムアウトした場合（`subprocess.TimeoutExpired`）のテストケースを追加する場合を考えてください。
   1. `fake_run`が`subprocess.TimeoutExpired`を送出するようにする方法を考えてください。
   2. `call_llm`側でこの例外をキャッチしていない場合、テストで何を`assert`すべきか考えてください（`pytest.raises`の対象）。

## 理解度チェック

- [ ] pytestのfixtureがテスト関数にどう注入されるか、`monkeypatch`がなぜ後始末不要で使えるか説明できる
- [ ] `call_llm`をモック化する際にどの2箇所を差し替えればよいか説明できる
- [ ] 正常系・異常系の両方をテストする理由を説明できる
- [ ] `call_llm=default_call_llm`という引数デフォルトパターンがテストしやすさにどう寄与するか説明できる
- [ ] サブプロセス境界のモックと関数引数のフェイク注入、2つのモック化手法を使い分けられる

---

[← 前へ: バッチ化・並列化](04-batching-and-parallelization.md) | [次へ: 04-trust-and-safety-ux →](../04-trust-and-safety-ux/00-README.md)
