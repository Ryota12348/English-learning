# 新英語学習システム　**「English Training」**

英検・入試対策向けの CLI（コマンドライン）英語学習ツール です。
ジャンル・問題形式・問題数を選択し、対話形式で学習できます。

「短時間で」「何度も」「自分のペースで」学べることを重視しています。

## 特徴

- CLIベースで軽量・高速に動作
- 学習ジャンルを選択可能
   - 英検 準1級
   - 英検 2級
   - 英検 準2級
   - 入試問題
   - ワーク復習 など
- 問題形式を選択可能
   - 選択肢問題（対応済み）
   - 並べ替え問題（今後対応予定）
   - 英作文問題（今後対応予定）
- 問題数を自由に入力可能
- ヒント表示機能あり
- 正誤判定＋語義・解説表示
- 学習結果を 100点満点で表示
- 学習結果のファイル保存なし（画面表示のみ）

#### 想定利用シーン
- 英検・入試前の短時間演習
- 単語・語彙の確認
- 授業や塾での補助教材
- 自作問題（JSON）を使った復習

#### 動作環境
Python 3.9 以上推奨
CLI（ターミナル / コマンドプロンプト）
※ Windows / macOS / Linux いずれも使用可能
（ANSIカラー対応端末推奨）

#### iOS での使い方
1. App Store から「a-Shell」をインストール。
2. a-Shellにはデフォルトでgitコマンドがサポートされていないので、以下の方法で追加：
```bash
mkdir ~/Documents/bin
cd ~/Documents/bin
curl -L https://github.com/holzschu/a-Shell-commands/releases/download/0.1/git -o ~/Documents/bin/git
```
3. a-Shell のターミナルで以下を実行：
```bash
git clone --filter=blob:none --sparse https://github.com/Ryota12348/English-learning.git
cd English-learning
git sparse-checkout set a-shell
```

成功すると、次のような構成になります：

```pgsql
English-learning/
└─ a-shell/
   ├─ english-quiz-a-shell.py
   └─ data/
```

4. 実行用ディレクトリに移動
```bash
cd a-shell
```
確認：
```bash
ls
```

以下が表示されればOK：
```bash
python.py
data
```
5. Python の動作確認
   
```pash
python3 --version
```

※ python が使えない場合は 必ず python3 を使用してください。

6. プロジェクトの配置を確認（重要）

このプログラムは以下の場所で動作するように設計されています：
```pgsql
~/Documents/english_quiz/
├─ python.py
└─ data/
```

もし clone したフォルダ名が違う場合は、以下のように移動してください：
```bash
mv a-shell ~/Documents/english_quiz
cd ~/Documents/english_quiz
```
7. 実行する
```bash
python3 english-quiz-a-shell.py
```
ジャンル選択メニューが表示されれば成功です 🎉


## ファイル構造

```pgsql
python.py←実行
data/
├─ eiken/
│  ├─ pre1/
│  │  ├─ choice.json
│  │  ├─ reorder.json
│  │  └─ writing.json
│  └─ grade2/
│     ├─ choice.json
│     └─ reorder.json
├─ exam/
│  ├─ choice.json
│  └─ writing.json
└─ workbook/
   └─ review.json

```

## 注意事項
問題データは、試験の種類、レベル、問題形式に基づいた階層的なディレクトリ構造で管理されます。 新しい問題を追加するには、適切なディレクトリにJSONファイルを置くだけで済みます。コードを変更する必要はありません。