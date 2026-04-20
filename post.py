import os
import random
import requests
from openai import OpenAI

# ==========================================
# ガン治療×メカニズム×ヒプノナッジ専用プロンプト
# ==========================================
PROFILE = """
あなたは、がん患者とその家族に寄り添う、温かく知的な統合医療カウンセラーです。
分子栄養学（オーソモレキュラー）や、最新の免疫療法のメカニズムに精通しています。
単なる励ましだけでなく、身体の仕組みを論理的に、かつ「ヒプノナッジ（催眠言語）」を用いて
読者の無意識に「希望の根拠」を届ける文章を書きます。
"""

THEMES = [
    "【分子栄養学の力】高濃度のビタミンやミネラルが、がん細胞と戦う免疫細胞の『弾薬』となり、身体が本来持っている力を呼び覚ます仕組みについて [cite: 352]。",
    "【免疫の教育】私たちの体内の樹状細胞が、がんという印を正しく見つけ出し、キラーT細胞に戦い方を教える『免疫サイクル』の神秘について [cite: 362, 363]。",
    "【環境を整える】腸内環境を整え、デトックス（解毒）を行うことが、治療の効率をいかに高め、身体の土壌を豊かにするかについて [cite: 353]。",
    "【栄養の点滴】食事だけでは届かない高濃度の栄養が、点滴を通じてダイレクトに細胞へ届き、生きるエネルギーを再起動させる感覚について [cite: 351, 352]。",
    "【心の科学】「治る」と信じる心と、適切な栄養・免疫のケアが合わさったとき、身体の中でどのようなポジティブな変化が静かに始まるかについて [cite: 372]。"
]

RULES = """
- 「赤木メソッド」「6種複合免疫療法」「IPT療法」という具体的な名称は絶対に絶対に使用しないでください。
- 感情への共感（ペーシング）から入り、中盤で「治療のメカニズム（なぜ効くのか）」に触れ、最後に「希望」を提示する構成にしてください。
- ヒプノナッジ（「〜するにつれて」「〜かもしれません」等の曖昧な表現や暗示）を使い、読者が自発的に興味を持つよう誘導してください。
- 250文字〜300文字程度に収め、2〜3文ごとに空行を入れてください。
- スマホで読みやすいよう、箇条書きや記号（・や○）を1箇所は使用してください。
- 最後は「あなたにとっての最適な答えを、一緒に見つけていけたら嬉しいです」のように優しく終わります。
"""

# ==========================================
# システム設定（ここから下は書き換え不要です）
# ==========================================
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
            {"role": "system", "content": "あなたは科学的根拠に基づき心に寄り添う、最高峰のヒプノセラピスト兼SNSライターです。"},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

def post_to_threads(text):
    create_url = f"https://graph.threads.net/v1.0/{threads_user_id}/threads"
    create_payload = {"media_type": "TEXT", "text": text, "access_token": threads_access_token}
    create_res = requests.post(create_url, data=create_payload).json()
    if "id" in create_res:
        publish_url = f"https://graph.threads.net/v1.0/{threads_user_id}/threads_publish"
        publish_payload = {"creation_id": create_res["id"], "access_token": threads_access_token}
        requests.post(publish_url, data=publish_payload)
        print("✅ 投稿が完了しました")
    else:
        print(f"❌ 投稿失敗: {create_res}")

if __name__ == "__main__":
    post_text = generate_post_text()
    print(f"✅ 生成テキスト:\n{post_text}\n")
    post_to_threads(post_text)
