"""
Streamlit UIを使ったコードです。
・pip install streamlit
実行は「ターミナル」で下記を打ち込みます
python -m streamlit run "C:\\Users\\7Java15\\Desktop\\kotobaasobi\\kotobaasobi3.py"
そうすると最初は青文字でEmail：と聞いてきます。無視してリターンを押せば実行。
その後は出てきません。

・CTRL+Cでストップ
"""

from dotenv import load_dotenv
import google.generativeai as genai
import os
import streamlit as st


load_dotenv()
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

model = genai.GenerativeModel("models/gemini-2.5-pro")

#セッション保持するときの定型文
if "words" not in st.session_state:
    st.session_state["words"] = []

#入力中の文字列をセッションで保持
if "typed" not in st.session_state:
    st.session_state.typed = ""

# Streamlit UI
st.title("giminiとしりとり対決～!")

st.session_state.typed = st.text_input("あなたの番（ひらがな）", value=st.session_state.typed)

gojuon = [
    ["あ","い","う","え","お"],
    ["か","き","く","け","こ"],
    ["さ","し","す","せ","そ"],
    ["た","ち","つ","て","と"],
    ["な","に","ぬ","ね","の"],
    ["は","ひ","ふ","へ","ほ"],
    ["ま","み","む","め","も"],
    ["や","","ゆ","","よ"],
    ["ら","り","る","れ","ろ"],
    ["わ","","","","ん"],
]
st.markdown("### あいうえおボタン")

st.write("ボタン描画開始")  # ← これが表示されるか確認

for row in gojuon:
    cols = st.columns(5)
    for i,char in enumerate(row):
        if char and cols[i].button(char, key=f"btn_{char}_{i}"):
            st.session_state.typed += char

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

if st.button("OK"):
    user = st.session_state.typed.strip()
    if not is_valid(st.session_state["words"],user):
        st.error("あなたの負け～")
    else:
        st.session_state.words.append(user)
        ai = get_ai_word(user[-1])
        st.write(f'あいての番:{ai}')
        if not is_valid(st.session_state["words"],ai):
            st.error('geminiの負け～')
        else:
            st.session_state.words.append(ai)
    st.session_state.typed = ""
st.write("これまでの単語：","→".join(st.session_state.words))