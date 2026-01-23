import argparse
import json
import random
import signal
import sys
import time
from pathlib import Path

class Color:
	BLACK     = '\033[30m'#(文字)黒
	RED       = '\033[31m'#(文字)赤
	GREEN     = '\033[32m'#(文字)緑
	YELLOW    = '\033[33m'#(文字)黄
	BLUE      = '\033[34m'#(文字)青
	RESET     = '\033[0m'#全てリセット

# パス設定
BASE_DIR = Path.home() / "Documents"
DATA_DIR = BASE_DIR / "eiken"

# ユーティリティ
def load_questions(path: Path):
    if not path.exists():
        raise FileNotFoundError(f"JSONファイルが見つかりません: {path}")
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
        print(f"{Color.RED}※ 問題形式が不正なためスキップします{Color.RESET}")
        return False

    print(f"\n【第{q_num}問】")
    print(question)
    print("")
    for i, c in enumerate(choices, 1):
        print(f"{i}: {c}", end="   ")
    print("\n")
    print(f"{Color.YELLOW}（ヒントを見る: h）{Color.RESET}")
    print("\n")
    # 入力ループ
    while True:
        raw = input("番号を入力: ").strip()

        if raw.lower() == "h":
            if hint:
                print(f"{Color.BLUE}\nヒント: {hint}\n{Color.RESET}")
                hint_shown = True
            else:
                print(f"{Color.RED}\nヒントはありません。\n{Color.RESET}")
            continue

        try:
            sel = int(raw) - 1
            user_choice = choices[sel]
            break
        except Exception:
            print(f"{Color.RED}→ 無効な入力。数字か h を入力してください。{Color.RESET}")

    correct = (user_choice == answer)

    if correct:
        print("\n")
        print(f"{Color.GREEN}→ 正解！{Color.RESET}")
    else:
        print("\n")
        print(f"{Color.RED}→ 不正解。{Color.RESET}")

    user_index = sel + 1
    correct_index = choices.index(answer) + 1

    print(f"あなた: {user_index} {user_choice}")
    print(f"正答  : {correct_index} {answer}")

    # =========================
    # comment / hint 表示
    # =========================
    if comment or (hint and not hint_shown):
        print("\n[Comment]")

        for i, c in enumerate(choices, 1):
            meaning = comment.get(c)
            if meaning:
                print(f"{i}) {c}: {meaning}")

        if hint and not hint_shown:
            print(f"\nヒント: {hint}")

    input(f"\n{Color.YELLOW}Enter を押して次の問題へ…{Color.RESET}")

    return correct

def signal_handler(sig, frame):
    print("\n中断しました。")
    print(f"進捗: {answered} / {total}")
    sys.exit(0)

# メイン処理
def main():
    global answered, total

    parser = argparse.ArgumentParser(description="CLI英検問題ツール（a-Shell対応）")
    parser.add_argument("-f", "--file", required=True, help="JSONファイル名（拡張子不要）")
    parser.add_argument("-n", "--num", type=int, default=10, help="出題数（デフォルト10問）")
    parser.add_argument("-o", "--order", choices=["random", "sequential"], default="random", help="出題順")
    args = parser.parse_args()

    DATA_DIR.mkdir(exist_ok=True)
    json_path = DATA_DIR / f"{args.file}.json"

    try:
        questions = load_questions(json_path)
    except Exception as e:
        print(f"{Color.RED}読み込みエラー: {e}{Color.RESET}")
        sys.exit(1)

    if not isinstance(questions, list):
        print(f"{Color.RED}JSONの形式が不正です（配列である必要があります）{Color.RESET}")
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
            print(f"進捗: {answered}/{total}  正答: {correct_count}")

    elapsed = time.time() - start
    print("\n=== 結果 ===")
    print(f"正答数: {correct_count}/{total}")
    print(f"所要時間: {int(elapsed//60):02d}分{int(elapsed%60):02d}秒")

if __name__ == "__main__":
    main()