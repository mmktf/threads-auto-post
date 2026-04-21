import os
import random
import requests
from openai import OpenAI

# ==========================================
# 免疫療法深掘り × 短文（150-250文字） × ヒプノナッジ
# ==========================================
PROFILE = """
あなたは、がんの統合医療と分子栄養学に精通した、心に寄り添うカウンセラーです。
「なぜその治療が体に変化をもたらすのか」という医学的メカニズムを、
ミルトンの催眠言語（ヒプノナッジ）を使い、読者の潜在意識に「希望」として届けます。
"""

THEMES = [
    "【免疫のブレーキを外す】がん細胞が免疫にかけた『ブレーキ』を外し、キラーT細胞が本来の攻撃力を取り戻す仕組みについて。自分を信じる力が強まるかもしれません。",
    "【細胞の目印を見つける】樹状細胞ががんの情報を正しく読み取り、免疫の主役たちに『戦う相手』を教育するプロセスの重要性について。身体の賢さに気づく瞬間です。",
    "【浸透を高める知恵】体内のホルモンの働きを味方につけ、必要な成分をよりダイレクトにがん細胞へ届ける技術のメカニズムについて。効率的なケアが安心感に繋がります。",
    "【水素と活性酸素】抗酸化力の強いガスを使い、正常細胞を守りながら免疫細胞が動きやすい環境を整える科学的根拠について。深く呼吸するような安心感を届けます。",
    "【高濃度栄養の弾丸】高濃度の栄養素が血液を通じて細胞のミトコンドリアを呼び覚まし、免疫の『武器』を再充填していくプロセスについて。力が満ちる感覚を呼び起こします。"
]

RULES = """
- 150文字〜250文字程度で簡潔に作成してください。
- 「赤木メソッド」「6種複合免疫療法」「IPT療法」という具体的な名称は絶対に使用しないでください。
- 以下の内容を必ず1つ以上盛り込み、メカニズムを具体的に説明してください。
  1. 免疫細胞（T細胞や樹状細胞）の教育や活性化 [cite: 364, 365]
  2. ホルモンを利用した薬剤の透過性向上（IPTの仕組みを名称なしで） 
  3. ビタミンや水素による細胞環境の改善 
- ヒプノナッジ（「〜するにつれて」「自然と〜」等）を用い、読者が自ら気づきを得るよう誘導してください。
- 2〜3文ごとに空行を入れ、視覚的に読みやすくしてください。
- 最後は「ふと気になった時は、いつでもお話を聞かせてくださいね」のように優しく結んでください。
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
            {"role": "system", "content": "あなたは短文で核心を突く、専門知識の豊富なヒプノセラピストです。"},
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
        print("✅ 投稿成功")
    else:
        print(f"❌ 投稿失敗: {res}")

if __name__ == "__main__":
    post_text = generate_post_text()
    print(f"✅ 生成テキスト:\n{post_text}\n")
    post_to_threads(post_text)
