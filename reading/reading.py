#!/usr/bin/env python3
import argparse
import json
import random
import signal
import sys
import time
from pathlib import Path

# =========================
# 色定義
# =========================
class Color:
    RED   = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE  = '\033[34m'
    RESET = '\033[0m'

# =========================
# パス設定
# =========================
BASE_DIR = Path(r"C:\Users\user\Desktop\a-Shall\eiken\eiken\reading")
DATA_DIR = BASE_DIR

# =========================
# グローバル（Ctrl+C 用）
# =========================
answered = 0
total = 0

# =========================
# JSON読み込み
# =========================
def load_questions(path: Path):
    if not path.exists():
        raise FileNotFoundError(f"JSONファイルが見つかりません: {path}")
    with path.open(encoding="utf-8") as f:
        return json.load(f)

# =========================
# 小問（選択問題）
# =========================
def ask_subquestion(q: dict, label: str):
    print(f"\n[{label}]")
    print(q["question"])
    print()

    for i, c in enumerate(q["choices"], 1):
        print(f"{i}: {c}")
    print()

    while True:
        raw = input("input number: ").strip()
        try:
            sel = int(raw) - 1
            if sel < 0 or sel >= len(q["choices"]):
                raise ValueError
            user_choice = q["choices"][sel]
            break
        except:
            print(f"{Color.RED}→ wrong input{Color.RESET}")

    correct = (user_choice == q["answer"])

    if correct:
        print(f"{Color.GREEN}→ correct!{Color.RESET}")
    else:
        print(f"{Color.RED}→ incorrect{Color.RESET}")
        print(f"answer: {q['answer']}")

    return correct

# =========================
# 大問（説明文＋複数小問）
# =========================
def ask_big_question(problem: dict, q_num: int):
    global answered

    # 大問タイトル・説明文だけ表示
    print("\n" + "=" * 50)
    print(f"【No.{q_num}】")
    print(f"{Color.GREEN}{problem['title']}{Color.RESET}")
    print()
    print(problem["description"])
    print("=" * 50)

    # ★ ここで一旦止める
    input(f"{Color.YELLOW}Are you ready? Press Enter to continue!{Color.RESET}")

    correct = 0
    total_sub = len(problem["questions"])

    # 小問スタート
    for sub in problem["questions"]:
        label = f"No.{q_num}-{sub['sub_id']}"
        answered += 1
        if ask_subquestion(sub, label):
            correct += 1

    print(f"\n→ No.{q_num} count: {correct}/{total_sub}")
    input(f"{Color.YELLOW}Press Enter to continue…{Color.RESET}")

    return correct, total_sub

# =========================
# Ctrl+C ハンドラ
# =========================
def signal_handler(sig, frame):
    print("\nPaused.")
    print(f"進捗: {answered}/{total}")
    sys.exit(0)

# =========================
# メイン処理
# =========================
def main():
    global total

    parser = argparse.ArgumentParser(description="CLI 共通テスト風 出題ツール")
    parser.add_argument("-f", "--file", required=True, help="JSONファイル名（拡張子不要）")
    parser.add_argument("-n", "--num", type=int, default=1, help="出題する大問数")
    parser.add_argument("-o", "--order", choices=["random", "sequential"], default="random", help="出題順")
    args = parser.parse_args()

    json_path = DATA_DIR / f"{args.file}.json"

    try:
        problems = load_questions(json_path)
    except Exception as e:
        print(f"{Color.RED}ERROR!!: {e}{Color.RESET}")
        sys.exit(1)

    if not isinstance(problems, list):
        print(f"{Color.RED}The JSON must be in array format.{Color.RESET}")
        sys.exit(1)

    if args.order == "random":
        random.shuffle(problems)

    if args.num:
        problems = problems[:args.num]

    total = sum(len(p["questions"]) for p in problems)

    correct_total = 0
    answered_sub = 0
    start = time.time()

    signal.signal(signal.SIGINT, signal_handler)

    for i, problem in enumerate(problems, 1):
        c, t = ask_big_question(problem, i)
        correct_total += c
        answered_sub += t
        print(f"progress: {answered}/{total}  correct: {correct_total}")

    elapsed = time.time() - start

    print("\n=== Result ===")
    print(f"count: {correct_total}/{total}")
    print(f"time: {int(elapsed//60):02d} min {int(elapsed%60):02d} sec")
    print(f"{Color.GREEN}SEE YOU AGAIN!{Color.RESET}")
    print("")


# =========================
if __name__ == "__main__":
    main()
