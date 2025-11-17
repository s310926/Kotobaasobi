from dotenv import load_dotenv
import google.generativeai as genai
import os

load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("models/gemini-2.5-pro")

user_words = []

def is_hiragana(text):
    return all('あ' <= ch <= 'ん' for ch in text)

def is_valid(words,next):
    if next in words: #重複禁止
        return False
    if next[-1] == 'ん': #最後の文字がんは禁止
        return False
    if words and next[0] != words[-1][-1]:  #いわれた文字の頭とさっきのワードの最後が一緒じゃないダメ
        return False
    if not is_hiragana(next):
        return False
    return True

def get_ai_word(start):
    prompt  = f'''「{start}」から始まる小学生が知っている単語1文字返して、最後の文字に「ん」はつかないで、しりとりしよう、説明は不要
    ひらがなで返答してきて
    ''' #geminiに送る言葉
    response = model.generate_content(prompt)   #geminiに問い合わせ
    return response.text.strip() #いらない空白とかなくして返す


while True:
    user = input('あなたの番>>')
    if not is_valid(user_words,user):
        print('負け～')
        break
    user_words.append(user) #userの言葉を保存

    ai = get_ai_word(user[-1])
    print(f'あいての番>>{ai}')
    if not is_valid(user_words,ai):
        print('負け～')
        break
    user_words.append(ai)   #aiの言葉を保存