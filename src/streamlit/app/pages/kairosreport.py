import streamlit as st
from pages.functions.definitions import *

set_page_config()
gen_back_button()

param = st.query_params
if 'nodesdb' in param and param['nodesdb'] : st.session_state.nodesdb = param['nodesdb']
if 'systemdb' in param and param['systemdb'] : st.session_state.systemdb = param['systemdb']
if 'node' in param and param['node'] : st.session_state.node = param['node']
if 'colors' in param and param['colors'] : st.session_state.colors = param['colors']
if 'template' in param and param['template'] : st.session_state.template = param['template']
if 'plotorientation' in param and param['plotorientation'] : st.session_state.plotorientation = param['plotorientation']
if 'top' in param and param['top'] : st.session_state.top = param['top']
if 'report' in param and param['report'] : st.session_state.report = param['report']
st.session_state.systemdb = 'kairos_system_system' if 'systemdb' not in st.session_state else st.session_state.systemdb
st.session_state.colors = 'COLORS' if 'colors' not in st.session_state else st.session_state.colors
st.session_state.template = 'DEFAULT' if 'template' not in st.session_state else st.session_state.template
st.session_state.plotorientation = 'vertical' if 'plotorientation' not in st.session_state else st.session_state.plotorientation
st.session_state.top = 10 if 'top' not in st.session_state else st.session_state.top
st.subheader(f"{st.session_state.report}@{st.session_state.nodesdb}:{getpath(st.session_state.node)}", divider='rainbow')
command = f'kairos -s getobject --database {st.session_state.nodesdb} --id {st.session_state.report} --type report'
act = run(command)
if 'success' in act and act['success']:
    source = act['data']
    p = compile(source, '', 'exec')
    exec(p, locals())
    obj = locals()['UserObject']()
    for a in obj['actions']:
        if a['name'] == 'header': st.subheader(a['value'])
        if a['name'] == 'runchart':
            command = f'kairos -s runchart --nodesdb {st.session_state.nodesdb} --systemdb {st.session_state.systemdb} --id {st.session_state.node} --colors {st.session_state.colors} --template {st.session_state.template} --plotorientation {st.session_state.plotorientation} --chart {a["value"]} --top {st.session_state.top} --width 2000 --height 1600'
            act = run(command)
            if 'success' in act and act['success']:
                figure = go.Figure(act['data']['chart']['figure'])
                st.plotly_chart(figure, use_container_width=True)
            else: st.error(act['message'])
        if a['name'] == 'runcollection':
            command = f'kairos -s displaycollection --nodesdb {st.session_state.nodesdb} --systemdb {st.session_state.systemdb} --id {st.session_state.node} --collection {a["value"]}'
            act = run(command)
            if 'success' in act and act['success']:
                st.dataframe(pd.DataFrame(act['data']), use_container_width=True)   
            else: st.error(act['message'])
else: st.error(act['message'])