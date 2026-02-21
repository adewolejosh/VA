# Voice Assistant API

A Flask-based REST API for speech transcription and AI-powered conversational responses. Accepts audio uploads, transcribes them using OpenAI Whisper, and generates intelligent replies via Google Gemini. ~was essentially supposed to be a THA, but seemed like a WRF~

## Architecture

The application exposes two primary endpoints:

- `POST /upload` - Accepts audio files and returns transcribed text
- `POST /reply` - Accepts text input and returns AI-generated responses

Audio processing is handled by Whisper's tiny model for optimal speed-accuracy tradeoff. AI responses are generated using Gemini 1.5 Flash for low-latency conversational interactions.

## Requirements

Python 3.9 or higher is required due to Whisper dependencies. Lower versions will fail during model loading.

System dependencies:

- ffmpeg (required by Whisper for audio processing)

Python packages:

- flask
- openai-whisper
- google-generativeai
- python-dotenv

## Installation

Install ffmpeg through your system package manager:

```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt install ffmpeg

# Windows
# Download from https://ffmpeg.org/download.html
```

Install Python dependencies:

```bash
pip install flask openai-whisper google-generativeai python-dotenv
```

## Configuration

Create a `.env` file in the project root:

```
SECRET_KEY=your_flask_secret_key
GEMINI_API_KEY=your_google_gemini_api_key
```

Obtain a Gemini API key from Google AI Studio at https://makersuite.google.com/app/apikey

## Usage

Start the development server:

```bash
flask run --debug
```

The API will be available at `http://localhost:5000`

### Transcribe Audio

```bash
curl -X POST http://localhost:5000/upload \
  -F "file=@recording.mp3"
```

Supported formats: WAV, MP3, OGG, FLAC, M4A

Response:

```json
{
  "transcription": "transcribed text from audio"
}
```

### Generate AI Response

```bash
curl -X POST http://localhost:5000/reply \
  -H "Content-Type: application/json" \
  -d '{"text": "your transcribed text here"}'
```

Response:

```json
{
  "response": "AI-generated reply to your input"
}
```

## File Structure

```
.
├── src/
│   └── app.py          # Main application entry point
├── uploads/            # Temporary audio file storage
├── .env                # Environment configuration
└── README.md
```

Uploaded audio files are stored temporarily in the `uploads/` directory. The directory is created automatically on first run if it does not exist.

## Production Considerations

This implementation is suitable for development and prototyping. Production deployment requires:

Authentication and authorization layer to restrict API access and track usage per user.

Persistent conversation storage to maintain context across multiple interactions. Requires database integration for message history and session management.

Context switching capabilities to allow users to reference and continue previous conversations. Implement conversation threading with unique session identifiers.

Model fine-tuning using accumulated conversation data to improve response quality for specific use cases and user patterns.

File cleanup mechanism to prevent disk exhaustion from accumulated audio uploads. Implement scheduled deletion or post-processing cleanup.

Rate limiting to prevent API abuse and manage compute costs for transcription and AI inference.

HTTPS termination and proper CORS configuration for web client integration.

Horizontal scaling strategy as Whisper model loading and inference are CPU-intensive operations.

## Extension Ideas

Customer support integration: Embed this API into web applications as an interactive help desk. Ingest page content into the AI context window, enabling users to ask questions about documentation via voice input. Combine with text-to-speech synthesis for complete voice-driven support experiences.

Multi-language support: Whisper supports 99 languages natively. Extend the API to detect input language and provide multilingual AI responses.

Real-time streaming: Replace batch processing with WebSocket connections for live transcription and conversational experiences.

Custom model training: Fine-tune Gemini responses on domain-specific datasets for specialized assistant behaviors.

Voice cloning: Integrate text-to-speech with voice synthesis to create personalized AI assistant voices.

## Limitations

The tiny Whisper model prioritizes speed over accuracy. For higher transcription quality, replace with `base`, `small`, `medium`, or `large` models at the cost of increased latency and memory usage.

Gemini 1.5 Flash has no conversation memory between requests. Each `/reply` call is stateless. Implementing conversation history requires manual context management in request payloads.

Audio files are stored on disk without automatic cleanup. Long-running instances will accumulate files and exhaust storage.

No input validation beyond file extension checking. Malicious files could potentially exploit ffmpeg vulnerabilities.

API has no authentication. Any client with network access can consume compute resources.
