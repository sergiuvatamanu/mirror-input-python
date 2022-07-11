#!/usr/bin/env python3
import socket
import queue
from pynput import mouse, keyboard
import json
import sys

class InputMonitor:
    def __init__(self) -> None:
        self.queue = queue.Queue()

        self.keyboard_listener = keyboard.Listener(
        on_press=self.on_press,
        on_release=self.on_release)

        self.mouse_listener = mouse.Listener(
        on_move=self.on_move,
        on_click=self.on_click,
        on_scroll=self.on_scroll)

    def on_move(self, x, y):
        msg = json.dumps({'t': 'm_m', 'xy': (x,y)})
        self.queue.put(msg)

    def on_click(self, x, y, button, pressed):
        msg = json.dumps({'t':'m_c', 'b': button.name, 'xy':(x,y), 'p': pressed})
        self.queue.put(msg)

    def on_scroll(self, x, y, dx, dy):
        msg = json.dumps({'t':'m_s', 'val':dy})
        self.queue.put(msg)

    def on_press(self, key):
        key_type = ""
        if type(key) is keyboard.Key:
            key_type = "k" # is key
            key_val = key.name
        elif type(key) is keyboard.KeyCode:
            key_type = "c" # is character
            key_val = key.char
        msg = json.dumps({'t': 'k_p', 'kt': key_type, 'val': key_val})
        self.queue.put(msg)

    def on_release(self, key):
        key_type = ""
        if type(key) is keyboard.Key:
            key_type = "k" # is key
            key_val = key.name
        elif type(key) is keyboard.KeyCode:
            key_type = "c" # is code
            key_val = key.char
        msg = json.dumps({'t': 'k_r', 'kt': key_type, 'val': key_val})
        self.queue.put(msg)

    def start(self):
        self.mouse_listener.start()
        self.keyboard_listener.start()

HOST = 'IP addr'
PORT = 50001

input_monitor = InputMonitor()
input_monitor.start()

while True:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        item = input_monitor.queue.get()
        s.connect((HOST, PORT))
        s.sendall(len(item).to_bytes(4, 'big')+bytes(item, 'utf8'))
        s.close()
        input_monitor.queue.task_done()
