import streamlit as st
import requests
import base64

st.set_page_config(page_title="ElevenLabs TTS", layout="centered")
st.title("🎤 ElevenLabs TTS")

# Sidebar untuk API key
with st.sidebar:
    st.header("🔑 API Key")
    api_key = st.text_input("Masukkan API Key", type="password")
    if not api_key:
        st.warning("Masukkan API Key untuk melanjutkan.")
        st.stop()

# Form input teks
st.subheader("📝 Masukkan Teks")
text = st.text_area("Teks untuk diubah jadi suara:", height=150)

# Model dan Voice ID manual (bisa diganti otomatis kalau mau)
st.subheader("⚙️ Pengaturan Model & Voice")
model_id = st.text_input("Model ID", value="eleven_multilingual_v2")
voice_id = st.text_input("Voice ID", value="EXAVITQu4vr4xnSDxMaL")

# Tombol Generate
if st.button("🎧 Generate & Play"):
    if not text.strip():
        st.warning("Teks tidak boleh kosong.")
        st.stop()

    try:
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        headers = {
            "xi-api-key": api_key,
            "Content-Type": "application/json",
            "xi-model-id": model_id
        }
        payload = {"text": text}

        with st.spinner("Mengubah teks jadi suara..."):
            response = requests.post(url, headers=headers, json=payload)
            response.raise_for_status()
            audio_data = response.content

            # Putar audio
            st.audio(audio_data, format="audio/mp3")

            # Link download
            b64 = base64.b64encode(audio_data).decode()
            href = f'<a href="data:audio/mp3;base64,{b64}" download="output.mp3">📥 Download MP3</a>'
            st.markdown(href, unsafe_allow_html=True)

    except requests.exceptions.HTTPError as e:
        st.error(f"Gagal generate audio: {e}")
