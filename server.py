import aiohttp_jinja2
import aiohttp
import asyncio
from aiohttp import web


routes = web.RouteTableDef()


@routes.get('/')
@aiohttp_jinja2.template('base.html')
async def handle(request):
    name = request.match_info.get('name', "Anonymous")
    return {'name': name}


@routes.get('/ws')
async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    for _ws in request.app['websockets']:
        await _ws.send_str('Client joined')
    request.app['websockets'].append(ws)

    await call_js(ws, fname='Math.min', fargs=[-1, 23, 33])

    async for msg in ws:
        if msg.data.startswith('result'):
            print(msg.data)

    request.app['websockets'].remove(ws)
    print('websocket connection closed')

    return ws


async def call_js(ws, fname, fargs):
    func_with_args = '{}({})'.format(fname, ','.join(map(str, fargs)))
    await ws.send_str(func_with_args)


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


async def on_startup(app):
    await open_chrome(app)


app.on_cleanup.append(on_shutdown)
app.on_startup.append(on_startup)
app['websockets'] = []

if __name__ == '__main__':
    web.run_app(app)
