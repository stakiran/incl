# incl
A simple incremental searchable launcher for Windows.

![incl_demo](https://user-images.githubusercontent.com/23325839/38617274-88dfdb18-3dd1-11e8-883b-d5c9e884b317.gif)

<!-- toc -->
- [incl](#incl)
  - [Feature](#feature)
  - [Usage](#usage)
    - [Datafile Format](#datafile-format)
    - [Commandline Options](#commandline-options)
  - [Requirement](#requirement)
  - [Build](#build)
  - [License](#license)
  - [Author](#author)

## Feature
- シンプルなデータファイル
  - plain text で一行一アイテムを書いていくだけ
- シンプルなインターフェース
  - 検索したい語を打って、カーソルキーで選んで Enter を押すだけ
  - アイテムを開くとすぐに終了する
- インクリメンタルサーチ
  - 各アイテムにはキーワードも指定できるので自分好みの語で検索しやすい
- 行えること
  - ファイル, フォルダ, URL を開く
  - 登録した文字列をクリップボードにコピーする

## Usage

```
$ youreditor items.txt
データファイルにアイテムを書く。

$ python incl.py -i items.txt
```

てっとり早く動作を見たい場合は [execute_sample_items.bat](execute_sample_items.bat) を実行してください。 [サンプルのデータファイル](sample_items.txt) を使って起動します。

### Datafile Format
コンセプトは以下のとおり。

- 一行一アイテム
- アイテムの種類は以下の通り
  - プログラムパス
  - コピー文字列
  - システムコマンド

細かい書き方は以下のとおり。

- プログラムパス
  - `(PATH), (KEYWORDS)`
  - 例1: `notepad.exe, メモ帳 memo`
  - 例2: `c:\Program Files, program install binary`
  - 例3: `https://tools.ietf.org/html/rfc7231, rfc http 1.1 protocol`
- コピー文字列
  - `!(KEYWORDS)!(TEXT)`
  - 例1: `!mail ma!this_is_my_address@example.com`
  - 例2: `!tokyo tochosya address!東京都新宿区西新宿二丁目8番1号`
- システムコマンド
  - `@dir` 実行ファイルのあるディレクトリを開く
  - `@edit` データファイルを開く
  - `@quit` 終了する
- コメント
  - `;(COMMENT)`
  - 例1: `; これはコメントです。画面には表示されません。`

[サンプルのデータファイル](sample_items.txt) も参考にしてください。

### Commandline Options
`-i` によるデータファイル指定のみ必須で、残りはオプショナルです。

```
usage: incl.py [-h] [-i INPUT] [-x WINDOWX] [-y WINDOWY]

A simple incremental searchable launcher.

optional arguments:
  -h, --help            show this help message and exit
  -i INPUT, --input INPUT
                        A datafile path. (default: None)
  -x WINDOWX, --windowx WINDOWX
                        Window X size. (default: 640)
  -y WINDOWY, --windowy WINDOWY
                        Window Y size. (default: 320)
```

## Requirement
- Windows 7+
- Python 3.6
- See [requirements.txt](requirements.txt) about libraries.

## Build
[cx_Freeze](https://anthony-tuininga.github.io/cx_Freeze/) でビルドしています。

- [build_preferences.bat.sample](build_preferences.bat.sample) を build_preferences.bat にリネーム後、設定を埋める
- [build.bat](build.bat) を実行する

## License
[MIT License](LICENSE)

## Author
[stakiran](https://github.com/stakiran)
