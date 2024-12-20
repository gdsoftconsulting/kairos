import streamlit as st
from pages.functions.definitions import *

set_page_config()
gen_back_button()

param = st.query_params
if 'nodesdb' in param and param['nodesdb'] : st.session_state.nodesdb = param['nodesdb']
if 'systemdb' in param and param['systemdb'] : st.session_state.systemdb = param['systemdb']
st.session_state.systemdb = 'kairos_system_system' if 'systemdb' not in st.session_state else st.session_state.systemdb

st.subheader(f"Manage objects", divider='rainbow')
objects = pd.DataFrame(get_objects())
ufiles = st.file_uploader("Upload objects", accept_multiple_files=True)
for ufile in ufiles: 
    nodesdb = st.session_state.nodesdb
    name = ufile.name
    f = open(f'/tmp/{name}', 'w')
    f.write(ufile.read().decode())
    f.close()
    command = f"kairos -s uploadobject --nodesdb {nodesdb} --file '/tmp/{name}'"
    act = run(command)
    if 'success' in act and act['success']: 
        del st.session_state.objects
    else: st.error(act['message'])
objects['Delete ?'] = pd.Series([False for x in range(len(objects.index))]) 
objects['Download ?'] = pd.Series([False for x in range(len(objects.index))]) 
objects['Edit ?'] = pd.Series([False for x in range(len(objects.index))])
config = dict()
config['Delete ?'] = st.column_config.CheckboxColumn(default=False)
config['Download ?'] = st.column_config.CheckboxColumn(default=False)
config['Edit ?'] = st.column_config.CheckboxColumn(default=False)
disabled = ["created", "id", "origin", "rid", "type"]
st.data_editor(objects, key="manageobjects", column_config=config, disabled=disabled, use_container_width=True)
moa = st.session_state.manageobjects['edited_rows']
if len(moa) > 0:
    for x in moa:
        if "Delete ?" in moa[x] and moa[x]["Delete ?"]:
            curobj = objects.iloc[x]
            command = f"kairos -s deleteobject --id '{curobj['id']}' --database {curobj['origin']} --type {curobj['type']}"
            act = run(command)
            if 'success' in act and act['success']:
                del st.session_state.objects
                st.rerun()
            else: st.error(act['message'])
        if "Download ?" in moa[x] and moa[x]["Download ?"]:
            curobj = objects.iloc[x]
            command = f"kairos -s getobject --id '{curobj['id']}' --database {curobj['origin']} --type {curobj['type']}"
            act = run(command)
            if 'success' in act and act['success']:
                content = act['data']
                st.download_button('Download', data=content, file_name=f"{curobj['id']}.py", type="secondary")
                st.code(content)
            else: st.error(act['message'])
        if "Edit ?" in moa[x] and moa[x]["Edit ?"]:
            curobj = objects.iloc[x]
            st.session_state.object = curobj['id']
            st.session_state.type = curobj['type']
            del st.session_state.objects
            st.session_state.callstack.call('kairosedit', 'kairosobjects')

