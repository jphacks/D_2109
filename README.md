# <img style="width:20px" src="./public/favicon.png"> trim</dvi>

## 紹介動画 (下記画像をクリック！)
[![IMAGE ALT TEXT HERE](https://github.com/jphacks/D_2109/wiki/images/lp.png)](https://www.youtube.com/watch?v=b0qmjrAcZtw)

## デモ

[![IMAGE ALT TEXT HERE](https://github.com/jphacks/D_2109/wiki/images/trim_demo_play.png)](https://youtu.be/LZ33qJSdBPs)

## 目次
- [製品概要](#製品概要)
  - [背景](#背景)
  - [製品説明](#製品説明)
  - [Trim on Browser](#Trim-on-Browser)
  - [Trim Auto Notification](#Trim-Auto-Notification)
  - [Trim API](#Trim-API)



## 製品概要
<span style="font-weight:bold">ディベロッパー × Tech</span>

<img src="https://github.com/jphacks/D_2109/wiki/images/start_moc.png" />

### 背景
エンジニアがプログラムを書く際には **「キャメルケース」** **「スネークケース」** **「ケバブケース」** などの **「命名規則」** や **「1行のに記述する文字数の制限」** などの守らなければいけない **暗黙的なルール** が数多く存在する。

これらのルールをプログラミング初心者が意識しながらプログラムを書くことは難しいという課題がある。
また、オンライン化が進む中、チーム開発をしている場合でも随時ルールを考慮して開発を進める必要がある。

私たちはこれらの課題を解決するサービスを作成しました。



### 製品説明
- Trim on Browser
  - GUIベースの**ルールベースソースコードフォーマッター**です。初学者でも簡単にルールの設定ができるほか、ファイルをアップロードするだけで簡単に自動で整形が行わます。

- Trim Auto Notification
  - Trim on Browserの「**書き方を揃える**」という遺伝子はそのままに、より**チーム開発に特化**させました。プロジェクトファイル全体に渡って整形し、整形結果やルール情報をpdfで可視化・共有します。**常にきれいなコードに保ちたい！**、**きれいなコードの書き方を効率的に学びたい**といったチームの要望に応えます。
 
- Trim API
  - 整形処理やルールの可視化といった処理を**APIベース**で提供します。整形結果やTrim Auto Notificationで必要な連携情報(GitHubレポジトリ、Slackチャンネル)をTrimサービス側に置かないため、**セキュリティ的にも安心**です。APIを用いてチーム開発サービス等を独自に構築して頂くことも可能です。

Trimは、使用率が最も高く汎用性のある**Python**言語をフォーマットします。


### Trim-on-Browser
#### 1. **フォーマットルール**の作成は初心者向けなわかりやすいGUIを提供
様々なルールが視覚的に分かりやすくなっており、簡単にカスタマイズする事ができます。
例えば、**CapWords** や **Snake** といった命名規則やimportのソーティング・グルーピングなどがあります。
Pythonのスタンダードな規約であるPEP8に準拠したデフォルトの値を設定しているため、初学者が学習用途として使う事も可能です。
<img src="https://github.com/jphacks/D_2109/wiki/images/rule_make_menu.gif" />

#### 2. 修正対象のコードは直接入力とファイルアップロードの双方が可能
事前に作成した **Python** のファイルを修正することが可能です。
また、アプリケーション内で直接 **Python** のコードを書くことも可能です。
<img src="https://github.com/jphacks/D_2109/wiki/images/input_python_select.png" />

#### 3. 修正後のコードをハイライト表示してプレビューすることができる
コードを修正するツールは競合サービスで数多く存在しますが、どこを修正したのかを表示してくれるようなサービスはありません。
そこで『 <img style="width:10px" src="./public/favicon.png"> trim 』は修正したプログラムの概要を上部に表示して、該当箇所にはコメントアウトで修正したことを表示する機能を持ちます。
<img src="https://github.com/jphacks/D_2109/wiki/images/code_gen_complete.png" />

#### 4. 修正後のコードをダウンロードすることができる。
上記で示した通り『 <img style="width:10px" src="./public/favicon.png"> trim 』は修正済みのプログラムと修正前のプログラムを一眼で比較できるUIを持っています。また、さらに修正後のプログラムをダウンロードすることもできるため、エンジニア本人がローカルで開発することも可能になります。
<img src="https://github.com/jphacks/D_2109/wiki/images/code_dl.png" />


#### 5. デスクトップ/ウェブの両方に対応




### Trim-Auto-Notification
#### 1. プロジェクト全体に渡って整形処理が可能
「GitHub WebPushの設定」・「rule.jsonをプロジェクトルートに置く」・「Git Remote Push」この3操作により、プロジェクト全体に渡っての整形を提供します。
- rule.jsonはTrim on Browserのルール作成からGUIベースで簡単に作成できます。
- GitHubのリポジトリがプライベートの場合、Trim Botアカウントを入れて頂く事でTrimサービスからのリポジトリアクセスを可能にします。(承認制)
- .trimignoreファイルより、ignoreするpythonファイルを設定できます。


#### 2.




### Trim-API





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
 
 
 ### 技術構成
 <img src="https://github.com/jphacks/D_2109/wiki/images/trim_drawio.png" />

### 独自技術
#### ハッカソンで開発した独自機能・技術
- 入力と同時にシンタックスハイライトを行うテキスト入力ボックス
    - commit_id : [07c2f51a48ced98d10e032d0a3968f464e8b3a8e](https://github.com/jphacks/D_2109/commit/07c2f51a48ced98d10e032d0a3968f464e8b3a8e)

- [PEP8準拠] import部(1行に複数個のインポートをしてる場合に分割)
    - split_import.py

    ```python
    # Wrong
    import os, sys

    # Correct
    import os
    import sys
    ```

- [PEP8準拠] import部(3グループに分割)
    - group_sort_import.py/group_import :  [5f6f5a784a83f0acecb405397202b36cf519b40a](https://github.com/jphacks/D_2109/commit/5f6f5a784a83f0acecb405397202b36cf519b40a)
    1.  Python の標準ライブラリ
    2.  サードパーティのライブラリ (今回は、PyPIに登録されているライブラリをhttpリクエストにより検出)
    3.  自作ライブラリなどのローカルライブラリ
    
    ```python
    # Wrong
    import numpy
    import local_module
    import os
    from datetime import timedelta

    # Correct
    # 1. Python標準ライブラリ
    from datetime import timedelta
    import os

    # 2. サードパーティ ライブラリ
    import numpy

    # 3. 自作ライブラリ
    import local_module
    ```
    
- [オリジナル] import部(アルファベット順ソート) 
     - group_sort_import.py/sort_import :  [fe80c75e10c9e6805fd122e07607f7d2d6fd1980](https://github.com/jphacks/D_2109/commit/fe80c75e10c9e6805fd122e07607f7d2d6fd1980)

- [PEP8準拠] 1行がX文字を超える場合は、改行警告 
    - line_checkcount.py : [9a45cf15e4f0285671d867ec89803815c6292f73](https://github.com/jphacks/D_2109/commit/9a45cf15e4f0285671d867ec89803815c6292f73)

    ```python
        # [trim] Warning: 1行あたりの行数は最大{op_count_word["length"]}文字です.適切な位置で折り返してください.
        Customer.obejects.************************
    ```

- [PEP8準拠] 演算子の前後に空白文字を1文字を追加
    - check_operators_space.py :  [9862616d33690dd0a98bc6e3ee42324cd7fa4973](https://github.com/jphacks/D_2109/commit/9862616d33690dd0a98bc6e3ee42324cd7fa4973)
    
    ＜注意した例外のパターン＞
    - def, class の引数には適用しない
    - スライス内には適用しない
    - 文中の and, or, not には適用しない
    
    ```python
    # Wrong
    x=1+2 

    # Correct
    x = 1 + 2
    ```

- [PEP8準拠] インデントの調整
    - scan_indent_config.py : [45ce98f11c8fc030de1fb04ea6ce49926e974061](https://github.com/jphacks/D_2109/commit/45ce98f11c8fc030de1fb04ea6ce49926e974061)
    
    ＜考慮した事＞
    - 末尾文字の削除
    - インデントの調整(ユーザの設定値やタブ文字を半角スペース変換)
    - 行前後のインデント値とスタックを用いて、コードブロックのネストを表現
    
    ```python
     # Wrong(タブ2字になっている)
     def AddBox():
            a = 2
            b = 3
     
     # Correct(タブ文字:4字扱い, インデント:半角4字)
     def AddBox():
         a = 2
         b = 3
    ```
    
- [PEP8準拠] 関数/クラスの整形、命名規則条件に沿っているか確認
    - scan_format_method_class.py : [26d16c81cba66085551d9f23720bd62a4fca3901](https://github.com/jphacks/D_2109/commit/26d16c81cba66085551d9f23720bd62a4fca3901) 
    - scan_operators_space.py : [6f0da59dde2bbb70ff3845658fb464d3ea5316ce](https://github.com/jphacks/D_2109/commit/6f0da59dde2bbb70ff3845658fb464d3ea5316ce)
    
    <考慮した事>
    - 先頭の空白文字の記憶によりインデントが崩れないようにする
    - 関数・クラスが取り得るワードパターンを正規表現で検知(関数だと戻り値があるパターンなどがあり、それも考慮している)
    - 上記正規表現から関数名・クラス名の取得
    - 関数・クラス部の空白を調整
    - 関数の仮引数部の整形
    
    ```python
    # Wrong
    def     Add_box     (box, a  = 2,   b) ->None   :
        pass
    
    # Correct(CapWordsのみ許容)
    # [trim] Warning: クラス名にアンダーバーは含められません.
    def Add_box (box, a=2, b) -> None:
        pass
    ```

- [PEP8準拠] 変数が命名規則条件に沿っているか確認
    - scan_naming_value.py : [56f357ab40a4f3812523ee5bddf08e64f60dc612](https://github.com/jphacks/D_2109/commit/56f357ab40a4f3812523ee5bddf08e64f60dc612)
    
    <考慮した事>
    - 関数・クラス・文字列を正規表現により無視する
    - 演算子や特殊文字でsplitする
    - 残ったワードから予約語を取り除くことで変数のみを抽出

    ```python
    # Wrong
    word_Count = 2
    
    # Correct(snakeのみ許容)
    # [trim] Warning: 変数名に大文字は含められません.
    word_Count = 2
    ```
    
- [PEP8準拠] クラス・関数ブロックの上下の空白行の行数を確認・修正
    - blank_lines.py : [2804f616e082b1e876af251292f6a404e5af394d](https://github.com/jphacks/D_2109/commit/2804f616e082b1e876af251292f6a404e5af394d)
    
    <考慮した事>
    - 正規表現を用いた独自のアルゴリズムで関数・クラスブロックを認識(returnがなくても認識可能)
    - PEP8に基づき、グローバル関数・クラスについてはブロックの上下2行、ローカル関数についてはブロックの上下1行に空白が入るよう調整
    - 関数・クラスの開始行の一つ上のコメント行は無視するよう実装

    ```python
    # Wrong
    def sample_func():
        return
    Class SampleClass:
        a = 1
        
        
        
        def sample_method():
            print(a)    
    
    # Correct
    def sample_func():
        return
        
        
    Class SampleClass:
        a = 1
     
        def sample_method():
            print(a)    
    ```

- [オリジナル] pythonコードをコンパイル
    - compile_test.py : [8076e361631e805b7337455852f2f29de736cca9](https://github.com/jphacks/D_2109/commit/8076e361631e805b7337455852f2f29de736cca9)
    
    ```python
    Traceback (most recent call last):
      File "/var/task/lambda_function.py", line 279, in is_comile_to_dic
        compile(line, '', 'exec')
      File "<string>", line 9
        a=3
    IndentationError: unexpected indent
    ```

# 使用方法
使用方法については[Wiki](https://github.com/jphacks/D_2109/wiki)をご覧ください。
