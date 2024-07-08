import asyncio
import websockets
import json
import base64
import sys
from io import StringIO
import subprocess
import select
import os
import threading
import fcntl
import time
from IPython.core.interactiveshell import InteractiveShell
from ansi2html import Ansi2HTMLConverter
from IPython.terminal.interactiveshell import TerminalInteractiveShell
import traceback
import signal

async def read_stdin(websocket, path):
    await websocket.send("stdin ok")
    async for message in websocket:
        # 将来自前端的输入消息发送到stdin
        print(message)
        if message == 'stop':
            process.send_signal(signal.SIGINT)
            print("in stop")
        else:
            print("in else")
            message = message + '\n'
            process.stdin.write(message.encode('utf-8'))
            #process.stdin.write(message)
        await process.stdin.drain()

async def write_stdout(websocket, path):
    conv = Ansi2HTMLConverter()
    while True:
        output = await process.stdout.readline()
        if not output:
            break
        output_str = output.decode('utf-8')
        output_str = output_str.strip('\n')
        print(output_str)
        output_str = conv.convert(output_str)
        await websocket.send(output_str)

async def main():
    global process
    # 啟動 interactive_a.py peocess
    process = await asyncio.create_subprocess_exec(
        "python3", "-u", "interactive_a.py",
        stdin=asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    server1 = websockets.serve(read_stdin, "0.0.0.0", 5567)
    server2 = websockets.serve(write_stdout, "0.0.0.0", 5568)

    await asyncio.gather(server1, server2)
    await asyncio.Future()

if __name__ == "__main__":
    asyncio.run(main())
