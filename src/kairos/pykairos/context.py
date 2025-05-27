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

#import binascii, hashlib, json, multiprocessing, os, re, shutil, sys, urllib, zipfile, pexpect, plotly, pykairos
import binascii, hashlib, json, multiprocessing, os, re, shutil, sys, urllib, zipfile, plotly, pykairos
import pandas
from collections import OrderedDict
from contextlib import suppress
from datetime import datetime
from functools import wraps
from time import time
from io import StringIO, BytesIO
from loguru import logger
from dask import bag as daskbag
from pykairos.analyzer import Analyzer
from pykairos.arcfile import Arcfile
from pykairos.parallel import *
from pykairos.repository import Repository
from fabric import Connection as Runner

#  Lambdas

getdatabases = lambda repository: [row['datname'] for row in repository.execute("select datname from pg_database")]
getnextid = lambda repository: [row['objid'] for row in repository.execute("select nextval('objid') as objid")][0]
getdbsizes = lambda repository: {row['datname']:row['size'] for row in repository.execute("select datname, pg_database_size(datname) as size from pg_database where datname like 'kairos_%'")}
getgroupdatabases = lambda repository, user: [f'kairos_group_{row["groname"]}' for row in repository.execute(f"select groname from pg_group,pg_user where usesysid = any(grolist) and usename='{user}'")]
getdefaultnodename = lambda repository: [row['name'] for row in repository.execute("select to_char(now(), 'YYYY-MM-DD HH24:MI:SS.MS') as name")][0]
getnodeparentid = lambda repository, id: [row['pid'] for row in repository.execute(f"select parent as pid from nodes where id = {id}")][0]
getrootid = lambda repository: [row['rid'] for row in repository.execute("select id as rid from nodes where parent is null")][0]
getprogeny = lambda repository, id:  [row['rid'] for row in repository.execute(f"with recursive tree as (select id, parent from nodes where id={id} union all select p.id, p.parent from nodes p join tree c on p.parent = c.id) select id as rid from tree where id != {id}")]
getancestors = lambda repository, id:  [x for x in reversed([row['rid'] for row in repository.execute(f"with recursive tree as (select id, parent from nodes where id={id} union all select p.id, p.parent from nodes p join tree c on p.id = c.parent) select id as rid from tree where id != {id}")])]
fff1 = lambda repository, id, name: [row['rid'] for row in repository.execute(f"select id as rid from nodes where parent = {id} and name = '{name}'")]
getnodesidfromp = lambda repository, id: [row['rid'] for row in repository.execute(f"select id as rid from nodes where parent = {id}")]
getnodeidfrompn = lambda repository, id, name: fff1(repository, id, name)[0] if len(fff1(repository, id, name)) > 0 else None
getpath = lambda context, repository, id: ('/'.join([x['name'] for x in [context.getnode(i) for i in getancestors(repository, id)]]) + '/' + context.getnode(id)['name'])[1:]
ftype = lambda x: x['icon']
getkey = lambda x: x['text']
ficon = lambda node: ("fa fa-trash btnt", "fa fa-trash-o btnt", "fa fa-trash btnt") if node['icon'] == 'T' else ("fa fa-folder btnb", "fa fa-folder-open btnb", "fa fa-folder btnb") if node['icon'] == 'B' else ("fa fa-folder btna", "fa fa-folder-open btna", "fa fa-folder btna") if node['icon'] == 'A' else ("fa fa-folder btnc", "fa fa-folder-open btnc", "fa fa-folder btnc") if node['icon'] == 'C' else ("fa fa-folder btnl", "fa fa-folder-open btnl", "fa fa-folder btnl") if node['icon'] == 'L' else ("fa fa-database btnd", "fa fa-database btnd", "fa fa-database btnd") if node['icon'] == 'D' else ("fa fa-folder btnn", "fa fa-folder-open btnn", "fa fa-folder btnn")
depthp = lambda d, n: 0 if d[n] == None else depthp(d, d[n]) + 1
nullistener = lambda col, d, v, n: None
getchartproducers = lambda node: [k['path'] for k in node['datasource']['producers']] if 'producers' in node['datasource'] and node['datasource']['type'] == 'C' else []
getcolor = lambda colors, x: colors[x] if x in colors else '#' + hashlib.md5(x.encode('utf-8')).hexdigest()[0:6]

def timing(method):
    @wraps(method)
    def _impl(self, *args, **kwargs):
        ts = time()
        x = method(self, *args, **kwargs)
        te = time()
        logger.debug(f'METHOD: {method.__name__} args: {args}, kwargs: {kwargs} TIME: {te -ts:.4f} sec')
        return x
    return _impl

def getfontsize(width, binf=1000, bsup=2000, vinf=0, vsup=0):
    if width <= binf: return int(vinf)
    if width >= bsup: return int(vsup)
    return int(vinf + ((vsup - vinf) / (bsup - binf)) * (width - binf))

def getyposition(yaxis, width, numleftyaxis=1, binf=1000, bsup=2000, vinf=0.08, vsup=0.05, rows=1):
    begposition = yaxis['position']
    if begposition == 0: return begposition
    if begposition == 0.05 and numleftyaxis / rows == 1: return 0
    if begposition == 0.05:
        if width <= binf: return vinf
        if width >= bsup: return vsup
        return vinf + ((vsup -vinf) / (bsup - binf) * (width - binf))
    if begposition == 0.90:
        if width <= binf: return 1 - (2 * vinf)
        if width >= bsup: return 1 - (2 * vsup)
        return 1 - (2 * (vinf + ((vsup -vinf) / (bsup - binf) * (width - binf))))
    if begposition == 0.95:
        if width <= binf: return 1 - vinf
        if width >= bsup: return 1 - vsup
        return 1 - (1 * (vinf + ((vsup -vinf) / (bsup - binf) * (width - binf))))

def getaposition(width, index=0, numleftyaxis=1, numrightyaxis=0, numxaxis=1, binf=1000, bsup=2000, vinf=0.08, vsup=0.05, rows=1):
    if rows == 1:
        cols = numxaxis
        nbseparators = cols - 1
        lengthseparator = 0.02
        lengthseparators = lengthseparator * nbseparators
        lengthaxis = vinf if width <= binf else vsup if width >= bsup else vinf + ((vsup -vinf) / (bsup - binf) * (width - binf))
        lengthaxis = 0 if numleftyaxis + numrightyaxis == 0 else lengthaxis
        availablespace = 1 - ((numleftyaxis + numrightyaxis - 1) * lengthaxis) - 2 * lengthseparator
        lengthdomain = (availablespace - lengthseparators) / cols 
        positiondomain = (numleftyaxis - 1) * lengthaxis + lengthseparator + index * (lengthdomain + lengthseparator) 
        return positiondomain + lengthdomain / 2
    else:
        nbseparators = rows - 1
        lengthseparator = 0.02
        lengthseparators = lengthseparator * nbseparators
        availablespace = 1 - lengthseparators
        lengthdomain = (availablespace - lengthseparators) / rows
        positiondomain = lengthdomain + index * (lengthdomain + lengthseparator * 2)
        return positiondomain

def getdomain(width, index=0, numleftyaxis=1, numrightyaxis=0, numxaxis=1, binf=1000, bsup=2000, vinf=0.08, vsup=0.05, rows=1):
    cols = numxaxis if rows == 1 else 1
    nbseparators = cols - 1
    lengthseparator = 0.02
    lengthseparators = lengthseparator * nbseparators
    lengthaxis = vinf if width <= binf else vsup if width >= bsup else vinf + ((vsup -vinf) / (bsup - binf) * (width - binf))
    lengthaxis = 0 if numleftyaxis + numrightyaxis == 0 else lengthaxis
    availablespace = 1 - ((numleftyaxis / rows + numrightyaxis / rows  - 1) * lengthaxis) - 2 * lengthseparator
    lengthdomain = (availablespace - lengthseparators) / cols 
    positiondomain = (numleftyaxis / rows  - 1) * lengthaxis + lengthseparator + index * (lengthdomain + lengthseparator)
    return [positiondomain, positiondomain+lengthdomain]

def replaceeval(obj, contextvariables, recursive=False):
    if not recursive:
        for e in obj:
            obj[e] = replaceeval(obj[e], contextvariables, recursive=True)
    if type(obj) == type('a'):
        with suppress(Exception): obj = obj % contextvariables
    elif type(obj) == type([]):
        i=0
        for e in obj:
            obj[i] = replaceeval(e, contextvariables, recursive=True)
            i+=1
    elif type(obj) == type({}):
        for e in obj:
            obj[e] = replaceeval(obj[e], contextvariables, recursive=True)
    else: pass
    return obj


def gettimestampdf(d, co, plotorientation):
    converttime = lambda x: datetime.strptime(x, '%Y%m%d%H%M%S%f')
    if  len(d) > 0 and 'timestamp' not in d[0] and plotorientation == 'horizontal':
        co['cols'] = len(d)
        co['isarray'] = True
    if  len(d) > 0 and 'timestamp' not in d[0] and plotorientation == 'vertical': 
        co['rows'] = len(d)
        co['isarray'] = True
    ret = []
    if co['isarray']:
        for x in d:
            r = pandas.DataFrame(data=x)
            if 'timestamp' in r:
                r['timestamp'] = r['timestamp'].apply(converttime)
                r = r.set_index('timestamp').sort_index()
            ret.append(r)
    else:
        r = pandas.DataFrame(data=d)
        if 'timestamp' in r: 
            r['timestamp'] = r['timestamp'].apply(converttime)
            r = r.set_index('timestamp').sort_index()
        ret.append(r)
    return ret

def getnewaxis(co, reftimedf, template, axistype=None, options=None, index=0):
    if axistype == 'y' and index not in co['alreadyright']: co['alreadyright'][index] = False
    if axistype == 'y' and index not in co['alreadyleft']: co['alreadyleft'][index] = False
    d = co['yaxis'] if axistype == 'y' else co['xaxis']
    l = len(d)
    d[l] = dict()
    d[l]['name'] = axistype + 'axis' if l == 0 else  axistype + 'axis' + str(l + 1)
    d[l]['smallname'] = axistype if l == 0 else axistype + str(l + 1)
    if axistype == 'y':
        for e in template['yaxis']: d[l][e] = template['yaxis'][e].copy() if type(template['yaxis'][e]) == type(dict()) else template['yaxis'][e]
        d[l]['options']['title'] = options['title']
        if 'properties' in options and 'line' in options['properties'] and 'stroke' in options['properties']['line']: 
            d[l]['options']['tickfont'] = dict(color = options['properties']['line']['stroke'])
            d[l]['options']['color'] = options['properties']['line']['stroke']
            d[l]['options']['linecolor'] = options['properties']['line']['stroke']
        if 'properties' in options and 'text' in options['properties'] and 'fill' in options['properties']['text']: 
            d[l]['options']['titlefont'] = dict(color = options['properties']['text']['fill'])
        d[l]['options']['side'] = options['position'].lower()
        if d[l]['options']['side'] == 'left' and not co['alreadyleft'][index]: d[l]['options']['position'] = 0.05
        if d[l]['options']['side'] == 'left' and co['alreadyleft'][index]: 
            d[l]['options']['position'] = 0.00
            d[l]['options']['overlaying'] = 'y' if index == 0 else 'y' + str(index + 1)
        if d[l]['options']['side'] == 'right' and not co['alreadyright'][index]: 
            d[l]['options']['overlaying'] = 'y' if index == 0 else 'y' + str(index + 1)
            d[l]['options']['position'] = 0.95
        if d[l]['options']['side'] == 'right' and co['alreadyright'][index]: 
            d[l]['options']['overlaying'] = 'y' if index == 0 else 'y' + str(index + 1)
            d[l]['options']['position'] = 0.90
        if d[l]['options']['side'] == 'left': co['alreadyleft'][index] = True
        if d[l]['options']['side'] == 'right': co['alreadyright'][index] = True
        rows = co['rows']
        nbseparators = rows - 1
        lengthseparator = 0.02
        lengthseparators = lengthseparator * nbseparators
        lengthdomain = (1 - lengthseparators) / rows 
        positiondomain = 0.0 + index * (lengthdomain + lengthseparator)
        d[l]['options']['domain'] = [positiondomain, positiondomain + lengthdomain]
    else:
        for e in template['xaxis']: d[l][e] = template['xaxis'][e].copy() if type(template['xaxis'][e]) == type(dict()) else template['xaxis'][e]
        cols = co['cols']
        nbseparators = cols - 1
        lengthseparator = 0.02
        lengthseparators = lengthseparator * nbseparators
        lengthdomain = (0.8 - lengthseparators) / cols 
        positiondomain = 0.1 + index * (lengthdomain + lengthseparator)
        d[l]['options']['domain'] = [positiondomain, positiondomain + lengthdomain]
        d[l]['options']['range'] = [reftimedf[index].index.min(),reftimedf[index].index.max()]
    logger.debug(f'Axis index: {index}, options: {d[l]}')
    return l

def paddeddf(t, d):
    r = t.copy()
    r['a'] = 0
    r['b'] = d['value']
    r['value'] = r['a'] + r['b'].fillna(0)
    return r

def settrace(co, r, dataframe=None, label=None, yaxisindex=0, index=0, alreadyinlegend = None, groupname=None, plotorientation=None, colors=None):
    param = dict()
    param['x'] = dataframe.index
    param['y'] = dataframe['value']
    param['name'] = label
    param['legendgroup'] = label
    param['showlegend'] = True if label not in alreadyinlegend else False
    alreadyinlegend[label] = True
    if r['type'] == 'WM': 
        param['mode'] = 'markers'
        param['marker'] = dict(color=(getcolor(colors, label)))
        trace = plotly.graph_objs.Scattergl(**param)
    if r['type'] == 'WA': 
        param['line'] = dict(color=(getcolor(colors, label)), shape='hv')
        param['fill'] = 'tozeroy'
        param['fillcolor'] = getcolor(colors, label)
        trace = plotly.graph_objs.Scattergl(**param)
    if r['type'] == 'WL': 
        param['line'] = dict(color=(getcolor(colors, label)), shape='hv')
        trace = plotly.graph_objs.Scattergl(**param)
    if r['type'] == 'L': 
        param['line'] = dict(color=(getcolor(colors, label)), shape='spline')
        trace = plotly.graph_objs.Scatter(**param)
    if r['type'] == 'A': 
        param['mode'] = 'lines'
        param['fill'] = 'tozeroy'
        param['fillcolor'] = getcolor(colors, label)
        param['line'] = dict(color=(getcolor(colors, label)), shape='spline')
        trace = plotly.graph_objs.Scatter(**param)
    if r['type'] == 'SA':  
        param['line'] = dict(color=(getcolor(colors, label)), shape='spline')
        param['mode'] = 'lines'
        param['stackgroup'] = groupname
        param['fillcolor'] = getcolor(colors, label)
        trace = plotly.graph_objs.Scatter(**param)
    if r['type'] == 'C': 
        param['marker']=dict(color=getcolor(colors, label))
        trace = plotly.graph_objs.Bar(**param)
        co['layoutoptions']['barmode'] = 'group'
    if r['type'] == 'CC': 
        param['marker']=dict(color=getcolor(colors, label))
        trace = plotly.graph_objs.Bar(**param)
        co['layoutoptions']['barmode'] = 'group'
    if r['type'] == 'SC':
        param['marker']=dict(color=getcolor(colors, label))
        trace = plotly.graph_objs.Bar(**param)
        co['layoutoptions']['barmode'] = 'stack'
    l = len(co['traces'])
    xaxis = index if co['shared_yaxes'] else 0
    yaxis = yaxisindex
    row = 1 if plotorientation=='horizontal' else index+1
    col = index+1 if plotorientation=='horizontal' else 1
    logger.debug(f'settrace, xaxis: {xaxis}, yaxis: {yaxis}, row: {row}, col: {col}, label: {label}')
    co['traces'][l] = dict(trace=trace, yaxis=yaxis, xaxis=xaxis, row=row, col=col)

class Object: pass


class Status:
    def __init__(self):
        self.errors = 0
        self.errormessages = []
    
    def pusherrmessage(self, m):
        logger.error(m)
        self.errormessages.append(m)
        self.errors = self.errors + 1

class Context:
    
    def __init__(self, nodesdb=None, systemdb=None, postgres=False, autocommit=True):
        self.nodesdb = nodesdb
        self.systemdb = systemdb
        self.postgresdb = postgres
        self.removecollections  = []
        self.createcollections  = []
        self.grepo = Repository() if postgres else None
        self.nrepo = Repository(nodesdb) if nodesdb else None
        self.srepo = Repository(systemdb) if systemdb else None
        self.cache = dict(nodes=dict(), objects=dict(chart=dict(), query=dict(), analyzer=dict(), liveobject=dict(), template=dict(), color=dict(), aggregator=dict(), function=dict(), layout=dict(), choice=dict(), report=dict()))
        self.status = Status()
        self.variables = dict()
        self.nocache = False
    
    def free(self):
        if self.postgresdb: self.grepo.disconnect()
        if self.nodesdb: self.nrepo.disconnect()
        if self.systemdb: self.srepo.disconnect()
        if self.status.errors > 0:
            for m in self.status.errormessages: logger.error(m)

    def setschema(self, schema=None):
        self.nrepo.setschema(schema)

    def createsystem(self):
        r = self.grepo
        databases = getdatabases(r)
        if 'kairos_system_system' in databases: return
        r.execute("create database kairos_system_system with encoding 'utf8'")
        self.systemdb = 'kairos_system_system'
        self.srepo = Repository(self.systemdb)
        r = self.srepo
        r.execute("create language plpython3u")
        r.execute("create sequence objid start 1")
        r.execute("create table objects(rid integer primary key, id text, type name, created timestamp, filename text, stream bytea)")
        r.execute("create unique index iobjects on objects(type, id)")        

    def createuser(self, user, skiperror=False):
        curdatabase = f"kairos_user_{user}"
        r = self.grepo
        databases = getdatabases(r)
        if curdatabase in databases:
            if not skiperror: self.status.pusherrmessage(f'{user} user already exists!')
            return dict()
        r.execute(f"create database kairos_user_{user} with encoding 'utf8'")
        r.execute(f"create user {user} password '{user}'")
        self.nodesdb = curdatabase
        self.nrepo = Repository(self.nodesdb)
        r = self.nrepo
        r.execute("create language plpython3u")
        r.execute("create extension oracle_fdw")
        r.execute("create extension postgres_fdw")
        r.execute("create sequence objid start 1")
        r.execute("create table objects(rid integer primary key, id text, type name, created timestamp, filename text, stream bytea)")
        r.execute("create unique index iobjects on objects(type, id)")        
        r.execute("create table nodes(id integer primary key, parent integer, name text, type text, created timestamp, status text, liveobject text, aggregatorselector text, aggregatorsort text, aggregatortake integer, aggregatorskip integer, aggregatormethod text, aggregatortimefilter text, aggregated timestamp, producers text)")
        r.execute("create table settings(colors text, logging text, nodesdb text, plotorientation text, systemdb text, template text, top integer, wallpaper text)")
        r.execute("create table sources(id integer primary key, created timestamp, collections text, stream bytea)")
        r.execute("create table caches(id integer primary key, name text, created timestamp, queries text, collections text)")
        r.execute(f"insert into settings(colors, logging, nodesdb, plotorientation, systemdb, template, top, wallpaper) values ('COLORS', 'info', 'kairos_user_{user}', 'horizontal', 'kairos_system_system', 'DEFAULT', 15, 'DEFAULT')")
        rootid = getnextid(r)
        r.execute(f"insert into nodes(id, parent, name, type, created, status) values ({rootid}, null, '/', 'N', now(), 'ACTIVE')")
        trashid = getnextid(r)
        r.execute(f"insert into nodes(id, parent, name, type, created, status) values ({trashid}, {rootid}, 'Trash', 'T', now(), 'DELETED')")
        with suppress(Exception): shutil.rmtree(f'/autoupload/{curdatabase}')
        os.mkdir(f'/autoupload/{curdatabase}')
        return dict(data=dict(msg=f"{user} user has been successfully created!"))
        
    def createrole(self, role):
        curdatabase = f"kairos_group_{role}"
        r = self.grepo
        databases = getdatabases(r)
        if curdatabase in databases:
            self.status.pusherrmessage(f'{role} role already exists!')
            return dict()
        r.execute(f"create database kairos_group_{role} with encoding 'utf8'")
        r.execute(f"create role {role}")
        self.nodesdb = curdatabase
        self.nrepo = Repository(self.nodesdb)
        r = self.nrepo
        r.execute("create language plpython3u")
        r.execute("create extension oracle_fdw")
        r.execute("create extension postgres_fdw")
        r.execute("create sequence objid start 1")
        r.execute("create table objects(rid integer primary key, id text, type name, created timestamp, filename text, stream bytea)")
        r.execute("create unique index iobjects on objects(type, id)")        
        r.execute("create table nodes(id integer primary key, parent integer references nodes(id), name text, type text, created timestamp, status text, liveobject text, aggregatorselector text, aggregatorsort text, aggregatortake integer, aggregatorskip integer, aggregatormethod text, aggregatortimefilter text, aggregated timestamp, producers text)")
        r.execute("create table sources(id integer primary key, created timestamp, collections text, stream bytea)")
        r.execute("create table caches(id integer primary key, name text, created timestamp, queries text, collections text)")
        rootid = getnextid(r)
        r.execute(f"insert into nodes(id, parent, name, type, created, status) values ({rootid}, null, '/', 'N', now(), 'ACTIVE')")
        trashid = getnextid(r)
        r.execute(f"insert into nodes(id, parent, name, type, created, status) values ({trashid}, {rootid}, 'Trash', 'T', now(), 'DELETED')")
        with suppress(Exception): shutil.rmtree(f'/autoupload/{curdatabase}')
        os.mkdir(f'/autoupload/{curdatabase}')
        return dict(data=dict(msg=f"{role} role has been successfully created!"))

    def deleteuser(self, user):
        if user=='admin': 
            self.status.pusherrmessage('admin user cannot be removed!')
            return dict()
        dbuser = f"kairos_user_{user}"
        r = self.grepo
        r.execute(f"drop database {dbuser}")
        r.execute(f"drop user {user}")
        return dict(data=dict(msg=f"{user} user has been successfully removed!"))

    def deleterole(self, role):
        dbgroup = f"kairos_group_{role}"
        r = self.grepo
        r.execute(f"drop database {dbgroup}")
        r.execute(f"drop role {role}")
        return dict(data=dict(msg=f"{role} role has been successfully removed!"))

    def creategrant(self, user, role):
        r = self.grepo
        databases = getdatabases(r)
        dbgroup = f"kairos_group_{role}"
        dbuser = f"kairos_user_{user}"
        if dbgroup not in databases:
            self.status.pusherrmessage(f"{role} role doesn't exist!")
            return dict()
        if dbuser not in databases:
            self.status.pusherrmessage(f"{user} user doesn't exist!")
            return dict()
        x = r.execute(f"select groname,usename from pg_group,pg_user where usesysid = any(grolist) and groname='{role}' and usename='{user}'")
        if len([row for row in x.fetchall()]) > 0:
            self.status.pusherrmessage(f"{user} user is already granted with {role} role!")
            return(dict())
        r.execute(f"grant {role} to {user}")
        return dict(data=dict(msg=f"{role} role has been successfully granted to {user} user!"))

    def deletegrant(self, user, role):
        r = self.grepo
        r.execute(f"revoke {role} from {user}")
        return dict(data=dict(msg=f"{user} user has been successfully revoked from {role} role!"))

    def resetpassword(self, user):
        if user=='admin':
            self.status.pusherrmessage('admin password cannot be reset!')
            return dict()
        r = self.grepo
        r.execute(f"alter user {user} password '{user}'")
        return dict(data=dict(msg=f"{user} password has been successfully reset!"))

    def changepassword(self, user, password):
        r = self.grepo
        r.execute(f"alter user {user} password '{password}'")

    def getsettings(self):
        r = self.nrepo
        y = r.execute("select top, colors, logging, nodesdb, systemdb, template, wallpaper, plotorientation from settings")
        settings = dict()
        for row in y.fetchall():
            for x in row.keys(): settings[x] = row[x]
        return settings

    def updatesettings(self, newsettings):
        r = self.nrepo
        r.execute("delete from settings")
        r.execute(f"insert into settings(colors, logging, nodesdb, plotorientation, systemdb, template, top, wallpaper) values ('{newsettings['colors']}', '{newsettings['logging']}', '{newsettings['nodesdb']}', '{newsettings['plotorientation']}', '{newsettings['systemdb']}', '{newsettings['template']}', {newsettings['top']}, '{newsettings['wallpaper']}')")

    def listdatabases(self, user, adminrights):
        r = self.grepo
        data = []
        databases = getdbsizes(r)
        groups = getgroupdatabases(r, user)
        for k in databases:
            if adminrights:
                data.append(dict(name=k, size=databases[k] * 1.0 / 1024 / 1024))
            else:
                if k == f'kairos_user_{user}':
                    data.append(dict(name=k, size=databases[k] * 1.0 / 1024 / 1024))
                if 'kairos_group_' in k:
                    if k in groups:
                        data.append(dict(name=k, size=databases[k] * 1.0 / 1024 / 1024))
        return data
    
    def listroles(self):
        r = self.grepo
        databases = getdatabases(r)
        data = [dict(_id=k.replace('kairos_group_',''), role=k.replace('kairos_group_','')) for k in databases if 'kairos_group_' in k]
        return data
    
    def listusers(self):
        r = self.grepo
        databases = getdatabases(r)
        data = [dict(_id=k.replace('kairos_user_',''), user=k.replace('kairos_user_','')) for k in databases if 'kairos_user_' in k]
        return data

    def listgrants(self):
        r = self.grepo
        data = [dict(_id=row['usename'] + ':' + row['groname'], user=row['usename'], role=row['groname']) for row in r.execute("select groname,usename from pg_group,pg_user where usesysid = any(grolist)")]
        return data

    def listsystemdb(self):
        r = self.grepo
        databases = getdatabases(r)
        data = [dict(name=k) for k in databases if 'kairos_system_' in k]
        return data

    def listnodesdb(self, user):
        r = self.grepo
        databases = getdatabases(r)
        groupdb = getgroupdatabases(r, user)
        data = [dict(name=k) for k in databases if k == 'kairos_user_' + user or k in groupdb]
        return data

    def listobjects(self, where):
        data = []
        listdb = []
        if self.nodesdb: listdb.append(self.nodesdb)
        if self.systemdb: listdb.append(self.systemdb)
        for db in listdb:
            r = self.nrepo if db == self.nodesdb else self.srepo
            for row in r.execute(f"select rid, id, type, to_char(created, 'YYYY-MM-DD HH24:MI:SS.MS') as created from objects {where} order by type, id"):
                item = dict()
                for x in row.keys(): item[x] = row[x]
                item['origin'] = db
                data.append(item)
        return data
    
    def readobjects(self, where, evalobject=True, allbases=False):
        data = []
        interrupt = False
        for db in [self.nodesdb, self.systemdb]:
            if interrupt and not allbases: break
            r = self.nrepo if db == self.nodesdb else self.srepo
            command = f"select filename, stream as content, to_char(created, 'YYYY-MM-DD HH24:MI:SS.MS') as created from objects {where}"
            for row in r.execute(command):
                source = binascii.a2b_base64(row['content'])
                filename = row['filename']
                created = row['created']
                p = compile(source, filename, 'exec')
                true = True
                false = False
                null = None
                exec(p, locals())
                obj = locals()['UserObject']()
                obj['origin'] = db
                obj['created'] = created
                if evalobject: obj = replaceeval(obj, self.variables)
                data.append(obj)
                interrupt = True
        return data

    def getobject(self, id, typeobj):
        if id not in self.cache['objects'][typeobj]:
            objs = self.readobjects(f"where id='{id}' and type='{typeobj}'")
            if len(objs) == 0: return None
            self.cache['objects'][typeobj][id]= objs[0]
        return self.cache['objects'][typeobj][id]

    def getanalyzer(self, id): 
        analyzer = self.getobject(id, 'analyzer')
        if analyzer == None: self.status.pusherrmessage(f"Analyzer '{id}' doesn't exist!")
        return analyzer

    def getliveobject(self, id): 
        liveobject = self.getobject(id, 'liveobject')
        if liveobject == None: self.status.pusherrmessage(f"Liveobject '{id}' doesn't exist!")
        return liveobject

    def gettemplate(self, id): 
        template = self.getobject(id, 'template')
        if template == None: self.status.pusherrmessage(f"Template '{id}' doesn't exist!")
        return template

    def getcolors(self, id): 
        colors = self.getobject(id, 'color')
        if colors == None: self.status.pusherrmessage(f"Colors '{id}' doesn't exist!")
        return colors

    def getchart(self, id): 
        chart = self.getobject(id, 'chart')
        if chart == None: self.status.pusherrmessage(f"Chart '{id}' doesn't exist!")
        return chart

    def getaggregator(self, id): 
        aggregator = self.getobject(id, 'aggregator')
        if aggregator == None: self.status.pusherrmessage(f"Aggregator '{id}' doesn't exist!")
        return aggregator

    def getfunction(self, id): 
        function = self.getobject(id, 'function')
        if function == None: self.status.pusherrmessage(f"Function '{id}' doesn't exist!")
        return function

    def getlayout(self, id): 
        layout = self.getobject(id, 'layout')
        if layout == None: self.status.pusherrmessage(f"Layout '{id}' doesn't exist!")
        return layout

    def getchoice(self, id): 
        choice = self.getobject(id, 'choice')
        if choice == None: self.status.pusherrmessage(f"Choice '{id}' doesn't exist!")
        return choice

    def getquery(self, id): 
        query = self.getobject(id, 'query')
        return query

    def getmenus(self):
        return self.readobjects("where type='menu'", allbases=True)

    def writeobject(self, source):
        r = self.nrepo
        p = compile(source, 'stream', 'exec')
        kairos = dict()
        true = True
        false = False
        null = None
        exec(p, locals())
        obj = locals()['UserObject']()
        typeobj = obj['type']
        id = obj['id']
        filename = f'{id.lower()}.py'
        if 'tobeputinpykairos' in obj and obj['tobeputinpykairos']:
            dir = os.path.dirname(pykairos.__file__)
            f = open(f'{dir}/{filename}', 'w')
            f.write(source)
            f.close()
        content = binascii.b2a_base64(source.encode())
        r.execute(f"delete from objects where id='{id}' and type='{typeobj}'")
        objid = getnextid(r)
        r.executep("insert into objects(rid, id, type, created, filename, stream) values (%s, %s, %s, now(), %s, %s)", (objid, id, typeobj, filename, content))
        return (id, typeobj)

    def getobjectstream(self, id, otype):
        r = self.nrepo
        result = dict()
        for row in r.execute(f"select filename, stream from objects where id='{id}' and type = '{otype}'"):
            for x in row.keys(): result[x] = row[x]
        return (result['filename'], binascii.a2b_base64(result['stream']))

    def uploadobject(self, multipart):
        upload = multipart['file']
        filename = upload.filename
        content = upload.file.read()
        uploadtype = upload.content_type
        if uploadtype == 'image/jpeg':
            typeobj = 'wallpaper'
            id = filename.replace('.jpg', '')
        else:
            p = compile(content, filename, 'exec')
            kairos = dict()
            true = True
            false = False
            null = None
            exec(p, locals())
            obj = locals()['UserObject']()
            typeobj = obj['type']
            id = obj['id']
            if 'tobeputinpykairos' in obj and obj['tobeputinpykairos']:
                filename = f'{id.lower()}.py'
                dir = os.path.dirname(pykairos.__file__)
                f = open(f'{dir}/{filename}', 'w')
                f.write(content.decode())
                f.close()
        content = binascii.b2a_base64(content)
        r = self.nrepo
        r.execute(f"delete from objects where id='{id}' and type='{typeobj}'")
        objid = getnextid(r)
        r.executep("insert into objects(rid, id, type, created, filename, stream) values (%s, %s, %s, now(), %s, %s)", (objid, id, typeobj, filename, content))
        return (id, filename, typeobj)
    
    def deleteobject(self, id, typeobj):
        r = self.nrepo
        obj = self.getobject(id, typeobj)
        if 'tobeputinpykairos' in obj and obj['tobeputinpykairos']:
            dir = os.path.dirname(pykairos.__file__)
            filename = f'{id.lower()}.py'
            os.system(f'rm -f {dir}/{filename}')
        r.execute(f"delete from objects where id='{id}' and type='{typeobj}'")

    @timing
    def deletesource(self, id):
        r = self.nrepo
        r.execute(f"delete from sources where id={id}")

    @timing
    def createsource(self, nid, stream, filename):
        filepath = '/tmp/' + self.nodesdb + '_' + str(nid) + '.zip'
        infile = Arcfile(stream, 'r')
        ziparchive = Arcfile(filepath, 'w:zip')
        for m in infile.list(): ziparchive.write(m, infile.read(m))
        ziparchive.close()
        infile.close()
        collections = dict()
        def listener(col, d, v, n):
            for x in v['collections']:
                if x not in collections: collections[x] = dict(analyzer=v['analyzer'],members=[])
                collections[x]['members'].append(v['member'])
        analmain = self.getanalyzer('ANALMAIN')
        analyzer = Analyzer(analmain, {}, listener, None)
        def do(member):
            analyzer.analyze(ziparchive.read(member), member)
            return None
        ziparchive = Arcfile(filepath, 'r')
        #for member in ziparchive.list(): do(member)
        bag = daskbag.from_sequence(ziparchive.list(), npartitions=multiprocessing.cpu_count())
        task = bag.map(do)
        task.compute(scheduler='threads')
        ziparchive.close()
        r = self.nrepo
        f=open(filepath, 'rb')
        content = binascii.b2a_base64(f.read())
        f.close()
        os.unlink(filepath)
        r.executep("insert into sources (id, created, collections, stream) values(%s, now(), %s, %s)", (nid, json.dumps(collections), content))
        r.execute(f"update nodes set type = 'B' where id = {nid}")

    def readnode(self, id):
        r = self.nrepo
        projection = "id as rid, type, name, status, to_char(created, 'YYYY-MM-DD HH24:MI:SS.MS') as created, liveobject, aggregatorselector, aggregatorsort, aggregatortake, aggregatorskip, aggregatormethod, aggregatortimefilter, to_char(aggregated, 'YYYY-MM-DD HH24:MI:SS.MS') as aggregated, producers"
        selectednodes = [row for row in r.execute(f"select {projection} from nodes where id = {id}")]
        nodes=[]
        for row in selectednodes:
            node = dict(datasource=dict(cache=dict()))
            node['id'] = row['rid']
            node['name'] = row['name']
            node['icon'] = row['type']
            node['status'] = row['status']
            node['created'] = row['created']
            node['datasource']['type'] = row['type']
            node['datasource']['producers'] = json.loads(row['producers']) if 'producers' in row  and row['producers'] else []
            if row['type'] in ['A', 'L']:
                node['datasource']['aggregated'] = row['aggregated'] if 'aggregated' in row and row['aggregated'] else None
                node['datasource']['aggregatorselector'] = row['aggregatorselector'] if 'aggregatorselector' in row and row['aggregatorselector'] else '/'
                node['datasource']['aggregatorsort'] = row['aggregatorsort'] if 'aggregatorsort' in row and row['aggregatorsort'] else 'desc'
                node['datasource']['aggregatortake'] = row['aggregatortake'] if 'aggregatortake' in row and row['aggregatortake'] else 1
                node['datasource']['aggregatorskip'] = row['aggregatorskip'] if 'aggregatorskip' in row and row['aggregatorskip'] else 0
                node['datasource']['aggregatormethod'] = row['aggregatormethod'] if 'aggregatormethod' in row and row['aggregatormethod'] else '$none'
                node['datasource']['aggregatortimefilter'] = row['aggregatortimefilter'] if 'aggregatortimefilter' in row and row['aggregatortimefilter'] else '.'
            if row['type'] in ['D']:
                node['datasource']['liveobject'] = row['liveobject']
                d = dict()
                with suppress(Exception):
                    liveobject = self.getliveobject(row['liveobject'])
                    for e in liveobject['tables']: d[e] = True
                node['datasource']['collections'] = d
            nodes.append(node)
        return nodes
    
    def countchildren(self, node):
        r = self.nrepo
        for row in r.execute(f"select count(*) as count from nodes where parent = {node['id']}"): node['kids'] = row['count']

    def getnode(self, id):
        if id not in self.cache['nodes']:
            lnodes = self.readnode(id)
            if len(lnodes) == 0: return None
            self.cache['nodes'][id] = lnodes[0]
        return self.cache['nodes'][id]

    def deletenode(self, id):
        r = self.nrepo
        node = self.getnode(id)
        if node == None:
            self.status.pusherrmessage(f"Node with id: {id} doesn't exist!")
            return
        self.getcache(node)
        self.getsource(node)
        rootid = getrootid(r)
        trashid = getnodeidfrompn(r, rootid, 'Trash')
        if rootid == node['id']: 
            self.status.pusherrmessage('Root node cannot be removed!')
            return
        if trashid == node['id']: 
            self.status.pusherrmessage('A trash cannot be removed!')
            return
        listnodes = getprogeny(r, id)
        listnodes.append(id)
        if node['status'] == 'DELETED':
            for rid in listnodes:
                self.deletesource(rid)
                self.deletecache(rid)
                curnode = self.getnode(id)
                if curnode['datasource']['type'] == 'D' and curnode['datasource']['liveobject'][0:5] == 'AGLO_': self.deleteobject(curnode['datasource']['liveobject'], 'liveobject')
                r.execute(f"delete from nodes where id = {rid}")
        else:
            r.execute(f"update nodes set parent = {trashid} where id = {id}")
            for rid in listnodes: r.execute(f"update nodes set status = 'DELETED' where id = {rid}")
    
    @timing
    def uploadnode(self, id, multipart):
        r = self.nrepo
        upload = multipart['file']
        filename = urllib.parse.unquote(upload.filename)
        id = getrootid(r) if id == None else id
        node = self.getnode(id)
        (base, ext) = os.path.splitext(filename)
        while ext != '': (base, ext) = os.path.splitext(base)
        nodes = base.split('_')
        for d in nodes:
            nid = getnodeidfrompn(r, node['id'], d)
            if nid == None:
                child = self.createnode(node['id'], d)
                node = self.getnode(child)
            else:
                node = self.getnode(nid)
        id = node['id']
        self.deletesource(id)
        self.createsource(id, upload.file, filename)
        return filename
    
    def createnode(self, pid, name=None):
        r = self.nrepo
        name = getdefaultnodename(r) if not name else name
        objid = getnextid(r)
        r.execute(f"insert into nodes(id, parent, name, type, created, status) values ({objid}, {pid}, '{name}', 'N', now(), 'ACTIVE')")
        return objid
    
    def duplicatenode(self, id, name=None):
        r = self.nrepo
        name = getdefaultnodename(r) if not name else name
        pid = getnodeparentid(r, id)
        fnode = self.getnode(id)
        objid = getnextid(r)
        ntype = fnode['datasource']['type']
        status = fnode['status']
        if ntype == 'D':
            loname = fnode['datasource']['liveobject']
            objstream = self.getobjectstream(loname, 'liveobject')[1].replace(loname.encode(), f'AGLO_{objid}_OLGA'.encode()).decode()
            (newloname, typeobj) = self.writeobject(objstream)
        r.execute(f"insert into nodes(id, parent, name, type, created, status) values ({objid}, {pid}, '{name}', '{ntype}', now(), '{status}')")
        if ntype == 'D':
            self.applyliveobject(objid, newloname)
        return objid

    def renamenode(self, id, new):
        r = self.nrepo
        node = self.getnode(id)
        rootid = getrootid(r)
        if rootid == node['id']:
            self.status.pusherrmessage('Root node cannot be renamed!')
            return node
        if node['datasource']['type'] == 'T':
            self.status.pusherrmessage('A trash cannot be renamed!')
            return node
        pid = getnodeparentid(r, id)
        parent = self.getnode(pid)
        x = getnodeidfrompn(r, pid, new)
        if x!= None:
            self.status.pusherrmessage(f"{new} is already a child for node: {parent['name']}")
            return node
        r.execute(f"update nodes set name = '{new}' where id = {id}")
        del self.cache['nodes'][id]
        node = self.getnode(id)
        return node
    
    def movenode(self, pfrom, pto):
        r = self.nrepo
        fromnode = self.getnode(pfrom)
        if fromnode['datasource']['type'] == 'T':
            self.status.pusherrmessage('A trash cannot be moved!')
            return fromnode
        r.execute(f"update nodes set parent = {pto} where id = {pfrom}")
        status = [row['status'] for row in r.execute(f"select status from nodes where id = {pto}")][0]
        listnodes = getprogeny(r, pfrom)
        for rid in listnodes: r.execute(f"update nodes set status = '{status}' where id = {rid}")
        del self.cache['nodes'][pfrom]
        node = self.getnode(pfrom)
        return node

    def compareaddnode(self, fid, tid):
        r = self.nrepo
        fnode = self.getnode(fid)
        tnode = self.getnode(tid)
        if fnode['status'] == 'DELETED' or tnode['status'] == 'DELETED':
            self.status.pusherrmessage('A deleted element cannot be part of a compare operation!')
            return tnode
        for e in tnode['datasource']['producers']:
            if fid == e['id']:
                self.status.pusherrmessage(f"{fid}: this node is already included in the list of producers!")
                return tnode
        producers = tnode['datasource']['producers']
        producers.append(dict(path=getpath(self, r, fid), id=fid))
        self.getsource(tnode)
        r.execute(f"update nodes set type='C', producers='{json.dumps(producers)}' where id ={tid}")
        del self.cache['nodes'][tid]
        tnode = self.getnode(tid)
        self.getsource(tnode)
        return tnode

    def aggregateaddnode(self, fid, tid):
        r = self.nrepo
        fnode = self.getnode(fid)
        tnode = self.getnode(tid)
        if fnode['status'] == 'DELETED' or tnode['status'] == 'DELETED':
            self.status.pusherrmessage('A deleted element cannot be part of an aggreagte operation!')
            return tnode
        for e in tnode['datasource']['producers']:
            if fid == e['id']:
                self.status.pusherrmessage(f"{fid}: this node is already included in the list of producers!")
                return tnode
        producers = tnode['datasource']['producers']
        producers.append(dict(path=getpath(self, r, fid), id=fid))
        self.getsource(tnode)
        if 'aggregatorselector' not in tnode['datasource']:
            r.execute(f"update nodes set type='A', producers='{json.dumps(producers)}', aggregated=now(), aggregatorselector='{getpath(self, r, fid)}$', aggregatortake=1, aggregatortimefilter='.', aggregatorskip=0, aggregatorsort='desc', aggregatormethod='$none' where id ={tid}")
        else:
            r.execute(f"update nodes set producers='{json.dumps(producers)}', aggregated=now(), aggregatorselector='{tnode['datasource']['aggregatorselector']}|{getpath(self, r, fid)}$', aggregatortake={int(tnode['datasource']['aggregatortake'])+1} where id ={tid}")
        del self.cache['nodes'][tid]
        tnode = self.getnode(tid)
        self.getsource(tnode)
        return tnode
    
    def applyaggregator(self, id, aggregatorselector, aggregatortake, aggregatorskip, aggregatortimefilter, aggregatorsort, aggregatormethod):
        r = self.nrepo
        node = self.getnode(id)
        if node['datasource']['type'] in ['A']:
            if node['datasource']['aggregatormethod'] != aggregatormethod or node['datasource']['aggregatortimefilter'] != aggregatortimefilter:
                logger.info(f"Node: {id}, Type: {node['datasource']['type']}, deleting cache ...")
                self.deletecache(id)
        if node['datasource']['type'] in ['A', 'N']:  
            producers = self.expand(aggregatorselector, aggregatorsort, aggregatortake, aggregatorskip)
            for pid in [p['id'] for p in producers]:
                pnode = self.getnode(pid)
                ds = pnode['datasource']
                if pnode['datasource']['type'] in ['A']: self.applyaggregator(pid, ds['aggregatorselector'], ds['aggregatortake'], ds['aggregatorskip'], ds['aggregatortimefilter'], ds['aggregatorsort'], ds['aggregatormethod'])
            self.getsource(node)
            r.execute(f"update nodes set type='A', producers='{json.dumps(producers)}', aggregated=now(), aggregatorselector='{aggregatorselector}', aggregatortake={aggregatortake}, aggregatortimefilter='{aggregatortimefilter}', aggregatorskip={aggregatorskip}, aggregatorsort='{aggregatorsort}', aggregatormethod='{aggregatormethod}' where id ={id}")
        if node['datasource']['type'] in ['L']:
            cproducers = dict()
            producers = self.expand(aggregatorselector, aggregatorsort, aggregatortake, aggregatorskip)
            r.execute(f"update nodes set type='L', producers='{json.dumps(producers)}', aggregated=now(), aggregatorselector='{aggregatorselector}', aggregatortake={aggregatortake}, aggregatortimefilter='{aggregatortimefilter}', aggregatorskip={aggregatorskip}, aggregatorsort='{aggregatorsort}', aggregatormethod='{aggregatormethod}' where id ={id}")
            for p in producers:
                pchilds = getnodesidfromp(r, p['id'])
                for c in pchilds:
                    child = self.getnode(c)
                    if child['datasource']['type'] in ['B','D']:
                        if child['name'] not in cproducers:
                            cproducers[child['name']] = [dict(id=child['id'], path=getpath(self, r, child['id']))]
                        else:
                            cproducers[child['name']].append(dict(id=child['id'], path=getpath(self, r, child['id'])))
            nchilds = [self.getnode(x) for x in getnodesidfromp(r, id)]
            pnames = {x for x in cproducers.keys()}
            nnames = {x['name'] for x in nchilds}
            dids = {x['id'] for x in nchilds if x['name'] not in pnames}
            for e in dids:
                logger.info(f"Node: {id}, Type: {node['datasource']['type']}, deleting obsolete child: '{e}' ...")
                self.deletenode(e)
            for n in pnames - nnames:
                logger.info(f"Node: {id}, Type: {node['datasource']['type']}, creating new child: '{n}' ...")
                self.createnode(node['id'], n)
            nchilds = [self.getnode(x) for x in getnodesidfromp(r, id)]
            for c in nchilds:
                if 'aggregatormethod' in c['datasource'] and 'aggregatortimefilter' in c['datasource']:
                    if c['datasource']['aggregatormethod'] != aggregatormethod or c['datasource']['aggregatortimefilter'] != aggregatortimefilter:
                        logger.info(f"Node: {c['id']}, Type: {c['datasource']['type']}, deleting cache if exists ...")
                        self.deletecache(c['id'])
                tpath = [x['path'] for x in cproducers[c['name']]]
                aggregatorselector = '|'.join(tpath)
                r.execute(f"update nodes set type='A', producers='{json.dumps(cproducers[c['name']])}', aggregated=now(), aggregatorselector='{aggregatorselector}', aggregatortake={aggregatortake}, aggregatortimefilter='{aggregatortimefilter}', aggregatorskip={aggregatorskip}, aggregatorsort='{aggregatorsort}', aggregatormethod='{aggregatormethod}' where id ={c['id']}")
        del self.cache['nodes'][id]
        node = self.getnode(id)
        self.getsource(node)
        return node

    def linkfathernode(self, fid, tid):
        r = self.nrepo
        fnode = self.getnode(fid)
        tnode = self.getnode(tid)
        fpath = getpath(self, r, fid)
        if fnode['status'] == 'DELETED' or tnode['status'] == 'DELETED':
            self.status.pusherrmessage('A trash cannot be part of a link operation!')
            return tnode
        producers = tnode['datasource']['producers']
        if fid in [producer['id'] for producer in producers]:
            self.status.pusherrmessage(f'{fpath}: this node is already included in the list of producers!')
            return tnode
        producers.append(dict(path=getpath(self, r, fid), id=fid))
        if 'aggregatorselector' not in tnode['datasource']: r.execute(f"update nodes set type='L', producers='{json.dumps(producers)}', aggregated=now(), aggregatorselector='{getpath(self, r, fid)}$', aggregatortake=1, aggregatortimefilter='.', aggregatorskip=0, aggregatorsort='desc', aggregatormethod='$none' where id ={tid}")
        else: r.execute(f"update nodes set producers='{json.dumps(producers)}', aggregated=now(), aggregatorselector='{tnode['datasource']['aggregatorselector']}|{getpath(self, r, fid)}$', aggregatortake={int(tnode['datasource']['aggregatortake'])+1} where id ={tid}")
        del self.cache['nodes'][tid]
        tnode = self.getnode(tid)
        return tnode
    
    def applyliveobject(self, id, loname):
        r = self.nrepo
        liveobject = self.getliveobject(loname)
        node = self.getnode(id)
        if node['datasource']['type'] in ['D']: self.deletecache(id, default=False)
        self.createcache(id)
        cache = self.readcache(id)
        self.setschema(cache.name)
        extension = liveobject['extension']
        server = liveobject['id']
        options = liveobject['options']
        r.execute(f'drop server if exists {server} cascade')
        r.execute(f'create server {server} foreign data wrapper {extension} options ({options})')
        r.execute(f'grant usage on foreign server {server} to postgres')
        user = liveobject['user']
        password = liveobject['password']
        r.execute(f"create user mapping for postgres server {server} options (user '{user}', password '{password}')")
        collections = []
        for t in liveobject['tables']:
            description = liveobject['tables'][t]['description']
            if extension == 'oracle_fdw': request = liveobject['tables'][t]['request']
            if extension == 'postgres_fdw': schema = liveobject['tables'][t]['schema']
            desc = ", ".join(["%(k)s %(v)s" % dict(k=d, v=description[d]) for d in description])
            if extension == 'oracle_fdw': r.execute('create foreign table foreign_' + t + '(' + desc + ') server ' + server + " options (table '(" + request.replace("'", "''").replace('kairos_nodeid_to_be_replaced', str(id)) + ")')")
            if extension == 'postgres_fdw': r.execute('create foreign table foreign_' + t + '(' + desc + ') server ' + server + " options (schema_name '" + schema + "', table_name '" + t + "')")
            collections.append(t)
        self.setschema()
        r.execute(f"update nodes set type='D', aggregated=now(), liveobject='{loname}' where id = {id}")
        del self.cache['nodes'][id]
        node = self.getnode(id)
        return node

    def emptytrash(self):
        r = self.nrepo
        rootid = getrootid(r)
        trashid = getnodeidfrompn(r, rootid, 'Trash')
        again = True
        while again:
            again = False
            for rid in getprogeny(r, trashid):
                if rid != trashid:
                    node = self.getnode(rid)
                    self.countchildren(node)
                    deletable = True if node['kids'] == 0 else False
                    if deletable:
                        self.deletesource(rid)
                        self.deletecache(rid)
                        r.execute(f"delete from nodes where id = {rid}")
                    else: again = True
        r.execute(f"vacuum full sources")
        r.execute(f"vacuum full nodes")

    def getpath(self, id):
        r = self.nrepo
        return getpath(self, r, id)
    
    def expand(self, pattern, sort, take, skip):
        r = self.nrepo
        skip=int(skip)
        take=int(take)
        d=dict()
        rootid = getrootid(r)
        rootnode = self.getnode(rootid)
        for i in pattern.split('|'):
            nodes = [rootnode]
            for p in i.split('/')[1:]:
                newnodes = []
                for n in nodes:
                    for e in [self.getnode(x) for x in getnodesidfromp(r, n['id'])]:
                        if re.match(p, e['name']):
                            ds = e['datasource']
                            if e['datasource']['type'] == 'L': e = self.applyaggregator(e['id'], ds['aggregatorselector'], ds['aggregatortake'], ds['aggregatorskip'], ds['aggregatortimefilter'], ds['aggregatorsort'], ds['aggregatormethod'])
                            newnodes.append(e)
                nodes = newnodes
            for n in nodes: d[getpath(self, r, n['id'])] = n['id']
        result = [dict(path=k, id=d[k]) for k in sorted(d.keys())] if sort != 'desc' else [dict(path=k, id=d[k]) for k in sorted(d.keys(), reverse=True)][skip:skip+take]
        return result


    def getsource(self, node, getstream=False):
        if node['datasource']['type'] == 'B':
            if 'collections' not in node['datasource']: 
                source = self.readsource(node['id'], stream=getstream)
                if hasattr(source, 'rid'):
                    node['datasource']['uploaded'] = source.created
                    node['datasource']['collections'] = source.collections
                    if getstream: node['datasource']['stream'] = source.stream
            if 'stream' not in node['datasource'] and getstream:
                source = self.readsource(node['id'], stream=getstream)
                node['datasource']['stream'] = source.stream
        if node['datasource']['type'] in ['A', 'C']:
            if 'collections' not in node['datasource']:
                allparts = self.getallparts(node['id'])
                collections = set()
                for p in allparts:
                    pnode = self.getnode(p)
                    if pnode['datasource']['type'] in ['B', 'D']:
                        self.getsource(pnode)
                        collections = collections.union(set(pnode['datasource']['collections']))
                node['datasource']['collections'] = dict()
                for c in collections: node['datasource']['collections'][c] = dict()
    
    def readsource(self, id, stream=False):
        r = self.nrepo
        if stream: x = r.execute(f"select id as rid, to_char(created, 'YYYY-MM-DD HH24:MI:SS.MS') as created, collections, stream from sources where id = {id}")
        else: x = r.execute(f"select id as rid, to_char(created, 'YYYY-MM-DD HH24:MI:SS.MS') as created, collections from sources where id = {id}")
        o = Object()
        for rx in x:
            o.rid = rx['rid']
            o.created = rx['created']
            o.collections = json.loads(rx['collections'])
            if stream: o.stream = binascii.a2b_base64(rx['stream'])
        return o
    
    def downloadsource(self, id):
        r = self.nrepo
        node = self.getnode(id)
        self.getsource(node, getstream=True)
        filename = getpath(self, r, id)[1:].replace('/','_') + '.zip'
        return (filename, node['datasource']['stream'])

    @timing
    def unload(self, id):
        r = self.nrepo
        logger.info(f"Unloading node: {id} ...")
        path = getpath(self, r, id)
        archive = path.replace('/', '_')[1:] + '-unload.zip'
        fname = '/tmp/' + archive
        zip = Arcfile(fname, 'w:zip')
        cut = 10000
        self.buildcollectioncache(id, {'*'})
        node = self.getnode(id)
        self.getsource(node)
        self.getcache(node)
        schema = node['datasource']['cache']['name']
        self.setschema(schema)
        for collection in node['datasource']['collections']:
            logger.info(f"Unloading collection: {collection} ...")
            d = dict(collection=collection, desc=dict(), data=[])
            desc = OrderedDict()
            x = r.execute(f"select column_name, data_type from information_schema.columns where table_name = '{collection.lower()}' and table_schema = '{schema}'")
            for row in x.fetchall(): desc[row['column_name']] = row['data_type']
            request = 'select '
            for k in desc:
                if k != 'kairos_nodeid':
                    d['desc'][k] = desc[k]
                    request += k + ', '
            request = request[:-2] + ' from ' + collection
            recordset = 0
            nbrec = 0
            if len(desc) != 0:
                for x in r.execute(request):
                    nbrec += 1
                    res = dict()
                    for k in desc:
                        if k != 'kairos_nodeid': res[k] = x[k]
                    d['data'].append(res)
                    if nbrec == cut:
                        logger.info(f"Writing file: {collection}{recordset} ...")
                        zip.write(collection + str(recordset), json.dumps(d, sort_keys=True, indent=4))
                        recordset += 1
                        d['data']=[]
                        nbrec = 0
            if nbrec > 0: 
                logger.info(f"Writing file: {collection}{recordset} ...")
                zip.write(collection + str(recordset), json.dumps(d, sort_keys=True, indent=4))
        
        zip.close()
        logger.info(f"Unloading node: {id}, file is ready to download !")
        return (archive, open(fname, 'rb').read())

    def createcache(self, nid):
        r = self.nrepo
        schname = f'cache_{nid}'
        r.execute(f"create schema {schname}")
        r.execute("insert into caches (id, name, created, queries, collections) values(%s, %s, now(), %s, %s)", (nid, schname, json.dumps(dict()), json.dumps(dict())))
    
    def deletecache(self, nid, default=True):
        node = self.getnode(nid)
        if default and node['datasource']['type'] == 'D' and node['status'] == 'ACTIVE': self.applyliveobject(nid, node['datasource']['liveobject'])
        else:
            r = self.nrepo
            logger.info(f"Node: {nid}, deleting cache: cache_{nid} ...")
            r.execute(f"delete from caches where id = {nid}")
            with suppress(Exception): r.execute(f"drop schema cache_{nid} cascade")

    def getcache(self, node):
        if node['icon'] in ['A', 'B', 'C', 'D']:
            if 'name' not in node['datasource']['cache']:
                cache = self.readcache(node['id'])
                if hasattr(cache, 'rid'):
                    node['datasource']['cache']['collections'] = cache.collections
                    node['datasource']['cache']['queries'] = cache.queries
                    node['datasource']['cache']['name'] = cache.name

    def readcache(self, id):
        r = self.nrepo
        o = Object()
        for rx in r.execute(f"select id as rid, name, queries, to_char(created, 'YYYY-MM-DD HH24:MI:SS.MS') as created, collections from caches where id = {id}"):
            o.rid = rx['rid']
            o.name = rx['name']
            o.queries = json.loads(rx['queries'])
            o.created = rx['created']
            o.collections = json.loads(rx['collections'])
        return o

    def gettree(self, pid):
        r = self.nrepo
        root = True if pid == '0' else False
        if root:
            rootid = getrootid(r)
            root = self.getnode(rootid)
            (icon_file, icon_opened, icon_closed) = ficon(root)
            result = [dict(kids=True, id=root['id'], text='/', userdata=dict(type=ftype(root)), icons=dict(file=icon_file, folder_opened=icon_opened, folder_closed=icon_closed))]
        else:
            children = []
            for nid in getnodesidfromp(r, pid):
                node = self.getnode(nid)
                self.countchildren(node)
                (icon_file, icon_opened, icon_closed) = ficon(node)
                kids = True if node['kids'] > 0 else False
                children.append(dict(kids=kids, id=node['id'], text=node['name'], userdata=dict(type=ftype(node)), icons=dict(file=icon_file, folder_opened=icon_opened, folder_closed=icon_closed)))
            result = [dict(id=pid, items=sorted(children, key=getkey))]
        return result

    def getwholetree(self):
        r = self.nrepo
        result = dict()
        for row in r.execute(f"select id, parent, name, type from nodes"):result[row['id']]=dict(parent=row['parent'], name=row['name'], type=row['type'])
        return result
    
    def getcollections(self, id):
        node = self.getnode(id)
        self.getsource(node)
        data = []
        if node['datasource']['type'] == 'D':
            loname = node['datasource']['liveobject']
            liveobject = self.getliveobject(loname)
            for t in liveobject['tables']: data.append(dict(label=t))
        else:
            for collection in node['datasource']['collections']: data.append(dict(label=collection))
        return data

    def executequery(self, id, qname, limit):
        operations = self.schedulecacheoperations(id, 'query', qname)
        if self.status.errors > 0: return
        self.executecacheoperations(operations)
        if self.status.errors > 0: return
        result = self.queryexecute(id, qname, limit)
        return result

    def queryexecute(self, nid, qid, limit):
        r = self.nrepo
        node = self.getnode(nid)
        ntype = node['datasource']['type']
        logger.info(f"Node: {nid}, Type: {ntype}, executing query: '{qid}' ...")
        self.getcache(node)
        result = []
        if ntype in ['C', 'L']:
            for producer in node['datasource']['producers']:
                pid = producer['id']
                iresult = self.queryexecute(pid, qid, limit)
                if ntype in ['L']: result = iresult
                else: result.append(iresult)
        else:
            query = self.getquery(qid)
            query = dict(id=qid) if query==None else query
            if 'name' not in node['datasource']['cache']: 
                self.status.pusherrmessage(f"Cache for node id: {nid} doesn't exist!")
                return
            self.setschema(node['datasource']['cache']['name'])
            table = qid.lower()
            for b in r.execute(f"select exists(select * from information_schema.tables where table_schema = current_schema() and table_name = '{table}') foo"): existstable = b['foo']
            if existstable: 
                if 'filterable' in query and query['filterable']:
                    for x in r.execute(f"select * from {table} where label in (select label from (select label, sum(value) weight from {table} group by label order by weight desc limit {limit}) as foo)"):
                        result.append(x)
                else:
                    for x in r.execute(f"select * from {table}"):
                        result.append(x)
            else: self.status.pusherrmessage(f"Table {table.upper()} doesn't exist within schema {node['datasource']['cache']['name']}")
        return result
    
    def displaycollection(self, id, collection):
        self.buildcollectioncache(id, {collection})
        if self.status.errors > 0: return
        result = self.queryexecute(id, collection, 0)
        return result
    
    def exportdatabases(self, nodesdb):
        r = self.grepo
        run = Runner("localhost")
        if len(nodesdb) == 0:
            databases = getdatabases(r)
            nodesdb = [x for x in databases if 'kairos_user_' in x or 'kairos_group_' in x]
        for db in nodesdb:
            try:
                with suppress(Exception): shutil.rmtree(f'/export/{db}')
                run.local(f'mkdir -p /export/{db}')
                run.local(f'chmod 777 /export/{db}')
                command = f'su - postgres -c "pg_dump -Fd -vv -j {multiprocessing.cpu_count()} -f /export/{db}/database.dump {db}"'
                logger.info(command)
                result = run.local(command, hide=False)
                if result.failed:
                    self.status.pusherrmessage(f"Export of database {db} failed!")
                    logger.error(f'Result for {db}: {result.stderr}')
                else:
                    logger.info(f'Result for {db}: {result.stderr}')
            except Exception as e:
                logger.error(f"Error processing database {db}: {str(e)}")
                self.status.pusherrmessage(f"Error processing database {db}: {str(e)}")

    def importdatabases(self, nodesdb):
        r = self.grepo
        run = Runner("localhost")
        if len(nodesdb) == 0:
            for d in os.listdir('/export'):
                wdir = f'/export/{d}'
                if 'kairos_' in d and os.path.isdir(wdir): nodesdb.append(d)
        for db in nodesdb:
            try:
                r.execute(f"UPDATE pg_database SET datallowconn = 'false' WHERE datname = '{db}'")
                r.execute(f"SELECT pg_terminate_backend(pid) FROM pg_stat_activity WHERE datname = '{db}'")
                logger.info(f"Dropping database: {db}")
                run.local(f"su - postgres -c \"psql -c 'DROP DATABASE IF EXISTS {db}'\"", hide=False)
                logger.info(f"Creating database: {db}")
                run.local(f"su - postgres -c \"psql -c 'CREATE DATABASE {db}'\"", hide=False)
                logger.info(f"Restoring database: {db}")
                command = f'su - postgres -c "pg_restore -vv -j {multiprocessing.cpu_count()} -d {db} /export/{db}/database.dump"'
                logger.info(command)
                result = run.local(f"{command}", hide=False)
                if result.failed:
                    self.status.pusherrmessage(f"Import of database {db} failed!")
                    logger.error(f'Result for {db}: {result.stderr}')
                else:
                    logger.info(f'Result for {db}: {result.stderr}')
                    r.execute(f"UPDATE pg_database SET datallowconn = 'true' WHERE datname = '{db}'")
                    logger.info(f"Connections are now possibles on imported database {db}.")
            except Exception as e:
                logger.error(f"Error processing database {db}: {str(e)}")
                self.status.pusherrmessage(f"Error processing database {db}: {str(e)}")


    def clearprogenycaches(self, id):
        r = self.nrepo
        for nid in getprogeny(r, id): self.deletecache(nid)

    def buildprogenycaches(self, id):
        run = Runner("localhost")
        r = self.nrepo
        for nid in getprogeny(r, id):
            command = f'kairos -s buildallcollectioncaches  --nodesdb {self.nodesdb} --systemdb {self.systemdb} --id {nid}'
            logger.info(command)
            result = run.local(f"{command}", hide=True)
            if result.failed: self.status.pusherrmessage(f"Build cache failed for node id: {nid}")
            else: logger.info(f"Cache built successfully for node id: {nid}")

    def getBchildren(self, id):
        r = self.nrepo
        data = [nid for nid in getprogeny(r, id) if self.getnode(nid)['datasource']['type'] == 'B']
        return data

    def buildcollectioncache(self, id, collections):
        node = self.getnode(id)
        ntype = node['datasource']['type']
        if ntype in ['N', 'L', 'C', 'T']: return
        self.getsource(node)
        if '*' in collections: collections = {k for k in node['datasource']['collections']}
        operations = self.schedulecacheoperations(id, 'buildcollectioncache', collections)
        if self.status.errors > 0: return
        self.executecacheoperations(operations)

    def dropcollectioncache(self, id, collections):
        node = self.getnode(id)
        self.getcache(node)
        operations = self.schedulecacheoperations(id, 'dropcollectioncache', collections)
        if self.status.errors > 0: return
        self.executecacheoperations(operations)

    def buildquerycache(self, nid, qid):
        r = self.nrepo
        node = self.getnode(nid)
        query = self.getquery(qid)
        if query == None: return
        self.getcache(node)
        ntype = node['datasource']['type']
        logger.info(f"Node: {nid}, Type: {ntype}, checking query cache: '{qid}' ...")
        if ntype in ['A', 'B', 'D']:
            todo = True if qid not in node['datasource']['cache']['queries'] else False
            todo = True if "nocache" in query and query["nocache"] else todo            
            for collection in query['collections']:
                for part in node['datasource']['cache']['collections'][collection]:
                    todo = True if qid in node['datasource']['cache']['queries'] and node['datasource']['cache']['queries'][qid] < node['datasource']['cache']['collections'][collection][part] else todo
            if todo:
                self.setschema(node['datasource']['cache']['name'])
                table = qid
                logger.info(f"Node: {nid}, Type: {ntype}, removing old query cache: '{qid}' ...")
                r.execute(f"drop table if exists {table}")
                logger.info(f"Node: {nid}, Type: {ntype}, building new query cache: '{qid}' ...")
                if 'userfunctions' in query:
                    for ufn in query['userfunctions']:
                        self.setschema()
                        uf = self.getfunction(ufn)
                        self.setschema(node['datasource']['cache']['name'])
                        r.execute(uf["function"])
                try: r.execute(f"create table {table} as select * from ({query['request']}) as foo")
                except: 
                    self.status.pusherrmessage(f"Check if data exists for collections: {query['collections']}")
                    return
                node['datasource']['cache']['queries'][qid] = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                logger.info(f"Node: {nid}, Type: {ntype}, updating cache with query info: '{qid}' ...")
                self.setschema()
                r.execute(f"update caches set queries = '{json.dumps(node['datasource']['cache']['queries'])}' where id = {nid}")
                del self.cache['nodes'][nid]
                node = self.getnode(nid)
                self.getcache(node)
            else: logger.info(f"Node: {nid}, Type: {ntype}, nothing to do for query cache: '{qid}' ...")
    
    def getallparts (self, id, v=None):
        d = dict()
        node = self.getnode(id)
        self.getcache(node)
        d[id] = v
        if node['datasource']['type'] in ['A', 'C']:
            producers = node['datasource']['producers']
            for p in producers:
                d[p['id']] = id
                dp = self.getallparts(p['id'], id)
                for x in dp: d[x] = dp[x]
        return d
    
    def schedulecacheoperations(self, id, type, name, recursive=False):
        operations = []
        r = self.nrepo
        node = self.getnode(id)
        ntype = node['datasource']['type']

        if type == 'buildcollectioncache':
            collections = name
            oldparts = self.getallparts(id)
            ds = node['datasource']
            if ntype in ['A']: node = self.applyaggregator(id, ds['aggregatorselector'], ds['aggregatortake'], ds['aggregatorskip'], ds['aggregatortimefilter'], ds['aggregatorsort'], ds['aggregatormethod'])
            newparts = self.getallparts(id)
            for p in set(oldparts) - set(newparts): 
                operations.append(dict(operation='removepart', nid=oldparts[p], part=p, collections=collections))
            ranks = dict()
            for p in set(newparts):
                dp = depthp(newparts, p)
                if dp not in ranks: ranks[dp] = [p]
                else: ranks[dp].append(p)
            for r in sorted(set(ranks), reverse=True):
                for p in ranks[r]:
                    node = self.getnode(p)
                    if node['datasource']['type'] in ['A']:
                        for x in [e['id'] for e in node['datasource']['producers']]:
                            if p not in set(newparts) - set(oldparts):
                                operations.append(dict(operation='checkpart', nid=p, part=x, collections=collections))
                                operations.append(dict(operation='removepart', nid=p, part=x, collections=None))
                                operations.append(dict(operation='createpartA', nid=p, part=x, collections=None))
                            else:
                                operations.append(dict(operation='createpartA', nid=p, part=x, collections=collections))
                    if node['datasource']['type'] in ['B', 'D']:
                        operations.append(dict(operation='checkpart', nid=p, part=p, collections=collections))
                        operations.append(dict(operation='removepart', nid=p, part=p, collections=None))
                        operations.append(dict(operation='createpart' + node['datasource']['type'], nid=p, part=p, collections=None))

        if type == 'dropcollectioncache':
            collections = name
            operations.append(dict(operation='removetable', nid=id, part=id, collections=collections))

        if type == 'query':
            query = self.getquery(name)
            if query == None: return
            collections = set(query['collections'])
            operations = self.schedulecacheoperations(id, 'buildcollectioncache', collections, recursive=True)
            if ntype in 'C':
                for p in node['datasource']['producers']:
                    operations.append(dict(operation='buildquerycache', nid=p['id'], qid=name))
            else: operations.append(dict(operation='buildquerycache', nid=id, qid=name))

        if type == 'chart':
            chart = self.getchart(name)
            if chart == None: return
            queries = set()
            queries.add(chart['reftime'])
            for y in chart['yaxis']:
                for r in y['renderers']:
                    for d in r['datasets']:
                        queries.add(d['query'])
            collections = set()
            for q in queries:
                query = self.getquery(q)
                if query == None:
                    self.status.pusherrmessage(f"Query '{q}' doesn't exist!")
                    return
                if 'nocache' in query and query['nocache']: self.nocache = True
                for e in query['collections']: collections.add(e)
            operations = self.schedulecacheoperations(id, 'buildcollectioncache', collections, recursive=True)
            for q in queries:
                if ntype in 'C':
                    for p in node['datasource']['producers']:
                        operations.append(dict(operation='buildquerycache', nid=p['id'], qid=q))
                else: operations.append(dict(operation='buildquerycache', nid=id, qid=q))

        if not recursive:
            logger.info('Sheduled operations:')
            for operation in operations:
                if operation['operation'] in ['checkpart', 'removepart', 'removetable', 'createpartA', 'createpartB', 'createpartD']: logger.info(f"Node: {operation['nid']}, Operation: {operation['operation']}, Partition: {operation['part']}, Collections: {operation['collections']}")
                if operation['operation'] in ['buildquerycache']: logger.info(f"Node: {operation['nid']}, Operation: {operation['operation']}, Query: {operation['qid']}")
        return operations
    
    def executecacheoperations(self, operations):
        for operation in operations:
            if operation['operation'] == 'checkpart': self.checkpart(operation['nid'], operation['part'], operation['collections'])
            if operation['operation'] == 'removepart': self.removepart(operation['nid'], operation['part'], operation['collections'])
            if operation['operation'] == 'removetable': self.removetable(operation['nid'], operation['part'], operation['collections'])
            if operation['operation'] == 'createpartA': self.createpartA(operation['nid'], operation['part'], operation['collections'])
            if operation['operation'] == 'createpartB': self.createpartB(operation['nid'], operation['part'], operation['collections'])
            if operation['operation'] == 'createpartD': self.createpartD(operation['nid'], operation['part'], operation['collections'])
            if operation['operation'] == 'buildquerycache': self.buildquerycache(operation['nid'], operation['qid'])
            if self.status.errors > 0: 
                logger.error('Breaking scheduled operations!')
                break

    def checkpart(self, nid, part, collections):
        node = self.getnode(nid)
        self.getcache(node)
        nodecache = node['datasource']['cache']
        if 'name' not in nodecache: self.createcache(nid)
        self.getcache(node)
        cachecol = node['datasource']['cache']['collections']
        ntype = node['datasource']['type']
        self.removecollections = set()
        self.createcollections = set()
        pnode = self.getnode(part)
        self.getcache(pnode)
        pcachecol = pnode['datasource']['cache']['collections']

        if ntype in ['A']:
            for collection in collections:
                logger.info(f"Node: {nid}, Type: {ntype}, checking partition cache: {part} for collection: '{collection}' ...")
                todo = False
                datepart = cachecol[collection][str(part)] if collection in cachecol and str(part) in cachecol[collection] else None
                if collection not in pcachecol: continue
                datesource = max([pcachecol[collection][x]  for x in  pcachecol[collection]])
                todo = True if datepart == None else todo
                todo = True if datepart != None and datepart < datesource else todo
                if todo: 
                    logger.warning(f"Node: {nid} ({getpath(self, self.nrepo, nid)}) must be built or built again for partition {part} ({getpath(self, self.nrepo, part)}) and collection {collection}!")
                    self.removecollections.add(collection)
                    self.createcollections.add(collection)

        if ntype in ['B']:
            self.getsource(node)
            for collection in collections:
                logger.info(f"Node: {nid}, Type: {ntype}, checking collection cache: '{collection}' ...")
                if collection not in node['datasource']['collections']: continue
                analyzername = node['datasource']['collections'][collection]['analyzer']
                analyzer = self.getanalyzer(analyzername)
                datepart = cachecol[collection][str(nid)] if collection in cachecol and str(nid) in cachecol[collection] else None
                todo = False
                todo = True if datepart == None else todo
                todo = True if datepart != None and node['datasource']['uploaded'] > datepart else todo
                todo = True if datepart != None and analyzer['created'] > datepart else todo
                if todo:
                    logger.warning(f"Node: {nid} ({getpath(self, self.nrepo, nid)}) must be built or built again for collection {collection}!")
                    self.removecollections.add(collection)
                    self.createcollections.add(collection)

        if ntype in ['D']:
            liveobject = self.getliveobject(node['datasource']['liveobject'])
            try: timeout = liveobject['retention']
            except: timeout = 60
            for collection in collections:
                logger.info(f"Node: {nid}, Type: {ntype}, checking collection cache: '{collection}' ...")
                todo = False
                datepart = cachecol[collection][str(nid)] if collection in cachecol and str(nid) in cachecol[collection] else None
                todo = True if datepart == None else todo
                todo = True if datepart != None and (datetime.now() - datetime.strptime(datepart, '%Y-%m-%d %H:%M:%S.%f')).seconds > timeout else todo
                if todo: 
                    logger.warning(f"Node: {nid} ({getpath(self, self.nrepo, nid)}) must be built or built again for collection {collection}!")
                    self.removecollections.add(collection)
                    self.createcollections.add(collection)

    def removetable(self, nid, part, collections):
        r = self.nrepo
        node = self.getnode(nid)
        self.getcache(node)
        ntype = node['datasource']['type']
        if collections == None: collections = self.removecollections
        if 'name' in node['datasource']['cache']:
            self.setschema(node['datasource']['cache']['name'])
            for collection in collections:
                logger.info(f"Node: {nid}, Type: {ntype}, removing table: {nid} for collection: '{collection}' ...")
                r.execute("drop table if exists " + collection)
        if 'collections' in node['datasource']['cache']:
            for collection in collections:
                if collection in node['datasource']['cache']['collections']: del node['datasource']['cache']['collections'][collection]
            self.setschema()
            r.execute(f"update caches set collections = '{json.dumps(node['datasource']['cache']['collections'])}' where id = {nid}")
            del self.cache['nodes'][nid]
            node = self.getnode(nid)
            self.getcache(node)


    def removepart(self, nid, part, collections):
        r = self.nrepo
        node = self.getnode(nid)
        self.getcache(node)
        ntype = node['datasource']['type']
        if collections == None: collections = self.removecollections
        if 'name' in node['datasource']['cache']:
            self.setschema(node['datasource']['cache']['name'])
            for collection in collections:
                logger.info(f"Node: {nid}, Type: {ntype}, removing partition: {part} for collection: '{collection}' ...")
                if ntype in ['A']:
                    partition = f'{collection}_{part}'
                    r.execute(f"drop table if exists {partition}")
                else:
                    r.execute(f"drop table if exists {collection}")
        if 'collections' in node['datasource']['cache']:
            for collection in collections:
                if collection in node['datasource']['cache']['collections']:
                    if part in node['datasource']['cache']['collections'][collection]: del node['datasource']['cache']['collections'][collection][part]
            self.setschema()
            r.execute(f"update caches set collections = '{json.dumps(node['datasource']['cache']['collections'])}' where id = {nid}")

    def createpartA(self, nid, part, collections):
        if collections == None: collections = self.createcollections
        if len(collections) == 0: return
        r = self.nrepo
        nodesdb = self.nodesdb
        node = self.getnode(nid)
        self.getcache(node)
        ntype = node['datasource']['type']
        logger.info(f"Node: {nid}, Type: {ntype}, building new partition cache: {part} for collections '{collections}' ...")
        self.setschema()
        function = self.getaggregator(node['datasource']['aggregatormethod'])
        meet = self.getfunction('meet')
        x = r.execute(f"select distinct table_name from information_schema.columns where table_schema='{node['datasource']['cache']['name']}'")
        schdesc = [row['table_name'] for row in x.fetchall()]
        pnode = self.getnode(part)
        self.getcache(pnode)
        inschname = pnode['datasource']['cache']['name']
        x = r.execute(f"select distinct table_name from information_schema.columns where table_schema='{inschname}'")
        inschdesc = [row['table_name'] for row in x.fetchall()]
        queues = dict()
        tabledesc = dict()
        queues['ERROR_QUEUE'] = multiprocessing.Queue()
        self.setschema(node['datasource']['cache']['name'])
        for collection in collections:
            if collection.lower() not in inschdesc: continue
            if collection.lower() not in schdesc:
                request = f"select column_name, data_type from information_schema.columns where table_name = '{collection.lower()}' and table_schema = '{pnode['datasource']['cache']['name']}'"
                coldesc = ', '.join([row['column_name'] + ' ' + row['data_type'] for row in r.execute(request)])
                request = f"create table {collection.lower()} ({coldesc}) partition by list(kairos_nodeid)"
                r.execute(request)
            pname = f'{collection}_{part}'
            request = f"create table {pname.lower()} partition of {collection.lower()} for values in ('{part}')"
            r.execute(request)
            tabledesc[collection] = OrderedDict()
            x = r.execute(f"select column_name, data_type from information_schema.columns where table_name = '{collection.lower()}' and table_schema = '{node['datasource']['cache']['name']}'")
            for row in x.fetchall(): tabledesc[collection][row['column_name']] = row['data_type']
            queues[collection] = multiprocessing.Queue()

        def write_to_queue(collection):
            try:
                logger.info(f"Node: {nid}, Type: {ntype}, building partition: {part} for collection: '{collection}' ...")
                pnode = self.getnode(part)
                self.getcache(pnode)
                inschname = pnode['datasource']['cache']['name']
                lgby = [k for k in tabledesc[collection] if tabledesc[collection][k] == 'text']
                lavg = [k for k in tabledesc[collection] if tabledesc[collection][k] == 'real']
                lsum = [k for k in tabledesc[collection] if tabledesc[collection][k] in ['integer', 'bigint']]
                where = f" where meet(timestamp,'{node['datasource']['aggregatortimefilter']}') or timestamp='00000000000000000'" if 'timestamp' in lgby else ' '
                subrequest = f"select * from {inschname}.{collection.lower()}{where}"
                request = "select "
                for x in lgby: request = request + function["name"] + '(timestamp) as timestamp, ' if x == "timestamp" else request + x + ', '
                for x in lavg: request += 'sum(coalesce(' + x + ', 0)) as ' + x + ', '
                for x in lsum: request += 'sum(' + x + ') as ' + x + ', '
                request = request[:-2] + ' from (' + subrequest + ') as foo group by '
                for x in lgby: request = request + function["name"] + '(timestamp), ' if x == 'timestamp' else request + x + ', '
                request = request[:-2]
                workrequest = f'select {function["name"]}(timestamp) as timestamp, kairos_nodeid, count(*) num from (select distinct timestamp, kairos_nodeid from {inschname}.{collection}{where}) as foo group by {function["name"]}(timestamp), kairos_nodeid'
                divisor = dict()
                context = Context(nodesdb=nodesdb)
                context.setschema(node['datasource']['cache']['name'])
                context.nrepo.execute(function["function"])
                context.nrepo.execute(meet["function"])
                if 'timestamp' in lgby:  
                    for x in context.nrepo.execute(workrequest).fetchall(): divisor[x['timestamp'] + x ['kairos_nodeid']] = x['num']
                if len(lgby) > 0:
                    for row in context.nrepo.execute(request).fetchall():
                        record = ''
                        if 'timestamp' in lgby:
                            for x in lavg: row[x] = row[x] * 1.0 / divisor[row['timestamp'] + row['kairos_nodeid']]
                        for k in tabledesc[collection].keys(): record += '\\N\t' if row[k] == None else str(row[k] if k != 'kairos_nodeid' else part).replace('\n','\\n').replace('\t','\\t').replace('\r', '').replace('\\', '\\\\') + '\t'
                        record = record[:-1] + '\n'
                        queues[collection].put(record)
                context.free()
            except: self.status.pusherrmessage(str(sys.exc_info()[1]))

        def read_from_queue(collection):
            context = Context(nodesdb=nodesdb)
            context.setschema(node['datasource']['cache']['name'])
            buffer = StringIO()
            bufferempty = True
            counter = 0
            partname = f'{collection}_{part}'
            try: limit = int(os.environ['BUFFER'])
            except: limit = 10000
            globalcounter = 0
            while True:
                try:
                    record = queues[collection].get()
                    if record == 'KAIROS_DONE': break
                    bufferempty = False
                    counter += 1
                    logger.debug(f'Buffer content at line: {counter}, record: {record}')
                    buffer.write(record)
                    if counter == limit:
                        buffer.seek(0)
                        logger.info(f"Writing {counter} records to partition: {partname}...")
                        context.nrepo.copy(buffer, partname, tuple(tabledesc[collection].keys()))
                        buffer = StringIO()
                        globalcounter += counter
                        counter = 0
                        bufferempty = True
                except:
                    self.status.pusherrmessage(str(sys.exc_info()[1]))
                    queues['ERROR_QUEUE'].put(collection)
                    buffer = StringIO()
                    counter = 0
                    bufferempty = True
            if not bufferempty:
                try:
                    buffer.seek(0)
                    logger.info(f"Writing {counter} records to partition: {partname}...")
                    context.nrepo.copy(buffer, partname, tuple(tabledesc[collection].keys()))
                    globalcounter += counter
                except:
                    self.status.pusherrmessage(str(sys.exc_info()[1]))
                    queues['ERROR_QUEUE'].put(collection)
            logger.info(f"Partition: {partname}: {globalcounter} records have been written! ")
            context.free()
        
        try:
            for collection in queues:
                if collection == 'ERROR_QUEUE': continue
                pr = Parallel(read_from_queue, workers = 1)
                pw = Parallel(write_to_queue, workers = 1)
                pr.push(collection)
                pw.push(collection)
                pw.join()
                queues[collection].put('KAIROS_DONE')
                pr.join()
                if not queues['ERROR_QUEUE'].empty():
                    self.status.pusherrmessage('At least one error found during collection cache bu@ilding! See KAIROS.LOG for more information!')
                else:
                    if collection not in node['datasource']['cache']['collections']: node['datasource']['cache']['collections'][collection] = dict()
                    node['datasource']['cache']['collections'][collection][part] = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
                    queues[collection].close()
                    queues[collection].join_thread()
            queues['ERROR_QUEUE'].close()
            queues['ERROR_QUEUE'].join_thread()
            logger.info(f"Node: {nid}, Type: A, updating cache with collections info: '{collections}' ...")
            self.setschema()
            r.execute(f"update caches set collections = '{json.dumps(node['datasource']['cache']['collections'])}' where id = {nid}")
            del self.cache['nodes'][nid]
            node = self.getnode(nid)
            self.getcache(node)

        except: self.status.pusherrmessage(str(sys.exc_info()[1]))
        del queues

    def createpartB(self, nid, part, collections):
        if collections == None: collections = self.createcollections
        if len(collections) == 0: return

        r = self.nrepo
        self.setschema()
        node = self.getnode(nid)
        self.getsource(node, getstream=True)
        queues = dict()
        writeheader = dict()
        readheader = dict()
        members = dict()
        queues['ERROR_QUEUE'] = multiprocessing.Queue()

        for collection in collections:
            queues[collection] = multiprocessing.Queue()
            writeheader[collection] = True
            readheader[collection] = True
            for member in node['datasource']['collections'][collection]['members']: members[member] = self.getanalyzer( node['datasource']['collections'][collection]['analyzer'])
        
        logger.info(f"Node: {nid}, Type: B, building collections caches for collections: '{collections}' ...")

        def write_to_queue(col, d, v, n):
            logger.debug(f'Writing to queue the following collection: {col}')
            if writeheader[col]:
                record = json.dumps(dict(header='KAIROS_START', desc=d)) 
                queues[col].put(record)
                writeheader[col] = False
            v = v if type(v) == type([]) else [v]
            trf = lambda x: str(x).replace('\n','\\n').replace('\t','\\t').replace('\r', '').replace('\\', '\\\\')
            for e in v:
                record = ''
                e['kairos_nodeid'] = nid
                for k in sorted(e.keys()):
                    if e[k] == '': record = f'{record}\\N\t'
                    else: record = f'{record}{trf(e[k])}\t'
                record = f'{record[:-1]}\n'
                queues[col].put(record)

        def read_from_queue(col):
            buffer = StringIO()
            bufferempty = True
            counter = 0
            limit = 10000
            globalcounter = 0
            context = Context(nodesdb=self.nodesdb)
            context.setschema(node['datasource']['cache']['name'])

            while True:
                try:
                    record = queues[col].get()
                    if record == 'KAIROS_DONE': break
                    with suppress(Exception): record = json.loads(record)
                    if type(record) == type(dict()) and 'header' in record and record['header'] == 'KAIROS_START':
                        if readheader[col]:
                            record['desc']['kairos_nodeid'] = 'text'
                            request = f'create table {col}('
                            description= sorted(record['desc'].keys())
                            for k in description: request += f'{k} {record["desc"][k]}, '
                            request = f'{request[:-2]})'
                            context.nrepo.execute(request)
                            readheader[col] = False
                    else:
                        bufferempty = False
                        counter += 1
                        logger.debug(f'Buffer content at line: {counter}, record: {record}')
                        buffer.write(record)
                        if counter == limit:
                            buffer.seek(0)
                            logger.info(f"Writing {counter} records to collection: {col}...")
                            context.nrepo.copy(buffer, col, tuple(description))
                            buffer = StringIO()
                            globalcounter += counter
                            counter = 0
                            bufferempty = True
                except:
                    self.status.pusherrmessage(str(sys.exc_info()[1]))
                    queues['ERROR_QUEUE'].put(col)
                    buffer = StringIO()
                    counter = 0
                    bufferempty = True
            if not bufferempty:
                try:
                    buffer.seek(0)
                    logger.info(f"Writing {counter} records to collection: {col}...")
                    context.nrepo.copy(buffer, col, tuple(description))
                    globalcounter += counter
                    logger.info(f"Collection: {col}: {globalcounter} records have been written! ")
                except:
                    self.status.pusherrmessage(str(sys.exc_info()[1]))
                    queues['ERROR_QUEUE'].put(col)
            context.free()
                            
        thezip = zipfile.ZipFile(BytesIO(node['datasource']['stream']))
        logger.info(f'Analyzing archive attached to node {nid}...')
        listen = write_to_queue

        def do(member):
            if member in members:
                analyzer = Analyzer(members[member], set(collections), listen, nid)
                logger.info(f'Analyzing member: {member}...')


















                status = analyzer.analyze(thezip.read(member), member)
                if status.error: queues['ERROR_QUEUE'].put(member)
                return None

        limit = multiprocessing.cpu_count()

        try:
            pr = Parallel(read_from_queue, workers=len(collections))
            for collection in collections: pr.push(collection)
            pw = Parallel(do, workers = limit)
            for e in thezip.namelist(): pw.push(e)
            pw.join()
            thezip.close()
            for collection in collections: queues[collection].put('KAIROS_DONE')
            pr.join()
            if not queues['ERROR_QUEUE'].empty(): self.status.pusherrmessage('At least one error found during collection cache building! See KAIROS.LOG for more information!')
            else:
                for collection in collections:
                    if collection not in node['datasource']['cache']['collections']: node['datasource']['cache']['collections'][collection] = dict()
                    node['datasource']['cache']['collections'][collection][nid] = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            for collection in collections: 
                queues[collection].close()
                queues[collection].join_thread()
            queues['ERROR_QUEUE'].close()
            queues['ERROR_QUEUE'].join_thread()
            logger.info(f"Node: {nid}, Type: B, updating cache with collections info: '{collections}' ...")
            self.setschema()
            r.execute(f"update caches set collections = '{json.dumps(node['datasource']['cache']['collections'])}' where id = {nid}")
            del self.cache['nodes'][nid]
            node = self.getnode(nid)
            self.getcache(node)

        except: self.status.pusherrmessage(str(sys.exc_info()[1]))
        del queues

    def createpartD(self, nid, part, collections):
        if collections == None: collections = self.createcollections
        r = self.nrepo
        node = self.getnode(nid)
        self.getcache(node)
        ntype = node['datasource']['type']
        self.setschema(node['datasource']['cache']['name'])
        for collection in collections:
            logger.info(f"Node: {nid}, Type: {ntype}, building new collection cache: '{collection}' ...")
            r.execute(f"create table {collection} as select '{nid}'::text as kairos_nodeid, * from foreign_{collection}")
            if collection not in node['datasource']['cache']['collections']: node['datasource']['cache']['collections'][collection] = dict()
            node['datasource']['cache']['collections'][collection][nid] = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
        logger.info(f"Node: {nid}, Type: D, updating cache with collections info: '{collections}' ...")
        self.setschema()
        r.execute(f"update caches set collections = '{json.dumps(node['datasource']['cache']['collections'])}' where id = {nid}")
        del self.cache['nodes'][nid]
        node = self.getnode(nid)
        self.getcache(node)

    def getchartcache(self, id, timeout):
        repository = self.nrepo

        class ChartCache:

            def __init__(self):
                self.timeout = timeout
                self.repository = repository
                self.cachename = f'cache_{id}'
                self.repository.setschema(self.cachename)
                x = self.repository.execute(f"select distinct table_name from information_schema.columns where table_schema='{self.cachename}'")
                if len([row['table_name'] for row in x.fetchall() if row['table_name'] == 'chartcache']) == 0: self.repository.execute("create table chartcache(k text primary key, v text)")

            def get(self, key):
                self.repository.setschema(self.cachename)
                ckey = hashlib.md5(json.dumps(key).encode('utf-8')).hexdigest()
                x = self.repository.execute(f"select v from chartcache where k = '{ckey}'")
                lvalues = [row['v'] for row in x.fetchall()]
                if len(lvalues) == 0: return None
                jsonvalueout = lvalues[0]
                valueout = json.loads(jsonvalueout)
                now = int(datetime.now().strftime('%s'))
                timestamp = int(valueout['timestamp'])
                if now - timestamp > self.timeout: return None
                else: return valueout['value']

            def set(self, key, valuein):
                self.repository.setschema(self.cachename)
                ckey = hashlib.md5(json.dumps(key).encode('utf-8')).hexdigest()
                x = self.repository.execute(f"select v from chartcache where k = '{ckey}'")
                lvalues = [row['v'] for row in x.fetchall()]
                valueout = json.dumps(dict(timestamp=datetime.now().strftime('%s'), value=valuein)).replace("'","''")
                if len(lvalues) == 0: self.repository.execute(f"insert into chartcache (k, v) values ('{ckey}', '{valueout}')")
                else:self.repository.execute(f"update chartcache set v = '{valueout}' where k ='{ckey}'")
        
        return ChartCache()

    def runchart(self, id, chart, width, height, limit, colors, plotorientation, template, toggle):
        r = self.nrepo
        node = self.getnode(id)
        self.getcache(node)
        nodecache = node['datasource']['cache']
        if 'name' not in nodecache: self.createcache(id)
        self.getcache(node)
        timeout = 3600
        if node['datasource']['type'] == 'D': 
            liveobject = self.getliveobject(node['datasource']['liveobject'])
            try: timeout = liveobject['retention']
            except: timeout = 60
        chartcache = self.getchartcache(id, timeout)
        ckey = dict(chart=chart, limit=limit, colors=colors, plotorientation=plotorientation, template=template, toggle=toggle)
        jsonchart = chartcache.get(ckey)
        if jsonchart:
            chartobj = json.loads(jsonchart)
            fig = chartobj['figure']
            rows = chartobj['rows']
        else:
            self.setschema()
            template = self.gettemplate(template)
            colors = self.getcolors(colors)['colors']
            operations = self.schedulecacheoperations(id, 'chart', chart)
            if self.status.errors > 0: return
            self.executecacheoperations(operations)
            if self.status.errors > 0: return
            co=dict(rows=1, cols=1, isarray=False, shared_yaxes=False, shared_xaxes=False, layoutoptions=dict(), xaxis=dict(), yaxis=dict(), alreadyright=dict(), alreadyleft=dict(), traces=dict(), pies=dict())
            chart = self.getchart(chart)
            result = self.queryexecute(id, chart['reftime'], limit)
            if self.status.errors > 0: return
            reftimedf = gettimestampdf(result, co, plotorientation)
            co['shared_yaxes'] = True if plotorientation == 'horizontal' else False
            co['shared_xaxes'] = True if plotorientation == 'vertical' else False
            getnewaxis(co, reftimedf, template, axistype='x', index=0)
            if co['shared_yaxes']:
                i = 1
                for e in reftimedf[1:]: 
                    getnewaxis(co, reftimedf, template, axistype='x', index=i)
                    i += 1
                co['cols'] = i
            if co['shared_xaxes']: co['rows'] = len(reftimedf)
            fig = plotly.tools.make_subplots(rows=co['rows'], cols=co['cols'], shared_yaxes=co['shared_yaxes'], shared_xaxes=co['shared_xaxes'], subplot_titles=tuple(getchartproducers(node)))
            for e in template['layout']: co['layoutoptions'][e] = template['layout'][e].copy() if type(template['layout'][e]) == type(dict()) else template['layout'][e]
            co['layoutoptions']['title']['text'] = chart['title']
            co['layoutoptions']['width'] = width
            co['numyaxis'] = 0
            events = dict()
            for y in chart['yaxis']:
                co['numyaxis'] += 1
                idxy = []
                if co['shared_yaxes']: 
                    idxy.append(getnewaxis(co, reftimedf, template, axistype='y', options=y, index=0))
                else:
                    for i in range(co['rows']): idxy.append(getnewaxis(co, reftimedf, template, axistype='y', options=y, index=i))
                for r in y['renderers']:
                    if toggle:
                        a = None
                        if r['type'] == 'WA': a = 'SA'
                        if r['type'] == 'SA': a = 'WA'
                        if a: r['type'] = a
                    co['pielabels'] = dict()
                    co['pievalues'] = dict()
                    co['piecolors'] = dict()
                    for d in r['datasets']:
                        alreadyinlegend = dict()
                        result = self.queryexecute(id, d['query'], limit)
                        if self.status.errors > 0: return
                        datasetdf = gettimestampdf(result, co, plotorientation)
                        try: labeldf = [x.groupby('label')[['value']].sum() for x in datasetdf]
                        except: labeldf = []
                        ascending = 0
                        i = 0
                        for e in labeldf:
                            if i not in co['pielabels']: co['pielabels'][i] = []
                            if i not in co['pievalues']: co['pievalues'][i] = []
                            if i not in co['piecolors']: co['piecolors'][i] = []
                            for label, row in e.sort_values(by=['value'], ascending=ascending).iterrows():
                                events[label] = dict(info=None, onclick=None)
                                if 'onclick' in d and d['onclick']: events[label]['onclick'] = d['onclick']
                                if 'info' in d and d['info']: events[label]['info'] = d['info']
                                if r['type'] == 'P':
                                    co['pielabels'][i].append(label)
                                    co['pievalues'][i].append(row['value'])
                                    co['piecolors'][i].append(getcolor(colors, label))
                                else:
                                    if r['type'] in ['WM']: paddeddatasetdf = datasetdf[i][datasetdf[i]['label'] == label]
                                    else: paddeddatasetdf = paddeddf(reftimedf[i], datasetdf[i][datasetdf[i]['label'] == label])
                                    settrace(co, r, dataframe=paddeddatasetdf, label=label, yaxisindex=idxy[i] if co['shared_xaxes'] else idxy[0], index=i, alreadyinlegend=alreadyinlegend, groupname=getcolor(colors, str(r)), plotorientation=plotorientation, colors=colors)
                            i += 1
                if r['type'] == 'P':
                    for i in co['pielabels']:
                        co['pies'][i]=dict(trace=plotly.graph_objs.Pie(labels=co['pielabels'][i], values=co['pievalues'][i], hoverinfo='label+percent', textinfo='none', marker=dict(colors=co['piecolors'][i], line=dict(color='#000000', width=2))), row=1, col=i)
            if len(co['pies']) > 0:
                fig['layout'].update(**co['layoutoptions'])
                fig = json.loads(json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder))
                for i in co['pies']:
                    fig['data'].append(json.loads(json.dumps(co['pies'][i]['trace'], cls=plotly.utils.PlotlyJSONEncoder)))
            else:
                for it in co['pies']: fig.append_trace(co['pies'][it]['trace'], co['pies'][it]['row'], co['pies'][it]['col'])
                for it in co['traces']: fig.append_trace(co['traces'][it]['trace'], co['traces'][it]['row'], co['traces'][it]['col'])
                for it in co['traces']: fig['data'][it].update(xaxis=co['xaxis'][co['traces'][it]['xaxis']]['smallname'], yaxis=co['yaxis'][co['traces'][it]['yaxis']]['smallname'])
                for iy in co['yaxis']: setattr(fig['layout'], co['yaxis'][iy]['name'], plotly.graph_objs.layout.YAxis())
                for ix in co['xaxis']: setattr(fig['layout'], co['xaxis'][ix]['name'], plotly.graph_objs.layout.XAxis())
                fig['layout'].update(**co['layoutoptions'])
                for iy in co['yaxis']: fig['layout'][co['yaxis'][iy]['name']].update(**co['yaxis'][iy]['options'])
                for ix in co['xaxis']: fig['layout'][co['xaxis'][ix]['name']].update(**co['xaxis'][ix]['options'])
            rows = co['rows']
            chartobj = dict(figure=fig, events=events, rows=rows)
            cvalue = json.dumps(chartobj, cls=plotly.utils.PlotlyJSONEncoder)
            if not self.nocache: chartcache.set(ckey, cvalue)
            chartobj = json.loads(cvalue)
            fig = chartobj['figure']
        fig['layout']['width'] = width
        if 'titlefont' not in fig['layout']: fig['layout']['titlefont'] = dict()
        fig['layout']['titlefont']['size'] = getfontsize(width, binf=1000, bsup=2000, vinf=12, vsup=18)
        if 'annotations' in fig['layout']:
            for a in fig['layout']['annotations']:
                a['font']['size'] = getfontsize(width, binf=1000, bsup=2000, vinf=10, vsup=14)
        if 'legend' not in fig['layout']: fig['layout']['legend'] = dict()
        if 'font' not in fig['layout']['legend']: fig['layout']['legend']['font'] = dict()
        fig['layout']['legend']['font']['size'] = getfontsize(width, binf=500, bsup=2000, vinf=8, vsup=12)
        fig['layout']['legend']['x'] = 1.02
        numleftyaxis = 0
        numrightyaxis = 0
        numxaxis = 0
        figtype = None
        fig['config'] = dict(showSendToCloud=True, editable=True, scrollZoom=True)
        for e in fig['data']:
            if e['type'] == 'pie': figtype = 'pie'
        for e in list(fig['layout']):
            if 'yaxis' in e:
                if 'side' not in fig['layout'][e]: del fig['layout'][e]
                else:
                    if fig['layout'][e]['side'] == 'left': numleftyaxis += 1
                    if fig['layout'][e]['side'] == 'right': numrightyaxis += 1
            if 'xaxis' in e: numxaxis += 1
        if figtype == 'pie':
            numleftyaxis = 0
            numrightyaxis = 0
            for e in list(fig['layout']):
                if 'xaxis' in e or 'yaxis' in e: del fig['layout'][e]
        for e in fig['layout']:
            if 'yaxis' in e or 'xaxis' in e:
                if 'titlefont' not in fig['layout'][e]: fig['layout'][e]['titlefont'] = dict()
                if 'tickfont' not in fig['layout'][e]: fig['layout'][e]['tickfont'] = dict()
                fig['layout'][e]['tickfont']['size'] = getfontsize(width, binf=500, bsup=2000, vinf=8, vsup=12)
                fig['layout'][e]['titlefont']['size'] = getfontsize(width, binf=500, bsup=2000, vinf=10, vsup=14)
            if 'yaxis' in e:
                fig['layout'][e]['position'] = getyposition(fig['layout'][e], width, numleftyaxis=numleftyaxis, rows=rows)
        for e in fig['layout']:
            if 'xaxis' in e:
                if 'xaxis' == e: index = 0
                else: index = int(e[-1]) - 1
                fig['layout'][e]['domain'] = getdomain(width, index=index, numleftyaxis=numleftyaxis, numrightyaxis=numrightyaxis, numxaxis=numxaxis, rows=rows)
        if figtype == 'pie':
            index = 0
            for e in fig['data']:
                if 'domain' not in e: e['domain'] = dict()
                e['domain']['x'] = getdomain(width, index=index, numleftyaxis=numleftyaxis, numrightyaxis=numrightyaxis, numxaxis=numxaxis, rows=rows)
                index += 1       
        if 'annotations' in fig['layout']:
                index = 0
                for a in list(fig['layout']['annotations']):
                    if plotorientation == 'horizontal': a['x'] = getaposition(width, index=index, numleftyaxis=numleftyaxis, numrightyaxis=numrightyaxis, numxaxis=numxaxis)
                    else: a['y'] = getaposition(width, index=index, numleftyaxis=numleftyaxis, numrightyaxis=numrightyaxis, numxaxis=numxaxis, rows=rows)
                    index += 1
        logger.debug(f'Generated figure: {json.dumps(chartobj)}')
        return chartobj
