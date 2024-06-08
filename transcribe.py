import whisper
from pathlib import Path
from moviepy.editor import VideoFileClip
import subprocess

# Verificar se o ffmpeg está no PATH
try:
    subprocess.run(['ffmpeg', '-version'], capture_output=True, check=True)
except subprocess.CalledProcessError as e:
    print("Erro ao verificar o ffmpeg: ", e)
    exit(1)
except FileNotFoundError:
    print("ffmpeg não encontrado. Certifique-se de que o ffmpeg está instalado e no PATH do sistema.")
    exit(1)

# Obtendo o caminho absoluto do diretório atual
current_path = Path.cwd()

# Nome do arquivo
file_name = "nomedoarquivo.mp4"

# Caminho completo para o arquivo
print("Caminho completo para o arquivo.")
full_file_path = current_path / file_name

# Carregando o modelo
print("Carregando o modelo.")
model = whisper.load_model("large") #base

# Extraindo áudio do arquivo AVI e salvando como MP3
print("Extraindo áudio do arquivo AVI e salvando como MP3.")
video_clip = VideoFileClip(str(full_file_path))
audio_clip = video_clip.audio
output_audio_path = current_path / (file_name[:-4] + ".mp3")  # Removendo a extensão .avi
audio_clip.write_audiofile(str(output_audio_path))

# Carregando os dados de áudio
#print("Carregando os dados do audio.")
#audio = whisper.load_audio(str(output_audio_path))

# Transcrição do arquivo de áudio
print("Iniciando transcrição do áudio.")
#result = model.transcribe(audio)
result = model.transcribe(str(output_audio_path), language='pt', verbose=True)

# Função para converter segundos em formato SRT
def format_timestamp(seconds: float):
    milliseconds = int((seconds - int(seconds)) * 1000)
    seconds = int(seconds)
    minutes = seconds // 60
    seconds = seconds % 60
    hours = minutes // 60
    minutes = minutes % 60
    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"

# Escrevendo a transcrição no formato SRT
print("Escrevendo a transcrição no formato SRT.")
srt_output_file_name = file_name[:-4] + ".srt"  # Removendo a extensão .avi
srt_output_file_path = current_path / srt_output_file_name

with open(srt_output_file_path, "w", encoding="utf-8") as srt_file:
    for i, segment in enumerate(result['segments']):
        start_time = format_timestamp(segment['start'])
        end_time = format_timestamp(segment['end'])
        text = segment['text'].strip()
        srt_file.write(f"{i + 1}\n")
        srt_file.write(f"{start_time} --> {end_time}\n")
        srt_file.write(f"{text}\n\n")

print("Fim.")
