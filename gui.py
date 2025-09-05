from flask import Flask, send_from_directory, render_template, request, jsonify, send_file
from Jarvis import JarvisAssistant  # Assuming recognize_audio is defined there
import os
import traceback
import tempfile
from queue_shared import voice_command_queue, response_queue
import threading
from pydub import AudioSegment
import queue
from TTS.api import TTS as CoquiTTS

# Initialize app and Jarvis
app = Flask(__name__, static_folder="futuristic_ui", template_folder="futuristic_ui")
jarvis = JarvisAssistant()
recognize_audio = jarvis.recognize_audio

# Load Coqui TTS model ONCE at startup
coqui_tts_model = None
try:
    coqui_tts_model = CoquiTTS("tts_models/multilingual/multi-dataset/xtts_v2")
except Exception as e:
    print(f"Failed to load Coqui TTS model: {e}")

# === ROUTES ===

@app.route("/")
def index():
    user_agent = request.headers.get("User-Agent")
    if "Android" in user_agent:
        return render_template("mobile.html")
    else:
        return render_template("index.html")

@app.route("/<path:filename>")
def static_files(filename):
    return send_from_directory(app.static_folder, filename)

@app.route("/api/shutdown", methods=["POST"])
def shutdown():
    print("❌ Shutdown triggered")
    # os.system("shutdown /s /t 3")
    return "Shutdown triggered"

@app.route("/api/restart", methods=["POST"])
def restart():
    print("🔄 Restart triggered")
    # os.system("shutdown /r /t 3")
    return "Restart triggered"

@app.route("/api/exit", methods=["POST"])
def exit_app():
    def delayed_exit():
        import time
        time.sleep(1)
        os._exit(0)

    threading.Thread(target=delayed_exit).start()
    return "✅ App will now exit"

@app.route("/api/listen", methods=["POST"])
def listen():
    if "audio" not in request.files:
        return jsonify({"error": "No audio file uploaded"}), 400

    audio_file = request.files["audio"]

    # Save uploaded WebM file
    with tempfile.NamedTemporaryFile(delete=False, suffix=".webm") as webm_file:
        audio_file.save(webm_file)
        webm_path = webm_file.name

    # Convert to WAV
    wav_path = webm_path.replace(".webm", ".wav")
    try:
        sound = AudioSegment.from_file(webm_path)
        sound.export(wav_path, format="wav")
    except Exception as e:
        os.remove(webm_path)
        return jsonify({"error": f"Audio conversion failed: {e}"}), 500
    finally:
        if os.path.exists(webm_path):
            os.remove(webm_path)

    # Recognize speech
    try:
        recognized_text = recognize_audio(wav_path)
    except Exception as e:
        if os.path.exists(wav_path):
            os.remove(wav_path)
        return jsonify({"error": f"Speech recognition failed: {e}"}), 500
    finally:
        if os.path.exists(wav_path):
            os.remove(wav_path)

    recognized_text = recognized_text.strip()
    if not recognized_text:
        return jsonify({"text": "", "reply": ""})  # Prevent triggering logic

    # Enqueue only non-empty text
    if "voice_command_queue" in globals():
        voice_command_queue.put(recognized_text)

    return jsonify({
        "text": recognized_text,
        "reply": f"🧠 Jarvis heard: {recognized_text}"
    })

@app.route("/api/poll_response", methods=["GET"])
def poll_response():
    try:
        response = response_queue.get_nowait()
        # If ai_response is a dict, get the text
        if isinstance(response, dict):
            reply = response.get('response_text', str(response))
        else:
            reply = str(response)
        return jsonify({"reply": reply, "should_listen": True})  # or False as needed
    except queue.Empty:
        return jsonify({"reply": None, "should_listen": False})

@app.route("/api/command", methods=["POST"])
def api_command():
    try:
        data = request.get_json()
        command = data.get("command", "").strip()
        if not command:
            return jsonify({"error": "No command provided"}), 400
        # Put the command in the queue for processing
        if "voice_command_queue" in globals():
            voice_command_queue.put(command)
        return jsonify({"reply": f"Command '{command}' received."})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/tts")
def tts():
    text = request.args.get("text", "")
    print(f"Received TTS request with text: {text}")
    if not text:
        return "No text provided", 400

    import tempfile
    import sounddevice as sd
    import soundfile as sf
    speaker_wav = r"C:\Users\Abdelrahman_Hatem\Desktop\Python Projects\JARVIS-mk.1\JARVIS-master\jarvis_sample.wav"

    if not os.path.isfile(speaker_wav):
        return jsonify({"error": f"Speaker WAV file '{speaker_wav}' not found."}), 500

    output_wav = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    output_wav.close()

    if coqui_tts_model is None:
        return jsonify({"error": "TTS model not loaded."}), 500

    coqui_tts_model.tts_to_file(
        text=text,
        speaker_wav=speaker_wav,  # <-- Use full path here
        language="en",
        file_path=output_wav.name
    )

    # Play the generated WAV file on the server (for testing)
    data, fs = sf.read(output_wav.name)
    sd.play(data, fs)
    sd.wait()

    return send_file(output_wav.name, mimetype="audio/wav")

@app.route("/api/tts_batch", methods=["POST"])
def tts_batch():
    try:
        data = request.get_json()
        replies = data.get("replies", [])

        if not isinstance(replies, list) or not replies:
            return jsonify({"error": "No replies provided."}), 400

        full_text = " ".join(replies)
        print(f"🗣️ Coqui will synthesize batch: {full_text}")

        import tempfile
        speaker_wav = r"C:\Users\Abdelrahman_Hatem\Desktop\Python Projects\JARVIS-mk.1\JARVIS-master\jarvis_sample.wav"  # <-- Use full path here

        if not os.path.isfile(speaker_wav):
            return jsonify({"error": f"Speaker WAV file '{speaker_wav}' not found."}), 500

        output_wav = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        output_wav.close()

        if coqui_tts_model is None:
            return jsonify({"error": "TTS model not loaded."}), 500

        coqui_tts_model.tts_to_file(
            text=full_text,
            language="en",
            speaker_wav=speaker_wav,  # <-- Use full path here
            file_path=output_wav.name
        )

        return send_file(output_wav.name, mimetype="audio/wav")

    except Exception as e:
        print("❌ TTS batch error:", e)
        return jsonify({"error": str(e)}), 500


@app.route("/api/should_listen", methods=["GET"])
def should_listen():
    return jsonify({"should_listen": True})


def run_ui():
    print("🚀 Flask UI is running at http://localhost:5000")
    app.run(host='0.0.0.0', debug=True, port=5000, use_reloader=False)


# === RUN APP ===
if __name__ == "__main__":
    print("🚀 Flask server is running at http://localhost:5000")
    app.run(debug=True)

