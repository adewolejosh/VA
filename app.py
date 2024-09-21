
import os
import whisper
import google.generativeai as genai

from flask import Flask, request, jsonify
from dotenv import load_dotenv


load_dotenv()


UPLOAD_FOLDER = "uploads/"
ALLOWED_EXTENSIONS = {"wav", "mp3", "ogg", "flac", "m4a"}


app = Flask(__name__)
app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

genai.configure(api_key=os.environ.get("GEMINI_API_KEY"))


if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/upload", methods=["POST"])
def upload_audio():
    files = request.files

    if "file" not in files:
        return jsonify({"error": "please upload an audio file"}), 400
    
    audio = request.files.get("file", "")

    if audio == "" or audio.filename == "":
        return jsonify({"error": "please select a valid file"}), 400

    if audio and allowed_file(audio.filename):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], audio.filename)
        audio.save(filepath)

        model = whisper.load_model("tiny")
        prompt = model.transcribe(filepath).get("text", "")
        return jsonify({"transcription": f"{prompt}"}), 200
    
    return jsonify({"error": "can't process your request please try again later"}), 404


@app.route("/reply", methods=["POST"])
def transcribe():
    data = request.json

    if data is None or not "text" in data:
        return jsonify({"error": f"input the transcribed text"}), 400
    
    prompt = data["text"]
    ai_model = genai.GenerativeModel("gemini-1.5-flash")
    response = ai_model.generate_content(str(prompt))
    return jsonify({"response": f"{response.text}"}), 200


if __name__ == "__main__":
    app.run(debug=True)
