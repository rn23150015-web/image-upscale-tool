# AIを用いた画質向上＆ノイズ除去Webアプリケーション

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-3.x-000000?style=flat&logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![OpenCV](https://img.shields.io/badge/OpenCV-Contrib_Headless-5C3EE8?style=flat&logo=opencv&logoColor=white)](https://opencv.org/)
[![Render](https://img.shields.io/badge/Render-Deployed-46E3B7?style=flat&logo=render&logoColor=white)](https://render.com/)

URL: [https://image-upscale-tool.onrender.com](https://image-upscale-tool.onrender.com)

---

## 1. アプリの概要と背景

### 概要
本アプリは、ECサイトやWebメディアにおける「低解像度な商品画像の画質向上」や「JPEG圧縮によるノイズの低減」をブラウザ上から即座に行える画質向上＆ノイズ除去Webツールです。

### 開発背景と目的
* **背景**: ECサイト運営において、商品画像のクオリティは購入率に直結します。しかし、過去の撮影データや小さなサムネイル画像しか残っていない場合、手動で拡大・レタッチを行うには時間がかかるという課題がありました。
* **目的**: 
  1. **実用的な課題解決**: AIモデルを活用し、誰でも1クリックで2倍〜4倍の高画質化とノイズ除去を行える環境を提供すること。
  2. **開発スキルの実践統合**: Java/Spring Bootで習得したWeb開発の基礎（MVC構造・例外処理）を基盤に、Pythonの画像処理・AIモデル連携、JavaScriptによるUI/UX改善、クラウドデプロイまでを一貫して自力でやり遂げること。

---

## 2. 使用技術・スキル一覧

| カテゴリ | 技術・ツール | 選定理由・活用内容 |
| :--- | :--- | :--- |
| **バックエンド** | Python 3.x / Flask | 軽量かつAI・画像処理ライブラリとの親和性が高いため選定。MVCのControllerとして機能。 |
| **WSGIサーバー** | Gunicorn | 本番環境（Linux）で複数リクエストに耐えうる安定した稼働を実現するために採用。 |
| **AI / 画像処理** | OpenCV | ESPCNモデルを用いた超解像およびノイズ除去に使用。 |
| **フロントエンド** | HTML5 / CSS3 / JavaScript | 見やすく直感的なUI/UXを追求。FileReader APIによるドラッグ＆ドロップ、プレビューを自作。 |
| **開発ツール** | Git / GitHub / VS Code |

---

## 3. 学習過程と成長のストーリー

### 本プロジェクト開始前のスキルレベル
* Java言語の基本構文、Servlet/JSP、MVCモデル、JDBCを用いたDB連携処理を学習。
* Webアプリケーションのリクエスト・レスポンスの流れや、サーバーサイドにおける例外処理の重要性を理解している状態。
* PythonおよびAI・画像処理ライブラリ、クラウドデプロイの実務経験は未習得。

### 新たに挑戦した技術
* **Python/FlaskによるWeb開発**: Javaで学んだMVCパターンを応用。
* **OpenCVを用いたAI超解像と前処理**: 単なる拡大ではなく、DNN（Deep Neural Network）を用いた画像の超解像および色情報を保持したノイズ除去。
* **フロントエンドUXの自作**: 画面遷移なしで送信前画像を確認できるプレビュー、ドラッグ＆ドロップ機能の実装。
* **クラウド環境へのデプロイ**: Renderにおけるビルドプロセスの理解。

### 開発中に直面した課題・工夫・成果

#### 課題1：壊れたファイルや不適切な形式によるサーバークラッシュ
* **問題**: ユーザーが画像以外のファイル（PDFやテキスト等）や破損した画像を送信した場合、OpenCVの読み込み処理でサーバーが停止（クラッシュ）する危険性がありました。
* **工夫**: 
  * 拡張子チェック、ファイル存在確認、OpenCVでの読み込み可否確認

#### 課題2：超解像処理による「ノイズの誤拡大」とUIの利便性
* **問題**: JPEG画像特有の圧縮ノイズがある状態で拡大を行うと、AIがノイズまで強調して拡大してしまう課題が発生しました。
* **工夫**: 
  * 超解像をかける前に「ノイズ除去前処理」を挟み解決
  * 処理の強さを「なし・低・中・高・最高」の5段階で調整可能にし、ユーザーがクリック1回で直感的に切り替えられるようラジオボタンUIで制作

#### 課題3：デプロイ時の `module 'cv2' has no attribute 'dnn_superres'` エラー
* **問題**: ローカル（Windows）では正常動作していたコードが、Renderにデプロイした途端、OpenCVのモジュールが見つからずエラーとなりました。
* **工夫**: 
  * 標準の `opencv-python-headless` には拡張モジュール（contrib）が含まれていないことが原因と突き止めました。
  * `opencv-contrib-python-headless` に変更後、Renderの過去ビルドキャッシュが残っていたため、**「Clear build cache & deploy」** を実行して解決しました。

---

## 4. 学習方法と学びの姿勢

* **「利用者目線（UX）」を考えた設計**
  * 単に「AIで処理できる」だけでなく、処理速度を可視化する処理時間バッジや、ダウンロードボタンを実装しました。

---

##  5. 今後の改善予定

### 現在取り組んでいる課題・改善予定
1. **処理の非同期化（バックグラウンド処理）**:
   現在は同期処理で超解像を行っているため、巨大な画像が送信された場合レスポンスが遅延します。今後は Celery などのタスクキューを導入し、非同期で処理完了を通知する構成へ改修予定です。
2. **クラウドストレージ連携**:
   生成された画像をローカルディスクではなくクラウドストレージへ直接保存する仕組みの導入。


---
