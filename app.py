import os
import streamlit as st
from yt_dlp import YoutubeDL

# ---------------------- Setup ----------------------
st.set_page_config(page_title="🎬 Universal Downloader", layout="centered")

OUT_DIR = "downloads"
os.makedirs(OUT_DIR, exist_ok=True)

st.title("🎬 Universal Video & Audio Downloader")
st.caption("Download from TikTok, YouTube, Instagram & more.")

# ---------------------- Sidebar Menu ----------------------
menu = st.sidebar.radio(
    "📂 Select Option",
    [
        "🏠 Home",
        "🎞️ Download from Custom Link (MP4)",
        "🎵 Download Audio Only (MP3)",
        "🎵 Download TikTok Account Videos",
        "📸 Download Instagram Account Videos",
        "⚙️ Set Instagram Cookie",
        "🌐 Explore My Projects"
    ]
)

INSTAGRAM_COOKIE = st.session_state.get("INSTAGRAM_COOKIE", "")

# ---------------------- Helper: Downloader ----------------------
def download_media(url, audio_only=False, out_dir=OUT_DIR, cookie=None):
    if not url:
        st.warning("⚠️ Please enter a valid link first.")
        return

    st.info("⏳ Downloading... Please wait.")
    try:
        if audio_only:
            ydl_opts = {
                "outtmpl": os.path.join(out_dir, "%(title).100s.%(ext)s"),
                "format": "bestaudio/best",
                "quiet": True,
                "postprocessors": [{
                    "key": "FFmpegExtractAudio",
                    "preferredcodec": "mp3",
                    "preferredquality": "192",
                }],
            }
        else:
            ydl_opts = {
                "outtmpl": os.path.join(out_dir, "%(title).100s.%(ext)s"),
                "format": "best",
                "quiet": True,
                "merge_output_format": "mp4",
            }

        if cookie:
            ydl_opts["cookiefile"] = cookie

        with YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        st.success("✅ Download completed!")
        with open(filename, "rb") as f:
            st.download_button(
                label="⬇️ Download File",
                data=f,
                file_name=os.path.basename(filename),
                mime="audio/mpeg" if audio_only else "video/mp4",
            )

    except Exception as e:
        st.error(f"❌ Error: {e}")


# ---------------------- TikTok account videos ----------------------
def download_tiktok_account(username):
    if not username:
        st.warning("⚠️ Enter a valid TikTok username.")
        return

    username = username.lstrip("@")
    playlist_url = f"https://www.tiktok.com/@{username}"
    st.info(f"Fetching videos from @{username} ...")

    try:
        ydl_opts = {
            "outtmpl": os.path.join(OUT_DIR, f"{username}_%(id)s.%(ext)s"),
            "format": "best",
            "quiet": True,
            "merge_output_format": "mp4",
        }
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([playlist_url])

        st.success(f"✅ All available videos from @{username} downloaded.")
    except Exception as e:
        st.error(f"❌ Failed: {e}")


# ---------------------- Instagram account videos ----------------------
def download_instagram_account(username, cookie_string):
    if not username:
        st.warning("⚠️ Enter a valid Instagram username.")
        return
    if not cookie_string:
        st.warning("⚠️ Please set Instagram cookie first.")
        return

    username = username.lstrip("@")
    profile_url = f"https://www.instagram.com/{username}/"

    # Save cookie to a temporary file
    cookie_file = "ig_cookie.txt"
    with open(cookie_file, "w") as f:
        f.write(cookie_string)

    st.info(f"Downloading all videos from @{username}...")

    try:
        ydl_opts = {
            "outtmpl": os.path.join(OUT_DIR, f"instagram_{username}_%(id)s.%(ext)s"),
            "format": "best",
            "quiet": True,
            "ignoreerrors": True,
            "merge_output_format": "mp4",
            "cookiefile": cookie_file,
        }
        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([profile_url])

        st.success(f"✅ Done! Videos saved in '{OUT_DIR}' folder.")
    except Exception as e:
        st.error(f"❌ Failed: {e}")


# ---------------------- Pages ----------------------

if menu == "🏠 Home":
    st.markdown("""
    ### 👋 Welcome!
    This is a **Universal Downloader** powered by `yt-dlp` and `Streamlit`.  
    - 🎞️ Download any video in MP4  
    - 🎵 Extract MP3 audio  
    - 📸 Download all videos from TikTok or Instagram accounts  
    - ⚙️ Save files directly from your browser  
    ---
    """)

elif menu == "🎞️ Download from Custom Link (MP4)":
    url = st.text_input("🎥 Paste any video link:")
    if st.button("Download Video"):
        download_media(url, audio_only=False)

elif menu == "🎵 Download Audio Only (MP3)":
    url = st.text_input("🎧 Paste any link to extract MP3:")
    if st.button("Download Audio"):
        download_media(url, audio_only=True)

elif menu == "🎵 Download TikTok Account Videos":
    username = st.text_input("Enter TikTok username (without @):")
    if st.button("Download TikTok Videos"):
        download_tiktok_account(username)

elif menu == "📸 Download Instagram Account Videos":
    username = st.text_input("Enter Instagram username (without @):")
    if st.button("Download Instagram Videos"):
        download_instagram_account(username, INSTAGRAM_COOKIE)

elif menu == "⚙️ Set Instagram Cookie":
    cookie = st.text_area("Paste your full Instagram cookie string:")
    if st.button("Save Cookie"):
        st.session_state["INSTAGRAM_COOKIE"] = cookie
        st.success("✅ Cookie saved successfully in session.")

elif menu == "🌐 Explore My Projects":
    st.markdown("""
    - 💖 [Love Games](https://love-games.netlify.app)
    - 🎬 [Watch Party](https://watch-party-yt.netlify.app)
    """)
