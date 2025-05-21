import streamlit as st
import requests

# ====================
# 🔧 Custom CSS & JS
# ====================
custom_css = """
<style>
    html, body, [class*="css"]  {
        font-family: 'Segoe UI', sans-serif;
        background-color: #f5f7fa;
    }

    h1 {
        color: #0d47a1;
        font-size: 2.3rem;
        margin-bottom: 0.5rem;
    }

    .stTextInput > div > div > input,
    .stTextArea > div > textarea {
        border: 2px solid #1e88e5;
        border-radius: 10px;
        padding: 0.5rem;
        font-size: 1rem;
    }

    button[kind="primary"] {
        background-color: #1976d2 !important;
        color: white !important;
        border-radius: 10px;
        padding: 0.6rem 1rem;
        font-size: 1rem;
        transition: all 0.2s ease;
    }

    button[kind="primary"]:hover {
        background-color: #0d47a1 !important;
    }

    .stDownloadButton {
        background-color: #43a047 !important;
        color: white !important;
        border-radius: 8px;
        font-weight: bold;
        transition: 0.2s;
    }

    .stDownloadButton:hover {
        background-color: #2e7d32 !important;
    }

    .stAlert {
        border-radius: 10px;
        padding: 1rem;
        font-size: 1rem;
    }

    @media (max-width: 768px) {
        h1 {
            font-size: 1.5rem;
        }

        .stTextArea > div > textarea {
            font-size: 0.9rem;
        }

        button[kind="primary"] {
            font-size: 0.9rem;
        }
    }
</style>
"""

dark_mode_toggle = """
<script>
function toggleDarkMode() {
  const root = document.documentElement;
  if (root.style.filter === 'invert(1) hue-rotate(180deg)') {
    root.style.filter = 'invert(0)';
  } else {
    root.style.filter = 'invert(1) hue-rotate(180deg)';
  }
}
</script>
<button onclick="toggleDarkMode()" style="
    position: fixed;
    top: 10px;
    right: 10px;
    z-index: 9999;
    padding: 8px 16px;
    background-color: #222;
    color: #fff;
    border: none;
    border-radius: 8px;
    font-weight: bold;
    cursor: pointer;">🌓 Dark Mode</button>
"""

# Inject CSS & JS
st.markdown(custom_css, unsafe_allow_html=True)
st.markdown(dark_mode_toggle, unsafe_allow_html=True)

# ====================
# 🧠 App Config
# ====================
st.set_page_config(page_title="ElevenLabs TTS", page_icon="🗣")
st.title("🗣 ElevenLabs Text to Speech (TTS)")
st.markdown("Bikin suara dari teks pakai ElevenLabs. Masukin API key & info lainnya, terus download deh hasilnya!")

# ====================
# 📝 Input Fields
# ====================
api_key = st.text_input("🔑 API Key", type="password")
voice_id = st.text_input("🎙 Voice ID", value="EXAVITQu4vr4xnSDxMaL")
model_id = st.text_input("🧠 Model ID", value="eleven_multilingual_v2")
text = st.text_area("📄 Teks yang ingin diubah jadi suara", height=200)

# ====================
# ▶️ Generate & Download
# ====================
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
            with st.spinner("🛠️ Lagi proses generate audio..."):
                response = requests.post(url, headers=headers, json=data)
                response.raise_for_status()
                audio_data = response.content

                st.success("✅ Berhasil generate suara! Download di bawah ini:")
                st.download_button("⬇️ Download MP3", data=audio_data, file_name="tts_output.mp3", mime="audio/mpeg")

        except requests.exceptions.HTTPError as e:
            st.error(f"❌ HTTP Error: {e}")
        except Exception as e:
            st.error(f"❌ Error: {e}")
