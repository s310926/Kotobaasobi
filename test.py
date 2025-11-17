

"""
Streamlit UIを使ったコードです。
・pip install streamlit
実行は「ターミナル」で下記を打ち込みます
python -m streamlit run "C:\\Users\\7Java15\\Desktop\\kotobaasobi\\test.py"
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

st.markdown("""
<style>
.vertical-text {
  writing-mode: vertical-rl;
  text-orientation: upright;
  font-size: 24px;
  line-height: 1.8;
  border: 1px solid #ccc;
  padding: 10px;
  height: 400px;
  width: 100%;
  display: flex;
  justify-content: center;
}
</style>
""", unsafe_allow_html=True)


gojuon = [
    ["わ","ら","や","ま","は","な","た","さ","か","あ"],
    ["　","り","　","み","ひ","に","ち","し","き","い"],
    ["　","る","ゆ","む","ふ","ぬ","つ","す","く","う"],
    ["　","れ","　","め","へ","ね","て","せ","け","え"],
    ["ん","ろ","よ","も","ほ","の","と","そ","こ","お"],
    
    ]

html = '<div class="vertical-text">'
for col in zip(*gojuon):  # 転置して列ごとに表示
    html += "<div>" + "<br>".join(col) + "</div>"
html += '</div>'

st.markdown(html, unsafe_allow_html=True)


st.markdown("### あいうえおボタン")

st.write("ボタン描画開始")  # ← これが表示されるか確認

gojuon_columns = list(zip(*gojuon))
cols = st.columns(len(gojuon_columns))

for col_idx, col_chars in enumerate(gojuon_columns):
    with cols[col_idx]:
        for row_idx, char in enumerate(col_chars):
            if char.strip() and st.button(char, key=f"btn_{char}_{col_idx}_{row_idx}"):
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