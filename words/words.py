import json
import random
import time
from pathlib import Path

# =========================
# 色定義
# =========================
class Color:
    RED    = '\033[31m'
    GREEN  = '\033[32m'
    YELLOW = '\033[33m'
    BLUE   = '\033[34m'
    RESET  = '\033[0m'

# =========================
# パス設定
# =========================
BASE_DIR = Path(__file__).parent
DATA_DIR = BASE_DIR / "data"

# =========================
# JSON読み込み
# =========================
def load_json(path):
    with open(path, encoding="utf-8") as f:
        return json.load(f)

# =========================
# メニュー表示
# =========================
def select_menu(title, options):
    print("\n" + "=" * 30)
    print(title)
    print("=" * 30)

    for i, opt in enumerate(options, 1):
        print(f"{i}) {opt}")

    while True:
        sel = input("Select: ").strip()
        if sel.isdigit() and 1 <= int(sel) <= len(options):
            return int(sel) - 1
        print("Invalid input.")

# =========================
# 問題出題（ヒント0対応）
# =========================
def ask_question(q, mode, index, total):
    print(f"\n{Color.YELLOW}Question No.{index}{Color.RESET}")
    print(f"No.{q['title']}")

    if mode == "ja_en":
        print(q["japanese"])
        answer = q["english"]
    else:
        print(q["english"])
        answer = q["japanese"]

    print("(Enter 0 to show hint)")

    hint_shown = False

    while True:
        user = input("> ").strip()

        if user == "0":
            if mode == "ja_en":
                print(f"{Color.BLUE}Hint: {q['first_letter']}_______{Color.RESET}")
            else:
                pos = q.get("part_of_speech", "unknown")
                print(f"{Color.BLUE}Hint: {pos}{Color.RESET}")
            hint_shown = True
            continue

        break

    if mode == "ja_en":
        correct = user.lower() == answer.lower()
    else:
        correct = answer in user

    if correct:
        print(f"{Color.GREEN}✔ Correct{Color.RESET}")
    else:
        print(f"{Color.RED}✖ Incorrect{Color.RESET}")
        print(f"Answer: {answer}")

    return correct

# =========================
# 復習モード（正解するまで）
# =========================
def review_mode(words, mode):
    while words:
        print(f"\n=== Review Mode ({len(words)} left) ===")
        random.shuffle(words)

        next_round = []

        for i, q in enumerate(words, 1):
            correct = ask_question(q, mode, i, len(words))
            if not correct:
                next_round.append(q)

        words = next_round

    print(f"\n{Color.GREEN}All words mastered.{Color.RESET}")

# =========================
# メイン処理
# =========================
def main():
    while True:

        # 単語帳選択
        books = [d.name for d in DATA_DIR.iterdir() if d.is_dir()]
        if not books:
            print("No word books found.")
            return

        b_idx = select_menu("Word Book", books)
        book_dir = DATA_DIR / books[b_idx]

        # 範囲選択
        ranges = [f.name for f in book_dir.glob("*.json")]
        if not ranges:
            print("No ranges found.")
            return

        r_idx = select_menu("Range", ranges)
        json_path = book_dir / ranges[r_idx]

        words = load_json(json_path)

        # 出題方向
        modes = ["日→英", "英→日"]
        m_idx = select_menu("Mode", modes)
        mode = "ja_en" if m_idx == 0 else "en_ja"

        # 問題数入力
        raw = input("How many questions? (default 10): ").strip()
        if raw == "":
            num = 10
        elif raw.isdigit() and int(raw) > 0:
            num = int(raw)
        else:
            print("Invalid input. Using default 10.")
            num = 10

        random.shuffle(words)
        questions = words[:min(num, len(words))]

        print("\nStart!")
        input("Press Enter to begin...")

        start = time.time()
        correct_count = 0
        wrong_words = []

        # 本試験
        for i, q in enumerate(questions, 1):
            correct = ask_question(q, mode, i, len(questions))
            if correct:
                correct_count += 1
            else:
                wrong_words.append(q)

        elapsed = time.time() - start
        score = round(correct_count / len(questions) * 100)

        # 結果表示
        print("\n" + "=" * 30)
        print("Result")
        print("=" * 30)
        print(f"Score   : {score} / 100")
        print(f"Correct : {correct_count} / {len(questions)}")
        print(f"Time    : {int(elapsed//60)}m {int(elapsed%60)}s")

        # 復習確認
        if wrong_words:
            print(f"\nRetry wrong words? ({len(wrong_words)} words)")
            print("1) Yes")
            print("2) No")

            while True:
                sel = input("Select: ").strip()
                if sel == "1":
                    review_mode(wrong_words, mode)
                    break
                if sel == "2":
                    break
                print("Invalid input.")
        else:
            print(f"\n{Color.GREEN}Perfect. All correct.{Color.RESET}")

        # 続行確認
        print("\n1) Back to menu")
        print("2) Exit")
        sel = input("Select: ").strip()
        if sel == "2":
            print("Good job. See you.")
            break


if __name__ == "__main__":
    main()