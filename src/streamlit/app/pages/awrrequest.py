import streamlit as st, numpy as np
from pages.functions.definitions import *

theme = set_page_config()
gen_back_button()

if "context" in st.session_state and "run" in st.session_state.context and st.session_state.context["run"]:
     url = st.session_state.context['url']
     cdb = st.session_state.context['cdb']
     mindate = st.session_state.context['mindate']
     maxdate = st.session_state.context['maxdate']
     oracle = st.session_state.context['oracle']
     flags = st.session_state.context['flags']
     grouping = st.session_state.context['grouping']
     top = st.session_state.context['top']
     oracle.vdollar = flags['ashvdollar']
     dbid = cdb.split(':')[1]
     st.header("", anchor="home")
     logger.info('Generating the AWRREQUEST page ...')
     logger.info(f'AWRREQUEST parameters: {st.session_state.context}')
     tcontents = st.expander(f"Table of contents")
     contents = ''
     xaxis=dict(type='date', range=[f'{mindate[0:4]}-{mindate[4:6]}-{mindate[6:8]}', f'{maxdate[0:4]}-{maxdate[4:6]}-{maxdate[6:8]}'])
     XTraceL = gentrace(awr_interval=oracle.getawrinterval(), top=top, grouping=grouping, type='L', ash=False)        
     XTraceSC = gentrace(awr_interval=oracle.getawrinterval(), top=top, grouping=grouping, type='SC', ash=False)
     XTraceSA = gentrace(awr_interval=oracle.getawrinterval(), top=top, grouping=grouping, type='SA', ash=False)
     YTraceL = gentrace(awr_interval=oracle.getawrinterval(), ash_interval=oracle.getashinterval(), top=top, type='L', grouping=grouping, ash=True)        
     YTraceSC = gentrace(awr_interval=oracle.getawrinterval(), ash_interval=oracle.getashinterval(), top=top, type='SC', grouping=grouping, ash=True)
     YTraceSA = gentrace(awr_interval=oracle.getawrinterval(), ash_interval=oracle.getashinterval(), top=top, type='SA', grouping=grouping, ash=True)
     YTraceWL = gentrace(awr_interval=oracle.getawrinterval(), ash_interval=oracle.getashinterval(), top=top, type='WL', grouping=grouping, ash=True)
     result = oracle.query(f"select distinct sqlid from ({oracle.orahqs()})")
     sqlids = tuple([''] + result['sqlid'].to_list())
     sqlid = st.selectbox( 'Choose a sqlid in the following list ...', sqlids)
     if sqlid:
          st.header(f"Request report for sqlid: {sqlid}", divider='rainbow')
          sqlids = f"('{sqlid}')"
          request = oracle.query(f"select distinct request from ({oracle.dborareq(dbid, sqlids)})")
          st.code(request.iloc[0,0])
          mincost = oracle.query(f"select min(optimizer_cost) from ({oracle.orahqs()}) where sqlid = '{sqlid}'").iloc[0,0]
          maxcost = oracle.query(f"select max(optimizer_cost) from ({oracle.orahqs()}) where sqlid = '{sqlid}'").iloc[0,0]
          st.write(oracle.query(f"select * from ({oracle.orahqs()}) where sqlid = '{sqlid}'"))
          st.write(f'The estimated cost for this request is between {mincost} and {maxcost}')
          phvenv = oracle.query(f"select distinct plan_hash_value, optimizer_env_hash_value, con_dbid from ({oracle.orahqs()}) where sqlid = '{sqlid}' order by 1, 2")
          phvs = list(sorted(set([phvenv['plan_hash_value'][i] for i in phvenv.index])))
          txt = "1 plan has been found: " if len(phvs) == 1 else f"{len(phvs)} distincts execution plans have been found: "
          st.write(txt + str(phvs))
         
          for ind in phvenv.index:
               phv = phvenv['plan_hash_value'][ind]
               ohv = phvenv['optimizer_env_hash_value'][ind]
               cdbid = phvenv['con_dbid'][ind]
               st.subheader(f'Plan hash value : {phv} - Optimizer env hash value: {ohv} - Container id : {cdbid}')

               elapsed = oracle.query(f"select h.timestamp timestamp, 'Elapsed' legend, h.elapsed_time_delta/1000000/m.elapsed value from ({oracle.orahqs()}) h, ({oracle.dboramisc()}) m where sqlid='{sqlid}' and plan_hash_value={phv} and optimizer_env_hash_value={ohv} and con_dbid = {cdbid} and h.timestamp=m.timestamp order by timestamp")
               ap = oracle.query(f"select h.timestamp timestamp, 'Application' legend, h.apwait_delta/1000000/m.elapsed value from ({oracle.orahqs()}) h, ({oracle.dboramisc()}) m where sqlid='{sqlid}' and plan_hash_value={phv} and optimizer_env_hash_value={ohv} and con_dbid = {cdbid} and h.timestamp=m.timestamp order by timestamp")
               cc = oracle.query(f"select h.timestamp timestamp, 'Concurrency' legend, h.ccwait_delta/1000000/m.elapsed value from ({oracle.orahqs()}) h, ({oracle.dboramisc()}) m where sqlid='{sqlid}' and plan_hash_value={phv} and optimizer_env_hash_value={ohv} and con_dbid = {cdbid} and h.timestamp=m.timestamp order by timestamp")
               io = oracle.query(f"select h.timestamp timestamp, 'User I/O' legend, h.iowait_delta/1000000/m.elapsed value from ({oracle.orahqs()}) h, ({oracle.dboramisc()}) m where sqlid='{sqlid}' and plan_hash_value={phv} and optimizer_env_hash_value={ohv} and con_dbid = {cdbid} and h.timestamp=m.timestamp order by timestamp")
               cl = oracle.query(f"select h.timestamp timestamp, 'Cluster' legend, h.clwait_delta/1000000/m.elapsed value from ({oracle.orahqs()}) h, ({oracle.dboramisc()}) m where sqlid='{sqlid}' and plan_hash_value={phv} and optimizer_env_hash_value={ohv} and con_dbid = {cdbid} and h.timestamp=m.timestamp order by timestamp")
               cpu = oracle.query(f"select h.timestamp timestamp, 'Cpu' legend, h.cpu_time_delta/1000000/m.elapsed value from ({oracle.orahqs()}) h, ({oracle.dboramisc()}) m where sqlid='{sqlid}' and plan_hash_value={phv} and optimizer_env_hash_value={ohv} and con_dbid = {cdbid} and h.timestamp=m.timestamp order by timestamp")
               contents += f'\n* [Plan hash value : {phv} - Optimizer env hash value: {ohv} - Container id : {cdbid}](#x{phv}{ohv}{cdbid}timesec)'
               contents += f'\n    * [Time statictics per second](#x{phv}{ohv}{cdbid}timesec)'
               genchart(Chart(title=f'SQL request: {sqlid} - Plan hash value: {phv} - Optimizer env hash value: {ohv} - {cdbid} - Time statistics per second (All executions)', ytitle = 'Seconds', plots=[[[XTraceSC(cpu) + XTraceSC(ap) + XTraceSC(cc) + XTraceSC(io) + XTraceSC(cl), XTraceL(elapsed)]]], xaxis=xaxis).draw(), anchor=f"x{phv}{ohv}{cdbid}timesec")

               elapsed = oracle.query(f"select timestamp, 'Elapsed' legend, elapsed_time_delta/1000000/decode(executions_delta, 0, 1, executions_delta) value from ({oracle.orahqs()}) where sqlid='{sqlid}' and plan_hash_value={phv} and optimizer_env_hash_value={ohv} and con_dbid = {cdbid} order by timestamp")
               ap = oracle.query(f"select timestamp, 'Application' legend, apwait_delta/1000000/decode(executions_delta, 0, 1, executions_delta) value from ({oracle.orahqs()}) where sqlid='{sqlid}' and plan_hash_value={phv} and optimizer_env_hash_value={ohv} and con_dbid = {cdbid} order by timestamp")
               cc = oracle.query(f"select timestamp, 'Concurrency' legend, ccwait_delta/1000000/decode(executions_delta, 0, 1, executions_delta) value from ({oracle.orahqs()}) where sqlid='{sqlid}' and plan_hash_value={phv} and optimizer_env_hash_value={ohv} and con_dbid = {cdbid} order by timestamp")
               io = oracle.query(f"select timestamp, 'User I/O' legend, iowait_delta/1000000/decode(executions_delta, 0, 1, executions_delta) value from ({oracle.orahqs()}) where sqlid='{sqlid}' and plan_hash_value={phv} and optimizer_env_hash_value={ohv} and con_dbid = {cdbid} order by timestamp")
               cl = oracle.query(f"select timestamp, 'Cluster' legend, clwait_delta/1000000/decode(executions_delta, 0, 1, executions_delta) value from ({oracle.orahqs()}) where sqlid='{sqlid}' and plan_hash_value={phv} and optimizer_env_hash_value={ohv} and con_dbid = {cdbid} order by timestamp")
               cpu = oracle.query(f"select timestamp, 'Cpu' legend, cpu_time_delta/1000000/decode(executions_delta, 0, 1, executions_delta) value from ({oracle.orahqs()}) where sqlid='{sqlid}' and plan_hash_value={phv} and optimizer_env_hash_value={ohv} and con_dbid = {cdbid} order by timestamp")
               contents += f'\n    * [Time statictics per execution](#x{phv}{ohv}{cdbid}perexec)'
               genchart(Chart(title=f'SQL request: {sqlid} - Plan hash value: {phv} - Optimizer env hash value: {ohv} - {cdbid} - Time statistics per execution', ytitle = 'Seconds', plots=[[[XTraceSC(cpu) + XTraceSC(ap) + XTraceSC(cc) + XTraceSC(io) + XTraceSC(cl), XTraceL(elapsed)]]], xaxis=xaxis).draw(), anchor=f"x{phv}{ohv}{cdbid}perexec")

               gets = oracle.query(f"select timestamp, 'Buffer gets' legend, buffer_gets_delta/decode(executions_delta, 0, 1, executions_delta) value from ({oracle.orahqs()}) where sqlid='{sqlid}' and plan_hash_value={phv} and optimizer_env_hash_value={ohv} and con_dbid = {cdbid} order by timestamp")
               reads = oracle.query(f"select timestamp, 'Disk reads' legend, disk_reads_delta/decode(executions_delta, 0, 1, executions_delta) value from ({oracle.orahqs()}) where sqlid='{sqlid}' and plan_hash_value={phv} and optimizer_env_hash_value={ohv} and con_dbid = {cdbid} order by timestamp")
               contents += f'\n    * [Buffer gets / Disk reads per execution](#x{phv}{ohv}{cdbid}gets)'
               genchart(Chart(title=f'SQL request: {sqlid} - Plan hash value: {phv} - Optimizer env hash value: {ohv} - {cdbid} - Buffer gets / Disk reads per execution', ytitle = '# of operations / exec', plots=[[[XTraceL(gets) + XTraceL(reads)]]], xaxis=xaxis).draw(), anchor=f"x{phv}{ohv}{cdbid}gets")

               fetc = oracle.query(f"select timestamp, 'Fetches' legend, fetches_delta/decode(executions_delta, 0, 1, executions_delta) value from ({oracle.orahqs()}) where sqlid='{sqlid}' and plan_hash_value={phv} and optimizer_env_hash_value={ohv} and con_dbid = {cdbid} order by timestamp")
               contents += f'\n    * [Fetches per execution](#x{phv}{ohv}{cdbid}fetc)'
               genchart(Chart(title=f'SQL request: {sqlid} - Plan hash value: {phv} - Optimizer env hash value: {ohv} - {cdbid} - Fetches per execution', ytitle = '# of operations / exec', plots=[[[XTraceL(fetc)]]], xaxis=xaxis).draw(), anchor=f"x{phv}{ohv}{cdbid}fetc")

               rows = oracle.query(f"select timestamp, 'Rows processed' legend, rows_processed_delta/decode(executions_delta, 0, 1, executions_delta) value from ({oracle.orahqs()}) where sqlid='{sqlid}' and plan_hash_value={phv} and optimizer_env_hash_value={ohv} and con_dbid = {cdbid} order by timestamp")
               contents += f'\n    * [Rows processed per execution](#x{phv}{ohv}{cdbid}rows)'
               genchart(Chart(title=f'SQL request: {sqlid} - Plan hash value: {phv} - Optimizer env hash value: {ohv} - {cdbid} - Rows processed per execution', ytitle = '# of operations / exec', plots=[[[XTraceL(rows)]]], xaxis=xaxis).draw(), anchor=f"x{phv}{ohv}{cdbid}rows")

               plan = oracle.query(f"select * from table(dbms_xplan.display_workload_repository(sql_id=>'{sqlid}', plan_hash_value=>{phv}, format=>'ALL', dbid=>{dbid}, con_dbid=>{cdbid}, awr_location=>'AWR_PDB'))")
               numl = plan.shape[0]
               if not plan.empty:
                    with st.expander(f"Execution plan: {phv}"):
                         pd.set_option('display.max_rows', numl)
                         pd.set_option('display.max_colwidth', 1000)
                         st.code(plan)
                         pd.reset_option('display.max_rows')
                         pd.reset_option('display.max_colwidth')
          
          contents += f'\n* [ASH View](#dbtimem)'
          st.write(oracle.query(f"select * from ({oracle.orahas()}) where sql_id = '{sqlid}'"))
          ash1 = oracle.query(f"select timestamp, 'in_sql_execution' legend, sum(kairos_count) value from ({oracle.orahas()}) where sql_id='{sqlid}' and in_sql_execution='Y' group by timestamp, 'in_sql_execution' order by timestamp")
          ash2 = oracle.query(f"select timestamp, 'in_sequence_load' legend, sum(kairos_count) value from ({oracle.orahas()}) where sql_id='{sqlid}' and in_sequence_load='Y' group by timestamp, 'in_sequence_load' order by timestamp")
          ash3 = oracle.query(f"select timestamp, 'in_hard_parse' legend, sum(kairos_count) value from ({oracle.orahas()}) where sql_id='{sqlid}' and in_hard_parse='Y' group by timestamp, 'in_hard_parse' order by timestamp")
          ash4 = oracle.query(f"select timestamp, 'in_parse' legend, sum(kairos_count) value from ({oracle.orahas()}) where sql_id='{sqlid}' and in_parse='Y' group by timestamp, 'in_parse' order by timestamp")
          ash5 = oracle.query(f"select timestamp, 'in_bind' legend, sum(kairos_count) value from ({oracle.orahas()}) where sql_id='{sqlid}' and in_bind='Y' group by timestamp, 'in_bind' order by timestamp")
          ash = YTraceWL(ash1) + YTraceWL(ash2) + YTraceWL(ash3) + YTraceWL(ash4) + YTraceWL(ash5)
          if not ash.df.empty:
               contents += f'\n    * [DB time model](#dbtimem)'
               genchart(Chart(title=f'SQL request: {sqlid} - DB time model', ytitle = 'Number of active sessions', plots=[[[ash]]], xaxis=xaxis).draw(), anchor=f"dbtimem")

          ash = oracle.query(f"select timestamp, decode(event, null, 'on cpu', event) legend, sum(kairos_count) value from ({oracle.orahas()}) where sql_id='{sqlid}' group by timestamp, event order by timestamp")
          if not ash.empty:
               contents += f'\n    * [Top wait events](#waitev)'
               genchart(Chart(title=f'SQL request: {sqlid} - Top wait events', ytitle = 'Number of active sessions', plots=[[[YTraceSC(ash)]]], xaxis=xaxis).draw(), anchor=f"waitev")

          ash = oracle.query(f"select timestamp, session_id||' - '||program legend, sum(kairos_count) value from ({oracle.orahas()}) where sql_id='{sqlid}' group by timestamp, session_id||' - '||program order by timestamp")
          if not ash.empty:
               contents += f'\n    * [Top sessions](#topsess)'
               genchart(Chart(title=f'SQL request: {sqlid} - Top sessions', ytitle = 'Number of active sessions', plots=[[[YTraceSC(ash)]]], xaxis=xaxis).draw(), anchor=f"topsess")

          ash = oracle.query(f"select timestamp, xid legend, sum(kairos_count) value from ({oracle.orahas()}) where sql_id='{sqlid}' and xid is not null group by timestamp, xid order by timestamp")
          if not ash.empty:
               contents += f'\n    * [Top transactions](#xact)'
               genchart(Chart(title=f'SQL request: {sqlid} - Top transactions', ytitle = 'Number of active sessions', plots=[[[YTraceSC(ash)]]], xaxis=xaxis).draw(), anchor=f"xact")

          ash = oracle.query(f"select timestamp, blocking_inst_id||' - '||blocking_session legend, sum(kairos_count) value from ({oracle.orahas()}) where sql_id='{sqlid}' and blocking_session is not null group by timestamp, blocking_inst_id||' - '||blocking_session order by timestamp")
          if not ash.empty:
               contents += f'\n    * [Top blocking sessions](#block)'
               genchart(Chart(title=f'SQL request: {sqlid} - Top blocking sessions', ytitle = 'Number of active sessions', plots=[[[YTraceSC(ash)]]], xaxis=xaxis).draw(), anchor=f"block")

          for phv in phvs:
               ash = oracle.query(f"select timestamp, sql_plan_operation||' - '||sql_plan_options||' - '||sql_plan_line_id legend, sum(kairos_count) value from ({oracle.orahas()}) where sql_id='{sqlid}' and sql_plan_hash_value={phv} and is_sqlid_current = 'Y' group by timestamp, sql_plan_operation||' - '||sql_plan_options||' - '||sql_plan_line_id order by timestamp")
               if not ash.empty:
                    contents += f'\n    * [Top sql plan operations - phv {phv}](#op{phv})'
                    genchart(Chart(title=f'SQL request: {sqlid} - Plan hash value: {phv} - Top sql plan operations', ytitle = 'Number of active sessions', plots=[[[YTraceSC(ash)]]], xaxis=xaxis).draw(), anchor=f"op{phv}")

          for phv in phvs:
               ash = oracle.query(f"select timestamp, to_char(sql_exec_id) legend, sum(kairos_count) value from ({oracle.orahas()}) where sql_id='{sqlid}' and sql_plan_hash_value={phv} group by timestamp, to_char(sql_exec_id) order by timestamp")
               if not ash.empty:
                    contents += f'\n    * [Top execute ids - phv {phv}](#id{phv})'
                    genchart(Chart(title=f'SQL request: {sqlid} - Plan hash value: {phv} - Top execute ids', ytitle = 'Number of active sessions', plots=[[[YTraceSC(ash)]]], xaxis=xaxis).draw(), anchor=f"id{phv}")

          ash = oracle.query(f"select timestamp, 'PGA allocated' legend, sum(pga_allocated)/1024/1024 value from ({oracle.orahas()}) where sql_id='{sqlid}' group by timestamp, 'PGA allocated' order by timestamp")
          if not ash.empty:
               contents += f'\n    * [PGA allocated](#pga)'
               genchart(Chart(title=f'SQL request: {sqlid} - PGA allocated', ytitle = 'Allocated size in Megabytes', plots=[[[YTraceL(ash)]]], xaxis=xaxis).draw(), anchor=f"pga")

          ash = oracle.query(f"select timestamp, 'Temp space allocated' legend, sum(temp_space_allocated)/1024/1024 value from ({oracle.orahas()}) where sql_id='{sqlid}' group by timestamp, 'Temp space allocated' order by timestamp")
          if not ash.empty:
               contents += f'\n    * [Temp space allocated](#temp)'
               genchart(Chart(title=f'SQL request: {sqlid} - Temp space allocated', ytitle = 'Allocated size in Megabytes', plots=[[[YTraceL(ash)]]], xaxis=xaxis).draw(), anchor=f"temp")

          tcontents.markdown(contents)


 
