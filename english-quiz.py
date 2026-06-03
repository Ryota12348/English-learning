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
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"

# =========================
# JSON 読み込み（エラーハンドリング付き）
# =========================
def load_questions(path: Path):
    if not path.exists():
        print(f"{Color.RED}エラー: JSONファイルが見つかりません: {path}{Color.RESET}")
        sys.exit(1)
    try:
        with path.open(encoding="utf-8") as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"{Color.RED}エラー: JSONファイルの記述に構文エラーがあります。{Color.RESET}")
        print(f"{Color.RED}詳細: {e}{Color.RESET}")
        sys.exit(1)

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
# 共通：ヒント表示処理
# =========================
def check_hint_request(raw_input, hint):
    if raw_input.lower() == "h":
        if hint:
            print(f"{Color.BLUE}\nHint: {hint}\n{Color.RESET}")
            return True, True
        else:
            print(f"{Color.RED}\nNo hint available.\n{Color.RESET}")
            return True, False
    return False, False

# =========================
# 1) 選択肢問題（シャッフル対応）
# =========================
def ask_select(q: dict, q_num: int):
    question = q.get("question")
    hint = q.get("hint")
    choices = q.get("choices", [])
    answer = q.get("answer")
    comment = q.get("comment", {})

    hint_shown = False

    print(f"\n{Color.BLUE}Question No.{q_num} [選択肢問題]{Color.RESET}")
    print(question + "\n")

    # 選択肢をシャッフルして表示（元のリストは崩さない）
    shuffled_choices = random.sample(choices, len(choices))

    for i, c in enumerate(shuffled_choices, 1):
        print(f"{i}: {c}", end="   ")
    print("\n\n(show hint: h)\n")

    while True:
        raw = input("Enter number: ").strip()

        is_hint, shown = check_hint_request(raw, hint)
        if is_hint:
            if shown: hint_shown = True
            continue

        if raw.isdigit():
            sel = int(raw) - 1
            if 0 <= sel < len(shuffled_choices):
                user_choice = shuffled_choices[sel]
                break

        print(f"{Color.RED}→ Invalid input.{Color.RESET}")

    correct = (user_choice == answer)

    print()
    print(f"{Color.GREEN}→ Correct!{Color.RESET}" if correct else f"{Color.RED}→ Incorrect.{Color.RESET}")
    print(f"You    : {user_choice}")
    print(f"Answer : {answer}")

    if comment or (hint and not hint_shown):
        print("\n[Comment]")
        for i, c in enumerate(shuffled_choices, 1):
            meaning = comment.get(c)
            if meaning:
                print(f"{i}) {c}: {meaning}")

        if hint and not hint_shown:
            print(f"\nHint: {hint}")

    input(f"\n{Color.YELLOW}Press Enter to continue...{Color.RESET}")
    return correct

# =========================
# 2) 並べ替え問題
# =========================
def ask_arrange(q: dict, q_num: int):
    question = q.get("question")  # 例: "私は毎朝彼に会います。 ( meet / I / him ) every morning."
    hint = q.get("hint")
    # JSON側で "words": ["meet", "I", "him"] のようにリストで持たせる想定
    words = q.get("words", []) 
    answer_seq = q.get("answer_seq") # 正解の並び順 例: "2 1 3" または "213"
    comment = q.get("comment", "")

    hint_shown = False

    print(f"\n{Color.BLUE}Question No.{q_num} [並べ替え問題]{Color.RESET}")
    print(question + "\n")

    # 選択肢単語をシャッフルして提示
    shuffled_words = random.sample(words, len(words))
    
    print("【使用する語句】")
    for i, w in enumerate(shuffled_words, 1):
        print(f"[{i}] {w}", end="  ")
    print("\n\n(番号を正しい順にスペース区切り、または連続して入力してください。例: 2 1 3)")
    print("(show hint: h)\n")

    while True:
        raw = input("Enter sequence: ").strip()

        is_hint, shown = check_hint_request(raw, hint)
        if is_hint:
            if shown: hint_shown = True
            continue

        # 入力から数字だけを抽出
        digits = [c for c in raw if c.isdigit()]
        
        # 入力された数字の数が単語数と一致し、有効な範囲かチェック
        if len(digits) == len(shuffled_words):
            try:
                user_seq = [shuffled_words[int(d) - 1] for d in digits if 1 <= int(d) <= len(shuffled_words)]
                if len(user_seq) == len(shuffled_words):
                    user_answer_str = " ".join(user_seq)
                    break
            except IndexError:
                pass

        print(f"{Color.RED}→ Invalid input. 正しい番号の数を入力してください。{Color.RESET}")

    # JSON側のanswer（文字列）を取得
    correct_answer = q.get("answer") # 例: "I meet him"

    correct = (user_answer_str.lower().replace(" ", "") == correct_answer.lower().replace(" ", ""))

    print()
    print(f"{Color.GREEN}→ Correct!{Color.RESET}" if correct else f"{Color.RED}→ Incorrect.{Color.RESET}")
    print(f"You    : {user_answer_str}")
    print(f"Answer : {correct_answer}")

    if comment or (hint and not hint_shown):
        print("\n[Comment]")
        if comment: print(comment)
        if hint and not hint_shown: print(f"Hint: {hint}")

    input(f"\n{Color.YELLOW}Press Enter to continue...{Color.RESET}")
    return correct

# =========================
# 3) 英作文問題
# =========================
def ask_writing(q: dict, q_num: int):
    question = q.get("question") # 日本語文など
    hint = q.get("hint")
    answer = q.get("answer")     # 模範解答英文
    comment = q.get("comment", "")

    hint_shown = False

    print(f"\n{Color.BLUE}Question No.{q_num} [英作文問題]{Color.RESET}")
    print(question + "\n")
    print("(英文を入力してください。大文字小文字・末尾のピリオド等は自動で補正されます)")
    print("(show hint: h)\n")

    while True:
        raw = input("Your Answer: ").strip()

        is_hint, shown = check_hint_request(raw, hint)
        if is_hint:
            if shown: hint_shown = True
            continue
        
        if raw != "":
            user_answer = raw
            break
        print(f"{Color.RED}→ 何か入力してください。{Color.RESET}")

    # 判定用にトリミング（文末のピリオドや空白を無視して比較しやすくする）
    def clean_text(text):
        return text.lower().strip().rstrip('.?!,')

    correct = (clean_text(user_answer) == clean_text(answer))

    print()
    print(f"{Color.GREEN}→ Correct!{Color.RESET}" if correct else f"{Color.RED}→ Incorrect.{Color.RESET}")
    print(f"You    : {user_answer}")
    print(f"Answer : {answer}")

    if comment or (hint and not hint_shown):
        print("\n[Comment]")
        if comment: print(comment)
        if hint and not hint_shown: print(f"Hint: {hint}")

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
        types = ["選択肢", "並べ替え", "英作文"]
        t_idx = select_menu("Question Type", types)

        # ファイル名のマッピング
        file_names = ["choice.json", "arrange.json", "writing.json"]
        json_path = genre_dir / file_names[t_idx]

        # =========================
        # 問題ロード
        # =========================
        questions = load_questions(json_path)

        if not questions:
            print(f"{Color.RED}問題が登録されていません。{Color.RESET}")
            continue

        print(f"総問題数: {len(questions)}")

        # =========================
        # 問題数（直接入力）
        # =========================
        while True:
            raw = input("How many questions? : ").strip()

            if raw.isdigit() and 0 < int(raw) <= len(questions):
                num = int(raw)
                break

            print(f"1～{len(questions)} の数字を入力してください。")

        print(f"\n{Color.GREEN}{genre_name} / {types[t_idx]} / {num}問{Color.RESET}")
        input(f"{Color.YELLOW}Press Enter to start...{Color.RESET}")

        # =========================
        # 出題開始（ランダム抽出）
        # =========================
        start = time.time()
        correct_count = 0

        # 指定された件数分、問題をランダムに抽出
        selected_questions = random.sample(questions, num)

        for i, q in enumerate(selected_questions, 1):
            if t_idx == 0:
                is_correct = ask_select(q, i)
            elif t_idx == 1:
                is_correct = ask_arrange(q, i)
            elif t_idx == 2:
                is_correct = ask_writing(q, i)

            if is_correct:
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
            print("\nGood job! See you next time 👋\n")
            break

if __name__ == "__main__":
    main()
