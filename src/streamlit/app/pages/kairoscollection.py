import streamlit as st
from pages.functions.definitions import *

set_page_config()
gen_back_button()

param = st.query_params
if 'nodesdb' in param and param['nodesdb'] : st.session_state.nodesdb = param['nodesdb']
if 'systemdb' in param and param['systemdb'] : st.session_state.systemdb = param['systemdb']
if 'node' in param and param['node'] : st.session_state.node = param['node']
if 'collection' in param and param['collection'] : st.session_state.collection = param['collection']
st.session_state.systemdb = 'kairos_system_system' if 'systemdb' not in st.session_state else st.session_state.systemdb

st.subheader(f"{st.session_state.collection}@{st.session_state.nodesdb}: {getpath(st.session_state.node)}", divider='rainbow')
command = f'kairos -s displaycollection --nodesdb {st.session_state.nodesdb} --systemdb {st.session_state.systemdb} --id {st.session_state.node} --collection {st.session_state.collection}'
act = run(command)
if 'success' in act and act['success']:
    st.dataframe(pd.DataFrame(act['data']), use_container_width=True)   
else: st.error(act['message'])