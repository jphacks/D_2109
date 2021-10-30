# <img style="width:20px" src="./public/favicon.png"> trim</dvi>

[![IMAGE ALT TEXT HERE](https://github.com/jphacks/D_2109/wiki/images/lp.png)](https://www.youtube.com/watch?v=LUPQFB4QyVo)

## デモ

[![IMAGE ALT TEXT HERE](https://github.com/jphacks/D_2109/wiki/images/trim_demo_play.png)](https://youtu.be/LZ33qJSdBPs)


## 製品概要
<span style="font-weight:bold">ディベロッパー × Tech</span>

<img src="https://github.com/jphacks/D_2109/wiki/images/start_moc.png" />

### 背景(製品開発のきっかけ、課題等）
エンジニアがプログラムを書く際には **「キャメルケース」** **「スネークケース」** **「ケバブケース」** などの **「命名規則」** や **「1行のに記述する文字数の制限」** などの守らなければいけない **暗黙的なルール** が数多く存在する。

これらのルールをプログラミング初心者が意識しながらプログラムを書くことは難しいという課題がある。
また、オンライン化が進む中、チーム開発をしている場合でも随時ルールを考慮して開発を進める必要がある。

私たちはこれらの課題を解決するサービスを作成しました。

### 製品説明（具体的な製品の説明）
本製品は **ルールベースソースコードフォーマッター** のデスクトップ/ウェブ アプリです。

- 使用率が高いプログラミング言語である **Python** をフォーマットするアプリケーション
- プログラミング初心者でも綺麗なコードを作成することが可能
- チーム開発においても作成したルールをもとに統一されたコードフォーマットを提供

### 特長

#### 1. **フォーマットルール**の作成は初心者向けなわかりやすいGUIを提供
熟練のエンジニアがよく使用する命名規則やインデント数などをカスタマイズ可能で **CapWords** や **Snake** 表現を選択できます。
また、初心者向けにはデフォルトの値を設定しているため、迷うことがなくなります。
<img src="https://github.com/jphacks/D_2109/wiki/images/rule_make_menu.gif" />

#### 2. 修正対象のコードは直接入力とファイルアップロードの双方が可能
事前に作成した **Python** のファイルを修正することが可能です。
また、アプリケーション内で直接 **Python** のコードを書くことも可能です。
<img src="https://github.com/jphacks/D_2109/wiki/images/input_python_select.png" />

#### 3. 修正後のコードをハイライト表示してプレビューすることができる
コードを修正するツールは競合サービスで数多く存在しますが、どこを修正したのかを表示してくれるようなサービスはありません。
そこで『 <img style="width:10px" src="./public/favicon.png"> trim 』は修正したプログラムの概要を上部に表示して、該当箇所にはコメントアウトで修正したことを表示する機能を持ちます。
<img src="https://github.com/jphacks/D_2109/wiki/images/code_gen_complete2.png" />

#### 4. 修正後のコードをダウンロードすることができる。
上記で示した通り『 <img style="width:10px" src="./public/favicon.png"> trim 』は修正済みのプログラムと修正前のプログラムを一眼で比較できるUIを持っています。また、さらに修正後のプログラムをダウンロードすることもできるため、エンジニア本人がローカルで開発することも可能になるのです。
<img src="https://github.com/jphacks/D_2109/wiki/images/code_gen_complete2.png" />

### 解決出来ること
『 <img style="width:10px" src="./public/favicon.png"> trim 』は全てのエンジニアが持つコーディングの個性やクセをストレスなく修正することができます。
さらにチーム開発におけるコーディング規約を『暗黙的』なものから『明示的な』なものへと変化させ、チームメンバーにストレスを与えることなく、コードの個性を整えることができます。

### 今後の展望
今後は 『VSCode』 の拡張機能としてのリリースを考えています。『 <img style="width:10px" src="./public/favicon.png"> trim 』では命名規則などの『暗黙的なルール』をJSON形式のファイルとして保存をしています。これは VSCode などの他サービスに転用しやすくすることを目的として開発しています。

また、現段階では修正することができる言語は Python のみですが、C++ やJavaScript といった言語・Vue.jsなどのフレームワークにも対応させることを考えています。

### 注力したこと（こだわり等）
- わかりやすいUIの追求
    - 『 <img style="width:10px" src="./public/favicon.png"> trim 』は初心者からベテランまでの全てのエンジニアをターゲットとした感覚的にわかるUIを実装しました。
- コードのシンタックスハイライト
    - 『 <img style="width:10px" src="./public/favicon.png"> trim 』は修正前と修正後のコードをアプリケーション内でプレビュー表示ができ、そのコードにシンタックスハイライトを適用させて表示をしています。
- プログラムを修正する独自アルゴリズムの開発
    - 『 <img style="width:10px" src="./public/favicon.png"> trim 』は作成したルールに沿って独自のアルゴリズムによってプログラムを修正します。正規表現などを用いることによってルールに反する異常の検知を行い、関数などのブロック単位でのプログラムの修正を実現しました。

## 開発技術

### フレームワーク・ライブラリ・モジュール
- フロントエンド
    - フレームワーク
        - Vue.js
        - Electron
    ライブラリ・モジュール
        - markdown-it-vue

- バックエンド
    - Python
 

### 独自技術
#### ハッカソンで開発した独自機能・技術
- 入力と同時にシンタックスハイライトを行うテキスト入力ボックス
    - commit_id : [07c2f51a48ced98d10e032d0a3968f464e8b3a8e](https://github.com/jphacks/D_2109/commit/07c2f51a48ced98d10e032d0a3968f464e8b3a8e)

- コードの修正を行う独自アルゴリズム
    - commit_id : [36dcf8782d50e9093beefece59063713c60d753d](https://github.com/jphacks/D_2109/commit/36dcf8782d50e9093beefece59063713c60d753d)

    
* 独自で開発したものの内容をこちらに記載してください
* 特に力を入れた部分をファイルリンク、またはcommit_idを記載してください。


# 使用方法
使用方法については[Wiki](https://github.com/jphacks/D_2109/wiki)をご覧ください。