import os
import random
import requests
from openai import OpenAI

# ==========================================
# 多角的な投稿テーマの設定（切り口を増やしました）
# ==========================================
THEMES = [
    "【標準治療を支える】抗がん剤や放射線治療などの標準治療を、分子栄養学がいかに支え、身体の土壌を整えるかという『併用』の重要性について。",
    "【副作用の不安に寄り添う】治療の副作用がつらいと感じる時、細胞レベルで栄養を満たすことが、心と体の負担をどう和らげるか。そのメカニズムについて。",
    "【免疫の視点】がん細胞が隠している『目印』を免疫細胞が正しく見つけ出し、攻撃を開始するまでの神秘的なプロセス。自己免疫を育てる希望について。",
    "【薬剤の届け方】身体の自然な仕組み（ホルモン等）を味方につけることで、必要な場所へ効率よくアプローチを届ける統合医療的な考え方について。",
    "【心の回復力】『がん難民』という言葉に不安を感じている方へ。標準治療以外の選択肢を知ることで、心に静かな安心が広がる感覚について。",
    "【環境のデトックス】水素やビタミンを活用し、酸化した細胞の錆を取り除くことが、免疫細胞の動きをいかに軽やかにするかについて。"
]

# ==========================================
# 毎回変わる「最後の一言」のリスト
# ==========================================
CLOSING_PHRASES = [
    "何かもやもやすることがあれば、いつでもメッセージをくださいね。",
    "あなたにとっての最善の道を、一緒に探していけたら嬉しいです。",
    "小さな疑問でも構いません。いつでもあなたの味方でいます。",
    "心が少しでも軽くなるお手伝いができれば幸いです。お気軽にご相談ください。",
    "あなたのペースで大丈夫。話したくなった時は、いつでもここにいますよ。",
    "ふとした瞬間に、この言葉を思い出して安心していただけたら嬉しいです。"
]

# ==========================================
# AIへの指示（プロンプト）
# ==========================================
PROFILE = """
あなたは、がん患者とその家族に寄り添う、温かく専門的な統合医療カウンセラーです。
標準治療（抗がん剤等）の重要性を尊重しつつ、分子栄養学や自由診療の免疫療法でそれを補完する知恵を持っています。
ヒプノナッジ（催眠言語）を使い、読者の無意識に「新しい可能性」と「深い安心」を届けます。
"""

RULES = """
- 文字数は150文字〜250文字程度。スマホで読みやすく、2〜3文ごとに必ず空行を入れてください。
- 「赤木メソッド」「6種複合免疫療法」「IPT療法」という名称は絶対に使用しないでください。
- 感情的な共感だけでなく、身体の仕組み（栄養、免疫、細胞）という論理的な視点を必ず含めてください。
- ヒプノナッジ（「〜するにつれて」「自然と〜」等）を用い、読者が自ら『相談してみたい』と感じるよう誘導してください。
- 文末（最後の一言）は、こちらで用意した特定のフレーズをそのまま使用してください。
"""

# ==========================================
# システム設定（書き換え不要）
# ==========================================
openai_api_key = os.environ.get("OPENAI_API_KEY")
threads_access_token = os.environ.get("THREADS_ACCESS_TOKEN")
threads_user_id = os.environ.get("THREADS_USER_ID")
client = OpenAI(api_key=openai_api_key)

def generate_post_text():
    theme = random.choice(THEMES)
    closing = random.choice(CLOSING_PHRASES)
    
    prompt = f"""
以下のプロフィール、テーマ、ルールに従って、Threads用の投稿文を作成してください。

【プロフィール】
{PROFILE}

【今回のテーマ】
{theme}

【文末に必ず入れる言葉】
{closing}

【ルール】
{RULES}
"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "あなたは心と科学の架け橋となる、最高峰のヒプノライターです。"},
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
        print("✅ 投稿が完了しました")
    else:
        print(f"❌ 投稿失敗: {res}")

if __name__ == "__main__":
    post_text = generate_post_text()
    print(f"✅ 生成テキスト:\n{post_text}\n")
    post_to_threads(post_text)
