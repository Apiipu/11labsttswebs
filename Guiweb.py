import streamlit as st
import requests
import base64
from io import BytesIO

st.set_page_config(page_title="ElevenLabs TTS", layout="centered")
st.title("🗣️ ElevenLabs Text-to-Speech")

# Sidebar API Key Input
with st.sidebar:
    st.header("🔑 API Key")
    api_key = st.text_input("Masukkan API Key Anda", type="password")
    if not api_key:
        st.warning("API Key diperlukan.")
        st.stop()

# Fungsi: Ambil daftar model
@st.cache_data(show_spinner=False)
def get_models():
    response = requests.get(
        'https://api.elevenlabs.io/v1/models',
        headers={
            "Content-Type": "application/json",
            "xi-api-key": api_key
        }
    )
    response.raise_for_status()
    return response.json()

# Fungsi: Ambil daftar voice
@st.cache_data(show_spinner=False)
def get_voices():
    response = requests.get(
        'https://api.elevenlabs.io/v1/voices',
        headers={
            "Content-Type": "application/json",
            "xi-api-key": api_key
        }
    )
    response.raise_for_status()
    return response.json()

# Dark mode toggle
st.sidebar.markdown("---")
dark_mode = st.sidebar.checkbox("🌙 Dark Mode", value=False)
if dark_mode:
    st.markdown("""
        <style>
        body { background-color: #0e1117; color: white; }
        </style>
    """, unsafe_allow_html=True)

# Ambil model dan voice
try:
    models = get_models()
    voices = get_voices()
except Exception as e:
    st.error(f"Gagal mengambil data: {e}")
    st.stop()

model_options = [m['model_id'] for m in models]
voice_options = {v['name']: v['voice_id'] for v in voices['voices']}

# Form input teks
st.subheader("🔊 Form TTS")
text_input = st.text_area("Masukkan teks:", height=150)
st.caption(f"Jumlah kata: {len(text_input.split())}")

selected_model = st.selectbox("Pilih model:", model_options)
selected_voice_name = st.selectbox("Pilih suara:", list(voice_options.keys()))
selected_voice_id = voice_options[selected_voice_name]

if st.button("🎙️ Generate Suara"):
    if not text_input.strip():
        st.warning("Teks tidak boleh kosong.")
        st.stop()

    url = f"https://api.elevenlabs.io/v1/text-to-speech/{selected_voice_id}"
    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json",
        "xi-model-id": selected_model
    }
    payload = {"text": text_input}

    with st.spinner("Menghasilkan audio..."):
        try:
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()

            audio_bytes = response.content
            st.audio(audio_bytes, format="audio/mp3")

            # Download link
            b64 = base64.b64encode(audio_bytes).decode()
            href = f'<a href="data:audio/mp3;base64,{b64}" download="tts_output.mp3">📥 Download MP3</a>'
            st.markdown(href, unsafe_allow_html=True)

        except requests.exceptions.RequestException as e:
            st.error(f"Gagal menghasilkan audio: {e}")

# Footer
st.markdown("""
---
🔧 Dibuat dengan Streamlit • ElevenLabs API
""")
