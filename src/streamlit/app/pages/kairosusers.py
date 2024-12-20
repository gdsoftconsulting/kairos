import streamlit as st
from pages.functions.definitions import *

theme = set_page_config()
gen_back_button()

param = st.query_params
if 'user' in param and param['user'] : st.session_state.user = param['user']
if 'password' in param and param['password'] : st.session_state.password = param['password']

st.subheader(f'Manage users and roles', divider='rainbow')
user = st.session_state.user
password = st.session_state.password
lusers = get_users()
lroles = get_roles()
lgrants = get_grants()
users = pd.DataFrame(lusers, columns=['User'])
users['Delete ?'] = pd.Series([False for x in range(len(users.index))])
roles = pd.DataFrame(lroles, columns=['Role'])
roles['Delete ?'] = pd.Series([False for x in range(len(roles.index))])
grants = pd.DataFrame(lgrants, columns=['Grantee', 'Granted'])
grants['Delete ?'] = pd.Series([False for x in range(len(grants.index))])
confusers = dict()
confusers['Delete ?'] = st.column_config.CheckboxColumn(default=False)
disabledusers = ["User"]
confroles = dict()
confroles['Delete ?'] = st.column_config.CheckboxColumn(default=False)
disabledroles = ["Role"]
confgrants = dict()
confgrants['Delete ?'] = st.column_config.CheckboxColumn(default=False)
disabledgrants = ["Grantee", 'Granted"']
col1, col2, col3, col4 = st.columns([1,1,2,1])
with col1:
    st.data_editor(users, key="manageusers", column_config=confusers, disabled=disabledusers, use_container_width=True)
with col2:
    st.data_editor(roles, key="manageroles", column_config=confroles, disabled=disabledroles, use_container_width=True)
with col3:
    st.data_editor(grants, key="managegrants", column_config=confgrants, disabled=disabledgrants, use_container_width=True)
with col4:
    menu = []
    menu.append({'label':'Create user', 'key':"Create user"})
    menu.append({'label':'Create role', 'key':"Create role"})
    menu.append({'label':'Create grant', 'key':"Create grant"})
    m1 = MENU(menu=menu, height=200, theme=theme['streamlit_theme'], id='kairos')
    if m1.get(): st.session_state.usermenu = m1.get()

manu = st.session_state.manageusers['edited_rows']
manr = st.session_state.manageroles['edited_rows']
mang = st.session_state.managegrants['edited_rows']

if len(manu) > 0:
    for x in manu:
        if "Delete ?" in manu[x] and manu[x]["Delete ?"]:
            curusr = users.iloc[x]
            command = f"kairos -s deleteuser -a {user} -p {password} --user {curusr['User']}"
            act = run(command)
            if 'success' in act and act['success']: 
                del st.session_state.users
                st.rerun()            
            else: st.error(act['message'])
if len(manr) > 0:
    for x in manr:
        if "Delete ?" in manr[x] and manr[x]["Delete ?"]:
            currol = roles.iloc[x]
            command = f"kairos -s deleterole -a {user} -p {password} --role {currol['Role']}"
            act = run(command)
            if 'success' in act and act['success']: 
                del st.session_state.roles
                st.rerun()            
            else: st.error(act['message'])
if len(mang) > 0:
    for x in mang:
        if "Delete ?" in mang[x] and mang[x]["Delete ?"]:
            curgra = grants.iloc[x]
            command = f"kairos -s deletegrant -a {user} -p {password} --user {curgra['Grantee']} --role {curgra['Granted']}"
            act = run(command)
            if 'success' in act and act['success']: 
                del st.session_state.grants
                st.rerun()               
            else: st.error(act['message'])

if "usermenu" not in st.session_state: st.session_state.usermenu = None
if st.session_state.usermenu == "Create user":
    newusr = st.text_input(f'Enter user name:', '')
    if newusr:
        command = f"kairos -s createuser -a {user} -p {password} --user {newusr}"
        act = run(command)
        if 'success' in act and act['success']:
            st.session_state.usermenu = None
            del st.session_state.users
            st.rerun()
        else: st.error(act['message'])
            
if st.session_state.usermenu == "Create role":
    newrol = st.text_input(f'Enter role name:', '')
    if newrol:
        command = f"kairos -s createrole -a {user} -p {password} --role {newrol}"
        act = run(command)
        if 'success' in act and act['success']: 
            st.session_state.usermenu = None
            del st.session_state.roles
            st.rerun()        
        else: st.error(act['message'])

if st.session_state.usermenu == "Create grant":
    lroles = tuple([''] + get_roles())
    lusers = tuple([''] + get_users())
    drole = st.selectbox( 'Choose a role to grant...', lroles, 0)
    duser = st.selectbox( 'Choose a user to be granted...', lusers, 0)
    if drole and duser:
        command = f"kairos -s creategrant -a {user} -p {password} --user {duser} --role {drole}"
        act = run(command)
        if 'success' in act and act['success']: 
            st.session_state.usermenu = None
            del st.session_state.grants
            st.rerun()        
        else: st.error(act['message'])