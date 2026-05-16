import os
import random
import requests
from openai import OpenAI

# ==========================================
# 投稿テーマのレパートリー（10パターンに拡張）
# ==========================================
THEMES = [
    "【標準治療を支える】抗がん剤などの標準治療を分子栄養学で支え、身体の土壌を整える併用の大切さについて。",
    "【副作用の和らげ方】治療のつらさを細胞レベルの栄養ケアで補い、心身の負担を静かに軽減するメカニズム。",
    "【免疫の教育】樹状細胞ががんの目印を捉え、キラーT細胞に戦い方を教える身体本来の賢い仕組みについて。",
    "【効率的なアプローチ】ホルモンなど身体の自然な働きを味方につけ、必要な場所に届ける自由診療の知恵。",
    "【選択肢がある安心】『もう手がない』と言われた時こそ、視野を広げることで心に広がる新しい可能性。",
    "【細胞のデトックス】水素やビタミンで細胞の錆を取り除き、免疫細胞が本来の軽やかさで動き出す根拠。",
    "【エネルギーの再起動】高濃度の栄養が細胞のミトコンドリアを満たし、戦う力が内側から目覚めていく感覚。",
    "【血液と栄養の運搬】サラサラな巡りを整えることで、必要な栄養やケアがダイレクトに患部へ届く安心感。",
    "【夜の修復力】深い休息と分子栄養学が合わさることで、寝ている間も免疫サイクルが静かに巡る不思議。",
    "【日常の小さな変化】今日選ぶ栄養やケアが、未来の身体を優しく、力強く変えていくという確かな希望。"
]

# ==========================================
# 最後の一言のレパートリー（10パターンに拡張）
# ==========================================
CLOSING_PHRASES = [
    "もやもやする時は、いつでもメッセージをくださいね。",
    "あなたに合う道を、一緒に探していけたら嬉しいです。",
    "小さな疑問でも構いません。いつでも味方でいます。",
    "心が軽くなるお手伝いをさせてください。お気軽にどうぞ。",
    "あなたのペースで大丈夫。話したくなったらここにいます。",
    "この言葉が、今のあなたの静かな安心になりますように。",
    "一人で抱え込まず、いつでもお声をかけてくださいね。",
    "次の一歩を、心地よく進めるようサポートさせてください。",
    "ふと頼りたくなった時は、いつでも頼ってくださいね。",
    "あなたの明日の心が、少しでも穏やかでありますように。"
]

# ==========================================
# AIへの指示（プロンプト）
# ==========================================
PROFILE = """
あなたは、がん患者とその家族に寄り添う温かい統合医療カウンセラーです。
標準治療を尊重しつつ、分子栄養学や免疫療法の仕組みを、ヒプノナッジ（催眠言語）を用いて読者の無意識に届けます。
"""

RULES = """
- 全体で「3つの文章（3文）」のみで構成し、文字数は必ず【120文字〜170文字】の間に収めてください。無駄を省いて非常に簡潔に！
- 「赤木メソッド」「6種複合免疫療法」「IPT療法」という具体的な名称は絶対に絶対に使用しないでください。
- 構成ルール：
  1文目：テーマに沿った共感や治療メカニズムの解説。
  2文目：ヒプノナッジ（「〜するにつれて」「自然と〜」等）を用いた、自発的な興味を促す気づき。
  3文目：指定された【文末に必ず入れる言葉】をそのまま記述。
- スマホでの圧倒的な読みやすさを出すため、1文目の後ろ、2文目の後ろに、それぞれ必ず「空行（1行あける）」を入れてください。
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

/【文末に必ず入れる言葉】
{closing}

【ルール】
{RULES}
"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "あなたは短文で心と科学の核心を突く、最高峰のヒプノライターです。"},
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
    print(f"✅ 生成テキスト（{len(post_text)}文字）:\n{post_text}\n")
    post_to_threads(post_text)
