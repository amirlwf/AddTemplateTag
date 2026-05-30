#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

# پسوندهایی که معمولاً باید با {% static %} پوشانده شوند
STATIC_EXTENSIONS = {
    ".css", ".js", ".mjs",
    ".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".ico",
    ".bmp", ".avif", ".tif", ".tiff",
    ".woff", ".woff2", ".ttf", ".eot", ".otf",
    ".map", ".pdf", ".mp3", ".mp4", ".webm", ".ogg",
}

LOAD_STATIC_RE = re.compile(r"{%\s*load\s+[^%]*\bstatic\b[^%]*%}", re.IGNORECASE)
ATTR_RE = re.compile(
    r'(?P<attr>\b(?:src|href)\b)\s*=\s*(?P<quote>["\'])(?P<value>.*?)(?P=quote)',
    re.IGNORECASE | re.DOTALL,
)

SKIP_PREFIXES = (
    "http://",
    "https://",
    "//",
    "mailto:",
    "tel:",
    "data:",
    "javascript:",
    "#",
)

def should_wrap_static(value: str, attr_name: str) -> bool:
    v = value.strip()

    if not v:
        return False

    # قبلاً template شده
    if "{%" in v or "{{" in v:
        return False

    lower = v.lower()
    if lower.startswith(SKIP_PREFIXES):
        return False

    # لینک‌های داخلی HTML را دست نزن
    # مثل about.html، contact.html، /blog/ و ...
    path_only = re.split(r"[?#]", v, maxsplit=1)[0]
    suffix = Path(path_only).suffix.lower()

    if suffix in STATIC_EXTENSIONS:
        return True

    # برای src معمولاً فایل استاتیک است، حتی اگر querystring داشته باشد
    if attr_name.lower() == "src" and suffix:
        return True

    return False

def build_static_tag(value: str) -> str:
    """
    خروجی:
      {% static 'img/a.png' %}
    یا
      {% static "img/a.png" %}
    """
    if "'" not in value:
        return f"{{% static '{value}' %}}"
    if '"' not in value:
        return f'{{% static "{value}" %}}'
    # مسیرهای خیلی نادر با هر دو نوع کوتیشن
    raise ValueError(f"Path contains both single and double quotes: {value}")

def process_html(content: str) -> tuple[str, int]:
    changed = 0

    def repl(match: re.Match) -> str:
        nonlocal changed
        attr = match.group("attr")
        quote = match.group("quote")
        value = match.group("value")

        if not should_wrap_static(value, attr):
            return match.group(0)

        try:
            static_value = build_static_tag(value)
        except ValueError:
            return match.group(0)

        changed += 1
        return f'{attr}={quote}{static_value}{quote}'

    new_content = ATTR_RE.sub(repl, content)

    # اگر static استفاده شده ولی load static ندارد، اضافه کن
    if changed > 0 and not LOAD_STATIC_RE.search(new_content):
        new_content = "{% load static %}\n" + new_content

    return new_content, changed

def output_path_for(src_file: Path, old_dir: Path, new_dir: Path) -> Path:
    rel = src_file.relative_to(old_dir)
    dest_dir = new_dir / rel.parent
    return dest_dir / f"{src_file.stem}_new{src_file.suffix}"

def main() -> int:
    parser = argparse.ArgumentParser(
        description="Add Django {% static %} tags to HTML files inside old/ and write results to nee/."
    )
    parser.add_argument(
        "--old",
        default="old",
        help="Folder containing original HTML files (default: old)",
    )
    parser.add_argument(
        "--new",
        default="new",
        help="Folder for output files (default: new)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would change without writing files",
    )
    args = parser.parse_args()

    base_dir = Path(__file__).resolve().parent
    old_dir = (base_dir / args.old).resolve()
    new_dir = (base_dir / args.new).resolve()

    if not old_dir.exists() or not old_dir.is_dir():
        print(f"Error: folder not found -> {old_dir}", file=sys.stderr)
        return 1

    html_files = sorted(old_dir.rglob("*.html"))
    if not html_files:
        print(f"No HTML files found in: {old_dir}")
        return 0

    total_files = 0
    total_changes = 0

    for src_file in html_files:
        original = src_file.read_text(encoding="utf-8", errors="ignore")
        updated, changes = process_html(original)

        dest_file = output_path_for(src_file, old_dir, new_dir)

        if args.dry_run:
            print(f"[DRY] {src_file.relative_to(old_dir)} -> {dest_file.relative_to(new_dir)} | changes: {changes}")
            continue

        dest_file.parent.mkdir(parents=True, exist_ok=True)
        dest_file.write_text(updated, encoding="utf-8")

        total_files += 1
        total_changes += changes
        print(f"[OK] {src_file.relative_to(old_dir)} -> {dest_file.relative_to(new_dir)} | changes: {changes}")

    if args.dry_run:
        print(f"\nDry run complete. Files scanned: {len(html_files)}")
    else:
        print(f"\nDone. Files written: {total_files}, total replacements: {total_changes}")

    return 0

if __name__ == "__main__":
    raise SystemExit(main())
