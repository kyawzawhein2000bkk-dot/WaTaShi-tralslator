import streamlit as st
import whisper
from deep_translator import GoogleTranslator
import os
import tempfile

st.set_page_config(page_title="AI Audio Translator", page_icon="🎙️")
st.title("🎙️ Audio to Myanmar Translator")

@st.cache_resource
def load_model():
    return whisper.load_model("base")

model = load_model()

if 'original_text' not in st.session_state:
    st.session_state.original_text = ""

def split_text(text, max_length=1000):
    return [text[i:i+max_length] for i in range(0, len(text), max_length)]

def format_for_ai_voice(text):
    text = text.replace("ကျွန်မ", "ကျွန်တော်")
    text = text.replace(". ", "။\n\n") 
    text = text.replace(".", "။\n\n")
    text = text.replace(", ", "၊ ")
    return text

uploaded_file = st.file_uploader("MP3 သို့မဟုတ် MP4 ဖိုင်တင်ပါ", type=["mp3", "mp4", "m4a", "wav"])

if uploaded_file is not None:
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        tmp_path = tmp_file.name

    if st.button("အသံမှ စာသားသို့ ပြောင်းပါ 📝"):
        with st.spinner("အသံကို စာသားအဖြစ် ပြောင်းနေသည်..."):
            try:
                result = model.transcribe(tmp_path)
                st.session_state.original_text = result['text']
            except Exception as e:
                st.error(f"Error: {e}")

    if st.session_state.original_text:
        st.subheader("မူရင်းစာသား (Original Text)")
        st.info(st.session_state.original_text)
        
        if st.button("မြန်မာလို ဘာသာပြန်ပါ 🇲🇲"):
            with st.spinner("မြန်မာဘာသာသို့ ပြန်ဆိုနေသည်..."):
                try:
                    chunks = split_text(st.session_state.original_text)
                    translated_chunks = [GoogleTranslator(source='auto', target='my').translate(c) for c in chunks]
                    final_ready_text = format_for_ai_voice(" ".join(translated_chunks))
                    
                    st.subheader("မြန်မာဘာသာပြန် (Copy ကူးရန် ညာဘက်အပေါ်ရှိ ခလုတ်ကိုနှိပ်ပါ)")
                    st.code(final_ready_text, language="text") # ဤနေရာတွင် Copy ခလုတ်ပေါ်ပါမည်
                    
                except Exception as e:
                    st.error(f"Error: {e}")

    if os.path.exists(tmp_path):
        os.remove(tmp_path)
