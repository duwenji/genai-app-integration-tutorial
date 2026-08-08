# LLM呼び出しのテスト

## この教材で身につくこと

- 非決定的なLLM呼び出しをモック化し、外部通信・CLI起動なしにテストできる
- 正常系・異常系の両方をテストする設計ができる
- `call_llm`を差し替え可能にする引数デフォルトパターンを理解できる

## 概要

LLMの応答は決定的ではなく、実際にCLIやAPIを呼び出すテストは遅く不安定です。
本教材では、`ai-stock-investing-tutorial`のアプリがどのように
`call_llm`をモック化してテストしているかを扱います。

## 位置づけ

本教材はカテゴリ03の最終教材です。これまでに学んだキャッシュ・並列化・
フォールバックの実装は、いずれもこの教材で学ぶモック化の手法でテスト可能です。

## 主要概念・設計判断の解説

### pytestのfixtureと`monkeypatch`の仕組み

`test_call_llm_returns_stdout_on_success(monkeypatch)`のように、テスト関数の
引数に`monkeypatch`と書くだけで使えています。これはpytestの**fixture**という
仕組みによるものです。テスト関数の引数名がfixture名と一致すると、pytestが
該当する値を自動的に注入してくれます（importは不要）。`monkeypatch`はpytestが
標準で提供しているfixtureの1つで、「実行中のオブジェクト・属性・環境変数を
一時的に差し替え、テスト終了後は自動的に元へ戻す」役割を持ちます。

コード中には2種類の書き方が出てきます。

```python
monkeypatch.setattr("shutil.which", lambda name: "claude-executable")
monkeypatch.setattr(subprocess, "run", fake_run)
```

どちらも`setattr(対象, 属性名, 差し替え後の値)`という同じ操作ですが、対象の
指定方法が異なります。前者は`"モジュール名.属性名"`という文字列で対象を指定し、
後者は`subprocess`モジュールオブジェクトと属性名`"run"`を分けて渡しています。
挙動は同じで、後者の書き方ではimport済みのオブジェクトをそのまま渡せます。

`monkeypatch.setattr`が`unittest.mock.patch`と違い`with`文や`try/finally`を
書かずに済むのは、fixtureの後始末（テアダウン）機構がテスト終了時に自動で
元の状態へ戻してくれるためです。

### モック化する2箇所

`call_llm`はサブプロセス呼び出しの境界が明確なため、
`shutil.which`（CLIパスの解決）と`subprocess.run`（実際の実行）の
2箇所だけを差し替えれば、CLIやネットワークに一切触れずにテストできます。

### 正常系・異常系の両方をテストする

- 正常系: `subprocess.run`が終了コード0でstdoutを返すケース
- 異常系1: CLIが見つからない（`shutil.which`が`None`）
- 異常系2: `subprocess.run`が非0終了コードを返す

### ログ出力の検証

リクエスト内容は成功時のみログに出し、失敗時のレスポンス内容は
ログに出さない設計になっています。これは、失敗時のレスポンスに
機密情報が含まれる可能性を考慮した意図的な設計です。
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

呼び出し元の関数を差し替え可能にするパターン（出典:
`ai-stock-investing-tutorial/app/analysis_agents/news_research_agent.py`）:

```python
def research_news_batch(
    news_by_ticker: dict[str, list[dict]], call_llm=default_call_llm
) -> dict[str, dict]:
    ...
```

このように`call_llm=default_call_llm`という引数デフォルトを持たせておくと、
テスト側は`research_news_batch(news_by_ticker, call_llm=fake_call_llm)`
のようにフェイク関数を注入でき、`test_llm_client.py`のような
サブプロセスレベルのモックすら不要になります。

## 演習課題

1. `research_news_batch`（`news_research_agent.py`）に対するテストを、
   `call_llm`をモック関数として注入する形で1つ書いてください。
2. `call_llm`がタイムアウトした場合（`subprocess.TimeoutExpired`）の
   テストケースを追加するなら、どうモックするか設計してください。

## 理解度チェック

- [ ] pytestのfixtureがテスト関数にどう注入されるか、`monkeypatch`が
      なぜ後始末不要で使えるか説明できる
- [ ] `call_llm`をモック化する際にどの2箇所を差し替えればよいか説明できる
- [ ] 正常系・異常系の両方をテストする理由を説明できる
- [ ] `call_llm=default_call_llm`という引数デフォルトパターンがテストしやすさに
      どう寄与するか説明できる

---

[← 前へ: バッチ化・並列化](03-batching-and-parallelization.md) | [次へ: 04-trust-and-safety-ux →](../04-trust-and-safety-ux/00-README.md)
