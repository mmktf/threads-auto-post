name: Threads Auto Post
on:
  schedule:
    - cron: '0 1 * * *'   # 日本時間 10:00
    - cron: '0 5 * * *'   # 日本時間 14:00
    - cron: '0 12 * * *'  # 日本時間 21:00
  workflow_dispatch: # 手動実行用
jobs:
  post:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.10'
      - run: pip install -r requirements.txt
      - env:
          OPENAI_API_KEY: ${{ secrets.OPENAI_API_KEY }}
          THREADS_ACCESS_TOKEN: ${{ secrets.THREADS_ACCESS_TOKEN }}
          THREADS_USER_ID: ${{ secrets.THREADS_USER_ID }}
        run: python post.py
