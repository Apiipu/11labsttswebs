import streamlit as st
import requests
import tempfile
import base64
from io import BytesIO
import pygame
import os

# Inisialisasi pygame untuk preview
pygame.mixer.init()

# Judul Aplikasi
st.set_page_config(page_title="ElevenLabs TTS", layout="centered")
st.title("🗣️ ElevenLabs TTS (Streamlit Edition)")

# Form Input
with st.form("tts_form"):
    api_key = st.text_input("🔑 API Key", type="password")
    text = st.text_area("📝 Masukkan Teks", height=150)
    model_id = st.text_input("📦 Model ID", value="eleven_multilingual_v2")
    voice_id = st.text_input("🗣️ Voice ID", value="EXAVITQu4vr4xnSDxMaL")

    col1, col2 = st.columns(2)
    generate_clicked = col1.form_submit_button("💾 Generate & Download")
    preview_clicked = col2.form_submit_button("🎧 Preview")

# Fungsi request TTS
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

# Proses Generate & Preview
if generate_clicked or preview_clicked:
    if not api_key or not text or not model_id or not voice_id:
        st.warning("⚠️ Semua input harus diisi.")
    else:
        try:
            audio_data = send_request(api_key, text, model_id, voice_id)

            # Simpan sementara
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
            temp_file.write(audio_data)
            temp_file.close()

            # Untuk preview
            if preview_clicked:
                st.audio(audio_data, format="audio/mp3")

            # Untuk download
            if generate_clicked:
                b64 = base64.b64encode(audio_data).decode()
                href = f'<a href="data:audio/mp3;base64,{b64}" download="tts_output.mp3">📥 Klik untuk download MP3</a>'
                st.markdown(href, unsafe_allow_html=True)
                st.success("✅ Audio berhasil dibuat!")

        except requests.exceptions.RequestException as e:
            st.error(f"Gagal menghasilkan audio: {e}")
