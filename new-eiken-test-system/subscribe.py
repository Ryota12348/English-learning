import argparse
import json
import random
import signal
import sys
import time
from pathlib import Path

# ==========================
# 色定義
# ==========================
class Color:
    BLACK  = '\033[30m'
    RED    = '\033[31m'
    GREEN  = '\033[32m'
    YELLOW = '\033[33m'
    BLUE   = '\033[34m'
    RESET  = '\033[0m'

# ==========================
# パス設定
# ==========================
BASE_DIR = Path(r"C:\Users\user\Desktop\a-Shall\eiken\eiken\new-eiken-test-system")

# ==========================
# ユーティリティ
# ==========================
def load_questions(path: Path):
    if not path.exists():
        raise FileNotFoundError(f"JSON file not found: {path}")
    with path.open(encoding="utf-8") as f:
        return json.load(f)

# =========================
# 問題出題
# =========================
def ask_select(q: dict, q_num: int):
    question = q.get("question")
    hint = q.get("hint")
    choices = q.get("choices")
    answer = q.get("answer")

    hint_shown = False

    print(f"\nQuestion No.{q_num}")
    print(question)
    print()

    for i, c in enumerate(choices, 1):
        print(f"{i}: {c}", end="   ")
    print("\n")
    print(f"{Color.YELLOW}(show hint: h){Color.RESET}\n")

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

    print()
    if correct:
        print(f"{Color.GREEN}→ Correct!{Color.RESET}")
    else:
        print(f"{Color.RED}→ Incorrect.{Color.RESET}")

    print(f"You: {sel + 1} {user_choice}")
    print(f"Answer: {choices.index(answer) + 1} {answer}")

    input(f"\n{Color.YELLOW}Press Enter to continue...{Color.RESET}")

    return {
        "question": question,
        "choices": choices,
        "user_choice": user_choice,
        "answer": answer,
        "correct": correct,
        "hint": hint
    }

# =========================
# 結果保存
# =========================
def save_result_txt(results, correct_count, total, elapsed, file_name, vocab):
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    out_path = BASE_DIR / f"result_{timestamp}.txt"

    with out_path.open("w", encoding="utf-8") as f:
        f.write("Eiken Quiz Result\n")
        f.write("=" * 40 + "\n")
        f.write(f"File   : {file_name}\n")
        f.write(f"Score  : {correct_count}/{total}\n")
        f.write(f"Time   : {int(elapsed//60)}m {int(elapsed%60)}s\n\n")

        for i, r in enumerate(results, 1):
            f.write(f"Q{i}: {r['question']}\n")
            f.write(f"Your answer   : {r['user_choice']}\n")
            f.write(f"Correct answer: {r['answer']}\n")
            f.write(f"Result        : {'Correct' if r['correct'] else 'Incorrect'}\n")
            if r["hint"]:
                f.write(f"Hint          : {r['hint']}\n")
            f.write("-" * 40 + "\n")

        # Vocabulary List
        f.write("\nVocabulary List\n")
        f.write("=" * 40 + "\n")

        for word in sorted(vocab):
            meaning = vocab[word]
            if meaning:
                f.write(f"{word} : {meaning}\n")
            else:
                f.write(f"{word}\n")

    print(f"\n{Color.GREEN}Result saved to:{Color.RESET} {out_path}")

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
    parser = argparse.ArgumentParser(description="CLI Eiken quiz tool")
    parser.add_argument("-f", "--file", required=True, help="JSON file name (with extension)")
    parser.add_argument("-n", "--num", type=int, default=10, help="Number of questions")
    parser.add_argument("-o", "--order", choices=["random", "sequential"], default="random")
    args = parser.parse_args()

    json_path = BASE_DIR / args.file

    try:
        questions = load_questions(json_path)
    except Exception as e:
        print(f"{Color.RED}Load error: {e}{Color.RESET}")
        sys.exit(1)

    if args.order == "random":
        random.shuffle(questions)

    questions = questions[:args.num]

    total = len(questions)
    correct_count = 0
    results = []
    vocab = {}

    start = time.time()
    signal.signal(signal.SIGINT, signal_handler)

    for i, q in enumerate(questions, 1):
        print("\n---")
        result = ask_select(q, i)
        results.append(result)

        if result["correct"]:
            correct_count += 1

        # 単語収集
        choices = q.get("choices", [])
        comment = q.get("comment", {})
        for w in choices:
            if w not in vocab:
                vocab[w] = comment.get(w, "")

        print(f"Progress: {i}/{total}  Correct: {correct_count}")

    elapsed = time.time() - start

    print("\n=== Result ===")
    print(f"Correct: {correct_count}/{total}")
    print(f"Elapsed time: {int(elapsed//60):02d}m{int(elapsed%60):02d}s")

    save_result_txt(
        results,
        correct_count,
        total,
        elapsed,
        args.file,
        vocab
    )

if __name__ == "__main__":
    main()
