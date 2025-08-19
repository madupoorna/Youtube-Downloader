{
  "version": 2,
  "builds": [
    { "src": "api/backend.py", "use": "@vercel/python" },
    { "src": "public/**/*", "use": "@vercel/static" }
  ],
  "routes": [
    { "src": "/api/(.*)", "dest": "api/backend.py" },
    { "src": "/", "dest": "/public/downloader.html" },
    { "src": "/(.*)", "dest": "/public/$1" }
  ]
}
