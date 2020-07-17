import asyncio
from server import call_js


loop = asyncio.get_event_loop()
loop.run_until_complete(call_js('Math.max', range(10)))
