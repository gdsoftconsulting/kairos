import streamlit as st
from pages.functions.definitions import *

set_page_config()
gen_back_button()

st.subheader("KAIROS upgrade", divider='rainbow')
st.markdown(f'The current system is: **{systemname()}**')
url = 'postgres@localhost'
postgres=Postgres(url=url)
st.success(f'Connected to server with url: {url}')
query = "select * from pg_database"
st.write(postgres.query(query))
try: 
    configuration=readconfig()
    st.success(f'An existing configuration has been found whith the following values:')
except:
    ### Configuration has not been found! We are supposed to be on the system to migrate, the system where exports are required!
    st.subheader("KAIROS databases to export within 'old' version", divider='rainbow')
    query = "select datname, pg_database_size(datname)*1.0/1024/1024/1024 as size from pg_database where datname like 'kairos_user_%' or datname like 'kairos_group_%'"
    dbs = postgres.query(query)
    st.write(dbs)
    st.markdown(f"In this KAIROS site there {'is' if dbs.shape[0] == 1 else 'are'} {dbs.shape[0]} database{'' if dbs.shape[0] == 1 else 's'} to migrate.")
    st.markdown('The databases can be exported and imported independently of each other in any order.')
    st.markdown('The kairos_system_system database is not included in the export/import process.')
    st.markdown('The target environment is pristine! It only has the admin user and its associated database, which is "kairos_user_admin". It is unaware of the existence of anything that existed in the original environment.')
    st.markdown('The tool performing the migration must therefore create a structure (in JSON format) that contains the necessary information for recreating the objects in the target environment.')
    st.markdown('This includes the list of users, the list of roles/groups, authorized accesses for users in relation to groups, etc.')
    st.markdown('Examples illustrating this latter possibility:')
    configuration=dict(export_started=False, import_started=False, origin=None, target=None)
    writeconfig(configuration)
    st.success(f'A new configuration has been initiated whith the following values:')
st.json(configuration)

### In the bloc hereafter, export has been started and we are on the system where exports are initiated
if configuration['export_started'] and systemname() == configuration['origin']:
    buttons = dict()
    with st.form("actions"):
        for x in configuration['users']:
            if configuration['status'][f'kairos_user_{x}'] == 'Not started': buttons[f'user@{x}@clear'] = st.form_submit_button(f'Clear cache for database: kairos_user_{x}') 
            if configuration['status'][f'kairos_user_{x}'] == 'Cache cleared': buttons[f'user@{x}@export'] = st.form_submit_button(f'Export database: kairos_user_{x}') 
        for x in configuration['roles']:
            if configuration['status'][f'kairos_group_{x}'] == 'Not started': buttons[f'group@{x}@clear'] = st.form_submit_button(f'Clear cache for database: kairos_group_{x}')
            if configuration['status'][f'kairos_group_{x}'] == 'Cache cleared': buttons[f'group@{x}@export'] = st.form_submit_button(f'Export database: kairos_group_{x}') 
    for b in buttons:
        if buttons[b]:
            (ty, id, ac) = b.split('@')
            if ac == 'clear':
                status = run(f"kairos -s getid --nodesdb kairos_{ty}_{id} --pattern '^'")
                if status['success']:
                    nid = status['data'][0]['id']
                    status = run(f"kairos -s clearprogenycaches --nodesdb kairos_{ty}_{id} --systemdb kairos_system_system --id {nid}")
                    if status['success']: 
                        st.success(status['data']['msg'])
                        configuration['status'][f'kairos_{ty}_{id}'] = 'Cache cleared'
                        writeconfig(configuration)
                    else: st.error(status['data']['msg'])
                else: st.error(st.error(status['data']['msg']))
                st.rerun()
            if ac == 'export':
                status = run(f"kairos -s export --nodesdb kairos_{ty}_{id}")
                if status['success']: 
                    st.success(status['data']['msg'])
                    configuration['status'][f'kairos_{ty}_{id}'] = 'Export done successfully'
                    writeconfig(configuration)
                else: st.error(status['data']['msg'])
                st.rerun()
    if len(buttons) == 0: st.success(f'The export process is succesfully completed on {systemname()}! Check on "target" system the amount of work remaining')
    else: st.warning(f'There are still operations to be carried out on the {systemname()}!')

### In the bloc hereafter, import has been started and we are on the system where imports are initiated
if configuration['import_started'] and systemname() == configuration['target']:
    users = run('kairos -s listusers')
    groups = run('kairos -s listroles')
    grants = run('kairos -s listgrants')
    existing=dict()
    existing['users'] = [x['user'] for x in users['data']]
    existing['roles'] = [x['role'] for x in groups['data']]
    existing['grants'] = [(x['user'],x['role']) for x in grants['data']]
    buttons = dict()
    with st.form("actions"):
        for x in configuration['users']:
            if x not in existing['users']: buttons[f'user@{x}@create'] = st.form_submit_button(f'Create user: {x}')
            else:
                if configuration['status'][f'kairos_user_{x}'] == 'Export done successfully': buttons[f'user@{x}@import'] = st.form_submit_button(f'Import database: kairos_user_{x}') 
        for x in configuration['roles']:
            if x not in existing['roles']: buttons[f'group@{x}@create'] = st.form_submit_button(f'Create role: {x}')
            else:
                if configuration['status'][f'kairos_group_{x}'] == 'Export done successfully': buttons[f'group@{x}@import'] = st.form_submit_button(f'Import database: kairos_group_{x}') 
        for (x,y) in configuration['grants']:
            if (x,y) not in existing['grants']: buttons[f'grant@{x}/{y}@create'] = st.form_submit_button(f'Grant role: {y} to {x}')
    for b in buttons:
        if buttons[b]:
            (ty, id, ac) = b.split('@')
            if ac == 'create' and ty == 'user':
                status = run(f'kairos -s createuser --user {id} -a admin -p admin')
                if status['success']: st.success(status['data']['msg'])
                else: st.error(status['data']['msg'])
                st.rerun()
            if ac == 'create' and ty == 'group':
                status = run(f'kairos -s createrole --role {id} -a admin -p admin')
                if status['success']: st.success(status['data']['msg'])
                else: st.error(status['data']['msg'])
                st.rerun()
            if ac == 'create' and ty == 'grant':
                (u,r) = id.split('/')
                status = run(f'kairos -s creategrant --user {u} --role {r} -a admin -p admin')
                if status['success']: st.success(status['data']['msg'])
                else: st.error(status['data']['msg'])
                st.rerun()
            if ac == 'import':
                status = run(f"kairos -s import --nodesdb kairos_{ty}_{id}")
                if status['success']: 
                    st.success(status['data']['msg'])
                    configuration['status'][f'kairos_{ty}_{id}'] = 'Import done successfully'
                    writeconfig(configuration)
                else: st.error(status['data']['msg'])
                st.rerun()
    if len(buttons) !=0: st.warning(f'There are still operations to be carried out on the {systemname()}!')
    else:
        done = True
        for x in configuration['status']:
            if configuration['status'][x] != 'Import done successfully': done=False
        if done:
            st.warning(f'The whole process is done! Configuration file can be removed!')
            os.remove('/export/configuration')
        else:
            st.warning(f"There are yet operations to run on {configuration['origin']} system")
            

### In the bloc hereafter, import has not yet been started and we are on the system where imports are initiated
if configuration['export_started'] and not configuration['import_started'] and systemname() != configuration['origin'] and configuration['target'] is None:
    run('kairos -s checkserverconfig')
    import_started =  st.button('START import process')
    if import_started:
        configuration['import_started'] = True
        configuration['target'] = systemname()
        writeconfig(configuration)
        st.rerun()

### In the bloc hereafter, export has not yet been started and we are on the system where exports are initiated
if not configuration['export_started'] and configuration['origin'] is None:
    st.markdown('When the "START export/import process" button is pressed, the configuration is updated with a status for each database. Initially, the status of each database is "Not started." This status will evolve as operations are carried out.')
    st.markdown('After being pressed the "START export/import process" button disappears to make room for other possible actions.')
    export_started =  st.button('START export process')
    if export_started:
        users = run('kairos -s listusers')
        groups = run('kairos -s listroles')
        grants = run('kairos -s listgrants')
        configuration['origin'] = systemname()
        configuration['target'] = None
        configuration['users'] = [x['user'] for x in users['data']]
        configuration['roles'] = [x['role'] for x in groups['data']]
        configuration['grants'] = [(x['user'],x['role']) for x in grants['data']]
        configuration['status'] = dict()
        for x in configuration['users']: configuration['status'][f'kairos_user_{x}']='Not started'
        for x in configuration['roles']: configuration['status'][f'kairos_group_{x}']='Not started'
        configuration['export_started'] = True
        writeconfig(configuration)
        st.rerun()

