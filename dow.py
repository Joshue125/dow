import tkinter as tk
from tkinter import messagebox
import yt_dlp as youtube_dl
import ffmpeg
import os
import re

def download_and_convert(url):
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': '%(title)s.%(ext)s',
        'noplaylist': True
    }

    try:    
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            video_title = info_dict['title']
            
            # Get the file extension of the downloaded file
            download_ext = info_dict['ext']
            original_audio_file = f"{video_title}.{download_ext}"
            
            # Ensure the filename is safe for ffmpeg
            safe_audio_file = re.sub(r'[<>:"/\\|?*]', '_', original_audio_file)
            os.rename(original_audio_file, safe_audio_file)  # Rename the file to be safe for ffmpeg

            output_wav_file = f"{safe_audio_file}.wav"
            
            # Convert to WAV using ffmpeg
            (
                ffmpeg
                .input(safe_audio_file)
                .output(output_wav_file, acodec='pcm_s16le')
                .run()
            )
            messagebox.showinfo("Descarga completada", f"Archivo guardado como: {output_wav_file}")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def on_download_click():
    url = url_entry.get()
    if not url:
        messagebox.showwarning("Entrada faltante", "Por favor, ingrese una URL.")
    else:
        download_and_convert(url)

root = tk.Tk()
root.title("Download")

tk.Label(root, text="Ingrese la URL del video: ").pack(pady=5)
url_entry = tk.Entry(root, width=50)
url_entry.pack(pady=5)
download_button = tk.Button(root, text="Descargar y Convertir", command=on_download_click)
download_button.pack(pady=10)
root.mainloop()