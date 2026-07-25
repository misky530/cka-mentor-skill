#!/usr/bin/env python3
"""哨兵脚本：对比本地 source-manifest.json 记录的 CKA curriculum 版本
与 https://github.com/cncf/curriculum 上游最新版本，版本不一致时报警。

用法：
    python3 scripts/check_curriculum_version.py
    python3 scripts/check_curriculum_version.py --manifest source-manifest.json --json

退出码：
    0 - 版本一致，或成功确认无需处理
    1 - 检测到上游版本变化（需要人工评估是否重新蒸馏 references/）
    2 - 检查失败（网络错误 / 解析失败 / manifest 缺失字段），无法判定

无第三方依赖，仅用标准库；可选设置环境变量 GITHUB_TOKEN 提升 GitHub API 速率限制。
"""
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path

REPO_CONTENTS_URL = "https://api.github.com/repos/cncf/curriculum/contents/{path}"
# 依次尝试的目录：根目录（历史布局）、cka/ 子目录（上游正在按考试类型重组）
CANDIDATE_DIRS = ("", "cka")
CKA_PDF_PATTERN = re.compile(r"^CKA_Curriculum_v([\d.]+)\.pdf$", re.IGNORECASE)


def load_local_version(manifest_path: Path) -> str:
    with manifest_path.open(encoding="utf-8") as f:
        manifest = json.load(f)
    try:
        return manifest["exam"]["curriculum_version"]
    except KeyError as exc:
        raise ValueError(
            f"manifest 缺少 exam.curriculum_version 字段: {manifest_path}"
        ) from exc


def _list_dir(path: str) -> list:
    req = urllib.request.Request(
        REPO_CONTENTS_URL.format(path=path), headers={"User-Agent": "cka-mentor-skill-sentinel"}
    )
    token = os.environ.get("GITHUB_TOKEN")
    if token:
        req.add_header("Authorization", f"Bearer {token}")

    with urllib.request.urlopen(req, timeout=15) as resp:
        return json.load(resp)


def fetch_upstream_version() -> str:
    checked = []
    for directory in CANDIDATE_DIRS:
        try:
            entries = _list_dir(directory)
        except urllib.error.HTTPError as exc:
            if exc.code == 404:
                checked.append(directory or "/")
                continue
            raise

        for entry in entries:
            match = CKA_PDF_PATTERN.match(entry.get("name", ""))
            if match:
                return match.group(1)
        checked.append(directory or "/")

    raise ValueError(
        "上游仓库未找到匹配 CKA_Curriculum_v*.pdf 的文件（已尝试目录："
        f"{', '.join(checked)}）"
    )


def main() -> int:
    manifest_path = Path("source-manifest.json")
    as_json = False
    args = sys.argv[1:]
    i = 0
    while i < len(args):
        if args[i] == "--manifest":
            manifest_path = Path(args[i + 1])
            i += 2
        elif args[i] == "--json":
            as_json = True
            i += 1
        else:
            print(f"未知参数: {args[i]}", file=sys.stderr)
            return 2

    result = {"manifest_path": str(manifest_path)}

    try:
        local_version = load_local_version(manifest_path)
        result["local_version"] = local_version
    except (FileNotFoundError, ValueError, json.JSONDecodeError) as exc:
        result["status"] = "error"
        result["error"] = str(exc)
        _emit(result, as_json)
        return 2

    try:
        upstream_version = fetch_upstream_version()
        result["upstream_version"] = upstream_version
    except (urllib.error.URLError, urllib.error.HTTPError, ValueError, TimeoutError) as exc:
        result["status"] = "error"
        result["error"] = f"无法获取上游版本: {exc}"
        _emit(result, as_json)
        return 2

    if local_version == upstream_version:
        result["status"] = "ok"
        _emit(result, as_json)
        return 0

    result["status"] = "version_drift"
    result["message"] = (
        f"上游 CNCF curriculum 已从 v{local_version} 更新到 v{upstream_version}，"
        "需要人工评估是否重新拉取 curriculum、更新 manifest 并重新蒸馏 references/。"
    )
    _emit(result, as_json)
    return 1


def _emit(result: dict, as_json: bool) -> None:
    if as_json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return

    status = result.get("status")
    if status == "ok":
        print(f"[OK] 版本一致：本地 v{result['local_version']} == 上游 v{result['upstream_version']}")
    elif status == "version_drift":
        print(f"[WARN] {result['message']}")
    else:
        print(f"[ERROR] {result.get('error')}", file=sys.stderr)


if __name__ == "__main__":
    sys.exit(main())
