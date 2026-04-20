name: Threads Auto Post

on:
  schedule:
    - cron: '0 22 * * *'
    - cron: '0 0 * * *'
    - cron: '0 3 * * *'
    - cron: '0 10 * * *'
    - cron: '0 13 * * *'
  workflow_dispatch:

jobs:
  post:
    runs-on: ubuntu-latest
    timeout-minutes: 5
    steps:
      - name: リポジトリをチェックアウト
        uses: actions/checkout@v3
      - name: Pythonをセットアップ
        uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - name: 依存パッケージをインストール
        run: pip install -r requirements.txt
      - name: 自動投稿を実行
        env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
          THREADS_ACCESS_TOKEN: ${{ secrets.THREADS_ACCESS_TOKEN }}
          THREADS_USER_ID: ${{ secrets.THREADS_USER_ID }}
        run: python post.py
