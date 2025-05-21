import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import requests
import os
import tempfile
import pygame

class ElevenLabsTTS:
    def __init__(self, master):
        self.master = master
        master.title("ElevenLabs TTS")
        master.geometry("400x500")
        master.resizable(False, False)
        pygame.mixer.init()

        style = ttk.Style()
        style.configure("TLabel", font=("Segoe UI", 10))
        style.configure("TEntry", font=("Segoe UI", 10))
        style.configure("TButton", font=("Segoe UI", 10))

        container = tk.Frame(master, padx=15, pady=15)
        container.pack(fill=tk.BOTH, expand=True)

        # API Key
        ttk.Label(container, text="API Key:").pack(anchor="w")
        self.api_key_entry = ttk.Entry(container, show="*", width=40)
        self.api_key_entry.pack(fill="x", pady=5)

        # Teks
        ttk.Label(container, text="Teks:").pack(anchor="w")
        self.text_entry = tk.Text(container, width=40, height=5, font=("Segoe UI", 10))
        self.text_entry.pack(fill="x", pady=5)

        # Model ID
        ttk.Label(container, text="Model ID:").pack(anchor="w")
        self.model_entry = ttk.Entry(container, width=40)
        self.model_entry.insert(0, "eleven_multilingual_v2")
        self.model_entry.pack(fill="x", pady=5)

        # Voice ID
        ttk.Label(container, text="Voice ID:").pack(anchor="w")
        self.voice_entry = ttk.Entry(container, width=40)
        self.voice_entry.insert(0, "EXAVITQu4vr4xnSDxMaL")
        self.voice_entry.pack(fill="x", pady=5)

        # Tombol Preview dan Generate
        button_frame = tk.Frame(container)
        button_frame.pack(fill="x", pady=10)

        self.preview_button = ttk.Button(button_frame, text="🔊 Preview", command=self.preview_tts)
        self.preview_button.pack(side="left", expand=True, fill="x", padx=(0, 5))

        self.generate_button = ttk.Button(button_frame, text="💾 Generate & Save", command=self.generate_tts)
        self.generate_button.pack(side="right", expand=True, fill="x", padx=(5, 0))

    def send_request(self, api_key, text, model, voice_id):
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

    def generate_tts(self):
        api_key = self.api_key_entry.get()
        text = self.text_entry.get("1.0", tk.END).strip()
        model = self.model_entry.get()
        voice_id = self.voice_entry.get()

        if not api_key or not text or not model or not voice_id:
            messagebox.showerror("Error", "Harap lengkapi semua input.")
            return

        try:
            audio_data = self.send_request(api_key, text, model, voice_id)

            save_path = filedialog.asksaveasfilename(defaultextension=".mp3", filetypes=[("MP3 Files", "*.mp3")])
            if save_path:
                with open(save_path, "wb") as file:
                    file.write(audio_data)
                messagebox.showinfo("Sukses", f"Audio disimpan di {save_path}")

        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Terjadi kesalahan: {e}")

    def preview_tts(self):
        api_key = self.api_key_entry.get()
        text = self.text_entry.get("1.0", tk.END).strip()
        model = self.model_entry.get()
        voice_id = self.voice_entry.get()

        if not api_key or not text or not model or not voice_id:
            messagebox.showerror("Error", "Harap lengkapi semua input.")
            return

        try:
            audio_data = self.send_request(api_key, text, model, voice_id)
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3")
            temp_file.write(audio_data)
            temp_file.close()

            pygame.mixer.music.load(temp_file.name)
            pygame.mixer.music.play()

        except requests.exceptions.RequestException as e:
            messagebox.showerror("Error", f"Terjadi kesalahan: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ElevenLabsTTS(root)
    root.mainloop()
