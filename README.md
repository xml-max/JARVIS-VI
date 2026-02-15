# J.A.R.V.I.S-VI
## <span style="color:red">DISCLAIMER</span>

This is a **fan-made project** created for **educational and non-commercial purposes**.
It is **not** affiliated with, endorsed by, or connected to any official entity, product, or service.
All trademarks and copyrights belong to their respective owners.
The user interface of this project is built using **PyQt5**.

An advanced personal AI assistant featuring:

* **PyQt5-based Desktop UI** for seamless interaction
* **Whisper** for offline speech recognition
* **Coqui TTS** for natural-sounding text-to-speech
* **PyTorch** for AI model processing
* Fully **offline** operation for maximum privacy

---

## ⚙️ Modes

J.A.R.V.I.S-VI supports **two modes**:

| Mode    | Engine                       | Internet Required | Recommended For                        |
| ------- | ---------------------------- | ----------------- | -------------------------------------- |
| Offline | Ollama + Whisper + Coqui TTS | ❌ No              | Maximum privacy, offline usage         |
| Online  | OpenAI / Vertex AI           | ✅ Yes             | Cloud-based AI models, larger datasets |

> You can switch modes in `Jarvis/config.py` by enabling/disabling the flags:
>
> ```python
> ollama = True   # Offline AI engine
> openai = False  # Online AI engine
> vertexai = False
> ```

---

## 📦 Installation

0. **Download Ollama and install the models**

   [Ollama Download](https://ollama.com/download)

   ```bash
   ollama pull llama3.2-vision
   ollama pull nomic-embed-text
   ```

1. **Clone this repository:**

   ```bash
   git clone https://github.com/xml-max/JARVIS-VI.git
   cd JARVIS-VI
   ```

2. **Create a virtual environment:**

   ```bash
   python -m venv venv
   # Activate on Linux/Mac
   source venv/bin/activate
   # Activate on Windows
   venv\Scripts\activate
   ```

3. **Install dependencies:**

   ```bash
   pip install -r requirements.txt
   ```

---

## ⚙️ Configuration

Before running the assistant, configure your credentials and API keys in `Jarvis/config.py`:

```python
# Email credentials (optional)
email = ""
email_password = ""

# API keys
wolframalpha_id = ""
weather_api_key = ""
openai_api_key = ""

# AI service flags
ollama = True    # Offline mode
openai = False   # Online mode
vertexai = False # Online mode

# Google Cloud (optional)
google_project_id = ""
google_creds_path = ""

# Speech engines
SR_ENGINE = "whisper"  # Options: "whisper" or "google"
TTS_ENGINE = "Coqui"   # Options: "Coqui", "Heavy", or leave empty
```

> **Tip:** For security, you can also set these as environment variables instead of hardcoding them.

---

## 🚀 Usage

Run the assistant:

```bash
python main.py
```

---

## 🔧 Features

* **Two Operation Modes:** Offline or Online
* **Real-time Speech Recognition** – Powered by Whisper
* **Natural TTS** – Using Coqui TTS for lifelike voices
* **PyQt5 Desktop Interface** – Modern and interactive
* **Offline Mode** – No internet required after setup

---

## 📝 License

This project is licensed under a custom [MIT License](https://github.com/xml-max/JARVIS-VI/blob/main/LICENSE)

---

## 👥 Credits

* **Abdelrahman Hatem (xml-max)** - Project Author

---

## 🛠️ Support

For issues or feature requests, please open a ticket in the [Issues](../../issues) section.
