import streamlit as st
import requests
import tempfile

st.set_page_config(page_title="ElevenLabs TTS Web App", layout="centered")
st.title("🗣️ ElevenLabs TTS")

# Input API Key
api_key = st.text_input("API Key", type="password")

# Input teks
text = st.text_area("Masukkan Teks")

# Model dan Voice ID
model_id = st.text_input("Model ID", value="eleven_multilingual_v2")
voice_id = st.text_input("Voice ID", value="EXAVITQu4vr4xnSDxMaL")

# Tombol Preview dan Generate
col1, col2 = st.columns(2)

# Fungsi kirim request ke API ElevenLabs
def generate_audio(api_key, text, model, voice_id):
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

if col1.button("🔊 Preview"):
    if not api_key or not text:
        st.error("Harap lengkapi semua input.")
    else:
        try:
            audio_data = generate_audio(api_key, text, model_id, voice_id)
            st.audio(audio_data, format="audio/mp3")
        except Exception as e:
            st.error(f"Terjadi kesalahan: {e}")

if col2.button("💾 Download"):
    if not api_key or not text:
        st.error("Harap lengkapi semua input.")
    else:
        try:
            audio_data = generate_audio(api_key, text, model_id, voice_id)
            tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
            tmp_file.write(audio_data)
            tmp_file.close()
            with open(tmp_file.name, "rb") as file:
                st.download_button("Download MP3", file, file_name="output.mp3")
        except Exception as e:
            st.error(f"Terjadi kesalahan: {e}")
