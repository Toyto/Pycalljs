import aiohttp_jinja2
import aiohttp
import asyncio
from aiohttp import web


routes = web.RouteTableDef()
WS = None
async def call_js(fname, fargs):
    print(WS)


@routes.get('/')
@aiohttp_jinja2.template('base.html')
async def handle(request):
    name = request.match_info.get('name', "Anonymous")
    return {'name': name}


@routes.get('/ws')
async def websocket_handler(request):
    global WS

    ws = web.WebSocketResponse()
    await ws.prepare(request)
    WS = ws

    for _ws in request.app['websockets']:
        await _ws.send_str('Client joined')
    request.app['websockets'].append(ws)

    async for msg in ws:
        print(msg)
        if msg.type == aiohttp.WSMsgType.TEXT:
            if msg.data == 'close':
                await ws.close()
            else:
                await ws.send_str(msg.data + '/ans')
        elif msg.type == aiohttp.WSMsgType.ERROR:
            print('ws connection closed with exception %s' %
                  ws.exception())

    print('websocket connection closed')

    return ws


app = web.Application()
app.add_routes(routes)
aiohttp_jinja2.setup(
    app, loader=aiohttp_jinja2.jinja2.FileSystemLoader('templates'))
app['static_root_url'] = '/static'
app.router.add_static('/static', 'static', name='static')


async def on_shutdown(app):
    for ws in app['websockets']:
        await ws.close(code=1001, message='Server shutdown')


async def open_chrome(app):
    cmd = '/Applications/Google\ Chrome.app/Contents/MacOS/Google\ Chrome --app=http://127.0.0.1:8080'
    await asyncio.create_subprocess_shell(cmd)


app.on_cleanup.append(on_shutdown)
app.on_startup.append(open_chrome)
app['websockets'] = []

web.run_app(app)
