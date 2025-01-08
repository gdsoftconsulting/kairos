import streamlit as st
from pages.functions.definitions import *

set_page_config()
gen_back_button()

param = st.query_params
if 'nodesdb' in param and param['nodesdb'] : st.session_state.nodesdb = param['nodesdb']
if 'systemdb' in param and param['systemdb'] : st.session_state.systemdb = param['systemdb']
if 'node' in param and param['node'] : st.session_state.node = param['node']
if 'query' in param and param['query'] : st.session_state.query = param['query']
if 'top' in param and param['top'] : st.session_state.top = param['top']

st.session_state.systemdb = 'kairos_system_system' if 'systemdb' not in st.session_state else st.session_state.systemdb
st.session_state.top = 10 if 'top' not in st.session_state else st.session_state.top

st.subheader(f"{st.session_state.query}@{st.session_state.nodesdb}: {getpath(st.session_state.node)}", divider='rainbow')
command = f"kairos -s executequery --nodesdb {st.session_state.nodesdb} --systemdb {st.session_state.systemdb} --id {st.session_state.node} --query '{st.session_state.query}' --top {st.session_state.top}"
act = run(command)
if 'success' in act and act['success']:
    st.dataframe(pd.DataFrame(act['data']), use_container_width=True)   
else: st.error(act['message'])