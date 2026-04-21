import streamlit as st
import whisper
from deep_translator import GoogleTranslator
import os
import tempfile

st.set_page_config(page_title="AI Audio Translator", page_icon="🎙️")
st.title("🎙️ Multi-Language Audio to Myanmar Translator")

@st.cache_resource
def load_model():
    # ဘာသာစကားမျိုးစုံအတွက် ပိုမှန်အောင် base model ကို သုံးထားပါတယ်
    return whisper.load_model("base")

model = load_model()

if 'original_text' not in st.session_state:
    st.session_state.original_text = ""

# စာသားရှည်ပါက အပိုင်းခွဲရန်
def split_text(text, max_length=1000):
    return [text[i:i+max_length] for i in range(0, len(text), max_length)]

# AI Thiha ဖတ်ရအဆင်ပြေစေရန်နှင့် ယောကျ်ားလေးအသုံးအနှုန်းဖြစ်စေရန် ပြင်ဆင်ခြင်း
def format_for_ai_voice(text):
    # 'ကျွန်မ' ကို 'ကျွန်တော်' သို့ပြောင်းရန်
    text = text.replace("ကျွန်မ", "ကျွန်တော်")
    # ပုဒ်ဖြတ်ပုဒ်ရပ်များကို ရှင်းလင်းစွာ ပြင်ရန် (AI ဖတ်ရလွယ်အောင်)
    text = text.replace(". ", "။\n\n") 
    text = text.replace(".", "။\n\n")
    text = text.replace(", ", "၊ ")
    return text

# အသံဖိုင်တင်ရန် (mp3, mp4 အပါအဝင်)
uploaded_file = st.file_uploader("MP3 သို့မဟုတ် MP4 ဖိုင်တင်ပါ (တရုတ်၊ ထိုင်း၊ ဂျပန်၊ အင်္ဂလိပ် အားလုံးရသည်)", type=["mp3", "mp4", "m4a", "wav"])

if uploaded_file is not None:
    # ယာယီဖိုင်ဆောက်ခြင်း
    with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(uploaded_file.name)[1]) as tmp_file:
        tmp_file.write(uploaded_file.getvalue())
        tmp_path = tmp_file.name

    st.write("---")
    
    # အဆင့် (၁) - အသံမှ စာသားသို့ ပြောင်းခြင်း
    if st.button("အသံမှ စာသားသို့ ပြောင်းပါ 📝"):
        with st.spinner("အသံကို စာသားအဖြစ် ပြောင်းနေသည်... (ဘာသာစကားကို အလိုအလျောက် ခွဲခြားနေသည်)"):
            try:
                # မည်သည့်ဘာသာစကားမဆို Auto Detect လုပ်ပေးမည်
                result = model.transcribe(tmp_path)
                st.session_state.original_text = result['text']
            except Exception as e:
                st.error(f"Error: {e}")

    # မူရင်းစာသားပြခြင်း
    if st.session_state.original_text:
        st.subheader("မူရင်းစာသား (Original Text)")
        st.info(st.session_state.original_text)
        
        st.write("---")
        
        # အဆင့် (၂) - မြန်မာလို ဘာသာပြန်ခြင်း
        if st.button("မြန်မာလို ဘာသာပြန်ပါ 🇲🇲"):
            with st.spinner("မြန်မာဘာသာသို့ ပြန်ဆိုနေသည်..."):
                try:
                    chunks = split_text(st.session_state.original_text)
                    translated_chunks = []
                    translator = GoogleTranslator(source='auto', target='my')
                    for chunk in chunks:
                        translated_chunks.append(translator.translate(chunk))
                    
                    full_translation = " ".join(translated_chunks)
                    
                    # ယောကျ်ားလေးအသံနှင့် ပုဒ်ဖြတ်ပုဒ်ရပ်အတွက် Format ချခြင်း
                    final_ready_text = format_for_ai_voice(full_translation)
                    
                    st.subheader("AI Thiha ဖတ်ရန်အဆင်သင့်ဖြစ်သော မြန်မာစာ")
                    st.success(final_ready_text)
                except Exception as e:
                    st.error(f"ဘာသာပြန်ရာတွင် အမှားဖြစ်သွားပါသည်: {e}")

    # ဖိုင်များကို ရှင်းလင်းခြင်း
    if os.path.exists(tmp_path):
        os.remove(tmp_path)
else:
    st.session_state.original_text = ""
