import streamlit as st
import whisper
from deep_translator import GoogleTranslator
import os

st.title("🎙️ Audio to Myanmar Text")

@st.cache_resource
def load_model():
    # ဖုန်းနဲ့သုံးမှာဖြစ်လို့ အမြန်ဆုံး model ကို သုံးပေးထားပါတယ်
    return whisper.load_model("tiny") 

model = load_model()
uploaded_file = st.file_uploader("MP3 သို့မဟုတ် MP4 ဖိုင်တင်ပါ", type=["mp3", "mp4"])

if uploaded_file:
    with open("temp_file", "wb") as f:
        f.write(uploaded_file.getbuffer())
    
    if st.button("ဘာသာပြန်မယ်"):
        with st.spinner("အလုပ်လုပ်နေပါပြီ..."):
            result = model.transcribe("temp_file")
            eng_text = result['text']
            translated = GoogleTranslator(source='auto', target='my').translate(eng_text)
            
            st.subheader("ရလဒ်")
            st.success(translated)
            st.write(f"မူရင်းစာသား: {eng_text}")
    os.remove("temp_file")
