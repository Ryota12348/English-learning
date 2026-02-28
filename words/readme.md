# 英単語

## ファイル構造

```
/
├─ README.md
├─ python.py
├─ a-shell.py
└─ data
	├─ sokutan
	│└─ 63.json
	└─ target1900
		└─ unit1.json
```

## JSON

```
[
    {
        title:
        english:
        japanese:
        first-letter
    }
]
```

## JSONプロンプト

```
以下はOCRで抽出された英単語帳のデータです。
このテキストを、指定のJSON形式に変換してください。

【ルール】
- 出力はJSONのみ（説明文は不要）
- 配列形式にする
- 各要素は以下のキーを持つこと
  - "title"：単語帳の通し番号（数値）
  - "english"：英単語（小文字に統一）
  - "japanese"：日本語の意味
  - "first_letter"：英単語の先頭1文字
  - "part_of_speech"：英単語の品詞を英語で
- OCRの改行崩れは適切に補正する
- 番号が行頭にある場合はそれをtitleとする
- 日本語が複数ある場合は1つの文字列にまとめる
- 不要な記号（. や - など）は削除する
- JSONとして正しい形式にする

【出力例】
[
  {
    "title": 153,
    "english": "abandon",
    "japanese": "捨てる",
    "first_letter": "a",
    "part_of_speech": "verb"
  }
]

```