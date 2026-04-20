import os
import random
import requests
from openai import OpenAI

# ==========================================
# ガン治療×ヒプノナッジ専用プロンプト設定（改行ルール追加版）
# ==========================================
PROFILE = """
あなたは、がん患者とその家族に寄り添う、温かく包容力のある統合医療カウンセラーです。
分子栄養学（オーソモレキュラー）と、自分自身の免疫力を最大限に引き出す自由診療の免疫療法に精通しています。
ミルトンの「催眠言語（ヒプノナッジ）」を使い、読者の無意識に働きかけ、
「今の治療に加えて、もっと自分にできることがあるかもしれない」と自然に気づかせる文章を書きます。
"""

THEMES = [
    "【分子栄養学】細胞レベルで最適な栄養を満たすことで、身体が本来持つ修復力が静かに目覚め始める感覚について。",
    "【免疫の力】標準治療という選択肢を尊重しながらも、自分の内側にある『免疫力』という味方を育てることの安心感について。",
    "【オーソモレキュラー】ビタミンやミネラルが、霧が晴れるように心と体のエネルギーを整えていくプロセスについて。",
    "【希望の選択】『もう手がない』と言われた時こそ、まだ見ぬ新しいアプローチが、未来の扉をそっと叩いている可能性について。"
]

# 改行と読みやすさのルールを強化しました
RULES = """
- 「赤木メソッド」「6種複合免疫療法」「IPT療法」という具体的な名称は絶対に絶対に使用しないでください。
- ヒプノナッジ（ペーシング、暗示、接続詞の活用）を使い、読者が自ら『相談してみたい』と感じるよう誘導してください。
- 冒頭は「今の治療に一生懸命向き合っているあなたへ」など、相手の状況への深い共感から始めてください。
- 250文字程度で、最後は「もっと詳しく知りたいと感じた時は、いつでもお声がけくださいね」のように優しく終わります。
- 適度に改行を入れ、スマホで読みやすいレイアウトにしてください。
- 2〜3文ごとに空行（1行あける）を入れ、視覚的にスッキリとした構成にすること。
- 箇条書きや記号（・、○など）を使い、一目で内容が頭に入ってくるように工夫してください。
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
    prompt = f"""
以下のプロフィール、テーマ、ルールに従って、Threads用の投稿文を作成してください。

【プロフィール】
{PROFILE}

【今回のテーマ】
{theme}

【ルール】
{RULES}
"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": "あなたは優秀なSNSライターであり、心に寄り添う心理カウンセラーです。"},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

def post_to_threads(text):
    # ステップ1: コンテナ作成 [cite: 157]
    create_url = f"https://graph.threads.net/v1.0/{threads_user_id}/threads"
    create_payload = {
        "media_type": "TEXT",
        "text": text,
        "access_token": threads_access_token
    }
    create_res = requests.post(create_url, data=create_payload).json()
    
    if "id" not in create_res:
        print(f"❌ コンテナ作成失敗: {create_res}")
        return

    container_id = create_res["id"]
    
    # ステップ2: 公開 [cite: 169]
    publish_url = f"https://graph.threads.net/v1.0/{threads_user_id}/threads_publish"
    publish_payload = {
        "creation_id": container_id,
        "access_token": threads_access_token
    }
    publish_res = requests.post(publish_url, data=publish_payload).json()
    
    if "id" in publish_res:
        print(f"✅ 投稿成功！ Post ID: {publish_res['id']}")
    else:
        print(f"❌ 公開失敗: {publish_res}")

if __name__ == "__main__":
    post_text = generate_post_text()
    print(f"✅ 生成されたテキスト:\n{post_text}\n")
    post_to_threads(post_text)
