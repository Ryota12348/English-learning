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
    BLACK  = '\033[30m'
    RED    = '\033[31m'
    GREEN  = '\033[32m'
    YELLOW = '\033[33m'
    BLUE   = '\033[34m'
    RESET  = '\033[0m'

# =========================
# パス設定
# =========================
BASE_DIR = Path(r"C:\Users\user\Desktop\a-Shall\eiken\eiken\english-learning")
DATA_DIR = BASE_DIR / "data"

# =========================
# JSON 読み込み
# =========================
def load_questions(path: Path):
    if not path.exists():
        raise FileNotFoundError(f"JSON file not found: {path}")
    with path.open(encoding="utf-8") as f:
        return json.load(f)

# =========================
# メニュー選択
# =========================
def select_menu(title, options):
    print("\n" + "=" * 35)
    print(f"{title}")
    print("=" * 35)

    for i, opt in enumerate(options, 1):
        print(f"{i}) {opt}")

    while True:
        sel = input("Select: ").strip()
        if sel.isdigit() and 1 <= int(sel) <= len(options):
            return int(sel) - 1
        print(f"{Color.RED}Invalid input.{Color.RESET}")

# =========================
# 選択肢問題
# =========================
def ask_select(q: dict, q_num: int):
    question = q.get("question")
    hint = q.get("hint")
    choices = q.get("choices", [])
    answer = q.get("answer")
    comment = q.get("comment", {})

    hint_shown = False

    print(f"\n{Color.BLUE}Question No.{q_num}{Color.RESET}")
    print(question + "\n")

    for i, c in enumerate(choices, 1):
        print(f"{i}: {c}", end="   ")
    print("\n\n(show hint: h)\n")

    while True:
        raw = input("Enter number: ").strip()

        if raw.lower() == "h":
            if hint:
                print(f"{Color.BLUE}\nHint: {hint}\n{Color.RESET}")
                hint_shown = True
            else:
                print(f"{Color.RED}\nNo hint available.\n{Color.RESET}")
            continue

        if raw.isdigit():
            sel = int(raw) - 1
            if 0 <= sel < len(choices):
                user_choice = choices[sel]
                break

        print(f"{Color.RED}→ Invalid input.{Color.RESET}")

    correct = (user_choice == answer)

    print()
    print(f"{Color.GREEN}→ Correct!{Color.RESET}" if correct else f"{Color.RED}→ Incorrect.{Color.RESET}")
    print(f"You    : {user_choice}")
    print(f"Answer : {answer}")

    if comment or (hint and not hint_shown):
        print("\n[Comment]")
        for i, c in enumerate(choices, 1):
            meaning = comment.get(c)
            if meaning:
                print(f"{i}) {c}: {meaning}")

        if hint and not hint_shown:
            print(f"\nHint: {hint}")

    input(f"\n{Color.YELLOW}Press Enter to continue...{Color.RESET}")

    return {
        "question": question,
        "choices": choices,
        "user_choice": user_choice,
        "user_meaning": comment.get(user_choice, ""),
        "answer": answer,
        "meaning": comment.get(answer, ""),
        "correct": correct,
        "hint": hint
    }

# =========================
# 結果保存
# =========================
def save_result_txt(results, correct_count, total, elapsed, title):
    timestamp_file = time.strftime("%Y%m%d_%H%M%S")
    timestamp_print = time.strftime("%Y/%m/%d %H:%M:%S")
    out_path = BASE_DIR / f"result_{timestamp_file}.txt"

    with out_path.open("w", encoding="utf-8") as f:
        f.write(f"{title}\n\n")
        f.write("=" * 40 + "\n")
        f.write(f"Date   : {timestamp_print}\n")
        f.write(f"Score  : {correct_count}/{total}\n")
        f.write(f"Time   : {int(elapsed//60)}m {int(elapsed%60)}s\n\n")

        for i, r in enumerate(results, 1):
            f.write(f"Q{i}: {r['question']}\n")
            f.write(
                f"Result : {r['user_choice']}({r['user_meaning']}) - "
                f"{'○' if r['correct'] else '×'} - "
                f"{r['answer']}({r['meaning']})\n"
            )
            f.write("-" * 40 + "\n")

# =========================
# Ctrl+C
# =========================
def signal_handler(sig, frame):
    print("\nInterrupted.")
    sys.exit(0)

# =========================
# メイン処理
# =========================
def main():
    signal.signal(signal.SIGINT, signal_handler)

    # ジャンル
    genres = {
        "英検 準1級": DATA_DIR / "eiken" / "pre1",
        "英検 2級": DATA_DIR / "eiken" / "grade2",
        "入試問題": DATA_DIR / "exam",
        "ワーク復習": DATA_DIR / "workbook"
    }
    g_idx = select_menu("Genre", list(genres.keys()))
    genre_name = list(genres.keys())[g_idx]
    genre_dir = list(genres.values())[g_idx]

    # 問題形式
    types = ["選択肢", "並べ替え（未実装）", "英作文（未実装）"]
    t_idx = select_menu("Question Type", types)

    if t_idx != 0:
        print(f"{Color.RED}This mode is not implemented yet.{Color.RESET}")
        return

    # 問題数
    counts = [5, 10, 20, "Custom"]
    c_idx = select_menu("Number of Questions", counts)

    if counts[c_idx] == "Custom":
        num = int(input("Enter number: "))
    else:
        num = counts[c_idx]

    json_path = genre_dir / "choice.json"
    questions = load_questions(json_path)
    random.shuffle(questions)
    questions = questions[:num]

    print(f"\n{Color.GREEN}{genre_name} / 選択肢 / {num}問{Color.RESET}")
    input(f"{Color.YELLOW}Press Enter to start...{Color.RESET}")

    start = time.time()
    results = []
    correct_count = 0

    for i, q in enumerate(questions, 1):
        r = ask_select(q, i)
        results.append(r)
        if r["correct"]:
            correct_count += 1

    elapsed = time.time() - start

    print(f"\nResult: {correct_count}/{num}")
    save_result_txt(results, correct_count, num, elapsed, genre_name)

if __name__ == "__main__":
    main()
