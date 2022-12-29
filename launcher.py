from lib.bot import bot
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import uvicorn
import threading

app = FastAPI()

VERSION = "0.5.0"


@app.get("/api/embed/")
async def root(title: str = "Gccody", description: str = "Self bot created by Gccody", url: str = "https://gccody.com", color: str = "00ff00", image: str = "https://i.imgur.com/n5mioQi.jpg"):
    return HTMLResponse(content=f"""
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta http-equiv="X-UA-Compatible" content="IE=edge">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Gccody Self Bot</title>
  <meta property="og:type" content="website">
  <meta property="og:site_name" content="{title}">
  <meta name="title" content="{title}" property="og:title" />
  <meta name="description" content="{description}" property="og:description" />
  <meta name="url" content="{url}" property="og:url" />
  <meta name="image" content="{image}" property="og:image" />
  <meta content="#{color}" data-react-helmet="true" name="theme-color" />
</head>
<body>
  
</body>
</html>
    """)


if __name__ == "__main__":
    t = threading.Thread(target=bot.run, args=(VERSION,))
    t.start()

    uvicorn.run(app, host='0.0.0.0')
