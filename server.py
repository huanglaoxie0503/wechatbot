#!/usr/bin/python
# -*- coding:UTF-8 -*-
"""
# @Time    :    2024-08-29 14:21
# @Author  :   oscar
# @Desc    :   服务
"""
from fastapi import FastAPI, Form
from fastapi.responses import JSONResponse
import uvicorn
from loguru import logger

app = FastAPI()

# 配置 Loguru 日志
logger.add("logs/app.log", rotation="1 week", retention="1 month", level="INFO", format="{time} {level} {message}")


@app.post("/receive")
async def receive_message(
        type: str = Form(...),
        content: str = Form(...),
        source: str = Form(...),
        isMentioned: str = Form(...),
        isMsgFromSelf: str = Form(...),
):
    # 处理请求数据
    response_data = {
        "type": type,
        "content": content,
        "source": source,
        "isMentioned": isMentioned,
        "isMsgFromSelf": isMsgFromSelf,
    }
    try:
        # 填写处理逻辑-开始
        logger.info("Received data: {}", response_data)
        # 填写处理逻辑-结束
        return JSONResponse(content={"status": "success", "data": response_data})
    except Exception as e:
        logger.error("Error processing request: {}", e)
        return JSONResponse(content={"status": "error", "data": "处理失败"})


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=3000)
