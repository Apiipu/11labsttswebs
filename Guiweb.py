import streamlit as st
import requests
import tempfile
import base64

def send_request(api_key, text, model, voice_id):
    url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
    headers = {
        "xi-api-key": api_key,
        "Content-Type": "application/json",
        "xi-model-id": model
    }
    data = {"text": text}

    response = requests.post(url, headers=headers, json=data)
    response.raise_for_status()
    return response.content

st.set_page_config(page_title="ElevenLabs TTS", layout="centered")

st.title("🎙️ ElevenLabs Text-to-Speech")

# Input
api_key = st.text_input("🔑 API Key", type="password")
text = st.text_area("📝 Masukkan teks yang ingin diubah jadi suara")
model_id = st.text_input("🧠 Model ID", value="eleven_multilingual_v2")
voice_id = st.text_input("🗣️ Voice ID", value="EXAVITQu4vr4xnSDxMaL")

# Tombol
col1, col2 = st.columns(2)
with col1:
    preview_clicked = st.button("🔊 Preview")
with col2:
    save_clicked = st.button("💾 Generate & Download")

if (preview_clicked or save_clicked) and not all([api_key, text, model_id, voice_id]):
    st.error("Mohon lengkapi semua input terlebih dahulu.")

if preview_clicked and all([api_key, text, model_id, voice_id]):
    try:
        audio_data = send_request(api_key, text, model_id, voice_id)
        st.audio(audio_data, format="audio/mp3")
    except requests.exceptions.RequestException as e:
        st.error(f"Terjadi kesalahan saat request: {e}")

if save_clicked and all([api_key, text, model_id, voice_id]):
    try:
        audio_data = send_request(api_key, text, model_id, voice_id)
        b64 = base64.b64encode(audio_data).decode()
        href = f'<a href="data:audio/mp3;base64,{b64}" download="tts.mp3">📥 Klik untuk download audio</a>'
        st.markdown(href, unsafe_allow_html=True)
    except requests.exceptions.RequestException as e:
        st.error(f"Terjadi kesalahan saat request: {e}")
