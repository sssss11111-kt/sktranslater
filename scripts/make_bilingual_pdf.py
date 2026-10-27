#!/usr/bin/env python3
"""Assemble and verify an alternating English/Chinese PDF."""
from __future__ import annotations
import argparse, json, re
from pathlib import Path
import pymupdf

def render_size(page):
    pix = page.get_pixmap(matrix=pymupdf.Matrix(0.5, 0.5), alpha=False)
    return [pix.width, pix.height]

def chinese_count(text):
    return len(re.findall(r"[\u3400-\u9fff]", text))

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("source", type=Path)
    ap.add_argument("chinese", type=Path)
    ap.add_argument("--output", type=Path, required=True)
    ap.add_argument("--qc", type=Path)
    args = ap.parse_args()
    qc_path = args.qc or args.output.with_name(args.output.stem + "_qc.json")
    src = pymupdf.open(args.source)
    zh = pymupdf.open(args.chinese)
    if len(src) != len(zh):
        raise SystemExit(f"page count mismatch: source={len(src)} chinese={len(zh)}")
    out = pymupdf.open()
    source_checks, geometry_checks, zh_counts = [], [], []
    for i, (sp, zp) in enumerate(zip(src, zh), 1):
        source_checks.append(True)
        geometry_checks.append(render_size(sp) == render_size(zp))
        zh_counts.append(chinese_count(zp.get_text()))
        if zh_counts[-1] == 0:
            raise SystemExit(f"Chinese page {i} has no Chinese characters")
        out.insert_pdf(src, from_page=i-1, to_page=i-1)
        out.insert_pdf(zh, from_page=i-1, to_page=i-1)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    part = args.output.with_suffix(args.output.suffix + ".part")
    out.save(part, garbage=4, deflate=True)
    out.close(); part.replace(args.output)
    result = pymupdf.open(args.output)
    odd_checks = [result[2*i].get_text() == src[i].get_text() and render_size(result[2*i]) == render_size(src[i]) for i in range(len(src))]
    report = {
        "source": str(args.source.resolve()), "chinese": str(args.chinese.resolve()), "output": str(args.output.resolve()),
        "source_pages": len(src), "chinese_pages": len(zh), "output_pages": len(result),
        "expected_output_pages": 2*len(src), "alternating_order": len(result) == 2*len(src),
        "odd_pages_match_source": all(odd_checks), "rendered_geometry_match": all(geometry_checks),
        "chinese_characters_by_page": zh_counts, "issues": []
    }
    if not all(odd_checks): report["issues"].append("one or more original pages differ")
    if not all(geometry_checks): report["issues"].append("one or more Chinese pages differ in rendered geometry")
    qc_path.write_text(json.dumps(report, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if report["issues"]: raise SystemExit(2)

if __name__ == "__main__": main()

