#!/usr/bin/env python3
"""
a-Shell (iOS) 対応 CLI 問題出題ツール
- JSON形式の select 問題を出題
- 即時フィードバック
- 標準ライブラリのみ使用
"""

import argparse
import json
import random
import signal
import sys
import time
from pathlib import Path

# =========================
# パス設定（a-Shell 正解）
# =========================
BASE_DIR = Path.home() / "Documents"
DATA_DIR = BASE_DIR / "eiken"

# =========================
# ユーティリティ
# =========================
def load_questions(path: Path):
    if not path.exists():
        raise FileNotFoundError(f"JSONファイルが見つかりません: {path}")
    with path.open(encoding="utf-8") as f:
        return json.load(f)

def ask_select(q: dict):
    hint = q.get("hint")
    choices = q.get("choices")
    answer = q.get("answer")
    comment = q.get("comment", {})

    if not choices or answer is None:
        print("※ 問題形式が不正なためスキップします")
        return False

    for i, c in enumerate(choices, 1):
        print(f"{i}: {c}", end="   ")
    print()
    print("（ヒントを見る: h）")

    # =========================
    # 入力ループ（h 対応）
    # =========================
    while True:
        raw = input("番号を入力: ").strip()

        if raw.lower() == "h":
            if hint:
                print(f"\nヒント: {hint}\n")
            else:
                print("\nヒントはありません。\n")
            continue

        try:
            sel = int(raw) - 1
            user_choice = choices[sel]
            break
        except Exception:
            print("→ 無効な入力。数字か h を入力してください。")

    correct = (user_choice == answer)

    if correct:
        print("→ 正解！")
    else:
        print("→ 不正解。")

    user_index = sel + 1
    correct_index = choices.index(answer) + 1

    print(f"あなた: {user_index} {user_choice}")
    print(f"正答  : {correct_index} {answer}")

    # =========================
    # comment 表示
    # =========================
    if comment:
        print("\n[Comment]")
        for i, c in enumerate(choices, 1):
            meaning = comment.get(c)
            if meaning:
                print(f"{i}) {c}: {meaning}")

    return correct


def signal_handler(sig, frame):
    print("\n中断しました。")
    print(f"進捗: {answered} / {total}")
    sys.exit(0)

# =========================
# メイン処理
# =========================
def main():
    global answered, total

    parser = argparse.ArgumentParser(description="CLI英検問題ツール（a-Shell対応）")
    parser.add_argument("-f", "--file", required=True, help="JSONファイル名（拡張子不要）")
    parser.add_argument("-n", "--num", type=int, help="出題数（省略時は全問）")
    parser.add_argument(
        "-o", "--order",
        choices=["random", "sequential"],
        default="random",
        help="出題順"
    )
    args = parser.parse_args()

    DATA_DIR.mkdir(exist_ok=True)
    json_path = DATA_DIR / f"{args.file}.json"

    try:
        questions = load_questions(json_path)
    except Exception as e:
        print(f"読み込みエラー: {e}")
        sys.exit(1)

    if not isinstance(questions, list):
        print("JSONの形式が不正です（配列である必要があります）")
        sys.exit(1)

    if args.order == "random":
        random.shuffle(questions)

    if args.num:
        questions = questions[:args.num]

    total = len(questions)
    answered = 0
    correct_count = 0
    start = time.time()

    signal.signal(signal.SIGINT, signal_handler)

    for q in questions:
        print("\n---")
        if ask_select(q):
            correct_count += 1
        answered += 1
        print(f"進捗: {answered}/{total}  正答: {correct_count}")

    elapsed = time.time() - start
    print("\n=== 結果 ===")
    print(f"正答数: {correct_count}/{total}")
    print(f"所要時間: {int(elapsed//60):02d}分{int(elapsed%60):02d}秒")

if __name__ == "__main__":
    main()
