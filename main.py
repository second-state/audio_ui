import gradio as gr
import requests


# TTS 功能
def tts(base_url, speaker, text):
    print("TTS: ", text)
    # 发起HTTP请求到后端，获取wav文件

    response = requests.post(
        base_url,
        json={"speaker": speaker, "input": text},
    )
    # 确保请求成功
    if response.status_code == 200:
        return response.content
    else:
        return None


# Whisper 功能
def whisper(base_url, lang, audio_file):
    # 发起HTTP请求到后端，获取转录的文本
    audio = open(audio_file, "rb")
    files = {"file": audio}

    if lang != "":
        files["language"] = lang

    response = requests.post(base_url, files=files)
    # 确保请求成功
    if response.status_code == 200:
        return response.json()["text"]
    else:
        return "Error: Unable to process audio file."


opt = gr.WaveformOptions()
opt.sample_rate = 16000

with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column():
            with gr.Tab("TTS"):
                base_url = gr.Textbox(
                    label="TTS BaseURL",
                    value="http://localhost:8080/v1/audio/speech_gpt",
                )
                speaker = gr.Textbox(label="Speaker", value="speaker1")
                text_input = gr.TextArea(label="输入文本")
                audio_output = gr.Audio(label="合成语音")
                button = gr.Button(value="Run")
                button.click(
                    tts, inputs=[base_url, speaker, text_input], outputs=audio_output
                )

            with gr.Tab("Whisper"):
                base_url = gr.Textbox(
                    label="Whisper BaseURL",
                    value="http://localhost:10086/v1/audio/transcriptions",
                )
                lang = gr.Dropdown(
                    label="语言",
                    choices=["", "zh", "en"],
                    value="",
                )
                audio_input = gr.Audio(
                    sources=["upload", "microphone"],
                    type="filepath",
                    label="语音",
                    waveform_options=opt,
                )

                text_output = gr.TextArea(label="识别文本")
                button = gr.Button(value="Run")
                button.click(
                    whisper, inputs=[base_url, lang, audio_input], outputs=text_output
                )

# 启动应用
if __name__ == "__main__":
    demo.launch()
