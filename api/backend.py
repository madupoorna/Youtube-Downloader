import os, re
from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse, FileResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from yt_dlp import YoutubeDL

# Base directory for file paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

app = FastAPI()

# Mount public folder
app.mount("/public", StaticFiles(directory=os.path.join(BASE_DIR, "../public"), html=True), name="public")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # or specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Home page
@app.get("/")
def home():
    return RedirectResponse("/public/downloader.html")

# Download folder
DOWNLOAD_FOLDER = os.path.join(BASE_DIR, "downloads")
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

# Helper to fetch video info
def get_video_info(url: str):
    ydl_opts = {}
    with YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)
    return info

# Info endpoint
@app.get("/info")
def info(url: str = Query(..., description="YouTube video URL")):
    print("asd")
    try:
        url = url.strip()
        if not url.startswith("http"):
            url = "https://" + url

        info = get_video_info(url)
        formats = {}

        def to_int(val):
            if not val:
                return 0
            return int(re.sub(r'\D','', str(val)))

        def size_mb(f):
            size = f.get('filesize') or f.get('filesize_approx')
            if not size:
                return None
            return round(size / (1024*1024), 2)

        # Keep best encoding and remove duplicates
        for f in info['formats']:
            ext = f.get('ext')
            if ext not in ['mp4', 'webm', 'm4a', 'mp3']:
                continue

            ftype = 'audio' if f.get('acodec') != 'none' and f.get('vcodec') == 'none' else 'video'
            key = f"{f.get('resolution') if ftype=='video' else f.get('abr')}_{ftype}"

            if key in formats:
                existing = formats[key]
                if ftype == 'video':
                    if (f.get('fps') or 0) > (existing.get('fps') or 0):
                        formats[key] = f
                else:
                    if (f.get('abr') or 0) > (existing.get('abr') or 0):
                        formats[key] = f
            else:
                formats[key] = f

        final_formats = []
        for f in formats.values():
            ftype = 'audio' if f.get('acodec') != 'none' and f.get('vcodec') == 'none' else 'video'
            final_formats.append({
                'format_id': f['format_id'],
                'ext': f.get('ext'),
                'resolution': f.get('resolution') or '',
                'fps': f.get('fps') or '',
                'abr': f.get('abr') or '',
                'type': ftype,
                'size_mb': size_mb(f)
            })

        # Sort
        video_formats = sorted([f for f in final_formats if f['type']=='video'], key=lambda x: to_int(x['resolution']), reverse=True)
        audio_formats = sorted([f for f in final_formats if f['type']=='audio'], key=lambda x: to_int(x['abr']), reverse=True)
        all_formats = video_formats + audio_formats

        return {
            'title': info.get('title'),
            'author': info.get('uploader'),
            'length': info.get('duration'),
            'thumbnail': info.get('thumbnail'),
            'formats': all_formats
        }

    except Exception as e:
        print("❌ YouTube fetch error:", e)
        return JSONResponse(content={"error": str(e)}, status_code=400)

# Download endpoint
@app.get("/download")
def download(url: str = Query(...), format_id: str = Query(...)):
    try:
        url = url.strip()
        if not url.startswith("http"):
            url = "https://" + url

        info = get_video_info(url)
        filename = re.sub(r'[\\/*?:"<>|]', "", info['title'])
        outtmpl = os.path.join(DOWNLOAD_FOLDER, filename + ".%(ext)s")

        ydl_opts = {
            'format': format_id,
            'outtmpl': outtmpl
        }

        with YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        # Return downloaded file
        for ext in ['mp4','webm','m4a','mp3']:
            file_path = os.path.join(DOWNLOAD_FOLDER, f"{filename}.{ext}")
            if os.path.exists(file_path):
                return FileResponse(file_path, filename=os.path.basename(file_path))

        return JSONResponse(content={"error": "Download failed"}, status_code=500)

    except Exception as e:
        print("❌ Download error:", e)
        return JSONResponse(content={"error": str(e)}, status_code=400)

# if __name__ == "__main__": 
#    import uvicorn 
#    uvicorn.run("backend:app", host="127.0.0.1", port=8000, reload=True)
