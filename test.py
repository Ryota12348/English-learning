
import argparse
import json
import random
import signal
import sys
import time
from pathlib import Path

class Color:
	BLACK          = '\033[30m'#(文字)黒
	RED            = '\033[31m'#(文字)赤
	GREEN          = '\033[32m'#(文字)緑
	YELLOW         = '\033[33m'#(文字)黄
	BLUE           = '\033[34m'#(文字)青
	RESET          = '\033[0m'#全てリセット

def copy_to_clipboard(text):
    import tkinter as tk
    r = tk.Tk()
    r.withdraw()          # ウィンドウを表示しない
    r.clipboard_clear()
    r.clipboard_append(text)
    r.update()            # これがないとコピーされないことがある
    r.destroy()

while True:
    print(f'{Color.GREEN}hdhdhdhdhdhdhdhdhd{Color.RESET}')
    print(f'{Color.GREEN}●ABC{Color.RESET}')

    raw = input("入力（qで終了）: ").strip()
    if raw.lower() == "q":
        print(f"{Color.YELLOW}終了します{Color.RESET}")
        break

    print(f'{Color.GREEN}入力されたのは: {Color.RED}{raw}{Color.RESET}')

    yn = input("クリップボードにコピーしますか？（y/n）: ").strip().lower()
    if yn == "y":
        copy_to_clipboard(raw)
        print(f"{Color.GREEN}コピーしました{Color.RESET}")
    else:
        print("コピーしませんでした")

    input(f"\n{Color.YELLOW}Enter を押して次へ…{Color.RESET}")
