# convert-and-transcribe-mp4
MP4録画を変換して文字起こしする

## 概要
このプロジェクトは、MP4形式の録画ファイルから音声を抽出し、OpenAIのWhisperモデルを使用して文字起こしを行い、その結果をGoogleドキュメントに保存するためのGoogle Colabスクリプトを提供します。

## 使用方法
1. Google ColabでインスタンスのタイプをGPUに変更します。
2. 左側のメニューからGoogleドライブをマウントします。
3. フォームで会議の言語を選択します。
4. 処理するMP4ファイルのパスをコピーします。
5. 実行ボタンを押します。

## 必要なライブラリ
以下のライブラリをインストールする必要があります：
- openai-whisper
- ffmpeg-python
- torch

## ライセンス
このプロジェクトはMITライセンスの下で公開されています。詳細はLICENSEファイルを参照してください。
