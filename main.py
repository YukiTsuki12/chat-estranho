from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.staticfiles import StaticFiles
import redis
import json
import asyncio

app = FastAPI()

redis_client = redis.StrictRedis(host='localhost', port=6379, db=0, decode_responses=True)

connected_clients = []

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
async def get():
    with open("static/index.html", encoding='utf-8') as f:
        return HTMLResponse(content=f.read(), status_code=200)

@app.get("/style.css")
async def get_style():
    return FileResponse("static/style.css", media_type="text/css")

@app.websocket("/ws/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    await websocket.accept()
    connected_clients.append(websocket)
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            redis_client.publish("chat_channel", json.dumps({
                "esquisito": client_id,
                "enviado": message["message"]
            }))
    except WebSocketDisconnect:
        connected_clients.remove(websocket)
        await websocket.close()

async def broadcast_message(message):
    for websocket in connected_clients:
        await websocket.send_text(message)

@app.on_event("startup")
async def startup():
    asyncio.create_task(subscribe_to_redis())

async def subscribe_to_redis():
    pubsub = redis_client.pubsub()
    pubsub.subscribe("chat_channel")
    while True:
        message = pubsub.get_message()
        if message and message["type"] == "message":
            await broadcast_message(message["data"])
        await asyncio.sleep(0.01)
