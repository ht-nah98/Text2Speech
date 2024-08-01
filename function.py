import os
from openai import OpenAI
from dotenv import load_dotenv, find_dotenv
from pathlib import Path
from pydub import AudioSegment
import soundfile as sf

_ = load_dotenv(find_dotenv())
client = OpenAI(
    api_key=os.environ.get('OPENAI_API_KEY')
)

# Define the output directory and ensure it exists
output_dir = Path(__file__).parent / "output"
output_dir.mkdir(parents=True, exist_ok=True)

# Function to find the next available index for the output filename
def get_next_output_filename(output_dir, prefix="output", extension=".mp3"):
    existing_files = output_dir.glob(f"{prefix}*{extension}")
    indices = [int(f.stem[len(prefix):]) for f in existing_files if f.stem[len(prefix):].isdigit()]
    next_index = max(indices, default=0) + 1
    return output_dir / f"{prefix}{next_index}{extension}"

# Generate the next available filename
output_filename = get_next_output_filename(output_dir)

# Generate speech and save to the specified filename
with client.audio.speech.with_streaming_response.create(
    model="tts-1",
    voice="echo",
    input=""" Đầu tiên , chúng ta cần hiểu "vô ngã" là gì. Trong tiếng Pali, "vô ngã" được gọi là "anatta". Đây là một trong ba pháp ấn của Phật giáo, cùng với vô thường (anicca) và khổ (dukkha). Vậy vô ngã có nghĩa là gì?
"""
) as response:
    response.stream_to_file(output_filename)

audio = AudioSegment.from_file(output_filename)

# Adjust the playback speed (speed factor: >1.0 for faster, <1.0 for slower)
speed_factor = 0.89  # for example, to make it slower by 25% => it good: 0.9

# Change the playback speed
slowed_audio = audio._spawn(audio.raw_data, overrides={
     "frame_rate": int(audio.frame_rate * speed_factor)
})

# Resample to the original frame rate
slowed_audio = slowed_audio.set_frame_rate(audio.frame_rate)

# Save the modified audio file
slowed_audio.export(output_filename, format="mp3")

print(f"Saved slowed speech to {output_filename}")