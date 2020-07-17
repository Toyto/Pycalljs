import asyncio
import aiohttp


async def call_js(fname, fargs):
    session = aiohttp.ClientSession()
    async with session.ws_connect('ws://localhost:8080/ws') as ws:
        func_with_args = '{}({})'.format(fname, ','.join(map(str, fargs)))
        await ws.send_str(func_with_args)
        async for msg in ws:
            if msg.data.startswith('result'):
                return msg.data


result = asyncio.run(call_js('Math.max', range(10)))
print(result)
