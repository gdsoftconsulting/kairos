import plotly.figure_factory as ff, pandas as pd, hashlib, streamlit as st, json, subprocess,string, random, pexpect, pscript, textwrap, shutil, inspect, tempfile, os, pickle
import plotly.graph_objects as go
#import psycopg2
#import psycopg2.extensions
#import psycopg2.extras
from htmlgenerator import *
from plotly.subplots import make_subplots
from sqlalchemy.sql import text as alctext
from streamlit_extras.switch_page_button import switch_page
from streamlit_ace import st_ace
from streamlit_theme import st_theme
from loguru import logger
import streamlit_antd_components as sac
import streamlit.components.v1 as components

def set_page_config():
    st.set_page_config(layout="wide",initial_sidebar_state='collapsed')
    st.markdown("""<style> [data-testid="collapsedControl"] {display: none}</style>""", unsafe_allow_html=True)
    theme = st_theme()
    return dict(streamlit_theme=theme['base']) if theme else dict(streamlit_theme='light')

def run_again():
    logger.debug('Restarting SCRIPT ...')
    st.rerun()

def timeit(func):
    def wrapper(*args, **kwargs):
        logger.trace(f'>>> Entering {func.__name__}')
        ts = datetime.now()
        response = func(*args, **kwargs)
        te = datetime.now()
        logger.trace(f'FUNCTION: {func.__name__} args: {args}, kwargs: {kwargs} TIME: {te -ts}')
        logger.trace(f'<<< Leaving {func.__name__}')
        return response
    return wrapper

def gen_back_button():
    if 'callstack' in st.session_state and st.session_state.callstack and len( st.session_state.stackpages) > 0:
        c1, c2 = st.columns([10,1])
        with c2:
            if st.button('Back'): st.session_state.callstack.back()

def systemname():
        return run('uname -n', gson=False)

def writeconfig(configuration):
    configfile=open(f'/export/configuration', 'wb')
    pickle.dump(configuration, configfile)
    configfile.close()

def readconfig():
    configfile=open(f'/export/configuration', 'rb')
    configuration=pickle.load(configfile)
    configfile.close()
    return configuration

class CallStack:
    def __init__(self):
        st.session_state.stackpages = []

    def call(self, page, caller):
        st.session_state.stackpages.append(caller)
        switch_page(page)

    def back(self):
        page = st.session_state.stackpages.pop()
        switch_page(page)

getcolor = lambda colors, x: colors[x] if x in colors else '#' + hashlib.md5(x.encode('utf-8')).hexdigest()[0:6]
approx = lambda x, y: min(x, key=lambda z: abs(z-y))
from datetime import *

def get_random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

@timeit
def getpath(id):
    nodesdb = st.session_state.nodesdb
    command = f"kairos -s getpath --nodesdb {nodesdb} --id {id}"
    act = run(command)
    if 'success' in act and act['success']: return act['data']
    else: st.error(act['message'])

@timeit
def get_users():
    if "users" not in st.session_state:
        command = f"kairos -s listusers"
        act = run(command)
        if 'success' in act and act['success']: 
            st.session_state.users = sorted([x['user'] for x in act['data']])
        else: st.error(act['message'])
    return st.session_state.users

def get_roles():
    if "roles" not in st.session_state:
        command = f"kairos -s listroles"
        act = run(command)
        if 'success' in act and act['success']: 
            st.session_state.roles = sorted([x['role'] for x in act['data']])
        else: st.error(act['message'])
    return st.session_state.roles

def get_grants():
    if "grants" not in st.session_state:
        command = f"kairos -s listgrants"
        act = run(command)
        if 'success' in act and act['success']: 
            st.session_state.grants = sorted([(x['user'],x['role']) for x in act['data']])
        else: st.error(act['message'])
    return st.session_state.grants

def get_settings(theme):
    if "settings" not in st.session_state:
        command = f"kairos -s getsettings -a {st.session_state.user} -p {st.session_state.password}"
        act = run(command)
        if 'success' in act and act['success']: 
            st.session_state.settings = act['data']['settings']
            st.session_state.nodesdb = st.session_state.settings['nodesdb']
            st.session_state.systemdb = st.session_state.settings['systemdb']
            st.session_state.colors = st.session_state.settings['colors']
            st.session_state.template = st.session_state.settings['template']
            st.session_state.template = 'BLACK' if theme['streamlit_theme'] == 'dark' else 'DEFAULT'
            st.session_state.plotorientation = st.session_state.settings['plotorientation']
            st.session_state.top = st.session_state.settings['top']
        else: st.error(act['message'])
    return st.session_state.settings

def get_objects():
    nodesdb = st.session_state.nodesdb
    systemdb = st.session_state.systemdb
    if "objects" not in st.session_state:
        act = run(f'kairos -s listobjects --nodesdb {nodesdb} --systemdb {systemdb}')
        if 'success' in act and act['success']:
            st.session_state.objects = [x for x in act['data']]
        else: st.error(act['message'])
    return st.session_state.objects

def get_databases():
    if 'databases' not in st.session_state:
        command = f"kairos -s listdatabases --user {st.session_state.user}"
        act = run(command)
        if 'success' in act and act['success']:
            st.session_state.databases = [x['name'] for x in act['data']]
        else: st.error(act['message'])
    return st.session_state.databases

def get_aggregators(): return [x['id'] for x in get_objects() if x['type']=='aggregator']
def get_liveobjects(): return [x['id'] for x in get_objects() if x['type']=='liveobject']
def get_queries(): return [x['id'] for x in get_objects() if x['type']=='query']
def get_charts(): return [x['id'] for x in get_objects() if x['type']=='chart']
def get_reports(): return [x['id'] for x in get_objects() if x['type']=='report']
def get_wallpapers(): return [x['id'] for x in get_objects() if x['type']=='wallpaper']
def get_colors(): return [x['id'] for x in get_objects() if x['type']=='color']
def get_templates(): return [x['id'] for x in get_objects() if x['type']=='template']

def kairos_upload_node():
    nodesdb = st.session_state.nodesdb
    systemdb = st.session_state.systemdb
    node = st.session_state.node
    ufiles = st.file_uploader("Upload node", accept_multiple_files=True)
    for ufile in ufiles:
        name = ufile.name
        f = open(f'/tmp/{name}', 'wb')
        f.write(ufile.read())
        f.close()
        command = f"kairos -s uploadnode --nodesdb {nodesdb}  --systemdb {systemdb} --id {node} --file '/tmp/{name}'"
        act = run(command)
        if 'success' in act and act['success']:
            st.session_state.nodemenu = None
            st.session_state.treeupdated = True
            run_again()
        else: st.error(act['message'])

def kairos_create_node():
    nodesdb = st.session_state.nodesdb
    node = st.session_state.node
    logger.info(f'Creating a new node into {nodesdb} and attaching node to {node}')
    command = f'kairos -s createnode --nodesdb {nodesdb} --id {node}'
    act = run(command)
    logger.debug(act)
    if 'success' in act and act['success']:
        st.session_state.treeupdated = True
        st.session_state.nodemenu = None
        run_again()
    else: st.error(act['message'])

def kairos_rename_node():
    nodesdb = st.session_state.nodesdb
    node = st.session_state.node
    command = f'kairos -s getnode --nodesdb {nodesdb} --id {node}'
    act = run(command)
    if 'success' in act and act['success']: name = act['data']['name']
    else: st.error(act['message'])
    new = st.text_input(f'Enter node name:', name)
    if new != name:
        command = f'kairos -s renamenode --nodesdb {nodesdb} --id {node} --new {new}'
        act = run(command)
        if 'success' in act and act['success']:
            st.session_state.nodemenu = None
            st.session_state.treeupdated = True
            run_again()
        else: st.error(act['message'])

def kairos_delete_node():
    nodesdb = st.session_state.nodesdb
    node = st.session_state.node
    oldname = getpath(node)
    command = f'kairos -s deletenode --nodesdb {nodesdb} --id {node}'
    act = run(command)
    if 'success' in act and act['success']:
        st.session_state.node = 2
        st.session_state.nodemenu = None
        st.session_state.treeupdated = True
        run_again()
    else: st.error(act['message'])

def kairos_duplicate_d_node():
    nodesdb = st.session_state.nodesdb
    node = st.session_state.node
    command = f'kairos -s duplicatenode --nodesdb {nodesdb} --id {node}'
    act = run(command)
    if 'success' in act and act['success']:
        st.session_state.nodemenu = None
        st.session_state.treeupdated = True
        run_again()   
    else: st.error(act['message'])

def kairos_edit_liveobject():
    nodesdb = st.session_state.nodesdb
    systemdb = st.session_state.systemdb
    node = st.session_state.node
    command = f'kairos -s getnode --nodesdb {nodesdb} --id {node}'
    act = run(command)
    if 'success' in act and act['success']:
        st.session_state.nodemenu = None
        st.session_state.object =  act['data']['datasource']['liveobject']
        st.session_state.type = 'liveobject'
        st.session_state.callstack.call('kairosedit', 'kairos')
    else: st.error(act['message'])

def kairos_copy():
    node = st.session_state.node
    st.session_state.copied = node
    st.session_state.nodemenu = None
    st.success(f'Node {getpath(node)} has been copied!')

def kairos_paste_to_a_node():
    nodesdb = st.session_state.nodesdb
    node = st.session_state.node
    copied = st.session_state.copied
    act = run(f'kairos -s aggregateaddnode --nodesdb {nodesdb} --from {copied} --to {node}')
    if 'success' in act and act['success']:
        del st.session_state.copied
        st.session_state.nodemenu = None
        st.session_state.treeupdated = True
        run_again()
    else: st.error(act['message'])

def kairos_paste_to_c_node():
    nodesdb = st.session_state.nodesdb
    node = st.session_state.node
    copied = st.session_state.copied
    act = run(f'kairos -s compareaddnode --nodesdb {nodesdb} --from {copied} --to {node}')
    if 'success' in act and act['success']:
        del st.session_state.copied
        st.session_state.nodemenu = None
        st.session_state.treeupdated = True
        run_again()
    else: st.error(act['message'])

def kairos_move_node():
    nodesdb = st.session_state.nodesdb
    node = st.session_state.node
    copied = st.session_state.copied
    act = run(f'kairos -s movenode --nodesdb {nodesdb} --from {copied} --to {node}')
    if 'success' in act and act['success']:
        del st.session_state.copied
        st.session_state.nodemenu = None
        st.session_state.treeupdated = True
        run_again()
    else: st.error(act['message'])

def kairos_transform_to_a_node():
    nodesdb = st.session_state.nodesdb
    systemdb = st.session_state.systemdb
    node = st.session_state.node
    aggregators = get_aggregators()
    act = run(f'kairos -s getnode --nodesdb {nodesdb} --id {node}')
    if 'success' in act and act['success']:
        datasource = act['data']['datasource']
        aselector = datasource['aggregatorselector'] if 'aggregatorselector' in datasource else '/'
        amethod = datasource['aggregatormethod'] if 'aggregatormethod' in datasource else '$none'
        askip = datasource['aggregatorskip'] if 'aggregatorskip' in datasource else 0
        atake = datasource['aggregatortake'] if 'aggregatortake' in datasource else 1
        asort = datasource['aggregatorsort'] if 'aggregatorsort' in datasource else 'desc'
        atimefilter = datasource['aggregatortimefilter'] if 'aggregatortimefilter' in datasource else '.'
    else: st.error(act['message'])
    newselector = st.text_input(f'Enter the selector ...', aselector)
    newskip = st.text_input(f'Enter the number of reports to ignore...', askip)
    newtake = st.text_input(f'Enter the number of reports to take...', atake)
    newsort = st.text_input(f'Enter the sort order to select reports...', asort)
    newtimefilter = st.text_input(f'Enter the time date/filter...', atimefilter)
    curindex = -1
    for x in aggregators:
        curindex += 1
        if x == amethod: break
    aggregator = st.selectbox( 'Choose an aggregator in the following list ...', aggregators, curindex)
    if aggregator != amethod or newselector != aselector or newskip != askip or newtake != atake or newsort != asort or newtimefilter != atimefilter:
        act = run(f"kairos -s applyaggregator --nodesdb {nodesdb} --systemdb {systemdb} --id {node} --aggregatorselector '{newselector}' --aggregatortake {newtake} --aggregatorskip {newskip} --aggregatorsort {newsort} --aggregatormethod '{aggregator}' --aggregatortimefilter '{newtimefilter}'")
        if 'success' in act and act['success']: 
            st.session_state.nodemenu = None
            st.session_state.treeupdated = True
            run_again()
        else: st.error(act['message'])

def kairos_transform_to_d_node():
    nodesdb = st.session_state.nodesdb
    systemdb = st.session_state.systemdb
    node = st.session_state.node
    liveobjects = get_liveobjects()
    liveobject = st.selectbox( 'Choose a liveobject in the following list ...', tuple([''] + liveobjects))
    if liveobject:
        act = run(f"kairos -s applyliveobject --nodesdb {nodesdb} --systemdb {systemdb} --id {node} --liveobject {liveobject}")
        if 'success' in act and act['success']:
            st.session_state.nodemenu = None
            st.session_state.treeupdated = True
            run_again()
        else: st.error(act['message'])

def kairos_display_node():
    st.session_state.nodemenu = None
    st.session_state.callstack.call('kairosnode', 'kairos')

def kairos_display_collection():
    nodesdb = st.session_state.nodesdb
    systemdb = st.session_state.systemdb
    node = st.session_state.node
    act = run(f'kairos -s getnode --nodesdb {nodesdb} --id {node}')
    if 'success' in act and act['success']: collections = [x for x in act['data']['datasource']['collections']]
    else: st.error(act['message'])
    collection = st.selectbox( 'Choose a collection in the following list ...', tuple([''] + collections))
    if collection:
        st.session_state.collection = collection
        st.session_state.nodemenu = None
        st.session_state.callstack.call('kairoscollection', 'kairos')

def kairos_execute_query():
    queries = get_queries()
    query = st.selectbox( 'Choose a query in the following list ...', tuple([''] + queries))
    if query:
        st.session_state.query = query
        st.session_state.nodemenu = None
        st.session_state.callstack.call('kairosquery', 'kairos')

def kairos_run_chart():
    charts = get_charts()
    chart = st.selectbox( 'Choose a chart in the following list ...', tuple([''] + charts))
    if chart:
        st.session_state.chart = chart
        st.session_state.nodemenu = None
        st.session_state.callstack.call('kairoschart', 'kairos')

def kairos_run_report():
    reports = get_reports()
    report = st.selectbox( 'Choose a report in the following list ...', tuple([''] + reports))
    if report:
        st.session_state.report = report
        st.session_state.nodemenu = None
        st.session_state.callstack.call('kairosreport', 'kairos')

def kairos_download_node(): 
    nodesdb = st.session_state.nodesdb
    node = st.session_state.node
    url = f'https://localhost:44390/downloadsource?id={node}&nodesdb={nodesdb}'
    x = st.link_button("Download ...", url)
    logger.critical(x)
    os.system('sleep 5')
    if x:
        st.session_state.nodemenu = None
        run_again()


def kairos_clear_cache():
    nodesdb = st.session_state.nodesdb
    systemdb = st.session_state.systemdb
    node = st.session_state.node
    act = run(f'kairos -s clearcollectioncache --nodesdb {nodesdb} --systemdb {systemdb} --id {node}')
    if 'success' in act and act['success']:
        st.session_state.nodemenu = None
        run_again()
    else: st.error(act['message'])

def kairos_clear_progeny_caches():
    nodesdb = st.session_state.nodesdb
    systemdb = st.session_state.systemdb
    node = st.session_state.node
    act = run(f'kairos -s clearprogenycaches --nodesdb {nodesdb} --systemdb {systemdb} --id {node}')
    if 'success' in act and act['success']:
        st.session_state.nodemenu = None
        run_again()
    else: st.error(act['message'])

def kairos_build_progeny_caches():
    nodesdb = st.session_state.nodesdb
    systemdb = st.session_state.systemdb
    node = st.session_state.node
    act = run(f'kairos -s buildprogenycaches --nodesdb {nodesdb} --systemdb {systemdb} --id {node}')
    if 'success' in act and act['success']:
        st.session_state.nodemenu = None
        run_again()
    else: st.error(act['message'])

def kairos_empty_trash():
    nodesdb = st.session_state.nodesdb
    command = f'kairos -s emptytrash --nodesdb {nodesdb}'
    act = run(command)
    if 'success' in act and act['success']:
        st.session_state.nodemenu = None
        st.session_state.treeupdated = True
        run_again()
    else: st.error(act['message'])

class KairosTree:
    def __init__(self, nodesdb, expanded=True):
        self.nodesdb = nodesdb
        self.expanded = expanded
        if "tree" not in st.session_state or "treeupdated" not in st.session_state or st.session_state.treeupdated:
            self.tree=self.gettree()
            st.session_state.tree = self.tree
            st.session_state.nodes = self.nodes
            st.session_state.treeupdated = False
        else: 
            self.tree = st.session_state.tree
            self.nodes = st.session_state.nodes
    def gettree(self):
        act = run(f'kairos -s getwholetree --nodesdb {self.nodesdb}')
        self.nodes = act['data']
        def f(id=None):
            id = str(id) if id else "1"
            node = self.nodes[id]
            type = self.nodes[id]['type']
            name = self.nodes[id]['name']
            children = []
            lchildren = sorted([self.nodes[e]['name'] for e in self.nodes if str(self.nodes[e]['parent'])==id])
            for e in lchildren:
                cnode = [x for x in self.nodes if str(self.nodes[x]['parent'])==id and self.nodes[x]['name']==e][0]
                children.append(f(cnode))
            icon ="FolderOutlined" if type == "N" else "DatabaseOutlined" if type == "D" else "DeleteOutlined" if type == "T" else "ApartmentOutlined" if type == "C" else "ClusterOutlined" if type == "A" else "FileOutlined"
            color = "error" if type == 'A' else "processing" if type == 'B' else "success" if type == 'C' else "geekblue" if type == "D" else "gold" if type == "N" else "default"
            return dict(title=name, key=id, tag=type, icon=icon, tagProps=dict(color=color), titleProps=dict(italic=True, level=5), spaceProps=dict(size='small'), children=children)
        return f()
    def render(self):
        x = TREE(tree=[self.tree], height=500, id='ktree', theme='dark', selectedKeys=[str(st.session_state.node)], expandedKeys=[str(st.session_state.node)], default=f'-{st.session_state.node}')
        nsel = x.get()
        if type(nsel) == type({}):
            if nsel['event'] == 'move':
                if nsel['ftype'] in ["A", "B", "C", "D", "N"] and nsel['ttype'] in ["N"]:
                    st.session_state.copied = nsel['from']
                    st.session_state.node = nsel['to']
                    kairos_move_node()            
            if nsel['event'] == 'pasteA':
                if nsel['ftype'] in ["A", "B", "D"] and nsel['ttype'] in ["A" , "N"]:
                    st.session_state.copied = nsel['from']
                    st.session_state.node = nsel['to']
                    kairos_paste_to_a_node()
            if nsel['event'] == 'pasteC':
                if nsel['ftype'] in ["A", "B", "D"] and nsel['ttype'] in ["C" , "N"]:
                    st.session_state.copied = nsel['from']
                    st.session_state.node = nsel['to']
                    kairos_paste_to_c_node()
            nsel = st.session_state.node
        else:
            if int(nsel) < 0:
                nsel = nsel[1:]
                st.session_state.node =nsel
                st.session_state.type = self.nodes[nsel]['type']
            else:
                st.session_state.node =nsel
                st.session_state.type = self.nodes[nsel]['type']
                run_again()
        return nsel

def run0(cmd, pattern=None, gson=True):
    logger.debug(cmd)
    if gson:
        try: result = json.loads(subprocess.check_output([cmd], shell=True))
        except subprocess.CalledProcessError as e: result=json.loads(e.output)
        if pattern: result = jq(pattern).transform(result)
    else:
        try: result = subprocess.check_output([cmd], shell=True)
        except subprocess.CalledProcessError as e: result=e.output
    return result

def run(cmd, pattern=None, gson=True):
    logger.debug(cmd)
    child = pexpect.spawn(cmd, encoding='utf8', timeout=None)
    x = ''.join([line for line in child])
    logger.debug(x)
    if gson:
        result = json.loads(x)
        if pattern: result = jq(pattern).transform(result)
    else:
        result = x
    return result


class Postgres:
    def __init__(self, url=None, caching=None):
        self.conn = st.connection('postgresql', type='sql', url=f'postgresql+psycopg2://{url}', ttl=caching)
        self.session=self.conn.session
        self.schema='public'

    @timeit
    def execute(self, query):
        self.session.execute(alctext(query))

    @timeit
    def setschema(self, schema=None):
        self.schema = 'public' if schema == None else schema
        self.execute(f'set search_path={self.schema}')

    @timeit
    def query(self, query):
        x = self.session.execute(alctext(query))
        keys = x.keys()
        result = x.fetchall()
        df = pd.DataFrame(result) if len(result) > 0 else pd.DataFrame(columns=keys)
        if len(result) > 0: df.columns = keys
        return df

class Oracle:
    def __init__(self, url=None, caching=None, decfmt='fm9999999999D00'):
        logger.debug('New ORACLE session initiated!')
        self.conn = st.connection('oracle', type='sql', url = f'oracle://{url}', ttl=caching)
        self.signature = 'BZB0JHCTH8CFR9BRPHNAQDUDKYAK9QTP'
        self.session = self.conn.session
        self.tables = dict()
        self.snapshots = None
        self.decfmt = decfmt
        self.vdollar = False
        #self.truncateall()

    @timeit
    def execute(self, query):
        self.session.execute(alctext(query))

    @timeit
    def query(self, query):
        x = self.session.execute(alctext(query))
        keys = x.keys()
        result = x.fetchall()
        df = pd.DataFrame(result) if len(result) > 0 else pd.DataFrame(columns=keys)
        if len(result) > 0: df.columns = keys
        return df

    @timeit
    def dropall(self):
        result = self.session.execute(alctext(f"select table_name from user_tables where temporary='Y' and table_name like '{self.signature}%'"))
        logger.debug(f'Dropping all global temporary table with name beginning by {self.signature}')
        for x in result.fetchall():
            logger.debug(f'Dropping table {x[0]}')
            self.session.execute(alctext(f"drop table {x[0]}"))    
    
    @timeit
    def truncateall(self):
        result = self.session.execute(alctext(f"select table_name from user_tables where temporary='Y' and table_name like '{self.signature}%'"))
        logger.debug(f'Truncating all global temporary table with name beginning by {self.signature}')
        for x in result.fetchall():
            logger.debug(f'Truncating table {x[0]}')
            self.session.execute(alctext(f"truncate table {x[0]}"))

    @timeit
    def createtable(self, name, query):
        if name in self.tables and self.tables[name]:
            logger.debug(f'Ignoring create global temporary table {self.signature}_{name}')
            return
        result = self.session.execute(alctext(f"select table_name from user_tables where temporary='Y' and table_name = '{self.signature}_{name.upper()}'"))
        a = 0
        for x in result: a += 1
        if a == 0:
            logger.debug(f'Creating global temporary table {self.signature}_{name}')
            self.execute(f"create global temporary table {self.signature}_{name} on commit preserve rows as {query}")
        else:
            logger.debug(f'Adding rows to global temporary table {self.signature}_{name}')
            self.execute(f"insert into {self.signature}_{name} {query}")
        self.tables[name] = True

    @timeit
    def name(self, table):
        return f"{self.signature}_{table}"

    @timeit
    def listofcdbs(self):
        result = self.query(f"select distinct instance_name||'@'||host_name||':'||dbid cdb from dba_hist_database_instance order by 1")
        cdbs = tuple([''] + result['cdb'].to_list())
        return cdbs

    @timeit
    def getconndbid(self):
        return self.query(f"select dbid from v$database").iloc[0,0]

    @timeit
    def getdmin(self, dbid):
        return self.query(f"select to_char(min(end_interval_time), 'yyyy/mm/dd') x from dba_hist_snapshot where dbid = {dbid}").iloc[0,0]

    @timeit
    def getdmax(self, dbid):
        return self.query(f"select to_char(max(end_interval_time), 'yyyy/mm/dd') x from dba_hist_snapshot where dbid = {dbid}").iloc[0,0]

    @timeit
    def getsnapshots(self, mindate=None, maxdate=None, dbid=None):
        self.createtable('dba_hist_snapshot', f"select * from dba_hist_snapshot where to_char(end_interval_time, 'YYYYMMDDHH24MISS') > '{mindate}' and to_char(begin_interval_time, 'YYYYMMDDHH24MISS') < '{maxdate}' and dbid = {dbid} order by end_interval_time")
        self.snapshots = self.query(f"select dbid, instance_number, to_char(startup_time, 'YYYYMMDDHH24MISS') startup_time, snap_id, end_interval_time from {self.name('dba_hist_snapshot')}")
        self.createtable('masterlist', f"select dbid, instance_number, to_char(startup_time, 'YYYYMMDDHH24MISS') startup_time from dba_hist_database_instance i where i.dbid = {dbid}")
        self.createtable('deltas', f"select dbid, instance_number, to_char(startup_time, 'YYYYMMDDHH24MISS') startup_time, bid, eid, to_char(snap_time, 'YYYYMMDDHH24MISS')|| '000' snap_time, round(((cast(snap_time as date) - cast(prev_snap_time as date)) * 1440 * 60), 0) elapsed from (select end_interval_time snap_time, first_value(end_interval_time) over (order by end_interval_time asc rows between 1 preceding and current row) prev_snap_time, first_value(snap_id) over (order by end_interval_time asc rows between 1 preceding and current row ) bid, snap_id eid, first_value(dbid) over (order by end_interval_time asc rows between 1 preceding and current row) prev_dbid, dbid, first_value(instance_number) over (order by end_interval_time asc rows between 1 preceding and current row) prev_instance_number, instance_number, first_value(startup_time) over (order by end_interval_time asc rows between 1 preceding and current row) prev_startup_time, startup_time from {self.name('dba_hist_snapshot')}) where dbid = prev_dbid and instance_number = prev_instance_number and startup_time = prev_startup_time and bid != eid")
        self.createtable('vdeltas', f"select d.dbid, d.instance_number, d.startup_time, d.bid, d.eid, d.snap_time, d.elapsed from {self.name('deltas')} d, {self.name('masterlist')} m where d.dbid = m.dbid and d.instance_number = m.instance_number and d.startup_time = m.startup_time")

    @timeit
    def extract(self, table):
        logger.debug(f'Extracting data for table {table}')
        ituples = [row.tolist() for row in self.snapshots[['dbid', 'instance_number', 'snap_id', 'end_interval_time']].to_records()]        
        tuples =[(x[1], x[2], x[3]) for x in ituples]
        self.createtable(table, f"select * from {table} where (dbid, instance_number, snap_id) in {tuple(tuples)}")

    @timeit
    def dboramisc(self):
        if 'dba_hist_sysstat' not in self.tables: self.extract('dba_hist_sysstat')
        return f"select to_timestamp(snap_time, 'YYYYMMDDHH24MISSFF') timestamp, elapsed, elapsed avgelapsed, s.value sessions from {self.name('vdeltas')} v, {self.name('dba_hist_sysstat')} s where s.stat_name = 'logons current' and v.eid = s.snap_id and v.instance_number = s.instance_number and v.dbid = s.dbid"

    @timeit
    def dboratms(self):
        if 'dba_hist_sys_time_model' not in self.tables: self.extract('dba_hist_sys_time_model')
        return f"select to_timestamp(v.snap_time, 'YYYYMMDDHH24MISSFF') timestamp, e.stat_name statistic, to_char((e.value - b.value) / v.elapsed / 1000000, '{self.decfmt}') time from {self.name('vdeltas')} v, {self.name('dba_hist_sys_time_model')} e, {self.name('dba_hist_sys_time_model')} b where b.snap_id = v.bid and e.snap_id = v.eid and b.dbid = v.dbid and e.dbid  = v.dbid and b.instance_number = v.instance_number and e.instance_number = v.instance_number and b.stat_id = e.stat_id and e.value - b.value > 0"

    @timeit
    def dborawec(self):
        if 'dba_hist_system_event' not in self.tables: self.extract('dba_hist_system_event')
        return f"select to_timestamp(v.snap_time, 'YYYYMMDDHH24MISSFF') timestamp, e.wait_class eclass, to_char((e.total_waits_fg - nvl(b.total_waits_fg,0)) / v.elapsed, '{self.decfmt}') count, to_char((e.total_timeouts_fg - nvl(b.total_timeouts_fg,0)) / v.elapsed, '{self.decfmt}') timeouts, to_char((e.time_waited_micro_fg - nvl(b.time_waited_micro_fg,0)) / v.elapsed / 1000000, '{self.decfmt}') time from {self.name('vdeltas')} v, {self.name('dba_hist_system_event')} b, {self.name('dba_hist_system_event')} e where b.snap_id(+) = v.bid and e.snap_id = v.eid and b.dbid(+) = v.dbid and e.dbid = v.dbid and b.instance_number(+) = v.instance_number and e.instance_number = v.instance_number and b.event_name(+) = e.event_name and e.total_waits_fg > nvl(b.total_waits_fg,0)"

    @timeit
    def dborawev(self):
        if 'dba_hist_system_event' not in self.tables: self.extract('dba_hist_system_event')
        return f"select to_timestamp(v.snap_time, 'YYYYMMDDHH24MISSFF') timestamp, e.event_name event, to_char((e.total_waits_fg - nvl(b.total_waits_fg,0)) / v.elapsed, '{self.decfmt}') count, to_char((e.total_timeouts_fg - nvl(b.total_timeouts_fg,0)) / v.elapsed, '{self.decfmt}') timeouts, to_char((e.time_waited_micro_fg - nvl(b.time_waited_micro_fg,0)) / v.elapsed / 1000000,'{self.decfmt}') time from {self.name('vdeltas')} v, {self.name('dba_hist_system_event')} b, {self.name('dba_hist_system_event')} e where b.snap_id(+) = v.bid and e.snap_id = v.eid and b.dbid(+) = v.dbid and e.dbid = v.dbid and b.instance_number(+) = v.instance_number and e.instance_number = v.instance_number and b.event_name(+) = e.event_name and e.total_waits_fg > nvl(b.total_waits_fg,0)"

    @timeit
    def dborawev(self):
        if 'dba_hist_system_event' not in self.tables: self.extract('dba_hist_system_event')
        return f"select to_timestamp(v.snap_time, 'YYYYMMDDHH24MISSFF') timestamp, e.event_name event, to_char((e.total_waits_fg - nvl(b.total_waits_fg,0)) / v.elapsed, '{self.decfmt}') count, to_char((e.total_timeouts_fg - nvl(b.total_timeouts_fg,0)) / v.elapsed, '{self.decfmt}') timeouts, to_char((e.time_waited_micro_fg - nvl(b.time_waited_micro_fg,0)) / v.elapsed / 1000000,'{self.decfmt}') time from {self.name('vdeltas')} v, {self.name('dba_hist_system_event')} b, {self.name('dba_hist_system_event')} e where b.snap_id(+) = v.bid and e.snap_id = v.eid and b.dbid(+) = v.dbid and e.dbid = v.dbid and b.instance_number(+) = v.instance_number and e.instance_number = v.instance_number and b.event_name(+) = e.event_name and e.total_waits_fg > nvl(b.total_waits_fg,0)"

    @timeit
    def dboraweh(self):
        if 'dba_hist_event_histogram' not in self.tables: self.extract('dba_hist_event_histogram')
        return f"select to_timestamp(v.snap_time, 'YYYYMMDDHH24MISSFF') timestamp, e.event_name event, e.wait_time_milli*1024 bucket, to_char((e.wait_count - nvl(b.wait_count, 0)) / v.elapsed, '{self.decfmt}') count from {self.name('vdeltas')} v, {self.name('dba_hist_event_histogram')} b, {self.name('dba_hist_event_histogram')} e where b.snap_id(+) = v.bid and e.snap_id = v.eid and b.dbid(+) = v.dbid and e.dbid = v.dbid and b.instance_number(+) = v.instance_number and e.instance_number = v.instance_number and b.event_id(+) = e.event_id and b.wait_time_milli(+) = e.wait_time_milli and e.wait_count - nvl(b.wait_count, 0) > 0"

    @timeit
    def dboraoss(self):
        if 'dba_hist_osstat' not in self.tables: self.extract('dba_hist_osstat')
        return f"select to_timestamp(v.snap_time, 'YYYYMMDDHH24MISSFF') timestamp, e.stat_name statistic, decode(instr(e.stat_name,'_TIME'),0 , e.value, e.value - b.value) value from {self.name('vdeltas')} v, {self.name('dba_hist_osstat')} b, {self.name('dba_hist_osstat')} e where b.snap_id = v.bid and e.snap_id = v.eid and b.dbid = v.dbid and e.dbid = v.dbid and b.instance_number = v.instance_number and e.instance_number = v.instance_number and b.stat_id = e.stat_id and e.value >= b.value and e.value > 0"

    @timeit
    def dborasta(self):
        if 'dba_hist_sysstat' not in self.tables: self.extract('dba_hist_sysstat')
        return f"select to_timestamp(v.snap_time, 'YYYYMMDDHH24MISSFF') timestamp, b.stat_name statistic, to_char((e.value - nvl(b.value,0)) / v.elapsed, '{self.decfmt}') value from {self.name('vdeltas')} v, {self.name('dba_hist_sysstat')} b, {self.name('dba_hist_sysstat')} e where b.snap_id(+) = v.bid and e.snap_id = v.eid and b.dbid(+) = v.dbid and e.dbid = v.dbid and b.instance_number(+) = v.instance_number and e.instance_number = v.instance_number and b.stat_name(+) = e.stat_name and e.stat_name not in ('logons current', 'opened cursors current', 'workarea memory allocated', 'session cursor cache count') and e.value >= nvl(b.value,0) and e.value  >  0"

    @timeit
    def dborasqe(self):
        if 'dba_hist_sqlstat' not in self.tables: self.extract('dba_hist_sqlstat')
        return f"select to_timestamp(v.snap_time, 'YYYYMMDDHH24MISSFF') timestamp, e.sql_id sqlid, to_char(sum(e.cpu_time_delta / v.elapsed) / 1000000, '{self.decfmt}') cpu, to_char(sum(e.elapsed_time_delta / v.elapsed) / 1000000, '{self.decfmt}') elapsed, to_char(sum(e.disk_reads_delta / v.elapsed), '{self.decfmt}') reads, to_char(sum(e.executions_delta / v.elapsed), '{self.decfmt}') execs from {self.name('vdeltas')} v, {self.name('dba_hist_sqlstat')} e where e.snap_id = v.eid and e.dbid = v.dbid and e.instance_number = v.instance_number group by v.snap_time, e.sql_id"

    @timeit
    def dborasqc(self):
        if 'dba_hist_sqlstat' not in self.tables: self.extract('dba_hist_sqlstat')
        return f"select to_timestamp(v.snap_time, 'YYYYMMDDHH24MISSFF') timestamp, e.sql_id sqlid, to_char(sum(e.cpu_time_delta / v.elapsed) / 1000000, '{self.decfmt}') cpu, to_char(sum(e.elapsed_time_delta / v.elapsed) / 1000000, '{self.decfmt}') elapsed, to_char(sum(e.buffer_gets_delta / v.elapsed), '{self.decfmt}') gets, to_char(sum(e.executions_delta / v.elapsed), '{self.decfmt}') execs from {self.name('vdeltas')} v, {self.name('dba_hist_sqlstat')} e where e.snap_id = v.eid and e.dbid = v.dbid and e.instance_number = v.instance_number group by v.snap_time, e.sql_id"

    @timeit
    def dborasqg(self):
        if 'dba_hist_sqlstat' not in self.tables: self.extract('dba_hist_sqlstat')
        return f"select to_timestamp(v.snap_time, 'YYYYMMDDHH24MISSFF') timestamp, e.sql_id sqlid, to_char(sum(e.cpu_time_delta / v.elapsed) / 1000000, '{self.decfmt}') cpu, to_char(sum(e.elapsed_time_delta / v.elapsed) / 1000000, '{self.decfmt}') elapsed, to_char(sum(e.buffer_gets_delta / v.elapsed), '{self.decfmt}') gets, to_char(sum(e.executions_delta / v.elapsed), '{self.decfmt}') execs from {self.name('vdeltas')} v, {self.name('dba_hist_sqlstat')} e where e.snap_id = v.eid and e.dbid = v.dbid and e.instance_number = v.instance_number group by v.snap_time, e.sql_id"

    def dborasqr(self):
        if 'dba_hist_sqlstat' not in self.tables: self.extract('dba_hist_sqlstat')
        return f"select to_timestamp(v.snap_time, 'YYYYMMDDHH24MISSFF') timestamp, e.sql_id sqlid, to_char(sum(e.cpu_time_delta / v.elapsed) / 1000000, '{self.decfmt}') cpu, to_char(sum(e.elapsed_time_delta / v.elapsed) / 1000000, '{self.decfmt}') elapsed, to_char(sum(e.disk_reads_delta / v.elapsed), '{self.decfmt}') reads, to_char(sum(e.executions_delta / v.elapsed), '{self.decfmt}') execs from {self.name('vdeltas')} v, {self.name('dba_hist_sqlstat')} e where e.snap_id = v.eid and e.dbid = v.dbid and e.instance_number = v.instance_number group by v.snap_time, e.sql_id"

    @timeit
    def dborasqx(self):
        if 'dba_hist_sqlstat' not in self.tables: self.extract('dba_hist_sqlstat')
        return f"select to_timestamp(v.snap_time, 'YYYYMMDDHH24MISSFF') timestamp, e.sql_id sqlid, to_char(sum(e.rows_processed_delta / v.elapsed), '{self.decfmt}') rowes, to_char(sum(e.executions_delta / v.elapsed), '{self.decfmt}') execs from {self.name('vdeltas')} v, {self.name('dba_hist_sqlstat')} e where e.snap_id = v.eid and e.dbid = v.dbid and e.instance_number = v.instance_number group by v.snap_time, e.sql_id"

    @timeit
    def dborasglr(self):
        if 'dba_hist_seg_stat' not in self.tables: self.extract('dba_hist_seg_stat')
        if 'dba_hist_seg_stat_obj' not in self.tables:
            self.createtable('dba_hist_seg_stat_obj', f"select * from dba_hist_seg_stat_obj where dbid in (select distinct dbid from {self.name('dba_hist_snapshot')})")
        return f"select to_timestamp(r.snap_time, 'YYYYMMDDHH24MISSFF') timestamp, n.owner owner, n.tablespace_name tablespace, n.object_name object, n.subobject_name subobject, n.object_type objtype, to_char(r.logical_reads / r.elapsed, '{self.decfmt}') gets from {self.name('dba_hist_seg_stat_obj')} n, (select * from (select v.snap_time, v.elapsed, e.dataobj#, e.obj#, e.ts#, e.dbid, e.logical_reads_delta logical_reads from {self.name('vdeltas')} v, {self.name('dba_hist_seg_stat')} e where e.snap_id = v.eid and e.dbid = v.dbid and e.instance_number = v.instance_number and e.logical_reads_delta > 0) d) r where n.dataobj# = r.dataobj# and n.obj# = r.obj# and n.ts# = r.ts# and n.dbid = r.dbid"

    @timeit
    def dborasgpr(self):
        if 'dba_hist_seg_stat' not in self.tables: self.extract('dba_hist_seg_stat')
        if 'dba_hist_seg_stat_obj' not in self.tables:
            self.createtable('dba_hist_seg_stat_obj', f"select * from dba_hist_seg_stat_obj where dbid in (select distinct dbid from {self.name('dba_hist_snapshot')})")
        return f"select to_timestamp(r.snap_time, 'YYYYMMDDHH24MISSFF') timestamp, n.owner owner, n.tablespace_name tablespace, n.object_name object, n.subobject_name subobject, n.object_type objtype, to_char(r.physical_reads / r.elapsed, '{self.decfmt}') reads from {self.name('dba_hist_seg_stat_obj')} n, (select * from (select v.snap_time, v.elapsed, e.dataobj#, e.obj#, e.ts#, e.dbid, e.physical_reads_delta physical_reads from {self.name('vdeltas')} v, {self.name('dba_hist_seg_stat')} e where e.snap_id = v.eid and e.dbid = v.dbid and e.instance_number = v.instance_number and e.physical_reads_delta > 0) d) r where n.dataobj# = r.dataobj# and n.obj# = r.obj# and n.ts# = r.ts# and n.dbid = r.dbid"

    @timeit
    def dborasrv(self):
        if 'dba_hist_service_stat' not in self.tables: self.extract('dba_hist_service_stat')
        return f"select to_timestamp(v.snap_time, 'YYYYMMDDHH24MISSFF') timestamp, e.service_name service, to_char(sum(decode(e.stat_name, 'DB CPU', nvl(e.value, 0) - nvl(b.value, 0), 0) / v.elapsed) / 1000000, '{self.decfmt}') cpu, to_char(sum(decode(e.stat_name, 'DB time', nvl(e.value,0) - nvl(b.value, 0), 0) / v.elapsed) / 1000000, '{self.decfmt}') dbtime, to_char(sum(decode(e.stat_name, 'session logical reads', nvl(e.value,0) - nvl(b.value, 0), 0) / v.elapsed) / 1024, '{self.decfmt}') gets, to_char(sum(decode(e.stat_name, 'physical reads', nvl(e.value,0) - nvl(b.value, 0), 0) / v.elapsed) / 1024, '{self.decfmt}') reads from {self.name('vdeltas')} v, {self.name('dba_hist_service_stat')} e, {self.name('dba_hist_service_stat')} b where b.snap_id(+) = v.bid and e.snap_id = v.eid and b.dbid(+) = v.dbid and e.dbid = v.dbid and b.dbid(+) = e.dbid and b.instance_number(+) = v.instance_number and e.instance_number = v.instance_number and b.instance_number(+) = e.instance_number and b.stat_name(+) = e.stat_name and nvl(e.value,0) - nvl(b.value,0) > 0 group by v.snap_time, e.service_name"

    @timeit
    def dborasga(self):
        if 'dba_hist_sgastat' not in self.tables: self.extract('dba_hist_sgastat')
        return f"select to_timestamp(v.snap_time, 'YYYYMMDDHH24MISSFF') timestamp, pool, name, to_char(s.bytes/1024/1024, '{self.decfmt}') sizex from {self.name('vdeltas')} v, {self.name('dba_hist_sgastat')} s where s.snap_id = v.eid and s.dbid = v.dbid and s.instance_number = v.instance_number"

    @timeit
    def dborareq(self, dbid, sqlids):
        return f"select sql_id sqlid, REGEXP_REPLACE(dbms_lob.substr(sql_text,3000,1), '[^[:print:]]', '?') as request from dba_hist_sqltext where dbid={dbid} and sql_id in {sqlids}"

    @timeit
    def orahqs(self):
        if 'dba_hist_sqlstat' not in self.tables: self.extract('dba_hist_sqlstat')
        return f"select to_timestamp(v.snap_time, 'YYYYMMDDHH24MISSFF') timestamp, 1 kairos_count, e.sql_id sqlid, plan_hash_value, optimizer_cost, optimizer_mode, optimizer_env_hash_value, sharable_mem, loaded_versions, version_count,  module, action, sql_profile, force_matching_signature, parsing_schema_id, parsing_schema_name, parsing_user_id, fetches_delta, end_of_fetch_count_delta, sorts_delta, executions_delta, px_servers_execs_delta, loads_delta, invalidations_delta, parse_calls_delta, disk_reads_delta, buffer_gets_delta, rows_processed_delta, cpu_time_delta, elapsed_time_delta, iowait_delta, clwait_delta, apwait_delta, ccwait_delta, direct_writes_delta, plsexec_time_delta, javexec_time_delta, io_offload_elig_bytes_delta, io_interconnect_bytes_delta, physical_read_requests_delta, physical_read_bytes_delta, physical_write_requests_delta, physical_write_bytes_delta, optimized_physical_reads_delta, cell_uncompressed_bytes_delta, io_offload_return_bytes_delta, con_dbid, e.con_id from {self.name('vdeltas')} v, {self.name('dba_hist_sqlstat')} e where e.snap_id = v.eid and e.dbid = v.dbid and e.instance_number = v.instance_number"

    @timeit
    def orahas(self):
        if 'dba_hist_active_sess_history' not in self.tables and not self.vdollar: self.extract('dba_hist_active_sess_history')
        if not self.vdollar: return f"select sample_time timestamp, 1 kairos_count, sql_id, sample_id, session_id, session_serial#, user_id, sql_child_number, sql_plan_hash_value, force_matching_signature, sql_opcode, service_hash, decode(session_type, 'USER', 'FOREGROUND', session_type) session_type, session_state, qc_session_id, qc_instance_id, blocking_session, blocking_session_status, blocking_session_serial#, event, event_id, seq#, p1, p1text, p2, p2text, p3, p3text, wait_class, wait_class_id, nvl(wait_time,0), nvl(time_waited,0), rawtohex(xid) xid, current_obj#, current_file#, current_block#, program, module, action, client_id, blocking_hangchain_info, blocking_inst_id, capture_overhead, consumer_group_id, current_row#, nvl(delta_interconnect_io_bytes,0), nvl(delta_read_io_bytes,0), nvl(delta_read_io_requests,0), nvl(delta_time,0), nvl(delta_write_io_bytes,0), nvl(delta_write_io_requests,0), ecid, flags, in_bind, in_connection_mgmt, in_cursor_close, in_hard_parse, in_java_execution, in_parse, in_plsql_compilation, in_plsql_execution, in_plsql_rpc, in_sequence_load, in_sql_execution, is_captured, is_replayed, is_sqlid_current, machine, nvl(pga_allocated,0) pga_allocated, plsql_entry_object_id, plsql_entry_subprogram_id, plsql_object_id, plsql_subprogram_id, port, qc_session_serial#, remote_instance#, replay_overhead, sql_exec_id, to_char(sql_exec_start, 'YYYYMMDDHH24MISS'), sql_opname, sql_plan_line_id, sql_plan_operation, sql_plan_options, nvl(temp_space_allocated,0) temp_space_allocated, time_model, nvl(tm_delta_cpu_time,0), nvl(tm_delta_db_time,0), nvl(tm_delta_time,0), top_level_call#, top_level_call_name, top_level_sql_id, top_level_sql_opcode, dbreplay_file_id, dbreplay_call_counter from {self.name('dba_hist_active_sess_history')}"
        else: return f"select sample_time timestamp, 1 kairos_count, sql_id, sample_id, session_id, session_serial#, user_id, sql_child_number, sql_plan_hash_value, force_matching_signature, sql_opcode, service_hash, decode(session_type, 'USER', 'FOREGROUND', session_type) session_type, session_state, qc_session_id, qc_instance_id, blocking_session, blocking_session_status, blocking_session_serial#, event, event_id, seq#, p1, p1text, p2, p2text, p3, p3text, wait_class, wait_class_id, nvl(wait_time,0), nvl(time_waited,0), rawtohex(xid) xid, current_obj#, current_file#, current_block#, program, module, action, client_id, blocking_hangchain_info, blocking_inst_id, capture_overhead, consumer_group_id, current_row#, nvl(delta_interconnect_io_bytes,0), nvl(delta_read_io_bytes,0), nvl(delta_read_io_requests,0), nvl(delta_time,0), nvl(delta_write_io_bytes,0), nvl(delta_write_io_requests,0), ecid, flags, in_bind, in_connection_mgmt, in_cursor_close, in_hard_parse, in_java_execution, in_parse, in_plsql_compilation, in_plsql_execution, in_plsql_rpc, in_sequence_load, in_sql_execution, is_captured, is_replayed, is_sqlid_current, machine, nvl(pga_allocated,0) pga_allocated, plsql_entry_object_id, plsql_entry_subprogram_id, plsql_object_id, plsql_subprogram_id, port, qc_session_serial#, remote_instance#, replay_overhead, sql_exec_id, to_char(sql_exec_start, 'YYYYMMDDHH24MISS'), sql_opname, sql_plan_line_id, sql_plan_operation, sql_plan_options, nvl(temp_space_allocated,0) temp_space_allocated, time_model, nvl(tm_delta_cpu_time,0), nvl(tm_delta_db_time,0), nvl(tm_delta_time,0), top_level_call#, top_level_call_name, top_level_sql_id, top_level_sql_opcode, dbreplay_file_id, dbreplay_call_counter from V$ACTIVE_SESSION_HISTORY"

    @timeit
    def orahsm(self):
        if 'dba_hist_sysmetric_history' not in self.tables: self.extract('dba_hist_sysmetric_history')
        return f"select begin_time, end_time, intsize, group_id, metric_id, metric_name, to_char(value, '{self.decfmt}') value, metric_unit, con_dbid, con_id from {self.name('dba_hist_sysmetric_history')}"

    @timeit
    def getawrinterval(self):
        if not hasattr(self, 'awr_interval'): self.awr_interval = approx([1, 10, 60, 300, 600, 900, 1200, 1800, 3600], self.query(f'select distinct timestamp from ({self.dboramisc()}) order by timestamp')['timestamp'].diff().min().total_seconds())
        return self.awr_interval

    @timeit
    def getashinterval(self):
        self.ash_interval = approx([1, 10], self.query(f'select distinct timestamp from ({self.orahas()}) order by timestamp')['timestamp'].diff().min().total_seconds())
        return self.ash_interval

def genchart(fig, anchor=None):
            st.header(f"",anchor=anchor)
            c1, c2 = st.columns([10,1])
            with c1:
                st.plotly_chart(fig, use_container_width=True)
            with c2:
               st.markdown('[Back to Top](#home)')

def gentrace(sampling=1, top=1, awr_interval=3600, ash_interval=10, grouping='10 seconds', type='L', ash=False):
    grp = lambda x: 1 if x=='second' else 10 if x=='10 seconds' else 60 if x=='minute' else 300 if x=='5 minutes' else 600 if x=='10 minutes' else 900 if x=='15 minutes' else 1200 if x=='20 minutes' else 1800 if x=='30 minutes' else 3600 if x=='hour' else 2*3600 if x=='2 hours' else 3*3600 if x=='3 hours' else 4*3600 if x=='4 hours' else 6*3600 if x=='6 hours' else 8*3600 if x=='8 hours' else 12*3600 if x=='12 hours' else 24*3600 if x=='day' else 0
    grouping = grp(grouping)
    divider = grouping / awr_interval if not ash and grouping > awr_interval else grouping / ash_interval if ash and grouping > ash_interval else 1
    cvd = lambda x: datetime(x.year, x.month, x.day)
    cv12h = lambda x: datetime(x.year, x.month, x.day, 12 * (x.hour // 12))
    cv8h = lambda x: datetime(x.year, x.month, x.day, 8 * (x.hour // 8))
    cv6h = lambda x: datetime(x.year, x.month, x.day, 6 * (x.hour // 6))
    cv4h = lambda x: datetime(x.year, x.month, x.day, 4 * (x.hour // 4))
    cv3h = lambda x: datetime(x.year, x.month, x.day, 3 * (x.hour // 3))
    cv2h = lambda x: datetime(x.year, x.month, x.day, 2 * (x.hour // 2))
    cvh = lambda x: datetime(x.year, x.month, x.day, x.hour)
    cv30m = lambda x: datetime(x.year, x.month, x.day, x.hour, 30 * (x.minute // 30))
    cv20m = lambda x: datetime(x.year, x.month, x.day, x.hour, 20 * (x.minute // 20))
    cv15m = lambda x: datetime(x.year, x.month, x.day, x.hour, 15 * (x.minute // 15))
    cv10m = lambda x: datetime(x.year, x.month, x.day, x.hour, 10 * (x.minute // 10))
    cv5m = lambda x: datetime(x.year, x.month, x.day, x.hour, 5 * (x.minute // 5))
    cvm = lambda x: datetime(x.year, x.month, x.day, x.hour, x.minute)
    cv10s = lambda x: datetime(x.year, x.month, x.day, x.hour, x.minute, 10 * (x.second // 10))
    cvs = lambda x: datetime(x.year, x.month, x.day, x.hour, x.minute, x.second)
    cvtime = lambda x: cvs(x) if grouping == 1 else cv10s(x) if grouping == 10 else cvm(x) if grouping == 60 else cv5m(x) if grouping == 300 else cv10m(x) if grouping == 600 else cv15m(x) if grouping == 900 else cv20m(x) if grouping == 1200 else cv30m(x) if grouping == 1800 else cvh(x) if grouping == 3600 else cv2h(x) if grouping == 2*3600 else cv3h(x) if grouping == 3*3600 else cv4h(x) if grouping == 4*3600 else cv6h(x) if grouping == 6*3600 else cv8h(x) if grouping == 8*3600 else cv12h(x) if grouping == 12*3600 else cvd(x)
    class Trace:
        def __init__(s, request=None, top=top, type=type):
            s.type = type
            s.df = request
            if not request.empty:
                s.df = request.sample(frac=sampling).sort_index()
                s.df.timestamp = s.df.timestamp.apply(cvtime)
                s.df.value = s.df.value.apply(pd.to_numeric)
                s.df = s.df.groupby(['timestamp', 'legend'])['value'].sum().reset_index()
                s.df.value = s.df.value / divider
                print(s.df)
                ltop = s.df.drop(columns=['timestamp']).groupby(['legend']).sum().reset_index().nlargest(top, 'value')['legend'].unique().tolist()
                #ltop.reverse()
                pdl = []
                for x in ltop: pdl.append(s.df.loc[s.df['legend'] == x])
                s.df = pd.concat(pdl) if len(pdl) > 0 else s.df
        def __add__(s, t):
            s.df = pd.concat([s.df, t.df])
            return s
    return Trace

class Chart:
    COLORS = {'DB CPU': 'yellow', 'wait events': 'pink', 'DB time': 'blue', 'NUM_CPUS': 'red', 'USER_TIME': 'yellow', 'SYS_TIME': 'orange', 'sessions': 'red'}
    def __init__(s, title=None, ytitle=None, plots=[[[]]], xaxis={}):
        s.title = title
        s.ytitle = ytitle
        s.plots = plots
        s.xaxis = xaxis
    def draw(s):
        rows = max(len(s.plots),1)
        cols = max(len(s.plots[0]),1)
        fig = make_subplots(rows=rows, cols=cols, shared_xaxes=True, vertical_spacing=0.1)
        for row in range(1, len(s.plots)+1):
            for col in range(1, len(s.plots[0])+1):
                traces = s.plots[row-1][col-1]
                layoptions = dict()
                for desc in traces:
                    for z in desc.df['legend'].unique():
                        d = dict()
                        d['x'] = desc.df.loc[desc.df['legend'] == z]['timestamp']
                        d['y'] = desc.df.loc[desc.df['legend'] == z]['value']
                        d['name'] = z
                        d['legendgroup'] = z
                        d['marker'] = dict(color=getcolor(Chart.COLORS, z))
                        if desc.type == 'L':
                            d['line_shape'] = 'spline'
                            subfig = go.Scatter(**d)
                        if desc.type == 'WL':
                            d['line'] = dict(color=getcolor(Chart.COLORS, z), shape='hv')
                            subfig = go.Scattergl(**d)
                        if desc.type == 'WA':
                            d['line'] = dict(color=getcolor(Chart.COLORS, z), shape='hv')
                            d['fill'] = 'tozeroy'
                            d['fillcolor'] = getcolor(Chart.COLORS, z)
                            subfig = go.Scattergl(**d)
                        if desc.type == 'WM':
                            d['mode'] = 'markers'
                            d['marker'] = dict(color=getcolor(Chart.COLORS, z))
                            subfig = go.Scattergl(**d)
                        if desc.type == 'SA':
                            d['stackgroup'] = f'sg{row}{col}'
                            d['line_shape'] = 'spline'
                            subfig = go.Scatter(**d)
                        if desc.type == 'SC':
                            d['offsetgroup'] = 0
                            layoptions['barmode'] = 'stack'
                            subfig = go.Bar(**d)
                        fig.add_trace(subfig, row=row, col=col)

        fig.update_layout(showlegend=True, title_text=s.title, yaxis_title=s.ytitle, **layoptions)
        fig.layout.xaxis = s.xaxis
        fig.layout.yaxis.rangemode = "tozero"
        fig.layout.legend = dict(x=0, y=-0.15, orientation='h')
        return fig

def genscript(f):
    source = pscript.py2js(textwrap.dedent(inspect.getsource(f)))
    name = f.__name__
    return dict(name=name, source=source)

def include(x, y):
    y.append(x)
    return x

def JS_header():
    def sendMessageToStreamlitClient(type, data):
        outData = Object.assign(dict(isStreamlitMessage=True, type=type), data)
        window.parent.postMessage(outData, "*")

    def setCR():
        sendMessageToStreamlitClient("streamlit:componentReady", dict(apiVersion=1))

    def setCV(value):
        sendMessageToStreamlitClient("streamlit:setComponentValue", dict(value=value))

    def setFH(height):
        sendMessageToStreamlitClient("streamlit:setFrameHeight", dict(height=height))

    def addEL(type, callback):
        def f(event):
            if event.data.type == type:
                callback(event)
        window.addEventListener("message",f)
    return dict(setComponentReady=setCR, setComponentValue=setCV, setFrameHeight=setFH, events=dict(addEventListener=addEL))

HEADERSCRIPT = genscript(JS_header)

def JS_body(entry):
    def onRender(event):
        if not window.rendered:
            domContainer = document.querySelector('#app')
            root = ReactDOM.createRoot(domContainer)
            root.render(React.createElement(entry, event.data.args))
            def f():         
                anchor.originFrameHeight = document.body.scrollHeight
                anchor.iframeHeight = event.data.args.extendHeight if hasattr(event.data.args, "extendHeight") else document.body.scrollHeight
                Streamlit.setFrameHeight(anchor.originFrameHeight)
            setTimeout(f, 100)
            window.rendered = True
    Streamlit.events.addEventListener("streamlit:render", onRender)
    Streamlit.setComponentReady()

BODYSCRIPT = genscript(JS_body)

class ReactComponent: pass

class GenPage:
    def __init__(self, *components):
        html = HTML()
        head = include(HEAD(), html)
        head.append(SCRIPT(src="react.development.js"))
        head.append(SCRIPT(src="react-dom.development.js"))
        head.append(SCRIPT(src="dayjs.min.js"))
        head.append(SCRIPT(src="antd.min.js"))
        head.append(SCRIPT(src="index.umd.min.js"))
        head.append(SCRIPT("ReactComponent=React.Component;anchor={};"))
        head.append(LINK(rel="stylesheet",href="reset.css"))
        source = f'{HEADERSCRIPT["source"]}\nStreamlit={HEADERSCRIPT["name"]}();'
        head.append(SCRIPT(mark_safe(source)))
        body = include(BODY(), html)
        body.append(DIV(id="app"))
        source = ''
        entry = ''
        for c in components:
            source += genscript(c)['source'] + '\n'
            entry = genscript(c)['name'] if not entry else entry
        source += f'{BODYSCRIPT["source"]}\n{BODYSCRIPT["name"]}({entry})'
        body.append(SCRIPT(mark_safe(source)))
        self.html = html
    def render(self, file=None):
        f =open(file, 'w')
        f.write('\n'.join([e for e in self.html.render(None)]))
        f.close()
    def gencomponent(self, name):
        dir = f"{tempfile.gettempdir()}/{name}"
        if not os.path.isdir(dir): os.mkdir(dir)
        shutil.copytree(f'/home/app/pages/scripts', dir, dirs_exist_ok=True)
        fname = f'{dir}/index.html'
        self.render(fname)
        func = components.declare_component(name, path=str(dir))
        def f(**params):
            component_value = func(**params)
            return component_value
        return f

class GenComponent:
    def __init__(self, name, *components):
        self.component = GenPage(*components).gencomponent(name)
    def encapsulate(self, use):
        return use(self.component)

def use_default(component):
    class Component:
        def __init__(self, **d):
            result = component(**d)
            self.result = result
        def get(self):
            return self.result if hasattr(self, 'result') else None
    return Component

def use_Menu(component):
    class Component:
        def __init__(self, id=None, **d):
            id = f'Component_{id}'
            if id not in st.session_state: st.session_state[id] = dict(old=0, new=0)
            result = component(id=id, counter=st.session_state[id]['new'], default={'key': None}, **d)
            if 'counter' in result and result['counter'] != st.session_state[id]['new']:
                st.session_state[id]['new'] = result['counter']
                st.session_state[id]['result'] = result
                del st.session_state[id]['result']['counter']
                run_again()
            if st.session_state[id]['old'] != st.session_state[id]['new']:
                self.result = st.session_state[id]['result']
                st.session_state[id]['old'] = st.session_state[id]['new']
            else: self.result = result
        def get(self):
            return self.result['key'] if hasattr(self, 'result') else None
    return Component

class Menu(ReactComponent):
    def handleMenuClick(e):
        result = {'counter': self.props.counter + 1, 'key': e.key}
        Streamlit.setComponentValue(result)
    def render():
        for m in self.props.menu:
            if m.icon: m.icon = React.createElement(icons[m.icon], {})
        props = dict()
        props['items'] = self.props.menu
        props['disabled'] = self.props.disabled
        props['mode'] = self.props.mode
        props['theme'] = self.props.theme
        props['onClick'] = self.handleMenuClick
        return React.createElement(antd.Menu, props)

class Tree(ReactComponent):
    def titleRender(x):
        iprops = x.iconProps if x.iconProps else {}
        gprops = x.tagProps if x.tagProps else {}
        icon = React.createElement(icons[x.icon], iprops) if x.icon else ''
        tag = React.createElement(antd.Tag, gprops, icon,' ', x.tag)
        tprops = x.titleProps if x.titleProps else {}
        sprops = x.spaceProps if x.spaceProps else {}
        return React.createElement(antd.Typography.Title, tprops, React.createElement(antd.Space, sprops, tag, x.title))               
    def onSelect(e):
        result = e[0]
        Streamlit.setComponentValue(result)        
    def onDrop(e):
        ctrl = True if e.event.ctrlKey == True else False
        alt = True if e.event.altKey == True else False
        event = 'pasteA' if alt else 'pasteC' if ctrl else 'move'
        result = {'event': event, 'from': e.dragNode.key, 'to': e.node.key, 'ftype': e.dragNode.tag, 'ttype': e.node.tag}
        Streamlit.setComponentValue(result)       
    def render():
        props = dict()
        props['onSelect'] = self.onSelect
        props['onDrop'] = self.onDrop
        props['treeData'] = self.props.tree
        props['theme'] = self.props.theme
        props['showLine'] = self.props.showLine
        props['showIcon'] = self.props.showIcon
        props['selectedKeys'] = self.props.selectedKeys
        props['expandedKeys'] = self.props.expandedKeys
        props['height'] = self.props.height
        props['titleRender'] = self.titleRender
        props['draggable'] = True
        return React.createElement(antd.Tree, props)
    

MENU = GenComponent('MENU', Menu).encapsulate(use_Menu)
TREE = GenComponent('TREE', Tree).encapsulate(use_default)
