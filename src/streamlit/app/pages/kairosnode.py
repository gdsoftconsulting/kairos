import streamlit as st
from pages.functions.definitions import *

set_page_config()
gen_back_button()

param = st.query_params
if 'nodesdb' in param and param['nodesdb'] : st.session_state.nodesdb = param['nodesdb']
if 'node' in param and param['node'] : st.session_state.node = param['node']

st.subheader(f"{st.session_state.nodesdb}: {getpath(st.session_state.node)}", divider='rainbow')
command = f'kairos -s getnode --nodesdb {st.session_state.nodesdb} --id {st.session_state.node}'
act = run(command)
if 'success' in act and act['success']:
    st.write(act['data'])
else: st.error(act['message'])