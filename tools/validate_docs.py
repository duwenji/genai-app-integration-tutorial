"""genai-app-integration-tutorialの教材ファイル構造を検証するスクリプト。

チェック内容:
1. 個別教材ファイル(00-README.md以外)が7つの必須見出しをこの順序で含むか
2. 図解計画に記載のファイルがMermaidコードブロック(```mermaid)を含むか
3. (--category未指定の全体実行時のみ) docs/配下および ルート/MASTER-INDEX.md
   等のMarkdownファイル内の相対リンクが実在するファイルを指しているか
   （カテゴリ執筆順に前後カテゴリへのリンクを書くため、全カテゴリが揃うまでは
   意図的にリンク切れが残る。そのため--category指定時はリンク検証を行わない）

依存: 標準ライブラリのみ。
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
DOCS_ROOT = REPO_ROOT / "docs"

REQUIRED_HEADINGS = [
    "## この教材で身につくこと",
    "## 概要",
    "## 位置づけ",
    "## 主要概念・設計判断の解説",
    "## 実ソースコード（Python / プロンプト例、出典パス明記）",
    "## 演習課題",
    "## 理解度チェック",
]

# 6.1節「図解計画」に対応するMermaid必須ファイル(カテゴリディレクトリ名, ファイル名)
MERMAID_REQUIRED = {
    ("01-invocation-and-architecture", "02-api-sdk-vs-cli-subprocess.md"),
    ("01-invocation-and-architecture", "03-system-prompt-and-io-boundary.md"),
    ("02-io-contract-design", "01-structured-output-json-contract.md"),
    ("02-io-contract-design", "04-multi-turn-dialogue-prompting.md"),
    ("03-reliability-and-cost", "01-defensive-parsing-and-fallback.md"),
    ("03-reliability-and-cost", "02-rate-limit-and-timeout.md"),
    ("03-reliability-and-cost", "03-caching-strategy.md"),
    ("03-reliability-and-cost", "04-batching-and-parallelization.md"),
    ("04-trust-and-safety-ux", "01-verification-checkpoint.md"),
    ("04-trust-and-safety-ux", "04-prompt-injection-defense.md"),
    ("05-agentic-workflow-patterns", "01-prompt-chaining.md"),
    ("05-agentic-workflow-patterns", "02-routing.md"),
    ("05-agentic-workflow-patterns", "03-orchestrator-workers.md"),
    ("05-agentic-workflow-patterns", "04-evaluator-optimizer.md"),
    ("05-real-world-case-study", "01-case-study-map.md"),
}

MD_LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")


def _category_dirs(only: str | None) -> list[Path]:
    dirs = sorted(p for p in DOCS_ROOT.glob("0*-*") if p.is_dir())
    if only:
        dirs = [d for d in dirs if d.name.startswith(only)]
    return dirs


def check_headings(path: Path) -> list[str]:
    problems = []
    text = path.read_text(encoding="utf-8")
    positions = []
    for heading in REQUIRED_HEADINGS:
        idx = text.find(heading)
        if idx == -1:
            problems.append(f"{path}: 見出し欠落 -> {heading}")
        positions.append(idx)
    present = [p for p in positions if p != -1]
    if present != sorted(present):
        problems.append(f"{path}: 見出しの順序が規定と一致しません")
    return problems


def check_mermaid(path: Path, category_dir: Path) -> list[str]:
    key = (category_dir.name, path.name)
    if key not in MERMAID_REQUIRED:
        return []
    text = path.read_text(encoding="utf-8")
    if "```mermaid" not in text:
        return [f"{path}: 図解計画対象だが```mermaidブロックが見つかりません"]
    return []


def check_links(path: Path) -> list[str]:
    problems = []
    text = path.read_text(encoding="utf-8")
    for match in MD_LINK_RE.finditer(text):
        target = match.group(1)
        if target.startswith(("http://", "https://", "#")):
            continue
        target_path = (path.parent / target).resolve()
        if not target_path.exists():
            problems.append(f"{path}: リンク切れ -> {target}")
    return problems


def main() -> int:
    # Windowsのコンソールがcp932等の場合に日本語出力が文字化けするのを防ぐ。
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    only = None
    if len(sys.argv) > 1 and sys.argv[1] == "--category":
        only = sys.argv[2]

    all_problems: list[str] = []
    for category_dir in _category_dirs(only):
        for md_file in sorted(category_dir.glob("*.md")):
            if only is None:
                # カテゴリを跨ぐ前後リンクは、他カテゴリが未執筆の間は必ず
                # リンク切れになるため、リンク検証は全体実行(only=None)時のみ行う。
                all_problems.extend(check_links(md_file))
            if md_file.name == "00-README.md":
                continue
            all_problems.extend(check_headings(md_file))
            all_problems.extend(check_mermaid(md_file, category_dir))

    if only is None:
        # ルート・docs/00-COVER.mdのリンク切れも全体実行時のみ合わせて確認する
        for md_file in [REPO_ROOT / "README.md", REPO_ROOT / "MASTER-INDEX.md", DOCS_ROOT / "00-COVER.md"]:
            if md_file.exists():
                all_problems.extend(check_links(md_file))

    if all_problems:
        print(f"{len(all_problems)}件の問題:")
        for problem in all_problems:
            print(f"  - {problem}")
        return 1

    print("OK: 問題は見つかりませんでした")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
