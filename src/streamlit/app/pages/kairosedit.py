import streamlit as st
import base64
from pages.functions.definitions import *

theme=set_page_config()
gen_back_button()

param = st.query_params
if 'nodesdb' in param and param['nodesdb'] : st.session_state.nodesdb = param['nodesdb']
if 'object' in param and param['object'] : st.session_state.nodesdb = param['object']
if 'type' in param and param['type'] : st.session_state.nodesdb = param['type']

command = f"kairos -s getobject --database {st.session_state.nodesdb} --id '{st.session_state.object}' --type {st.session_state.type}"
act = run(command)
if 'success' in act and act['success']:
    content = act['data']
    contentm = st_ace(content, keybinding='vim', language='python', theme='tomorrow_night' if theme['streamlit_theme'] == 'dark' else 'tomorrow')
    if contentm != content: 
        encode = lambda x: base64.b64encode(x.encode()).decode()
        command = f'kairos -s setobject --database {st.session_state.nodesdb} --source {encode(contentm)}'
        act = run(command)
        if 'success' in act and act['success']: st.success(act['data']['msg'])
        else: st.error(act['message'])
else: st.error(act['message'])