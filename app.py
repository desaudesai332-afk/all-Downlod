import os
from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import yt_dlp

app = Flask(__name__)
CORS(app)

DOWNLOAD_DIR = os.path.join(os.getcwd(), "downloads")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

@app.route("/")
def home():
    return send_file("index.html")

@app.route("/api/download", methods=["POST"])
def download():
    data = request.json or {}
    url = data.get("url")
    if not url:
        return jsonify({"error": "URL ज़रूरी है"}), 400

    output_path = os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s")
    ydl_opts = {
        "format": "best",
        "outtmpl": output_path,
        "quiet": True
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            return send_file(filename, as_attachment=True)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    print("वेबसाइट चालू है: http://127.0.0.1:5000")
    app.run(port=5000, debug=True)