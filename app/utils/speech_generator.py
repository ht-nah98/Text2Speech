import os
from openai import OpenAI
from pathlib import Path
from pydub import AudioSegment

# Define the output directory and ensure it exists
output_dir = Path(__file__).parent.parent.parent / "output"
output_dir.mkdir(parents=True, exist_ok=True)

def get_next_output_filename(output_dir, prefix="output", extension=".mp3"):
    existing_files = output_dir.glob(f"{prefix}*{extension}")
    indices = [int(f.stem[len(prefix):]) for f in existing_files if f.stem[len(prefix):].isdigit()]
    next_index = max(indices, default=0) + 1
    return output_dir / f"{prefix}{next_index}{extension}"

def generate_speech(text, voice="echo", speed_factor=0.89, api_key=None):
    if not api_key:
        raise ValueError("API key not provided")
    
    try:
        client = OpenAI(api_key=api_key)
        
        # Generate the next available filename
        output_filename = get_next_output_filename(output_dir)

        # Generate speech and save to the specified filename
        with client.audio.speech.with_streaming_response.create(
            model="tts-1",
            voice=voice,
            input=text
        ) as response:
            response.stream_to_file(output_filename)

        audio = AudioSegment.from_file(output_filename)

        # Change the playback speed
        slowed_audio = audio._spawn(audio.raw_data, overrides={
             "frame_rate": int(audio.frame_rate * speed_factor)
        })

        # Resample to the original frame rate
        slowed_audio = slowed_audio.set_frame_rate(audio.frame_rate)

        # Save the modified audio file
        slowed_audio.export(output_filename, format="mp3")

        print(f"Saved speech with voice '{voice}' to {output_filename}")
        
        return str(output_filename)
    except Exception as e:
        print(f"Error generating speech: {str(e)}")
        raise

# If you want to test the function directly
if __name__ == "__main__":
    test_text = """ Đầu tiên , chúng ta cần hiểu "vô ngã" là gì. Trong tiếng Pali, "vô ngã" được gọi là "anatta". Đây là một trong ba pháp ấn của Phật giáo, cùng với vô thường (anicca) và khổ (dukkha). Vậy vô ngã có nghĩa là gì?
    """
    generate_speech(test_text)