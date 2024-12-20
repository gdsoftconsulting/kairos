import streamlit as st
from pages.functions.definitions import *

theme = set_page_config()
gen_back_button()

logger.debug('Generating the KAIROS page ...')
ct=st.empty()
ct.error('Working ....')
notconnected = True if "user" not in st.session_state else False
admin = True if 'adminrights' in st.session_state and st.session_state.adminrights else False
notadminornotconnected = not admin or notconnected
col1, col2 = st.columns([1,4])
with col1:
    menu = []
    menu.append({'label':'Logout', 'key':"Logout", 'icon': 'LogoutOutlined', 'disabled': notconnected})
    menu.append({'label':'Manage password', 'key':"Manage password", 'icon': 'UserOutlined', 'disabled': notconnected})
    menu.append({'label':'Manage settings', 'key':"Manage settings", 'icon': 'ToolOutlined', 'disabled': notconnected})
    menu.append({'label':'Manage objects', 'key':"Manage objects", 'icon': 'BuildFilled', 'disabled': notconnected})
    menu.append({'label':'Manage users and roles', 'key':"Manage users and roles", 'icon': 'UserOutlined', 'disabled': notadminornotconnected})
    menu.append({'type':'divider'})
    menu.append({'label':'Kairos log', 'key':"Kairos log", 'icon': 'ProfileOutlined'})
    menu.append({'label':'Postgres log', 'key':"Postgres log", 'icon': 'ProfileOutlined'})
    menu.append({'label':'Web server log', 'key':"Web server log", 'icon': 'ProfileOutlined'})
    menu.append({'label':'Streamlit log', 'key':"Streamlit log", 'icon': 'ProfileOutlined'})
    menu.append({'type':'divider'})
    menu.append({'label':'Utilities','type': 'group', 'children':[
        {'label':'Kairos introspection', 'key':"Kairos introspection"},
        {'label':'Kairos upgrade', 'key':"Kairos upgrade"},
    ]})
    menu.append({'type':'divider'})
    menu.append({'label':'Documentation', 'key':"Documentation", 'icon': 'ReadOutlined'})
    m1 = MENU(menu=menu, height=500, theme=theme['streamlit_theme'], id='kairos')
    st.session_state.mainmenu = m1.get()
    logger.debug(f'Mainmenu option: {st.session_state.mainmenu}')

with col2:
    if not st.session_state.mainmenu:
        title = st.subheader('Kairos', divider='rainbow')
        if "user" not in st.session_state:
            lusers = tuple([''] + get_users())
            user = st.selectbox( 'Choose a user to connect to kairos...', lusers, 0)
            if user:
                if "password" not in st.session_state:
                    password = st.text_input(f'Enter "{user}" password:', type="password")
                    if password:
                        command = f"kairos -s checkuserpassword -a {user} -p {password}"
                        act = run(command)
                        if 'success' in act and act['success']:
                            st.session_state.user = user
                            st.session_state.password = password
                            st.session_state.adminrights = act['data']['adminrights']
                            st.rerun()
                        else: st.error(act['message'])
        else:
            title.empty()
            user = st.session_state.user
            password = st.session_state.password
            if 'node' not in st.session_state: st.session_state.node = 1
            get_settings(theme)
            title = st.subheader(f"{user}@{st.session_state.nodesdb}", divider='rainbow')
            col1, col2 = st.columns([3,1])
            with col1:
                st.session_state.prevnode = st.session_state.node
                st.session_state.node = KairosTree(st.session_state.nodesdb, expanded=True).render()
                logger.debug(f'Selected node : {st.session_state.node}')


            with col2:
                notN = True if st.session_state.type not in ["N"] else False
                notB = True if st.session_state.type not in ["B"] else False
                notD = True if st.session_state.type not in ["D"] else False
                notABD = True if st.session_state.type not in ["A", "B","D"] else False
                notABCD = True if st.session_state.type not in ["A", "B", "C", "D"] else False
                notAN = True if st.session_state.type not in ["A", "N"] else False
                notCN = True if st.session_state.type not in ["C", "N"] else False
                notDN = True if st.session_state.type not in ["D", "N"] else False
                inABCDT = True if st.session_state.type in ["A", "B", "C", "D", "T"] else False
                inNT = True if st.session_state.type in ["N", "T"] else False
                rootortrash = True if st.session_state.node == "1" or st.session_state.type in ["T"] else False
                notcopied = True if 'copied' not in st.session_state or st.session_state.copied == None else False
                menu = []
                menu.append({'label': 'Upload', 'key':"Upload", 'disabled': notN})
                menu.append({'label': 'Manage nodes', 'children': [
                    {'label':'Create node', 'key':"Create node", 'disabled': inABCDT},
                    {'label':'Rename node', 'key':"Rename node", 'disabled': rootortrash},
                    {'label':'Delete node', 'key':"Delete node", 'disabled': rootortrash},
                    {'label':'Duplicate "D" node', 'key':'Duplicate "D" node', 'disabled': notD},
                    {'label':'Edit live object', 'key':'Edit live object', 'disabled': notD},
                    {'type':'divider'},
                    {'label':'Copy', 'key':'Copy', 'disabled': notABD},
                    {'label':'Paste to "A" node', 'key':'Paste to "A" node', 'disabled': notcopied or rootortrash or notAN or st.session_state.copied == st.session_state.node},
                    {'label':'Paste to "C" node', 'key':'Paste to "C" node', 'disabled': notcopied or rootortrash or notCN or st.session_state.copied == st.session_state.node},
                    {'type':'divider'},
                    {'label':'Transform to "A" node', 'key':'Transform to "A" node', 'disabled': notAN or rootortrash},
                    {'label':'Transform to "D" node', 'key':'Transform to "D" node', 'disabled': notDN or rootortrash},
                ]})
                menu.append({'label': 'Display', 'children': [
                    {'label':'Display node', 'key':'Display node'},
                    {'label':'Display collection', 'key':'Display collection', 'disabled': inNT},
                    {'type':'divider'},
                    {'label':'Execute query', 'key':'Execute query', 'disabled': inNT},
                    {'label':'Run chart', 'key':'Run chart', 'disabled': inNT},
                    {'type':'divider'},
                    {'label':'Run report', 'key':'Run report', 'disabled': inNT},
                ]})
                menu.append({'label': 'Manage caches', 'children': [
                    {'label':'Clear cache', 'key':'Clear cache', 'disabled': notABCD},
                    {'label':'Clear progeny caches', 'key':'Clear progeny caches', 'disabled': notN},
                    {'label':'Build progeny caches', 'key':'Build progeny caches', 'disabled': notN},
                ]})
                # menu.append({'label':'Download', 'children': [
                #     {'label':'Download node', 'key':'Download node', 'disabled': notB},
                #     {'label':'Download children', 'key':'Download children', 'disabled': notN},
                #     {'label':'Unload', 'key':'Unload', 'disabled': notABD},
                # ]})
                menu.append({'label':'Empty trash', 'key':'Empty trash'})
                m2 = MENU(menu=menu, height=600, mode='inline', theme=theme['streamlit_theme'], id='options')
                if m2.get(): 
                    st.session_state.nodemenu = m2.get()
                    logger.debug(f'Nodemenu option: {st.session_state.nodemenu}')

            if 'nodemenu' not in st.session_state: st.session_state.nodemenu = None
            if st.session_state.nodemenu == "Upload": kairos_upload_node()
            if st.session_state.nodemenu == "Create node": kairos_create_node()
            if st.session_state.nodemenu == "Rename node": kairos_rename_node()
            if st.session_state.nodemenu == "Delete node": kairos_delete_node()
            if st.session_state.nodemenu == "Empty trash": kairos_empty_trash()
            if st.session_state.nodemenu == 'Duplicate "D" node': kairos_duplicate_d_node()
            if st.session_state.nodemenu == 'Edit live object': kairos_edit_liveobject()
            if st.session_state.nodemenu == 'Copy': kairos_copy()
            if st.session_state.nodemenu == 'Paste to "A" node': kairos_paste_to_a_node()
            if st.session_state.nodemenu == 'Paste to "C" node': kairos_paste_to_c_node()
            if st.session_state.nodemenu == 'Transform to "A" node': kairos_transform_to_a_node()
            if st.session_state.nodemenu == 'Transform to "D" node': kairos_transform_to_d_node()
            if st.session_state.nodemenu == 'Display node': kairos_display_node()
            if st.session_state.nodemenu == 'Display collection': kairos_display_collection()
            if st.session_state.nodemenu == 'Execute query': kairos_execute_query()
            if st.session_state.nodemenu == 'Run chart': kairos_run_chart()
            if st.session_state.nodemenu == 'Run report': kairos_run_report()
            if st.session_state.nodemenu == 'Download node': kairos_download_node()
            if st.session_state.nodemenu == 'Clear cache': kairos_clear_cache()
            if st.session_state.nodemenu == 'Clear progeny caches': kairos_clear_progeny_caches()
            if st.session_state.nodemenu == 'Build progeny caches': kairos_build_progeny_caches()

if 'callstack' not in st.session_state: st.session_state.callstack = CallStack()
if st.session_state.mainmenu == "Logout":
    for key in st.session_state.keys(): del st.session_state[key]
    st.rerun()    
if st.session_state.mainmenu == "Manage password": st.session_state.callstack.call('kairospassword', 'kairos')
if st.session_state.mainmenu == "Manage settings": st.session_state.callstack.call('kairossettings', 'kairos')
if st.session_state.mainmenu == "Manage objects": st.session_state.callstack.call('kairosobjects', 'kairos')
if st.session_state.mainmenu == "Manage users and roles": st.session_state.callstack.call('kairosusers', 'kairos')
if st.session_state.mainmenu == "Kairos log": st.session_state.callstack.call('kairosklog', 'kairos')
if st.session_state.mainmenu == "Postgres log": st.session_state.callstack.call('kairosplog', 'kairos')
if st.session_state.mainmenu == "Web server log": st.session_state.callstack.call('kairoswlog', 'kairos')
if st.session_state.mainmenu == "Streamlit log": st.session_state.callstack.call('kairosslog', 'kairos')
if st.session_state.mainmenu == "Kairos introspection": st.session_state.callstack.call('kairosintro', 'kairos')
if st.session_state.mainmenu == "Kairos upgrade": st.session_state.callstack.call('kairosupgrade', 'kairos')
if st.session_state.mainmenu == "Documentation": st.session_state.callstack.call('kairosdoc', 'kairos')
st.session_state.mainmenu = None
ct.empty()
