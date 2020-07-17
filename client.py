import asyncio
import aiohttp


async def call_js(fname, fargs):
    session = aiohttp.ClientSession()
    async with session.ws_connect('ws://localhost:8080/ws') as ws:
        func_with_args = '{}({})'.format(fname, ','.join(map(str, fargs)))
        await ws.send_str(func_with_args)
        async for msg in ws:
            print(msg)
            if msg.type == aiohttp.WSMsgType.TEXT:
                if msg.data == 'close cmd':
                    await ws.close()
                    break
            elif msg.type == aiohttp.WSMsgType.ERROR:
                break


loop = asyncio.get_event_loop()
loop.run_until_complete(call_js('Math.max', range(10)))
