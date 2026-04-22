import streamlit as st
import whisper
from deep_translator import GoogleTranslator
import os
import tempfile

# Page ကို အကျယ်ချဲ့ထားပေးပါတယ်
st.set_page_config(page_title="AI Audio Translator", page_icon="🎙️", layout="wide")
st.title("🎙️ Multi-Language Audio to Myanmar")

@st.cache_resource
def load_model():
    return whisper.load_model("base")

model = load_model()

if 'original_text' not in st.session_state:
    st.session_state.original_text = ""

def format_for_ai_voice(text):
    # ယောကျ်ားလေးအသံအတွက် ပြောင်းခြင်းနှင့် ပုဒ်ဖြတ်ပုဒ်ရပ်
    text = text.replace("ကျွန်မ", "ကျွန်တော်")
    text = text.replace(". ", "။\n\n") 
    text = text.replace(".", "။\n\n")
    return text

uploaded_file = st.file_uploader("MP3 သို့မဟုတ် MP4 ဖိုင်တင်ပါ", type=["mp3", "mp4", "m4a", "wav"])

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        tmp_path = tmp_file.name

    if st.button("အသံမှ စာသားသို့ ပြောင်းပါ 📝"):
        with st.spinner("အသံကို စာသားအဖြစ် ပြောင်းနေသည်..."):
            result = model.transcribe(tmp_path)
            st.session_state.original_text = result['text']

    if st.session_state.original_text:
        st.write("---")
        if st.button("မြန်မာလို ဘာသာပြန်ပါ 🇲🇲"):
            with st.spinner("ဘာသာပြန်နေသည်..."):
                translator = GoogleTranslator(source='auto', target='my')
                # စာလုံးရေ အများကြီးအတွက် အပိုင်းခွဲပြန်ပေးခြင်း
                text_to_translate = st.session_state.original_text
                chunks = [text_to_translate[i:i+1000] for i in range(0, len(text_to_translate), 1000)]
                translated_text = " ".join([translator.translate(c) for c in chunks])
                
                final_text = format_for_ai_voice(translated_text)
                
                st.subheader("မြန်မာဘာသာပြန်စာသား (အောက်ပါအကွက်ထဲတွင် Copy ကူးပါ)")
                # အမြင့် ၈၀၀ ထားပေးထားလို့ စာတွေအများကြီးကို တစ်ခါတည်း Copy ကူးလို့ရပါပြီ
                st.text_area("စာသားအားလုံးကို Select All လုပ်ပြီး Copy ကူးယူပါ", final_text, height=800)

    if os.path.exists(tmp_path):
        os.remove(tmp_path)
