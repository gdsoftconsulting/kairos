import streamlit as st
from pages.functions.definitions import *

theme = set_page_config()
gen_back_button()

param = st.query_params
if 'user' in param and param['user'] : st.session_state.user = param['user']
if 'password' in param and param['password'] : st.session_state.password = param['password']

st.subheader(f"{st.session_state.user} settings", divider='rainbow')
cursettings = get_settings(theme)
wallpapers = get_wallpapers()
colors = get_colors()
templates = get_templates()
databases = get_databases()
curindex = -1
for x in databases:
    curindex += 1
    if x == cursettings['nodesdb']: break
newnodesdb = st.selectbox('Choose the default repository...', databases, curindex)
loglevels =['trace', 'debug', 'info']
curindex = -1
for x in loglevels:
    curindex += 1
    if x == cursettings['logging']: break
newlogging = st.selectbox('Choose the logging level...', loglevels, curindex)
curindex = -1
for x in wallpapers:
    curindex += 1
    if x == cursettings['wallpaper']: break
newwallpaper = st.selectbox('Choose the default wallpaper...', wallpapers, curindex)
curindex = -1
for x in colors:
    curindex += 1
    if x == cursettings['colors']: break
newcolors = st.selectbox('Choose the default colors...', colors, curindex)
curindex = -1
for x in templates:
    curindex += 1
    if x == cursettings['template']: break
newtemplate = st.selectbox('Choose the default template...', templates, curindex)
plotorientations =['horizontal', 'vertical']
curindex = -1
for x in plotorientations:
    curindex += 1
    if x == cursettings['plotorientation']: break
newplotorientation = st.selectbox('Choose the plots orientation...', plotorientations, curindex)
newtop = st.slider("Choose the number of elements to display", 1, 50, cursettings['top'])
if newnodesdb==cursettings['nodesdb'] and newlogging==cursettings['logging'] and newwallpaper==cursettings['wallpaper'] and newcolors==cursettings['colors'] and newtemplate==cursettings['template'] and newplotorientation==cursettings['plotorientation'] and newtop==cursettings['top']: pass
else:
    command = f"kairos -s updatesettings -a {st.session_state.user} -p {st.session_state.password} --nodesdb {newnodesdb} --systemdb {cursettings['systemdb']} --logging {newlogging} --template {newtemplate} --colors {newcolors} --wallpaper {newwallpaper} --top {newtop} --plotorientation {newplotorientation}"
    act = run(command)
    if 'success' in act and act['success']: 
        del st.session_state.settings
        get_settings(theme)
        st.rerun()
    else: st.error(act['message'])

