#!/usr/bin/env python3
from platform import release
import socket
import json

HOST = ''                 # Symbolic name meaning all available interfaces
PORT = 50007              # Arbitrary non-privileged port

from pynput import mouse, keyboard

mouse_ctrl = mouse.Controller()
kb_ctrl = keyboard.Controller()

def perform_action(json_msg):
    t = json_msg["t"]
    if t == "m_m":
        mouse_ctrl.move(json_msg["xy"][0], json_msg["xy"][1])
    elif t == "m_c":
        b = json_msg["b"]

        if(json_msg["p"]):
            mouse_ctrl.press(mouse.Button[b])
        else:
            mouse_ctrl.release(mouse.Button[b])
    elif t == "m_s":
        mouse_ctrl.scroll(0, json_msg["val"])
    elif t.startswith("k"):
        kt = json_msg["kt"]
        kv = json_msg["val"]

        key = None

        if kt == "c":
            key = keyboard.KeyCode.from_char(kv)
        else:
            key = keyboard.Key[kv]
        
        if t == "k_p":
            kb_ctrl.press(key)
        else:
            kb_ctrl.release(key)


print(f"{socket.gethostbyname(socket.gethostname())}:{PORT} listening...")

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    s.bind((HOST, PORT))
    s.listen(1)

    while True:
        conn, addr = s.accept()
        with conn:
            size = int.from_bytes(conn.recv(4), 'big')
            msg = conn.recv(size)
            perform_action(json.loads(msg))
