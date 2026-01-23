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
import os

BASE_DIR = os.path.expanduser("~/Documents/english_quiz")
DATA_DIR = Path(BASE_DIR) / "data"

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
    print(title)
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

    return correct

# =========================
# Ctrl+C 対応
# =========================
def signal_handler(sig, frame):
    print("\nInterrupted.")
    sys.exit(0)

# =========================
# メイン処理
# =========================
def main():
    signal.signal(signal.SIGINT, signal_handler)

    while True:
        # =========================
        # ジャンル選択
        # =========================
        genres = {
            "英検 準1級": DATA_DIR / "eiken" / "pre1",
            "英検 2級": DATA_DIR / "eiken" / "grade2",
            "英検 準2級": DATA_DIR / "eiken" / "pre2",
            "入試問題": DATA_DIR / "exam",
            "ワーク復習": DATA_DIR / "workbook"
        }

        g_idx = select_menu("Genre", list(genres.keys()))
        genre_name = list(genres.keys())[g_idx]
        genre_dir = list(genres.values())[g_idx]

        # =========================
        # 問題形式
        # =========================
        types = ["選択肢", "並べ替え（未実装）", "英作文（未実装）"]
        t_idx = select_menu("Question Type", types)

        if t_idx != 0:
            print(f"{Color.RED}This mode is not implemented yet.{Color.RESET}")
            continue

        # =========================
        # 問題数（直接入力）
        # =========================
        while True:
            raw = input("How many questions? : ").strip()
            if raw.isdigit() and int(raw) > 0:
                num = int(raw)
                break
            print("Please enter a positive number.")

        # =========================
        # 問題ロード
        # =========================
        json_path = genre_dir / "choice.json"
        questions = load_questions(json_path)

        random.shuffle(questions)
        questions = questions[:num]

        print(f"\n{Color.GREEN}{genre_name} / 選択肢 / {num}問{Color.RESET}")
        input(f"{Color.YELLOW}Press Enter to start...{Color.RESET}")

        # =========================
        # 出題開始
        # =========================
        start = time.time()
        correct_count = 0

        for i, q in enumerate(questions, 1):
            if ask_select(q, i):
                correct_count += 1
            print(f"Progress: {i}/{num}  Correct: {correct_count}")

        # =========================
        # 結果表示（100点満点）
        # =========================
        elapsed = time.time() - start
        score = round(correct_count / num * 100)

        print("\n" + "=" * 30)
        print("Result")
        print("=" * 30)
        print(f"Score   : {score} / 100")
        print(f"Correct : {correct_count} / {num}")
        print(f"Time    : {int(elapsed//60)}m {int(elapsed%60)}s")

        def continue_menu():
            print("\n" + "=" * 30)
            print("Next Action")
            print("=" * 30)
            print("1) Back to menu")
            print("2) Exit")
            while True:
                sel = input("Select: ").strip()
                if sel == "1":
                    return True
                if sel == "2":
                    return False
                print("Invalid input.")

        # =========================
        # 続行 or 終了
        # =========================
        if not continue_menu():
            print("\nGood job! See you next time 👋")
            break


# =========================
# 実行
# =========================
if __name__ == "__main__":
    main()
