#    This file is part of Kairos.
#
#    Kairos is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Kairos is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Kairos.  If not, see <http://www.gnu.org/licenses/>.
#
import cgi, json, base64, os, subprocess, sys, zipfile, magic, multidict, psycopg2
from datetime import datetime
from time import time
from urllib.parse import parse_qs
from loguru import logger
from io import BytesIO
from aiohttp import WSCloseCode, WSMsgType, web
from pykairos.analyzer import Analyzer
from pykairos.context import Context

global kairos
kairos=dict()

# Lambdas
getresponse = lambda context, d: web.json_response(dict(success=False, message=context.status.errormessages[0]) if context.status.errors > 0 else dict(success=True, **d))
        
##### Alternative à étudier pour renvoyer un contenu compressé
def gzipped_json_response(obj):
    obj_as_bytes = bytes(json.dumps(obj), 'utf-8')
    out = gzip.compress(obj_as_bytes, compresslevel=5)
    return aiohttp.web.Response(
        body=out,
        headers={
            "Content-Encoding":"gzip"
        }
    )

def lsof():
    p = os.getpid()
    result = subprocess.run(['lsof', '-b', '-p', f'{p}'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    res = result.stdout.decode('utf-8').splitlines()
    return len(res) - 1

def trace_call(func):
    def wrapper(*args, **kwargs):
        logger.debug(f'>>> Entering {func.__name__}')
        ts = time()
        response = func(*args, **kwargs)
        te = time()
        logger.debug(f'FUNCTION: {func.__name__} args: {args}, kwargs: {kwargs} TIME: {te -ts:.4f} sec')
        logger.debug(f'<<< Leaving {func.__name__}')
        return response
    return wrapper

def set_logging_level(p):
    dlog = dict(Trace=5, Debug=10, Info=20, Success=25, Warning=30, Error=40, Critical=50)
    logger.remove()
    lvl = dlog[p]
    lf = ("<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | <red>{process}</red> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | - <level>{message}</level>")
    logger.add('/var/log/kairos/kairos.log', format=lf, level=lvl,  rotation="10 MB", retention="30 days", compression="zip")
    logger.info(f'Logging has been set to {p}')

def intercept_logging_and_internal_error(func):
    def wrapper(*args, **kwargs):
        request = args[1]
        params = parse_qs(request.query_string)
        if 'logging' in params:
            if params['logging'][0] == 'trace': set_logging_level('Trace')
            if params['logging'][0] == 'debug': set_logging_level('Debug')
            if params['logging'][0] == 'info': set_logging_level('Info')
            if params['logging'][0] == 'warn': set_logging_level('Warning')
            if params['logging'][0] == 'error': set_logging_level('Error')
            if params['logging'][0] == 'fatal': set_logging_level('Critical')
        try:
            response = func(*args, **kwargs)
            return response
        except:
            tb = sys.exc_info()
            logger.error(str(tb))
            message = str(tb[1])
            return web.json_response(dict(success=False, message=message))
    return wrapper

def intercept_internal_error(func):
    def wrapper(*args, **kwargs):
        try:
            response = func(*args, **kwargs)
            return response
        except:
            tb = sys.exc_info()
            logger.error(str(tb))
            message = str(tb[1])
            return web.json_response(dict(success=False, message=message))
    return wrapper
    
class KairosWorker:
    def __init__(self, jpypeflag=True):
        
        app = web.Application(client_max_size=1024**3)
        app['websockets'] = []

        @trace_call
        def on_shutdown(app):
            for ws in app['websockets']:
                ws.close(code=WSCloseCode.GOING_AWAY, message='Server shutdown')

        app.on_shutdown.append(on_shutdown)

        app.router.add_get('/', self.file_index)
        app.router.add_get('/index.html', self.file_index)
        app.router.add_get('/charter.js', self.file_charter)
        app.router.add_get('/client.js', self.file_client)
        app.router.add_get('/checkserverconfig', self.checkserverconfig)
        app.router.add_get('/createsystem', self.createsystem)
        app.router.add_get('/getsettings', self.getsettings)
        app.router.add_get('/getmenus', self.getmenus)
        app.router.add_get('/getpath', self.getpath)
        app.router.add_get('/gettree', self.gettree)
        app.router.add_get('/getwholetree', self.getwholetree)
        app.router.add_get('/getnode', self.getnode)
        app.router.add_get('/getchart', self.getchart)
        app.router.add_get('/getjsonobject', self.getjsonobject)
        app.router.add_get('/getchoice', self.getchoice)
        app.router.add_get('/getlayout', self.getlayout)
        app.router.add_get('/gettemplate', self.gettemplate)
        app.router.add_get('/getcolors', self.getcolors)
        app.router.add_get('/getqueries', self.getqueries)
        app.router.add_get('/getcharts', self.getcharts)
        app.router.add_get('/getchoices', self.getchoices)
        app.router.add_get('/getobject', self.getobject)
        app.router.add_get('/executequery', self.executequery)
        app.router.add_get('/getmemberlist', self.getmemberlist)
        app.router.add_get('/getcollections', self.getcollections)
        app.router.add_get('/getmember', self.getmember)
        app.router.add_get('/buildallcollectioncaches', self.buildallcollectioncaches)
        app.router.add_get('/buildcollectioncache', self.buildcollectioncache)
        app.router.add_get('/clearcollectioncache', self.clearcollectioncache)
        app.router.add_get('/dropcollectioncache', self.dropcollectioncache)
        app.router.add_get('/displaycollection', self.displaycollection)
        app.router.add_get('/createnode', self.createnode)
        app.router.add_get('/renamenode', self.renamenode)
        app.router.add_get('/duplicatenode', self.duplicatenode)
        app.router.add_get('/deletenode', self.deletenode)
        app.router.add_get('/movenode', self.movenode)
        app.router.add_get('/emptytrash', self.emptytrash)
        app.router.add_get('/listdatabases', self.listdatabases)
        app.router.add_get('/listroles', self.listroles)
        app.router.add_get('/listusers', self.listusers)
        app.router.add_get('/listgrants', self.listgrants)
        app.router.add_get('/listsystemdb', self.listsystemdb)
        app.router.add_get('/listnodesdb', self.listnodesdb)
        app.router.add_get('/listtemplates', self.listtemplates)
        app.router.add_get('/listaggregators', self.listaggregators)
        app.router.add_get('/listliveobjects', self.listliveobjects)
        app.router.add_get('/listwallpapers', self.listwallpapers)
        app.router.add_get('/listcolors', self.listcolors)
        app.router.add_get('/listobjects', self.listobjects)
        app.router.add_get('/createrole', self.createrole)
        app.router.add_get('/createuser', self.createuser)
        app.router.add_get('/creategrant', self.creategrant)
        app.router.add_get('/deleterole', self.deleterole)
        app.router.add_get('/deleteuser', self.deleteuser)
        app.router.add_get('/resetpassword', self.resetpassword)
        app.router.add_get('/deletegrant', self.deletegrant)
        app.router.add_get('/updatesettings', self.updatesettings)
        app.router.add_get('/get_kairos_log', self.websocket_handler)
        app.router.add_get('/get_webserver_log', self.websocket_handler)
        app.router.add_get('/get_postgres_logfile', self.websocket_handler)
        app.router.add_get('/deleteobject', self.deleteobject)
        app.router.add_get('/downloadobject', self.downloadobject)
        app.router.add_get('/downloadsource', self.downloadsource)
        app.router.add_get('/getBchildren', self.getBchildren)
        app.router.add_get('/unload', self.unload)
        app.router.add_get('/compareaddnode', self.compareaddnode)
        app.router.add_get('/aggregateaddnode', self.aggregateaddnode)
        app.router.add_get('/linkfathernode', self.linkfathernode)
        app.router.add_get('/applyaggregator', self.applyaggregator)
        app.router.add_get('/applyliveobject', self.applyliveobject)
        app.router.add_get('/uploadnode', self.uploadnode)
        app.router.add_get('/uploadobject', self.uploadobject)
        app.router.add_get('/getid', self.getid)
        app.router.add_get('/export', self.exportdatabase)
        app.router.add_get('/import', self.importdatabase)
        app.router.add_get('/clearprogenycaches', self.clearprogenycaches)
        app.router.add_get('/buildprogenycaches', self.buildprogenycaches)
        app.router.add_get('/runchart', self.runchart)
        app.router.add_post('/changepassword', self.changepassword)
        app.router.add_post('/uploadobject', self.uploadobject)
        app.router.add_post('/setobject', self.setobject)
        app.router.add_post('/checkuserpassword', self.checkuserpassword)
        app.router.add_post('/uploadnode', self.uploadnode)
        app.router.add_static('/resources/', path='/kairos/resources', name='resources')
        self.application = app
        set_logging_level('Info')
        import setproctitle
        setproctitle.setproctitle('KairosWorker')
        logger.info(f'Process name: {setproctitle.getproctitle()}')
        logger.info(f'Process id: {os.getpid()}')

    @trace_call
    async def websocket_handler(self, request):
        ws = web.WebSocketResponse()
        await ws.prepare(request)
        request.app['websockets'].append(ws)
        try:
            async for msg in ws:
                if msg.type == WSMsgType.TEXT:
                    logger.debug(f'Got request : {msg.data}')
                    alpha = subprocess.Popen("exec " + msg.data,stdout=subprocess.PIPE,stderr=subprocess.PIPE,shell=True)
                    line = alpha.stdout.readline()
                    while line:
                        if 'WARNING socket.send() raised exception' in line.decode(): break
                        await ws.send_str(line.decode())
                        line = alpha.stdout.readline()
                    await ws.send_str('__END_OF_PIPE__')
                elif msg.type == WSMsgType.ERROR:
                    logger.error(f'Unexpected error, ws connection closed with exception {ws.exception()}')
        finally:
            await ws.close()
            alpha.kill()
            request.app['websockets'].remove(ws)
        return ws

    def file_index(self, request):
        return web.Response(content_type='text/html', text=open('/kairos/index.html').read())

    def file_charter(self, request):
        return web.Response(content_type='application/octet-stream', text=open('/kairos/charter.js').read())

    def file_client(self, request):
        return web.Response(content_type='application/octet-stream', text=open('/kairos/client.js').read())
                
    @intercept_logging_and_internal_error
    @trace_call
    def getid(self, request):
        params = parse_qs(request.query_string)
        nodesdb = params['nodesdb'][0]
        pattern = params['pattern'][0]
        context = Context(nodesdb=nodesdb)
        result = context.expand(pattern, 'desc', 1, 0)
        context.free()
        return getresponse(context, dict(data=result))
                
    @intercept_logging_and_internal_error
    @trace_call
    def getpath(self, request):
        params = parse_qs(request.query_string)
        nodesdb = params['nodesdb'][0]
        id = params['id'][0]
        context = Context(nodesdb=nodesdb)
        result = context.getpath(id)
        context.free()
        return getresponse(context, dict(data=result))

    @intercept_logging_and_internal_error
    @trace_call
    def checkserverconfig(self, request):
        context = Context(postgres=True)
        context.createsystem()
        context.createuser('admin', skiperror=True)
        context.free()
        return getresponse(context, dict())

    @intercept_logging_and_internal_error
    @trace_call
    def createsystem(self, request):
        context = Context(postgres=True)
        context.createsystem()
        context.free()
        return getresponse(context, dict())

    @intercept_logging_and_internal_error
    @trace_call
    async def checkuserpassword(self, request):
        multipart = await request.post()
        params = parse_qs(request.query_string)
        user = multipart['user'] if 'user' in multipart else params['user'][0]
        password = multipart['password'] if 'password' in multipart else params['password'][0]
        adminrights = True if user == 'admin' else False
        postgresstr = f"host='localhost' dbname='kairos_user_{user}' user='{user}' password='{password}'"
        try: 
            postgres = psycopg2.connect(postgresstr)
            postgres.close()
            return web.json_response(dict(success=True, data=dict(adminrights = adminrights)))
        except:
            message = "Invalid password!"
            #logger.warning(message)
            return web.json_response(dict(success=False, message=message))


    @intercept_logging_and_internal_error
    @trace_call
    async def setobject(self, request):
        multipart = await request.post()
        params = parse_qs(request.query_string)
        database = multipart['database'] if 'database' in multipart else params['database'][0]
        if 'kairos_system_' in database:
            message = 'A system object cannot be updated! Use download and upload to update the object in a nodes database!'
            return web.json_response(dict(success=False, status='error', message=message))
        source = multipart['source'] if 'source' in multipart else params['source'][0]
        encoded = int(multipart['encoded'] if 'encoded' in multipart else params['encoded'][0])
        if encoded:
            decode = lambda x: base64.b64decode(x).decode()
            source = decode(source)
        context = Context(nodesdb=database)
        try:
            (id, typeobj) = context.writeobject(source)
            msg = dict(data=dict(msg=f'Object: {id} of type: {typeobj} has been successfully saved!', id=id))
        except:
            tb = sys.exc_info()
            logger.error(tb)
            context.status.pusherrmessage(str(tb[1]))
        context.free()
        return getresponse(context, msg)


    @intercept_logging_and_internal_error
    @trace_call
    def getsettings(self, request):
        params = parse_qs(request.query_string)
        user = params['user'][0]
        context = Context(nodesdb=f'kairos_user_{user}')
        settings = context.getsettings()
        context.free()
        return getresponse(context, dict(data=dict(settings=settings)))

    @intercept_logging_and_internal_error
    @trace_call
    def listdatabases(self, request):
        params = parse_qs(request.query_string)
        user = params['user'][0]
        adminrights = True if params['admin'][0] == "true" else False
        context = Context(postgres=True)
        data = context.listdatabases(user, adminrights)
        context.free()
        return getresponse(context, dict(data=data))

    @intercept_logging_and_internal_error
    @trace_call
    def listsystemdb(self, request):
        context = Context(postgres=True)
        data = context.listsystemdb()
        context.free()
        return getresponse(context, dict(data=data))

    @intercept_logging_and_internal_error
    @trace_call
    def listnodesdb(self, request):
        params = parse_qs(request.query_string)
        user = params['user'][0]
        context = Context(postgres=True)
        data = context.listnodesdb(user)
        context.free()
        return getresponse(context, dict(data=data))

    @intercept_logging_and_internal_error
    @trace_call
    def listtemplates(self, request):
        params = parse_qs(request.query_string)
        systemdb = params['systemdb'][0]
        nodesdb = params['nodesdb'][0]
        try: context = Context(nodesdb=nodesdb, systemdb=systemdb)
        except: context = Context(systemdb=systemdb)
        data = context.listobjects("where type='template'")
        context.free()
        return getresponse(context, dict(data=data))

    @intercept_logging_and_internal_error
    @trace_call
    def listaggregators(self, request):
        params = parse_qs(request.query_string)
        systemdb = params['systemdb'][0]
        nodesdb = params['nodesdb'][0]
        context = Context(nodesdb=nodesdb, systemdb=systemdb)
        data = context.listobjects("where type='aggregator'")
        context.free()
        return getresponse(context, dict(data=data))

    @intercept_logging_and_internal_error
    @trace_call
    def listliveobjects(self, request):
        params = parse_qs(request.query_string)
        #systemdb = params['systemdb'][0]
        nodesdb = params['nodesdb'][0]
        context = Context(nodesdb=nodesdb)
        data = context.listobjects("where type='liveobject'")
        context.free()
        return getresponse(context, dict(data=data))

    @intercept_logging_and_internal_error
    @trace_call
    def listwallpapers(self, request):
        params = parse_qs(request.query_string)
        systemdb = params['systemdb'][0]
        nodesdb = params['nodesdb'][0]      
        try: context = Context(nodesdb=nodesdb, systemdb=systemdb)
        except: context = Context(systemdb=systemdb)
        data = context.listobjects("where type='wallpaper'")
        context.free()
        return getresponse(context, dict(data=data))

    @intercept_logging_and_internal_error
    @trace_call
    def listcolors(self, request):
        params = parse_qs(request.query_string)
        systemdb = params['systemdb'][0]
        nodesdb = params['nodesdb'][0]
        try: context = Context(nodesdb=nodesdb, systemdb=systemdb)
        except: context = Context(systemdb=systemdb)
        data = context.listobjects("where type='color'")
        context.free()
        return getresponse(context, dict(data=data))

    @intercept_logging_and_internal_error
    @trace_call
    def listobjects(self, request):
        params = parse_qs(request.query_string)
        systemdb = params['systemdb'][0]
        nodesdb = params['nodesdb'][0]
        context = Context(nodesdb=nodesdb, systemdb=systemdb)
        data = context.listobjects("")
        context.free()
        return getresponse(context, dict(data=data))

    @intercept_logging_and_internal_error
    @trace_call
    def getobject(self, request):
        params = parse_qs(request.query_string)
        database = params['database'][0]
        objtype = params['type'][0]
        objid = params['id'][0]
        context = Context(nodesdb=database)
        (_, source) = context.getobjectstream(objid, objtype)
        context.free()
        return getresponse(context, dict(data=source.decode()))

    @intercept_logging_and_internal_error
    @trace_call
    def updatesettings(self, request):
        params = parse_qs(request.query_string)
        user = params['user'][0]
        systemdb = params['systemdb'][0]
        nodesdb = params['nodesdb'][0]
        template = params['template'][0]
        colors = params['colors'][0]
        wallpaper = params['wallpaper'][0]
        top = int(params['top'][0])
        plotorientation = params['plotorientation'][0]
        logging = params['logging'][0]
        newsettings = dict(nodesdb=nodesdb, systemdb=systemdb, colors=colors, template=template, wallpaper=wallpaper, plotorientation=plotorientation, logging=logging, top=top)
        context = Context(nodesdb=f'kairos_user_{user}')
        context.updatesettings(newsettings)
        context.free()
        return getresponse(context, dict())

    @intercept_logging_and_internal_error
    @trace_call
    async def uploadobject(self, request):
        params = parse_qs(request.query_string)
        if 'mode' in params:
            mode = params['mode'][0]
            if mode == 'conf':
                return web.json_response(dict(success=True, maxFileSize=2147483648))
        multipart = await request.post()
        nodesdb = multipart['nodesdb'] if 'nodesdb' in multipart else params['nodesdb'][0]
        context = Context(nodesdb=nodesdb)
        (id, filename, typeobj) = context.uploadobject(multipart)
        context.free()
        return getresponse(context, dict(state=True, name=filename, id=id, type=typeobj))

    @intercept_logging_and_internal_error
    @trace_call
    async def uploadnode(self, request):
        params = parse_qs(request.query_string)
        if 'mode' in params:
            mode = params['mode'][0]
            if mode == 'conf':
                return web.json_response(dict(success=True, maxFileSize=2147483648))
        multipart = await request.post()
        nodesdb = multipart['nodesdb'] if 'nodesdb' in multipart else params['nodesdb'][0]
        systemdb = multipart['systemdb'] if 'systemdb' in multipart else params['systemdb'][0]
        id = multipart['id'] if 'id' in multipart else params['id'][0] if 'id' in params else None
        context = Context(nodesdb=nodesdb, systemdb=systemdb)
        filename = context.uploadnode(id, multipart)
        context.free()
        return getresponse(context, dict(state=True, name=filename))

    @intercept_logging_and_internal_error
    @trace_call
    def listroles(self, request):
        context = Context(postgres=True)
        data = context.listroles()
        context.free()
        return getresponse(context, dict(data=data))

    @intercept_logging_and_internal_error
    @trace_call
    def listusers(self, request):
        context = Context(postgres=True)
        data = context.listusers()
        context.free()
        return getresponse(context, dict(data=data))

    @intercept_logging_and_internal_error
    @trace_call
    def listgrants(self, request):
        context = Context(postgres=True)
        data = context.listgrants()
        context.free()
        return getresponse(context, dict(data=data))

    @intercept_logging_and_internal_error
    @trace_call
    def createrole(self, request):
        params = parse_qs(request.query_string)
        role = params['role'][0]
        context = Context(postgres=True)
        response = context.createrole(role)
        context.free()
        return getresponse(context, response)

    @intercept_logging_and_internal_error
    @trace_call
    def createuser(self, request):
        params = parse_qs(request.query_string)
        user = params['user'][0]
        context = Context(postgres=True)
        response = context.createuser(user)
        context.free()
        return getresponse(context, response)

    @intercept_logging_and_internal_error
    @trace_call
    def creategrant(self, request):
        params = parse_qs(request.query_string)
        user = params['user'][0]
        role = params['role'][0]
        context = Context(postgres=True)
        response = context.creategrant(user, role)
        context.free()
        return getresponse(context, response)

    @intercept_logging_and_internal_error
    @trace_call
    def deleterole(self, request):
        params = parse_qs(request.query_string)
        role = params['role'][0]
        context = Context(postgres=True)
        response = context.deleterole(role)
        context.free()
        return getresponse(context, response)

    @intercept_logging_and_internal_error
    @trace_call
    def deleteuser(self, request):
        params = parse_qs(request.query_string)
        user = params['user'][0]
        context = Context(postgres=True)
        response = context.deleteuser(user)
        context.free()
        return getresponse(context, response)

    @intercept_logging_and_internal_error
    @trace_call
    def resetpassword(self, request):
        params = parse_qs(request.query_string)
        user = params['user'][0]
        context = Context(postgres=True)
        response = context.resetpassword(user)
        context.free()
        return getresponse(context, response)

    @intercept_logging_and_internal_error
    @trace_call
    def deletegrant(self, request):
        params = parse_qs(request.query_string)
        user = params['user'][0]
        role = params['role'][0]
        context = Context(postgres=True)
        response = context.deletegrant(user, role)
        context.free()
        return getresponse(context, response)

    @intercept_logging_and_internal_error
    @trace_call
    async def changepassword(self, request):
        multipart = await request.post()
        params = parse_qs(request.query_string)
        user = multipart['user'] if 'user' in multipart else params['user'][0]
        password = multipart['password'] if 'password' in multipart else params['password'][0]
        new = multipart['new'] if 'new' in multipart else params['new'][0]
        postgresstr = f"host='localhost' dbname='kairos_user_{user}' user='{user}' password='{password}'"
        try: 
            postgres = psycopg2.connect(postgresstr)
            postgres.close()
        except:
            message = "Invalid password!"
            logger.warning(message)
            return web.json_response(dict(success=False, message=message))
        context = Context(postgres=True)
        context.changepassword(user, new)
        context.free()
        return getresponse(context, dict(data=dict(msg='Password has been successfully updated!')))

    @intercept_logging_and_internal_error
    @trace_call
    def deleteobject(self, request):
        params = parse_qs(request.query_string)
        database = params['database'][0]
        if 'kairos_system_' in database:
            message = 'A system object cannot be deleted!'
            return web.json_response(dict(success=False, status='error', message=message))
        id = params['id'][0]
        typeobj = params['type'][0]
        context = Context(nodesdb=database)
        context.deleteobject(id, typeobj)
        context.free()
        return getresponse(context, dict(data=dict(msg=f'{id} {typeobj} object has been successfully removed!')))

    @intercept_logging_and_internal_error
    @trace_call
    def downloadobject(self, request):
        params = parse_qs(request.query_string)
        database = params['database'][0]
        id = params['id'][0]
        typeobj = params['type'][0]
        context = Context(nodesdb=database)
        (filename, stream) = context.getobjectstream(id, typeobj)
        context.free()
        return web.Response(headers=multidict.MultiDict({'Content-Disposition': 'Attachment;filename="' + filename + '"'}), body=stream)

    @intercept_logging_and_internal_error
    @trace_call
    def downloadsource(self, request):
        params = parse_qs(request.query_string)
        nodesdb = params['nodesdb'][0]
        id = params['id'][0]
        context = Context(nodesdb=nodesdb)
        (filename, stream) = context.downloadsource(id)
        context.free()
        return web.Response(headers=multidict.MultiDict({'Content-Disposition': 'Attachment;filename="' + filename + '"'}), body=stream)

    @intercept_logging_and_internal_error
    @trace_call
    def getBchildren(self, request):
        params = parse_qs(request.query_string)
        nodesdb = params['nodesdb'][0]
        id = params['id'][0]
        context = Context(nodesdb=nodesdb)
        data = context.getBchildren(id)
        context.free()
        return getresponse(context, dict(data=data))

    @intercept_logging_and_internal_error
    @trace_call
    def getmemberlist(self, request):
        params = parse_qs(request.query_string)
        nodesdb = params['nodesdb'][0]
        id = params['id'][0]
        context = Context(nodesdb=nodesdb)
        node = context.getnode(id)
        context.getsource(node, getstream=True)
        context.free()
        thezip = zipfile.ZipFile(BytesIO(node['datasource']['stream']))
        data = [dict(label=x) for x in thezip.namelist()]
        return getresponse(context, dict(data=data))

    @intercept_logging_and_internal_error
    @trace_call
    def getcollections(self, request):
        params = parse_qs(request.query_string)
        nodesdb = params['nodesdb'][0]
        systemdb = params['systemdb'][0]
        id = params['id'][0]
        context = Context(nodesdb=nodesdb, systemdb=systemdb)
        data = context.getcollections(id)
        context.free()
        return getresponse(context, dict(data=data))

    @intercept_logging_and_internal_error
    @trace_call
    def getmember(self, request):
        params = parse_qs(request.query_string)
        nodesdb = params['nodesdb'][0]
        member = params['member'][0]
        id = params['id'][0]
        context = Context(nodesdb=nodesdb)
        node = context.getnode(id)
        context.getsource(node, getstream=True)
        context.free()
        thezip = zipfile.ZipFile(BytesIO(node['datasource']['stream']))
        stream = thezip.read(member)
        type = magic.from_buffer(stream)
        stream = stream.decode().replace('#=', '# =').replace('#+', '# +')
        if 'html' in type.lower(): html = stream
        elif 'text' in type.lower(): html = f'<pre>{cgi.escape(stream)}</pre>'
        else: html = 'Not yet taken into account'
        return getresponse(context, dict(data=html))

    @intercept_logging_and_internal_error
    @trace_call
    def getmenus(self, request):
        params = parse_qs(request.query_string)
        nodesdb = params['nodesdb'][0]
        systemdb = params['systemdb'][0]
        context = Context(nodesdb=nodesdb, systemdb=systemdb)
        data = context.getmenus()
        context.free()
        return getresponse(context, dict(data=data))

    @intercept_logging_and_internal_error
    @trace_call
    def gettree(self, request):
        params = parse_qs(request.query_string)
        nodesdb = params['nodesdb'][0]
        parent = params['id'][0]
        context = Context(nodesdb=nodesdb)
        result = context.gettree(parent)
        context.free
        return web.json_response(result)

    @intercept_logging_and_internal_error
    @trace_call
    def getwholetree(self, request):
        params = parse_qs(request.query_string)
        nodesdb = params['nodesdb'][0]
        context = Context(nodesdb=nodesdb)
        result = context.getwholetree()
        context.free
        return getresponse(context, dict(data=result))

    @intercept_logging_and_internal_error
    @trace_call
    def getnode(self, request):
        params = parse_qs(request.query_string)
        nodesdb = params['nodesdb'][0]
        id = params['id'][0]
        context = Context(nodesdb=nodesdb)
        node = context.getnode(id)
        context.getsource(node)
        context.getcache(node)
        context.free()
        return getresponse(context, dict(data=node))

    @intercept_logging_and_internal_error
    @trace_call
    def createnode(self, request):
        params = parse_qs(request.query_string)
        nodesdb = params['nodesdb'][0]
        id = params['id'][0]
        context = Context(nodesdb=nodesdb)
        child = context.createnode(id)
        node = context.getnode(child)
        context.free()
        return getresponse(context, dict(data=node))

    @intercept_logging_and_internal_error
    @trace_call
    def renamenode(self, request):
        params = parse_qs(request.query_string)
        nodesdb = params['nodesdb'][0]
        id = params['id'][0]
        new = params['new'][0]
        context = Context(nodesdb=nodesdb)
        node = context.renamenode(id, new)
        context.free()
        return getresponse(context, dict(data=node))

    @intercept_logging_and_internal_error
    @trace_call
    def duplicatenode(self, request):
        params = parse_qs(request.query_string)
        nodesdb = params['nodesdb'][0]
        id = params['id'][0]
        context = Context(nodesdb=nodesdb)
        dup = context.duplicatenode(id)
        node = context.getnode(dup)
        context.free()
        return getresponse(context, dict(data=node))

    @intercept_logging_and_internal_error
    @trace_call
    def deletenode(self, request):
        params = parse_qs(request.query_string)
        nodesdb = params['nodesdb'][0]
        id = params['id'][0]
        context = Context(nodesdb=nodesdb)
        context.deletenode(id)
        context.free()
        return getresponse(context, dict())

    @intercept_logging_and_internal_error
    @trace_call
    def emptytrash(self, request):
        params = parse_qs(request.query_string)
        nodesdb = params['nodesdb'][0]
        context = Context(nodesdb=nodesdb)
        context.emptytrash()
        context.free()
        return getresponse(context, dict())

    @intercept_logging_and_internal_error
    @trace_call
    def movenode(self, request):
        params = parse_qs(request.query_string)
        nodesdb = params['nodesdb'][0]
        pfrom = params['from'][0]
        pto = params['to'][0]
        context = Context(nodesdb=nodesdb)
        node = context.movenode(pfrom, pto)
        context.free()
        return getresponse(context, dict(data=node))

    @intercept_logging_and_internal_error
    @trace_call
    def getchart(self, request):
        params = parse_qs(request.query_string)
        nodesdb = params['nodesdb'][0]
        systemdb = params['systemdb'][0]
        chart = params['chart'][0]
        variables = json.loads(params['variables'][0])
        context = Context(nodesdb=nodesdb, systemdb=systemdb)
        context.variables = variables.copy()
        chart = context.getchart(chart)
        context.free()
        return getresponse(context, dict(data=chart))

    @intercept_logging_and_internal_error
    @trace_call
    def getjsonobject(self, request):
        params = parse_qs(request.query_string)
        database = params['database'][0]
        id = params['id'][0]
        type = params['type'][0]
        context = Context(nodesdb=database, systemdb=database)
        obj = context.readobjects(f"where id = '{id}' and type = '{type}'", evalobject=False)[0]
        context.free()
        return getresponse(context, dict(data=obj))
    
    @intercept_logging_and_internal_error
    @trace_call
    def getlayout(self, request):
        params = parse_qs(request.query_string)
        nodesdb = params['nodesdb'][0]
        systemdb = params['systemdb'][0]
        layout = params['layout'][0]
        variables = json.loads(params['variables'][0])
        context = Context(nodesdb=nodesdb, systemdb=systemdb)
        context.variables = variables.copy()
        layout = context.getlayout(layout)
        context.free()
        return getresponse(context, dict(data=layout))
    
    @intercept_logging_and_internal_error
    @trace_call
    def getchoice(self, request):
        params = parse_qs(request.query_string)
        nodesdb = params['nodesdb'][0]
        systemdb = params['systemdb'][0]
        choice = params['choice'][0]
        variables = json.loads(params['variables'][0])
        context = Context(nodesdb=nodesdb, systemdb=systemdb)
        context.variables = variables.copy()
        choice = context.getchoice(choice)
        context.free()
        return getresponse(context, dict(data=choice))

    @intercept_logging_and_internal_error
    @trace_call
    def gettemplate(self, request):
        params = parse_qs(request.query_string)
        nodesdb = params['nodesdb'][0]
        systemdb = params['systemdb'][0]
        template = params['template'][0]
        context = Context(nodesdb=nodesdb, systemdb=systemdb)
        template = context.gettemplate(template)
        context.free()
        return getresponse(context, dict(data=template))

    @intercept_logging_and_internal_error
    @trace_call
    def getcolors(self, request):
        params = parse_qs(request.query_string)
        nodesdb = params['nodesdb'][0]
        systemdb = params['systemdb'][0]
        colors = params['colors'][0]
        context = Context(nodesdb=nodesdb, systemdb=systemdb)
        colors = context.getcolors(colors)
        context.free()
        return getresponse(context, dict(data=colors))

    @intercept_logging_and_internal_error
    @trace_call
    def getqueries(self, request):
        params = parse_qs(request.query_string)
        nodesdb = params['nodesdb'][0]
        systemdb = params['systemdb'][0]
        context = Context(nodesdb=nodesdb, systemdb=systemdb)
        queries = context.listobjects("where type='query'")
        context.free()
        return getresponse(context, dict(data=queries))

    @intercept_logging_and_internal_error
    @trace_call
    def getcharts(self, request):
        params = parse_qs(request.query_string)
        nodesdb = params['nodesdb'][0]
        systemdb = params['systemdb'][0]
        context = Context(nodesdb=nodesdb, systemdb=systemdb)
        charts = context.listobjects("where type='chart'")
        context.free()
        return getresponse(context, dict(data=charts))

    @intercept_logging_and_internal_error
    @trace_call
    def getchoices(self, request):
        params = parse_qs(request.query_string)
        nodesdb = params['nodesdb'][0]
        systemdb = params['systemdb'][0]
        context = Context(nodesdb=nodesdb, systemdb=systemdb)
        choices = context.listobjects("where type='choice'")
        context.free()
        return getresponse(context, dict(data=choices))

    @intercept_logging_and_internal_error
    @trace_call
    def executequery(self, request):
        params = parse_qs(request.query_string)
        nodesdb = params['nodesdb'][0]
        systemdb = params['systemdb'][0]
        id = params['id'][0]
        query = params['query'][0]
        limit = int(params['top'][0])
        variables = json.loads(params['variables'][0])
        context = Context(nodesdb=nodesdb, systemdb=systemdb)
        context.variables = variables.copy()
        result = context.executequery(id, query, limit)
        context.free()
        return getresponse(context, dict(data=result))

    @intercept_logging_and_internal_error
    @trace_call
    def displaycollection(self, request):
        params = parse_qs(request.query_string)
        nodesdb = params['nodesdb'][0]
        systemdb = params['systemdb'][0]
        id = params['id'][0]
        collection = params['collection'][0]
        context = Context(nodesdb=nodesdb, systemdb=systemdb)
        result = context.displaycollection(id, collection)
        context.free()
        return getresponse(context, dict(data=result))

    @intercept_logging_and_internal_error
    @trace_call
    def buildcollectioncache(self, request):
        params = parse_qs(request.query_string)
        nodesdb = params['nodesdb'][0]
        systemdb = params['systemdb'][0]
        collection = params['collection'][0]
        id = params['id'][0]
        context = Context(nodesdb=nodesdb, systemdb=systemdb)
        context.buildcollectioncache(id, {collection})
        context.free()
        return getresponse(context, dict())

    @intercept_logging_and_internal_error
    @trace_call
    def buildallcollectioncaches(self, request):
        params = parse_qs(request.query_string)
        nodesdb = params['nodesdb'][0]
        systemdb = params['systemdb'][0]
        id = params['id'][0]
        context = Context(nodesdb=nodesdb, systemdb=systemdb)
        _ = context.getnode(id)
        context.buildcollectioncache(id, {'*'})
        context.free()
        return getresponse(context, dict())

    @intercept_logging_and_internal_error
    @trace_call
    def clearcollectioncache(self, request):
        params = parse_qs(request.query_string)
        nodesdb = params['nodesdb'][0]
        id = params['id'][0]
        context = Context(nodesdb=nodesdb)
        context.deletecache(id)
        context.free()
        return getresponse(context, dict())

    @intercept_logging_and_internal_error
    @trace_call
    def dropcollectioncache(self, request):
        params = parse_qs(request.query_string)
        nodesdb = params['nodesdb'][0]
        id = params['id'][0] 
        collection = params['collection'][0]
        context = Context(nodesdb=nodesdb)
        context.dropcollectioncache(id, [collection])
        context.free()
        return getresponse(context, dict())

    @intercept_logging_and_internal_error
    @trace_call
    def compareaddnode(self, request):
        params = parse_qs(request.query_string)
        nodesdb = params['nodesdb'][0]
        fromid = int(params['from'][0])
        toid = int(params['to'][0])
        context = Context(nodesdb=nodesdb)
        tnode = context.compareaddnode(fromid, toid)
        context.free()
        return getresponse(context, dict(data=tnode))
    
    @intercept_logging_and_internal_error
    @trace_call
    def aggregateaddnode(self, request):
        params = parse_qs(request.query_string)
        nodesdb = params['nodesdb'][0]
        fromid = int(params['from'][0])
        toid = int(params['to'][0])
        context = Context(nodesdb=nodesdb)
        tnode = context.aggregateaddnode(fromid, toid)
        context.free()
        return getresponse(context, dict(data=tnode))
    
    @intercept_logging_and_internal_error
    @trace_call
    def applyaggregator(self, request):
        params = parse_qs(request.query_string)
        nodesdb = params['nodesdb'][0]
        id = int(params['id'][0])
        aggregatorselector = params['aggregatorselector'][0]
        aggregatortake = int(params['aggregatortake'][0])
        aggregatorskip = int(params['aggregatorskip'][0])
        aggregatortimefilter = params['aggregatortimefilter'][0]
        aggregatorsort = params['aggregatorsort'][0]
        aggregatormethod = params['aggregatormethod'][0]
        context = Context(nodesdb=nodesdb)
        node = context.applyaggregator(id, aggregatorselector, aggregatortake, aggregatorskip, aggregatortimefilter, aggregatorsort, aggregatormethod)
        context.free()
        return getresponse(context, dict(data=node))
     
    @intercept_logging_and_internal_error
    @trace_call
    def unload(self, request):
        params = parse_qs(request.query_string)
        nodesdb = params['nodesdb'][0]
        systemdb = params['systemdb'][0]
        id = params['id'][0]
        context = Context(nodesdb=nodesdb, systemdb=systemdb)
        (filename, stream) = context.unload(id)
        context.free()
        return web.Response(headers=multidict.MultiDict({'Content-Disposition': 'Attachment;filename="' + filename + '"'}), body=stream)
    
    @intercept_logging_and_internal_error
    @trace_call
    def linkfathernode(self, request):
        params = parse_qs(request.query_string)
        nodesdb = params['nodesdb'][0]
        fromid = int(params['from'][0])
        toid = int(params['to'][0])
        context = Context(nodesdb=nodesdb)
        tnode = context.linkfathernode(fromid, toid)
        context.free()
        return getresponse(context, dict(data=tnode))

    @intercept_logging_and_internal_error
    @trace_call
    def applyliveobject(self, request):
        params = parse_qs(request.query_string)
        nodesdb = params['nodesdb'][0]
        systemdb = params['systemdb'][0]
        loname = params['liveobject'][0]
        id = int(params['id'][0])
        context = Context(nodesdb=nodesdb, systemdb=systemdb)
        node= context.applyliveobject(id, loname)
        context.free()
        return getresponse(context, dict(data=node))

    @intercept_logging_and_internal_error
    @trace_call
    def exportdatabase(self, request):
        params = parse_qs(request.query_string)
        nodesdb = [params['nodesdb'][0]] if 'nodesdb' in params else []
        context = Context(postgres=True)
        context.exportdatabases(nodesdb)
        context.free()
        return getresponse(context, dict(data=dict(msg=f"Database(s): {nodesdb} has(ve) been exported sucessfully!")))

    @intercept_logging_and_internal_error
    @trace_call
    def importdatabase(self, request):
        params = parse_qs(request.query_string)
        nodesdb = [params['nodesdb'][0]] if 'nodesdb' in params else []
        context = Context(postgres=True)
        context.importdatabases(nodesdb)
        context.free()
        return getresponse(context, dict(data=dict(msg=f"Database(s): {nodesdb} has(ve) been imported sucessfully!")))

    @trace_call
    def clearprogenycaches(self, request):
        params = parse_qs(request.query_string)
        nodesdb = params['nodesdb'][0]
        systemdb = params['systemdb'][0]
        id = params['id'][0]
        context = Context(nodesdb=nodesdb, systemdb=systemdb)
        context.clearprogenycaches(id)
        context.free()
        return getresponse(context, dict(data=dict(msg="Caches have been cleared sucessfully!")))

    @trace_call
    def buildprogenycaches(self, request):
        params = parse_qs(request.query_string)
        nodesdb = params['nodesdb'][0]
        systemdb = params['systemdb'][0]
        id = params['id'][0]
        context = Context(nodesdb=nodesdb, systemdb=systemdb)
        context.buildprogenycaches(id)
        context.free()
        return getresponse(context, dict(data=dict(msg="Caches have been built sucessfully!")))

    @intercept_logging_and_internal_error
    @trace_call
    def runchart(self, request):
        params = parse_qs(request.query_string)
        nodesdb = params['nodesdb'][0]
        systemdb = params['systemdb'][0]
        id = int(params['id'][0])
        chart = params['chart'][0]
        width = int(params['width'][0])
        height = int(params['height'][0])
        limit = int(params['top'][0])
        colors = params['colors'][0]
        plotorientation = params['plotorientation'][0]
        template = params['template'][0]
        toggle = True if params['toggle'][0] == 'true' else False
        variables = json.loads(params['variables'][0])
        context = Context(nodesdb=nodesdb, systemdb=systemdb)
        context.variables = variables.copy()
        chartobj = context.runchart(id, chart, width, height, limit, colors, plotorientation, template, toggle)
        context.free()
        return getresponse(context, dict(data=dict(chart=chartobj)))
