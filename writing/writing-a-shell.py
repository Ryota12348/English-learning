import json
import random
import signal
import sys
import time
from pathlib import Path
import os
import difflib
from datetime import datetime

# =========================
# 色
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
BASE_DIR = os.path.expanduser("~/Documents/English-learning.git")
DATA_PATH = Path(BASE_DIR) / "data" / "writing.json"
LOG_DIR = Path(BASE_DIR) / "log"

# =========================
# JSON読み込み
# =========================
def load_questions():
    if not DATA_PATH.exists():
        raise FileNotFoundError(f"{DATA_PATH} not found")
    with open(DATA_PATH, encoding="utf-8") as f:
        data = json.load(f)
        return data["questions"]  # ←ここが超重要

# =========================
# ログ生成
# =========================
def create_log_file():
    LOG_DIR.mkdir(parents=True, exist_ok=True)
    now = datetime.now().strftime("%Y-%m-%d-%H-%M")
    log_path = LOG_DIR / f"{now}.txt"
    return log_path

def write_log(log_path, text):
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(text + "\n")

# =========================
# 添削
# =========================
def detailed_feedback(user, model):
    feedback = []

    user_words = user.lower().split()
    model_words = model.lower().split()

    # 冠詞
    articles = {"a", "an", "the"}
    missing_articles = [w for w in model_words if w in articles and w not in user_words]
    if missing_articles:
        feedback.append(f"冠詞不足: {', '.join(missing_articles)}")

    # 前置詞
    preps = {"in", "on", "at", "to", "for", "with", "of", "by"}
    user_preps = [w for w in user_words if w in preps]
    model_preps = [w for w in model_words if w in preps]
    if user_preps != model_preps:
        feedback.append("前置詞ミスの可能性")

    # 三単現
    for mw in model_words:
        if mw.endswith("s") and mw[:-1] in user_words:
            feedback.append(f"三単現のs抜け: {mw}")

    # 語順
    if user_words != model_words:
        if sorted(user_words) == sorted(model_words):
            feedback.append("語順ミスの可能性")

    # スペル
    for uw in user_words:
        matches = difflib.get_close_matches(uw, model_words, n=1, cutoff=0.8)
        if matches and uw != matches[0]:
            feedback.append(f"スペルミス: {uw} → {matches[0]}")

    # 不足語
    missing_words = set(model_words) - set(user_words)
    if missing_words:
        feedback.append(f"不足語: {', '.join(missing_words)}")

    if not feedback:
        feedback.append("大きなミスなし")

    return feedback

# =========================
# 出題
# =========================
def ask(q, num, log_path):
    question = q.get("question")
    answers = q.get("answers", [])
    hint = q.get("hint", "")
    title = q.get("title", "")

    print(f"\n{Color.BLUE}Question No.{num}{Color.RESET}")
    if title:
        print(f"{Color.YELLOW}{title}{Color.RESET}")
    print(question)
    print("(ヒント: h)\n")

    while True:
        user = input("Your answer: ").strip()

        if user.lower() == "h":
            print(f"{Color.BLUE}{hint}{Color.RESET}")
            continue

        if user:
            break

    model = answers[0]

    similarity = difflib.SequenceMatcher(None, user.lower(), model.lower()).ratio()
    score = int(similarity * 100)

    print("\n--- Result ---")

    if similarity > 0.9:
        print(f"{Color.GREEN}✔ Perfect{Color.RESET}")
    elif similarity > 0.7:
        print(f"{Color.YELLOW}△ Almost{Color.RESET}")
    else:
        print(f"{Color.RED}✖ Incorrect{Color.RESET}")

    print("\nYour:", user)
    print("Model:")
    for a in answers:
        print("-", a)

    print(f"\nScore: {score}")

    fb = detailed_feedback(user, model)

    print("\nFeedback:")
    for f in fb:
        print("・", f)

    # ログ書き込み
    write_log(log_path, f"Q{num}")
    write_log(log_path, f"Question: {question}")
    write_log(log_path, f"Your: {user}")
    write_log(log_path, f"Model: {model}")
    write_log(log_path, f"Score: {score}")
    write_log(log_path, "Feedback:")
    for f in fb:
        write_log(log_path, f" - {f}")
    write_log(log_path, "-"*30)

    input("\nEnterで次へ...")

    return similarity > 0.7

# =========================
# Ctrl+C
# =========================
def signal_handler(sig, frame):
    print("\n終了")
    sys.exit(0)

# =========================
# メイン
# =========================
def main():
    signal.signal(signal.SIGINT, signal_handler)

    questions = load_questions()

    while True:
        raw = input("問題数: ").strip()
        if raw.isdigit():
            num = int(raw)
            break

    random.shuffle(questions)
    questions = questions[:num]

    log_path = create_log_file()

    correct = 0
    start = time.time()

    for i, q in enumerate(questions, 1):
        if ask(q, i, log_path):
            correct += 1

    elapsed = time.time() - start
    score = round(correct / num * 100)

    print("\n===== RESULT =====")
    print(f"Score: {score}")
    print(f"Correct: {correct}/{num}")
    print(f"Time: {int(elapsed//60)}m {int(elapsed%60)}s")

    write_log(log_path, f"FINAL SCORE: {score}")
    write_log(log_path, f"TIME: {elapsed:.1f}s")

# =========================
# 実行
# =========================
if __name__ == "__main__":
    main()