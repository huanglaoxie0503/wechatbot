#!/usr/bin/python
# -*- coding:UTF-8 -*-
"""
# @Time    :    2024-08-29 10:58
# @Author  :   oscar
# @Desc    :   发送消息
"""
import requests
import json
import time

from typing import Union, List, Dict, Optional

from settings import BOT_URL, BOT_URL_FILE


def post_request_with_retries(url, headers, data, files=None, max_retries=3, timeout=10):
    """
    发送带有最大重试次数的 POST 请求。
    :param url: 服务器地址和路径
    :param headers: 请求头
    :param data: 请求的数据 (Python 字典)
    :param files: 文件内容
    :param max_retries: 最大重试次数，默认值为 3
    :param timeout: 请求超时时间（秒），默认值为 10 秒
    :return: 如果请求成功，返回响应对象；如果失败，返回 None
    """
    for attempt in range(max_retries):
        try:
            # 发送 POST 请求
            response = requests.post(url, headers=headers, data=data, files=files, timeout=timeout)

            # 检查响应状态码
            if response.status_code == 200:
                return response
            else:
                print(f"请求失败，状态码: {response.status_code}")
                if response.status_code == 502:
                    print("收到 502 错误，正在重试...")
                    time.sleep(5)  # 等待 5 秒后重试
                else:
                    break

        except requests.exceptions.RequestException as e:
            print("请求发生错误:", e)
            break

    return None  # 如果所有尝试都失败，返回 None


def create_request_data(to: str, data: Optional[Union[Dict, List]] = None, is_room: bool = False) -> Dict:
    """
    根据输入参数创建请求数据结构。

    :param to: 接收者，可以是个人昵称或群昵称
    :param data: 消息内容，可以是字典或列表。如果不存在或为 None，则不包含 data 字段
    :param is_room: 是否是群聊, 默认为 False
    :return: 封装好的请求数据字典
    """
    request_data = {"to": to}

    if data is not None:
        request_data["data"] = data

    if is_room:
        request_data["isRoom"] = True

    return request_data


def send_to_user(nick_name, data):
    """
    私聊
    :param nick_name: 昵称
    :param data: 消息内容
    :return:
    """
    # 请求头
    headers = {
        "Content-Type": "application/json",
    }
    data = create_request_data(nick_name, data)
    response = post_request_with_retries(url=BOT_URL, headers=headers, data=json.dumps(data))
    print(response.json())


def send_to_room(nick_name, data):
    """
    群聊
    :param nick_name: 群昵称
    :param data: 消息内容
    :return:
    """
    # 请求头
    headers = {
        "Content-Type": "application/json",
    }
    data = create_request_data(nick_name, data, is_room=True)
    response = post_request_with_retries(url=BOT_URL, headers=headers, data=data)
    print(response.json())


def send_to_rooms():
    """
    群发消息
    :return:
    """
    # 请求头
    headers = {
        "Content-Type": "application/json",
    }
    data = [
        {
            "to": "摩诘",
            "data": {
                "content": "你好👋"
            }
        },
        {
            "to": "杨",
            "data": [
                {
                    "content": "你好👋"
                },
                {
                    "content": "近况如何？测试群发机器人！"
                }
            ]
        }
    ]
    response = post_request_with_retries(url=BOT_URL, headers=headers, data=json.dumps(data))
    print(response.json())


def send_to_url(nick_name, content):
    # 给 url 拼接 query 参数 $alias 可用于指定发送给目标的文件名
    # 请求头
    headers = {
        "Content-Type": "application/json",
    }
    data = {
        "to": nick_name,
        "data": {
            "type": "fileUrl",
            "content": content
        }
    }
    response = post_request_with_retries(url=BOT_URL, headers=headers, data=json.dumps(data))
    print(response.json())


def send_to_local_file(nick_name, file_name, is_room=False):
    """
    发送本地文件
    :param nick_name: 昵称
    :param file_name: 文件路径
    :param is_room: 是否是群聊
    :return:
    """

    data = create_request_data(to=nick_name, is_room=is_room)

    files = {'content': open(file_name, 'rb')}
    # 因为 request 库中默认 ContentType: multipart/form-data类型，所以无需手动添加 headers。
    response = post_request_with_retries(url=BOT_URL_FILE, headers=None, data=data, files=files)
    print(response.json())


def run():
    # 单条消息
    data = {
        "content": "爬虫与AI前沿"
    }
    # 多条消息
    datas = [
        {
            "type": "text",
            "content": "你好👋"
        },
        {
            "type": "fileUrl",
            "content": "https://static.cninfo.com.cn/finalpage/2024-08-29/1221034055.PDF"
        }
    ]
    # send_to_user(nick_name='摩诘', data=datas)
    #
    # send_to_room(nick_name='6固戍中队防诈骗宣传群', data=data)

    # 给多人群发
    send_to_rooms()

    # # 发文件 url 同时支持修改成目标文件名
    # url_type = "https://download.samplelib.com/jpeg/sample-clouds-400x300.jpg?$alias=1234.jpg"
    # send_to_url(nick_name='摩诘', content=url_type)
    #
    # # 发送本地文件-私聊
    # file_path = '/Users/oscar/Downloads/dify.png'
    # send_to_local_file(nick_name='摩诘', file_name=file_path)


if __name__ == '__main__':
    run()
