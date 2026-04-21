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

uploaded_file = st.file_uploader("MP3 သို့မဟုတ် MP4 ဖိုင်တင်ပါ", type=["mp3", "mp4", "m4a", "wav"])

if uploaded_file is not None:
    # ယာယီဖိုင် ဆောက်ခြင်း (Error မတက်အောင်)
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        tmp_path = tmp_file.name

    if st.button("စတင်ဘာသာပြန်မယ်"):
        try:
            with st.spinner("အဆင့် (၁): အသံကို စာသားအဖြစ် ပြောင်းနေသည်..."):
                # Speech to Text
                result = model.transcribe(tmp_path)
                original_text = result['text']
                
                st.subheader("မူရင်းစာသား (Original Text)")
                st.info(original_text)

            with st.spinner("အဆင့် (၂): မြန်မာဘာသာသို့ ပြန်ဆိုနေသည်..."):
                # Translate to Myanmar
                translated = GoogleTranslator(source='auto', target='my').translate(original_text)
                
                st.subheader("မြန်မာဘာသာပြန် (Myanmar Translation)")
                st.success(translated)
                
        except Exception as e:
            st.error(f"အမှားအယွင်း ဖြစ်သွားပါသည်: {e}")
        finally:
            # ဖိုင်ကို ပြန်ဖျက်ခြင်း
            if os.path.exists(tmp_path):
                os.remove(tmp_path)
