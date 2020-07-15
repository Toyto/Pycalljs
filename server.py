import aiohttp_jinja2
import aiohttp
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

    async for msg in ws:
        if msg.type == aiohttp.WSMsgType.TEXT:
            if msg.data == 'close':
                await ws.close()
            else:
                await ws.send_str(msg.data + '/answer')
        elif msg.type == aiohttp.WSMsgType.ERROR:
            print('ws connection closed with exception %s' %
                  ws.exception())

    print('websocket connection closed')

    return ws


app = web.Application()
app.add_routes(routes)
aiohttp_jinja2.setup(app, loader=aiohttp_jinja2.jinja2.FileSystemLoader('templates'))
app['static_root_url'] = '/static'
app.router.add_static('/static', 'static', name='static')

web.run_app(app)