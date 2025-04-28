from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import lseg.data as ld
import os
import asyncio
import json
from typing import List
from pydantic import BaseModel
import datetime
import logging
from logging.handlers import RotatingFileHandler

# 配置日志
logger = logging.getLogger('lseg-data')
logger.setLevel(logging.INFO)
handler = RotatingFileHandler(
    'lseg-data-lib.log',
    maxBytes=10*1024*1024,  # 10MB
    backupCount=5  # 保留 5 个备份
)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

app = FastAPI()

# 挂载静态文件目录
app.mount("/static", StaticFiles(directory="static"), name="static")

# 配置 CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

currency_pairs = []
class CurrencyPairs(BaseModel):
    pairs: List[str]

config_path = os.path.join(os.getcwd(), "lseg-data.config.json")
ld.open_session(config_name=config_path)
pricing_stream = None
latest_data = {}

@app.post("/submit_pairs")
async def submit_pairs(pairs: CurrencyPairs):
    global currency_pairs, pricing_stream, latest_data
    # 清空旧数据
    latest_data.clear()
    logger.info("清空 latest_data")
    
    # 更新货币对
    currency_pairs = [p.strip() for p in pairs.pairs if p.strip()][:10]
    
    # 关闭旧数据流
    if pricing_stream:
        pricing_stream.close()
        logger.info("关闭旧数据流")
    
    # 创建新数据流
    pricing_stream = ld.content.pricing.Definition(
        universe=currency_pairs,
        fields=["BID", "ASK", "TIMACT"]
    ).get_stream()

    def on_refresh(fields, instrument_name, stream):
        timestamp = datetime.datetime.now().isoformat()
        latest_data[instrument_name] = {
            "BID": fields.get("BID"),
            "ASK": fields.get("ASK"),
            "TIMACT": fields.get("TIMACT"),
            "timestamp": timestamp
        }

    def on_update(fields, instrument_name, stream):
        timestamp = datetime.datetime.now().isoformat()
        latest_data[instrument_name] = {
            "BID": fields.get("BID"),
            "ASK": fields.get("ASK"),
            "TIMACT": fields.get("TIMACT"),
            "timestamp": timestamp
        }

    pricing_stream.on_refresh(on_refresh)
    pricing_stream.on_update(on_update)
    logger.info(f"打开数据流: {currency_pairs}")
    pricing_stream.open()
    return {"status": "success", "pairs": currency_pairs}

@app.websocket("/ws/data")
async def websocket_endpoint(websocket: WebSocket):
    client_ip = websocket.client.host
    logger.info(f"WebSocket 连接请求 - 客户端: {client_ip}")
    try:
        await websocket.accept()
        logger.info(f"WebSocket 连接建立 - 客户端: {client_ip}")
        while True:
            await websocket.send_json(latest_data)
            await asyncio.sleep(1)
    except Exception as e:
        logger.error(f"WebSocket 错误: {e} - 客户端: {client_ip}")
    finally:
        await websocket.close()
        logger.info(f"WebSocket 关闭 - 客户端: {client_ip}")

@app.get("/input", response_class=HTMLResponse)
async def get_input_page():
    with open("input.html") as f:
        return HTMLResponse(content=f.read())

@app.get("/display", response_class=HTMLResponse)
async def get_display_page():
    with open("display.html") as f:
        return HTMLResponse(content=f.read())

@app.get("/test", response_class=HTMLResponse)
async def get_test_page():
    with open("test.html") as f:
        return HTMLResponse(content=f.read())

@app.get("/display_http", response_class=HTMLResponse)
async def get_display_http_page():
    with open("display_http.html") as f:
        return HTMLResponse(content=f.read())

@app.get("/data")
async def get_data():
    logger.info("HTTP 数据请求")
    return latest_data

@app.on_event("shutdown")
async def shutdown_event():
    logger.info("关闭数据流和会话...")
    if pricing_stream:
        pricing_stream.close()
    ld.close_session()
    logger.info("会话已关闭。")
