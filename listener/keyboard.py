#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
@Time        : 2024/11/15 1:09
@Author      : SiYuan
@Email       : 863909694@qq.com
@File        : TraceBoard-keyboard.py
@Description :
"""
import requests
from pynput.keyboard import Key
from pynput import keyboard
import datetime

# 用于追踪已按下的键
pressed_keys = set()

# pynput 键名到 Windows 虚拟键码的映射
# 这些值与 HTML/JavaScript 中的 keyCode 保持一致
KEY_CODE_MAP = {
    # 功能键
    'esc': 27,
    'f1': 112, 'f2': 113, 'f3': 114, 'f4': 115,
    'f5': 116, 'f6': 117, 'f7': 118, 'f8': 119,
    'f9': 120, 'f10': 121, 'f11': 122, 'f12': 123,
    # 控制键
    'tab': 9,
    'caps_lock': 20,
    'shift': 16, 'shift_l': 160, 'shift_r': 161,
    'ctrl': 17, 'ctrl_l': 162, 'ctrl_r': 163,
    'alt': 18, 'alt_l': 164, 'alt_r': 165,
    'cmd': 91,  # Windows 键
    'space': 32,
    'enter': 13,
    'backspace': 8,
    # 导航键
    'insert': 45,
    'delete': 46,
    'home': 36,
    'end': 35,
    'page_up': 33,
    'page_down': 34,
    'up': 38,
    'down': 40,
    'left': 37,
    'right': 39,
    'print_screen': 44,
    'scroll_lock': 145,
    'pause': 19,
    # 数字小键盘
    'num_lock': 144,
    'divide': 111,
    'multiply': 106,
    'subtract': 109,
    'add': 107,
    'decimal': 110,
    'numpad0': 96, 'numpad1': 97, 'numpad2': 98, 'numpad3': 99,
    'numpad4': 100, 'numpad5': 101, 'numpad6': 102,
    'numpad7': 103, 'numpad8': 104, 'numpad9': 105,
    'numpad_enter': 13,
}

# 字符到虚拟键码的映射（基于 ASCII 和标准 Windows 键码）
CHAR_CODE_MAP = {
    # 数字行
    '`': 192, '~': 192,
    '1': 49, '!': 49,
    '2': 50, '@': 50,
    '3': 51, '#': 51,
    '4': 52, '$': 52,
    '5': 53, '%': 53,
    '6': 54, '^': 54,
    '7': 55, '&': 55,
    '8': 56, '*': 56,
    '9': 57, '(': 57,
    '0': 48, ')': 48,
    '-': 189, '_': 189,
    '=': 187, '+': 187,
    # 字母键（小写）
    'a': 65, 'b': 66, 'c': 67, 'd': 68, 'e': 69, 'f': 70,
    'g': 71, 'h': 72, 'i': 73, 'j': 74, 'k': 75, 'l': 76,
    'm': 77, 'n': 78, 'o': 79, 'p': 80, 'q': 81, 'r': 82,
    's': 83, 't': 84, 'u': 85, 'v': 86, 'w': 87, 'x': 88,
    'y': 89, 'z': 90,
    # 字母键（大写）
    'A': 65, 'B': 66, 'C': 67, 'D': 68, 'E': 69, 'F': 70,
    'G': 71, 'H': 72, 'I': 73, 'J': 74, 'K': 75, 'L': 76,
    'M': 77, 'N': 78, 'O': 79, 'P': 80, 'Q': 81, 'R': 82,
    'S': 83, 'T': 84, 'U': 85, 'V': 86, 'W': 87, 'X': 88,
    'Y': 89, 'Z': 90,
    # 符号键
    '[': 219, '{': 219,
    ']': 221, '}': 221,
    '\\': 220, '|': 220,
    ';': 186, ':': 186,
    "'": 222, '"': 222,
    ',': 188, '<': 188,
    '.': 190, '>': 190,
    '/': 191, '?': 191,
}


def get_virtual_key_code(key):
    """
    将 pynput 的键转换为标准的 Windows 虚拟键码
    这个键码与 HTML/JavaScript 的 keyCode 保持一致
    """
    if isinstance(key, Key):
        # 特殊键
        key_name = key.name.lower()
        # 处理左右区分的修饰键
        if key_name in ('shift', 'shift_l', 'shift_r'):
            return KEY_CODE_MAP.get('shift_l' if key_name == 'shift_l' else 'shift_r' if key_name == 'shift_r' else 'shift_l', 160)
        elif key_name in ('ctrl', 'ctrl_l', 'ctrl_r'):
            return KEY_CODE_MAP.get('ctrl_l' if key_name == 'ctrl_l' else 'ctrl_r' if key_name == 'ctrl_r' else 'ctrl_l', 162)
        elif key_name in ('alt', 'alt_l', 'alt_r'):
            return KEY_CODE_MAP.get('alt_l' if key_name == 'alt_l' else 'alt_r' if key_name == 'alt_r' else 'alt_l', 164)
        return KEY_CODE_MAP.get(key_name, key.value.vk)
    else:
        # 字符键
        char = key.char
        if char in CHAR_CODE_MAP:
            return CHAR_CODE_MAP[char]
        # 回退到 pynput 的 vk（可能不准确）
        return key.vk


# 插入按键信息到数据库
def insert_key_event(key_name: str, virtual_key_code: int):
    # 获取当前时间戳
    timestamp = datetime.datetime.now()
    print(key_name, virtual_key_code)
    # API URL
    url = "http://127.0.0.1:21315/key_events"

    # 要发送的数据
    data = {
        "key_name": key_name,  # 按键名称
        "virtual_key_code": virtual_key_code  # 虚拟按键码
    }

    # 发送 POST 请求
    response = requests.post(url, json=data)

    # 打印响应内容
    if response.status_code == 200:
        print("请求成功！响应数据:")
        print(response.json())  # 打印响应 JSON 数据
    else:
        print(f"请求失败! 状态码: {response.status_code}")
        print(response.text)


# 键盘按下事件处理函数
def on_press(key):
    try:
        # 获取标准化的虚拟键码
        vk = get_virtual_key_code(key)

        # 获取按键名称
        if isinstance(key, Key):
            key_name = key.name  # 特殊按键的名称（如 shift, ctrl, enter 等）
        else:
            key_name = key.char  # 普通字符按键的名称

        # 只在按键没有被记录时记录它
        if vk not in pressed_keys:
            insert_key_event(key_name, vk)
            pressed_keys.add(vk)  # 记录按下的按键
    except Exception as e:
        print(f"Error: {e}")


# 键盘释放事件处理函数
def on_release(key):
    try:
        # 使用相同的函数获取标准化的虚拟键码
        vk = get_virtual_key_code(key)
        # 按键释放时移除按键
        if vk in pressed_keys:
            pressed_keys.remove(vk)
    except Exception as e:
        print(f"Error: {e}")


def start_listener():
    with keyboard.Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()


if __name__ == '__main__':
    start_listener()
