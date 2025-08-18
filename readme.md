\# YouTube Downloader



A simple \*\*YouTube video/audio downloader\*\* built with \*\*FastAPI\*\* (backend) and \*\*TailwindCSS\*\* (frontend). Supports selecting video/audio formats, shows file sizes, and displays video thumbnails.



---



\## Features



\* Fetch YouTube video info (title, author, thumbnail, formats)

\* Display \*\*video/audio formats\*\* with resolution, FPS/bitrate, and file size in MB

\* \*\*Download\*\* selected format

\* Loading spinner while fetching info

\* Handles unknown file sizes gracefully

\* Static frontend built with \*\*TailwindCSS\*\*

\* Backend powered by \*\*FastAPI\*\* and \*\*yt-dlp\*\*



---



\## Folder Structure



```

project/

├── backend.py            # FastAPI backend

├── static/

│   └── downloader.html   # Frontend HTML

├── downloads/            # Folder for downloaded files

├── requirements.txt      # Python dependencies

└── README.md

```



---



\## Requirements



\* Python 3.10+

\* \[yt-dlp](https://github.com/yt-dlp/yt-dlp)

\* FastAPI

\* Uvicorn

\* TailwindCSS (via CDN in HTML)



---



\## Installation



1\. Clone the repository:



```bash

git clone https://github.com/yourusername/youtube-downloader.git

cd youtube-downloader

```



2\. Install dependencies:



```bash

pip install -r requirements.txt

```



3\. Create downloads folder:



```bash

mkdir downloads

```



---



\## Running Locally



```bash

uvicorn backend:app --reload

```



Open your browser at `http://127.0.0.1:8000/` to access the downloader.



---



\## Deployment on Vercel



1\. Install Vercel CLI:



```bash

npm i -g vercel

```



2\. Login:



```bash

vercel login

```



3\. Add `vercel.json` to your project:



```json

{

&nbsp; "version": 2,

&nbsp; "builds": \[

&nbsp;   { "src": "backend.py", "use": "@vercel/python" }

&nbsp; ],

&nbsp; "routes": \[

&nbsp;   { "src": "/(.\*)", "dest": "backend.py" }

&nbsp; ]

}

```



4\. Deploy:



```bash

vercel --prod

```



Vercel will automatically assign a URL for your app.



---



\## Usage



1\. Open the app in a browser.

2\. Paste a YouTube URL.

3\. Click \*\*Fetch\*\* to retrieve video info.

4\. Select the desired \*\*format\*\* (video/audio) from the dropdown.

5\. Click \*\*Download\*\*.



---



\## Notes



\* Some video/audio formats may show “unknown size” if `yt-dlp` cannot determine filesize.

\* Only formats with `mp4`, `webm`, `m4a`, or `mp3` extensions are displayed.

\* Adaptive streams (separate audio/video) may have missing FPS or size info.

\* \*\*This project is for educational purposes only. The author takes no liability for the usage of this software.\*\*



---



\## License



MIT License © 2025 Monarindu Madupoorna



