
## 使い方（はじめての人向け）

このツールは「ターミナル」という黒い画面で動きます。
難しそうに見えますが、やることは順番どおりにコマンドを入力するだけです。
以下のコードはそのままコピペして使えます。

### 🔰 まずは準備

**① Python が入っているか確認**

ターミナルで次を入力します。

```bash
python3 --version
```

数字（例：Python 3.10.4 など）が表示されればOKです。

エラーが出る場合は、Python 3.9 以上をインストールしてください。


### 📱 iPhone / iPad（a-Shell）の場合

**① a-Shell をインストール**

  
App Store から a-Shell をインストールします。


**② git を追加（最初だけ必要）**


a-Shell には git が入っていないので、次を順番に入力します。

```bash
mkdir ~/Documents/bin
```

```bash
cd ~/Documents/bin
```

```bash
curl -L https://github.com/holzschu/a-Shell-commands/releases/download/0.1/git -o git
```

```bash
chmod +x git
```

**③ このプロジェクトをダウンロード**

```bash
cd ~/Documents
```

```bash
git clone https://github.com/Ryota12348/English-learning.git
```

```bash
cd English-learning.git
```

```bash
git sparse-checkout set a-shell
```
  

④ フォルダを移動（重要）

このプログラムは次の場所で動くように作られています：
```
~/Documents/English-learning.git
```
もし違う場所にある場合は、移動してください。


⑤ 実行する

  
```
cd ~/Documents/English-learning.git/a-shell
```

```
python3 english-quiz-a-shell.py
```

ジャンル選択メニューが表示されれば成功です。


  



## 💻 パソコン（Windows / Mac）の場合

  
**① ターミナルを開く**

- Windows → コマンドプロンプト
- Mac → ターミナル

**② ダウンロード**

  
```bash
git clone https://github.com/Ryota12348/English-learning.git
```

```bash
cd English-learning.git
```
  

**③ 実行**

```
cd a-shell
```

```
python3 english-quiz-a-shell.py
```
  

### 🎮 実際の使い方

  プログラムを起動すると、次の順番で進みます。


1. ジャンルを選ぶ  
    例：英検2級、入試問題 など
2. 問題形式を選ぶ  
    今は「選択肢」のみ使えます
3. 問題数を入力  
    例：10 と入力すると10問出題
4. 問題スタート

```bash
===================================
Genre
===================================
1) 英検 準1級
2) 英検 2級
3) 英検 準2級
4) 入試問題
5) ワーク復習
Select:
```


### ⌨ 操作方法


- 数字を入力 → 解答
- 0 を入力 → ヒント表示
- Enter → 次へ進む
- Ctrl + C → 強制終了


### 📊 結果表示

最後に表示されます：
  
- 100点満点のスコア
- 正解数
- かかった時間

保存はされません。
気軽に何度も挑戦できます。

