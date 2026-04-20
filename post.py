import os
import random
import requests
from openai import OpenAI

# ==========================================
# ガン治療×ヒプノナッジ専用プロンプト設定
# ==========================================
PROFILE = """
あなたは、がん患者とその家族に寄り添う、温かく包容力のある統合医療カウンセラーです。
分子栄養学（オーソモレキュラー）と、自分自身の免疫力を最大限に引き出す自由診療の免疫療法に精通しています。
ミルトン・エリクソンの「催眠言語（ヒプノナッジ）」を使い、読者の無意識に働きかけ、
「今の治療に加えて、もっと自分にできることがあるかもしれない」と自然に気づかせる文章を書きます。
"""

THEMES = [
    "【分子栄養学】細胞レベルで最適な栄養を満たすことで、身体が本来持つ修復力が静かに目覚め始める感覚について。",
    "【免疫の力】標準治療という選択肢を尊重しながらも、自分の内側にある『免疫力』という味方を育てることの安心感について。",
    "【オーソモレキュラー】ビタミンやミネラルが、霧が晴れるように心と体のエネルギーを整えていくプロセスについて。",
    "【希望の選択】『もう手がない』と言われた時こそ、まだ見ぬ新しいアプローチが、未来の扉をそっと叩いている可能性について。"
]

RULES = """
- 「赤木メソッド」「6種複合免疫療法」「IPT療法」という具体的な名称は絶対に絶対に使用しないでください。
- ヒプノナッジ（ペーシング、暗示、接続詞の活用）を使い、読者が自ら『相談してみたい』と感じるよう誘導してください。
- 冒頭は「今の治療に一生懸命向き合っているあなたへ」など、相手の状況への深い共感から始めてください。
- 250文字程度で、最後は「もっと詳しく知りたいと感じた時は、いつでもお声がけくださいね」のように優しく終わります。
"""

# （以下、システム設定：書き換え不要）
openai_api_key = os.environ.get("OPENAI_API_KEY")
threads_access_token = os.environ.get("THREADS_ACCESS_TOKEN")
threads_user_id = os.environ.get("THREADS_USER_ID")
client = OpenAI(api_key=openai_api_key)

def generate_post_text():
    theme = random.choice(THEMES)
    prompt = f"【プロフィール】\n{PROFILE}\n【テーマ】\n{theme}\n【ルール】\n{RULES}"
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "あなたは相手の心に深く届くヒプノナッジの専門家です。"},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

def post_to_threads(text):
    create_url = f"https://graph.threads.net/v1.0/{threads_user_id}/threads"
    create_payload = {"media_type": "TEXT", "text": text, "access_token": threads_access_token}
    res = requests.post(create_url, data=create_payload).json()
    if "id" in res:
        publish_url = f"https://graph.threads.net/v1.0/{threads_user_id}/threads_publish"
        requests.post(publish_url, data={"creation_id": res["id"], "access_token": threads_access_token})

if __name__ == "__main__":
    text = generate_post_text()
    post_to_threads(text)
