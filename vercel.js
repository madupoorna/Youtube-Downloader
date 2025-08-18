{
  "version": 2,
  "builds": [
    { "src": "api/backend.py", "use": "@vercel/python" }
  ],
  "routes": [
    { "src": "/", "dest": "/api/backend.py" },
    { "src": "/info", "dest": "/api/backend.py" },
    { "src": "/download", "dest": "/api/backend.py" }
  ]
}
