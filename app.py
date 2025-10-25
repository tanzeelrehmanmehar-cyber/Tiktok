from flask import Flask, render_template, request, send_from_directory, redirect, url_for, flash
import os
import yt_dlp
from datetime import datetime

app = Flask(__name__)
app.secret_key = "your-secret-key"

DOWNLOAD_FOLDER = os.path.join("static", "downloads")
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        url = request.form.get("url")
        if not url:
            flash("Please enter a TikTok URL or username.")
            return redirect(url_for("index"))

        try:
            ydl_opts = {
                "outtmpl": os.path.join(DOWNLOAD_FOLDER, "%(title)s.%(ext)s"),
                "quiet": True,
                "format": "mp4",
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                filename = os.path.basename(filename)

            download_url = url_for("download_file", filename=filename)
            return render_template("index.html", download_url=download_url, title=info.get("title"))

        except Exception as e:
            flash(f"Error: {str(e)}")
            return redirect(url_for("index"))

    return render_template("index.html")

@app.route("/download/<filename>")
def download_file(filename):
    return send_from_directory(DOWNLOAD_FOLDER, filename, as_attachment=True)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
