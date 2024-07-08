import asyncio
import websockets
import json
import base64
import sys
import io
import subprocess
import select
import os
import threading
import time
from IPython.core.interactiveshell import InteractiveShell
from ansi2html import Ansi2HTMLConverter
from IPython.terminal.interactiveshell import TerminalInteractiveShell
import traceback

async def process_events(websocket, path):
    await websocket.send("ok")
    shell = TerminalInteractiveShell()
    conv = Ansi2HTMLConverter()
    
    while True:
        # 在這裡處理程式內部事件，可以是和stdin和stdout互動的邏輯
        message = await websocket.recv()
        message = json.loads(message)
        result = shell.run_cell(
            message['code'],
            store_history=False,
            silent=False,
        )
        if result.error_before_exec:
            message['error_time'] = 'compile'
            message['error_type'] = type(result.error_before_exec).__name__
            message['error_msg'] = result.error_before_exec.msg
            message['error_lineno'] = result.error_before_exec.lineno
            #print(result.error_before_exec.msg)
        if result.error_in_exec:
            message['error_time'] = 'runtime'
            message['error_type'] = type(result.error_in_exec).__name__
            message['error_msg'] = str(result.error_in_exec)
            message['error_lineno'] = result.error_in_exec.__traceback__.tb_next.tb_lineno
        
async def main():
    server = websockets.serve(process_events, "0.0.0.0", 5566)

    await asyncio.gather(server)

    await asyncio.Future()  # 保持主函數運行，避免提前結束


if __name__ == "__main__":
    asyncio.get_event_loop().run_until_complete(main())
