import streamlit as st
import requests
import tempfile

st.set_page_config(page_title="ElevenLabs TTS", layout="centered")
st.title("🗣️ ElevenLabs Text-to-Speech (TTS)")

# Input API Key
api_key = st.text_input("Masukkan API Key ElevenLabs kamu:", type="password")

if api_key:
    headers = {
        "Content-Type": "application/json",
        "xi-api-key": api_key
    }

    # Ambil daftar model
    try:
        models_res = requests.get("https://api.elevenlabs.io/v1/models", headers=headers)
        models_res.raise_for_status()
        models = models_res.json().get("models", [])
        model_ids = [model['model_id'] for model in models]
    except Exception as e:
        st.error(f"Gagal mengambil model: {e}")
        st.stop()

    # Ambil daftar voice
    try:
        voices_res = requests.get("https://api.elevenlabs.io/v1/voices", headers=headers)
        voices_res.raise_for_status()
        voices = voices_res.json().get("voices", [])
        voice_options = {f"{v['name']} ({v['voice_id'][:6]})": v['voice_id'] for v in voices}
    except Exception as e:
        st.error(f"Gagal mengambil voice: {e}")
        st.stop()

    # Form
    with st.form("tts_form"):
        text = st.text_area("Masukkan teks yang ingin dibacakan:", height=150)
        selected_model = st.selectbox("Pilih Model:", model_ids)
        selected_voice = st.selectbox("Pilih Voice:", list(voice_options.keys()))
        submitted = st.form_submit_button("🔊 Generate")

    if submitted and text:
        voice_id = voice_options[selected_voice]
        tts_url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}/stream"
        payload = {
            "text": text,
            "model_id": selected_model
        }

        try:
            with st.spinner("Menghasilkan audio..."):
                response = requests.post(tts_url, headers=headers, json=payload)
                response.raise_for_status()

                # Simpan audio
                with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmp_file:
                    tmp_file.write(response.content)
                    tmp_path = tmp_file.name

                st.audio(tmp_path, format="audio/mp3")
                with open(tmp_path, "rb") as f:
                    st.download_button("💾 Download Audio", f, file_name="output.mp3")

        except requests.exceptions.RequestException as e:
            st.error(f"Gagal generate audio: {e}")
