import streamlit as st
import requests

st.set_page_config(page_title="ElevenLabs TTS", page_icon="🗣")

st.title("🗣 ElevenLabs Text to Speech (TTS)")
st.markdown("Bikin suara dari teks pakai ElevenLabs. Masukin API key & info lainnya, terus download deh hasilnya!")

# Input fields
api_key = st.text_input("🔑 API Key", type="password")
voice_id = st.text_input("🎙 Voice ID", value="EXAVITQu4vr4xnSDxMaL")
model_id = st.text_input("🧠 Model ID", value="eleven_multilingual_v2")
text = st.text_area("📄 Teks yang ingin diubah jadi suara", height=200)

# Tombol generate
if st.button("💾 Generate & Download MP3"):
    if not api_key or not voice_id or not model_id or not text:
        st.error("Semua field harus diisi dulu ya tod!")
    else:
        url = f"https://api.elevenlabs.io/v1/text-to-speech/{voice_id}"
        headers = {
            "xi-api-key": api_key,
            "Content-Type": "application/json",
            "xi-model-id": model_id
        }
        data = {"text": text}

        try:
            with st.spinner("Lagi proses generate audio..."):
                response = requests.post(url, headers=headers, json=data)
                response.raise_for_status()
                audio_data = response.content

                st.success("Berhasil generate suara! Download di bawah ini:")
                st.download_button("⬇️ Download MP3", data=audio_data, file_name="tts_output.mp3", mime="audio/mpeg")

        except requests.exceptions.HTTPError as e:
            st.error(f"HTTP Error: {e}")
        except Exception as e:
            st.error(f"Error: {e}")
