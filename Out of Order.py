import argparse
import json
import random
import signal
import sys
import time
from pathlib import Path

class Color:
    BLACK          = '\033[30m'#(text) black
    RED            = '\033[31m'#(text) red
    GREEN          = '\033[32m'#(text) green
    YELLOW         = '\033[33m'#(text) yellow
    BLUE           = '\033[34m'#(text) blue
    RESET          = '\033[0m'#reset all

# パス設定
BASE_DIR =  Path(r"C:\Users\user\Desktop\a-Shall\eiken\eiken\new-eiken-test-system")
DATA_DIR =  BASE_DIR

# ユーティリティ
def load_questions(path: Path):
    if not path.exists():
        raise FileNotFoundError(f"JSON file not found: {path}")
    with path.open(encoding="utf-8") as f:
        return json.load(f)

def ask_select(q: dict, q_num: int):
    question = q.get("question")
    hint = q.get("hint")
    choices = q.get("choices")
    answer = q.get("answer")
    comment = q.get("comment", {})

    hint_shown = False

    if not question or not choices or answer is None:
        print(f"{Color.RED}Skipping question: invalid format{Color.RESET}")
        return False

    print(f"\nQuestion #{q_num}")
    print(question)
    print("")
    for i, c in enumerate(choices, 1):
        print(f"{i}: {c}", end="   ")
    print("\n")
    print(f"{Color.YELLOW}(show hint: h){Color.RESET}")
    print("")
    # input loop
    while True:
        raw = input("Enter number: ").strip()

        if raw.lower() == "h":
            if hint:
                print(f"{Color.BLUE}\nHint: {hint}\n{Color.RESET}")
                hint_shown = True
            else:
                print(f"{Color.RED}\nNo hint available.\n{Color.RESET}")
            continue

        try:
            sel = int(raw) - 1
            user_choice = choices[sel]
            break
        except Exception:
            print(f"{Color.RED}→ Invalid input. Enter a number or 'h'.{Color.RESET}")

    correct = (user_choice == answer)

    if correct:
        print("\n")
        print(f"{Color.GREEN}→ Correct!{Color.RESET}")
    else:
        print("\n")
        print(f"{Color.RED}→ Incorrect.{Color.RESET}")

    user_index = sel + 1
    correct_index = choices.index(answer) + 1

    print(f"You: {user_index} {user_choice}")
    print(f"Answer: {correct_index} {answer}")

    # comment / hint display
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

def signal_handler(sig, frame):
    print("\nInterrupted.")
    print(f"Progress: {answered} / {total}")
    sys.exit(0)

# メイン処理
def main():
    global answered, total

    parser = argparse.ArgumentParser(description="CLI Eiken quiz tool (a-Shell compatible)")
    parser.add_argument("-f", "--file", required=True, help="JSON file name (without extension)")
    parser.add_argument("-n", "--num", type=int, default=10, help="Number of questions (default 10)")
    parser.add_argument("-o", "--order", choices=["random", "sequential"], default="random", help="Order of questions")
    args = parser.parse_args()

    DATA_DIR.mkdir(exist_ok=True)
    json_path = DATA_DIR / f"{args.file}"

    try:
        questions = load_questions(json_path)
    except Exception as e:
        print(f"{Color.RED}Load error: {e}{Color.RESET}")
        sys.exit(1)

    if not isinstance(questions, list):
        print(f"{Color.RED}Invalid JSON format: expected an array{Color.RESET}")
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

    for i, q in enumerate(questions, 1):
        print("\n---")
        if ask_select(q, i):
            correct_count += 1
            answered += 1
            print(f"Progress: {answered}/{total}  Correct: {correct_count}")

    elapsed = time.time() - start
    print("\n=== Result ===")
    print(f"Correct: {correct_count}/{total}")
    print(f"Elapsed time: {int(elapsed//60):02d}m{int(elapsed%60):02d}s")

if __name__ == "__main__":
    main()

