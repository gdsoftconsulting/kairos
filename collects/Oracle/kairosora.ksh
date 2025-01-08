#!/bin/ksh
function finit_variables
{
     HELP=0
     CMDNAME=$1
     LD_INSTANCENAME=None
     INSTANCENAME=ORCL
     STDBYINSTANCENAME=STDBYORCL
     STDBYUNIQUENAME=UNKNOWN
     ORAENV=0
     BASH=0
     AWR=0
     SAR=0
     STDBY=0
     NMON=0
     TOPAS=0
     GLOBAL=0
     FORMAT=text
     EXT=txt
     GROUP=UNKNOWN
     PASSWD=perfstat
     DIR=/tmp
     COL=5000
     LVL=1
     ARCHIVE_TYP=tgz
     DATEORAFMT='YYYY-MM-DD'
}
function fanalyze_parameters
{
     while [[ ${1#-} != $1 ]]
     do
          if [[ $1 != ${1#"-day:"} ]]  # day selection
          then
               DAY=${1#"-day:"}
          elif [[ $1 != ${1#"-sid:"} ]]  # instance selection
          then
               INSTANCENAME=${1#"-sid:"}
          elif [[ $1 != ${1#"-ld:"} ]]  # Repository instance selection
          then
               LD_INSTANCENAME=${1#"-ld:"}
          elif [[ $1 != ${1#"-lvl:"} ]]  # level selection
          then
               LVL=${1#"-lvl:"}
          elif [[ $1 != ${1#"-zip"} ]]  # output required: zip
          then
               ARCHIVE_TYP=zip
          elif [[ $1 != ${1#"-oraenv"} ]]  # execute oraenv to setup environement
          then
               ORAENV=1
          elif [[ $1 != ${1#"-awr"} ]]  # process awr reports
          then
               AWR=1
               BASH=0
          elif [[ $1 != ${1#"-bash"} ]]  # process bash reports (ASH on v$session and without AWR with BASH coming from Marcus Monnig)
          then
               BASH=1
          elif [[ $1 != ${1#"-sar"} ]]  # process sar reports
          then
               SAR=1
          elif [[ $1 != ${1#"-topas"} ]]  # for nmon issued from topas
          then
               TOPAS=1
          elif [[ $1 != ${1#"-global"} ]]  # process rac awr reports
          then
               GLOBAL=1
               AWR=1
               FORMAT=html
               EXT=html
          elif [[ $1 != ${1#"-stdby:"} ]]  # process statspack standby reports
          then
               STDBY=1
               STDBYINSTANCENAME=${1#"-stdby:"}
          elif [[ $1 != ${1#"-html"} ]]  # process awr reports in html format
          then
               FORMAT=html
               EXT=html
          elif [[ $1 != ${1#"-grp"} ]]  # group as defined in kairos
          then
               GROUP=${1#"-grp:"}
          elif [[ $1 != ${1#"-pwd:"} ]]  # PERFSTAT password when STATSPACK
          then
               PASSWD=${1#"-pwd:"}
          elif [[ $1 != ${1#"-dir:"} ]]  # output directory default /tmp
          then
               DIR=${1#"-dir:"}
          elif [[ $1 != ${1#"-nmon:"} ]]  # directory in which nmon reports are stored
          then
               NMON=${1#"-nmon:"}
          elif [[ $1 != ${1#"-col:"} ]]  # Column length
          then
               COL=${1#"-col:"}
          elif [[ $1 = -h ]]      # help
          then
               HELP=1
          fi
          shift
     done
}
function fcheck_parameters
{
    if [[ ${STDBY} -eq 1 ]]
    then
       if [[ ${AWR} -eq 1 ]]
       then
          echo "Error:  '-awr' not available pour Statspack Standby reports"
          exit 1
       elif [[ ${SAR} -eq 1 || "${NMON}" != "0" || ${TOPAS} -eq 1 ]]
       then
          echo "Error:  '-sar','-nmon' and '-topas' not available pour Statspack Standby reports"
          exit 1
       else
          return 1
       fi
    else
       return 1
    fi
}
function fdisplay_help
{
     echo "  Usage :"
     echo "     $CMDNAME [options]"
     echo "         generate a KAIROS file with the result of Stastpack or AWR."
     echo "         This script must be run under the unix oracle account."
     echo "  "
     echo "  Options:"
     echo "       -h                 : this help command"
     echo "       -sid:<SID>         : database instance name (mandatory)"
     echo "       -ld:<SID>          : Repository instance selection default NO REPOSITORY so None"
     echo "       -day:<YYYY-MM-DD> : date where data was collected"
     echo "       -grp:<GROUP>      : KAIROS group"
     echo "       -dir:<DIR>        : target directory"
     echo "       -oraenv           : oraenv is used to setup ORACLE environment variables"
     echo "       -pwd:<PASSWD>     : PERFSTAT or STDBYPERF password(when STATSPACK)"
     echo "       -lvl:n            : With AWR:  Collect level (default 1)"
     echo "                         : With AWR: level 2: collect of both DBA_HIST_SQLSTAT and DBA_HIST_SQLTEXT  and DBA_HIST_SYSMETRIC"
     echo "                         : With AWR: level 3: collect of dba_hist_active_sess_history"
     echo "       -col:v            : Column length (default 5000) Useful to extend to have full text for SQL requests in AWR lvl 2"
     echo "       -awr              : AWR report requested"
     echo "       -html             : AWR report in HTML format requested"
     echo "       -global           : global AWR report for all databases instances"
     echo "       -stdby:<DG_SID>   : Statspack Standby report re quested (Standby SID)"
     echo "       -bash             : Includes result of bash collect (ASH without AWR and Diagnostic pack)"
     echo "       -nmon             : Directory in which NMON reports are generated"
     echo "       -topas            : used in conjunction with NMON to notify expected format"
     echo "       -zip              : ZIP files instead of TGZ files"
     echo "  "
     echo "  Example:"
     echo "       $CMDNAME -sid:${INSTANCENAME:-ORCL} -day:2005-05-17 -zip -awr"
}
function fversion
{
     echo "Version 1.2 generated on 2020/02/07">VERSION
     tar cf ${TEMPFILE} VERSION
     rm VERSION
}
function foraenv
{
     ORAENVFILE=oraenv_$$.out
     export PATH=$PATH:/usr/local/bin
     export ORACLE_SID=${INSTANCENAME}
     export ORAENV_ASK=NO
     export NLS_LANG=AMERICAN_AMERICA
     export NLS_DATE_LANGUAGE=AMERICAN
     echo ''|. oraenv  >$ORAENVFILE 2>&1
     nbc=$(cat $ORAENVFILE|wc -c)
     rm $ORAENVFILE
     if [[ ${nbc} -ne 0 ]]
     then
        echo ''|. oraenv -s >$ORAENVFILE 2>&1
        nbc=$(cat $ORAENVFILE|wc -c)
        rm $ORAENVFILE
        if [[ ${nbc} -ne 0 ]]
        then
           echo "oraenv doestn't return an expected result. Check oraenv"
           exit 1
        fi
     fi
}
function fenv
{
     export NLS_LANG=AMERICAN_AMERICA
     export NLS_DATE_LANGUAGE=AMERICAN
}
function fconnectstring
{
     case ${STDBY} in
          0) c="PERFSTAT/${PASSWD}" ;;
          *) c="STDBYPERF/${PASSWD}" ;;
     esac
     case ${AWR} in
          0) c="$c" ;;
          *) c="sys/${PASSWD}@${INSTANCENAME} as sysdba" ;;
     esac
     printf "$c"
}
function fcheckconnect
{
     nbc=$(fday|wc -c)
     if [[ ${nbc} -ne 11 ]]
     then
        echo "Unable to connect to the instance. Check manually"
        exit 1
     fi
}
function fld_instancename
{
     case ${LD_INSTANCENAME} in
          None) c=${INSTANCENAME} ;;
          *) c=${LD_INSTANCENAME} ;;
     esac
     printf "$c"
}
function fday
{
     sqlplus -s "$CONNECTSTRING" <<EOF
     set heading off feedback off pages 0 lines 5000 trimspool on verify off
     select to_char(nvl(to_date('$DAY','$DATEORAFMT'),sysdate-1),'$DATEORAFMT') from dual;
     exit
EOF
}
function foravers
{
     case ${AWR} in
          0) case ${STDBY} in
                0) i=$(fstatspack_oravers);;
                *) i="";;
             esac;;
          *) i=$(fawr_oravers);;
     esac
     printf "$i"
}
function fstatspack_oravers
{
     sqlplus -s "$CONNECTSTRING" <<EOF
     set heading off feedback off pages 0 lines 5000 trimspool on verify off
     select substr(version,1,4) from v\$instance;
     exit
EOF
}
function fawr_oravers
{
     sqlplus -s "$CONNECTSTRING" <<EOF
     set heading off feedback off pages 0 lines 5000 trimspool on verify off
     select distinct substr(version,1,4) from dba_hist_database_instance where instance_name = '$LD_INSTANCENAME';
     exit
EOF
}
function fweekday
{
     sqlplus -s "$CONNECTSTRING" <<EOF
     set heading off feedback off pages 0 lines 5000 trimspool on verify off
     select to_char(nvl(to_date('$DAY','$DATEORAFMT'),sysdate-1),'$DATEORAFMT')||','||(to_char(nvl(to_date('$DAY','$DATEORAFMT'),sysdate-1) ,'D' )-1) from dual;
     exit
EOF
}
function fdbid
{
     case ${AWR} in
          0) case ${STDBY} in
                0) i=$(fstatspack_dbid);;
                *) i="";;
             esac;;
          *) i=$(fawr_dbid);;
     esac
     printf "$i"
}
function fstatspack_dbid
{
     sqlplus -s "$CONNECTSTRING" <<EOF
     set heading off feedback off pages 0 lines 5000 trimspool on verify off
     select dbid from v\$database;
     exit
EOF
}
function fawr_dbid
{
     sqlplus -s "$CONNECTSTRING" <<EOF
     set heading off feedback off pages 0 lines 5000 trimspool on verify off
     select * from (select dbid from dba_hist_database_instance where instance_name = '$LD_INSTANCENAME' order by startup_time desc) where rownum=1;
     exit
EOF
}
function fstatspack_instancenumber
{
     sqlplus -s "$CONNECTSTRING" <<EOF
     set heading off feedback off pages 0 lines 5000 trimspool on verify off
     select * from (select to_char(instance_number) from stats\$database_instance where instance_name='$INSTANCENAME' and dbid=$DBID order by startup_time desc) where rownum=1;
     exit
EOF
}
function fstdbystatspack_uniquename
{
     sqlplus -s "$CONNECTSTRING" <<EOF
     set heading off feedback off pages 0 lines 5000 trimspool on verify off
     select * from (select db_unique_name from stats\$standby_config where inst_name='$STDBYINSTANCENAME') where rownum=1;
     exit
EOF
}
function fawr_instancenumber
{
     sqlplus -s "$CONNECTSTRING" <<EOF
     set heading off feedback off pages 0 lines 5000 trimspool on verify off
     select * from (select to_char(instance_number) from dba_hist_database_instance where instance_name='$LD_INSTANCENAME' and dbid=$DBID order by startup_time desc) where rownum=1;
     exit
EOF
}
function finstancenumber
{
     case ${AWR} in
          0) i=$(fstatspack_instancenumber);;
          *) i=$(fawr_instancenumber);;
     esac
     printf "$i"
}
function fstdbyuniquename
{
     case ${STDBY} in
          1) i=$(fstdbystatspack_uniquename);;
          *) i="";;
     esac
     printf "$i"
}
function fawr_dbname
{
     sqlplus -s "$CONNECTSTRING" <<EOF
     set heading off feedback off pages 0 lines 5000 trimspool on verify off
     select * from (select db_name from dba_hist_database_instance where instance_name='$LD_INSTANCENAME' and dbid=$DBID order by startup_time desc) where rownum=1;
     exit
EOF
}
function fdbname
{
     case ${AWR} in
          0) d='';;
          *) d=$(fawr_dbname);;
     esac
     printf "$d"
}
function fstatspack_list
{
     sqlplus -s "$CONNECTSTRING" <<EOF
     set heading off feedback off pages 0 lines 5000 trimspool on verify off
     alter session set nls_date_format='YYYYMMDDHH24MISS';
     select snap_time||'@'||prev_snap_id||'@'||snap_id from (
          select snap_time, first_value(snap_id) over (order by snap_time asc rows between 1 preceding and current row) prev_snap_id, snap_id
          from stats\$snapshot
          where session_id=0 and dbid=${DBID} and instance_number=${INSTANCENUMBER})
     where snap_time between to_date('${DAY}', '${DATEORAFMT}') and to_date('${DAY}', '${DATEORAFMT}') + 1 and prev_snap_id != snap_id;
     exit
EOF
}

function fstdbystatspack_list
{
     sqlplus -s "$CONNECTSTRING" <<EOF
     set heading off feedback off pages 0 lines 5000 trimspool on verify off
     alter session set nls_date_format='YYYYMMDDHH24MISS';
     select snap_time||'@'||prev_snap_id||'@'||snap_id from (
          select snap_time, first_value(snap_id) over (order by snap_time asc rows between 1 preceding and current row) prev_snap_id, snap_id
          from stats\$snapshot
          where session_id=0 and db_unique_name='${STDBYUNIQUENAME}' and instance_name='${STDBYINSTANCENAME}')
     where snap_time between to_date('${DAY}', '${DATEORAFMT}') and to_date('${DAY}', '${DATEORAFMT}') + 1 and prev_snap_id != snap_id;
     exit
EOF
}
function fstatspackstandby
{
     for i in $(fstdbystatspack_list)
     do
          echo $i
          timestmp=$(echo $i|cut -f 1 -d '@')
          bid=$(echo $i|cut -f 2 -d '@')
          eid=$(echo $i|cut -f 3 -d '@')
          REPORT=rep_${STDBYINSTANCENAME}_$timestmp.${EXT}
          sqlplus  $CONNECTSTRING<< EOF   >/dev/null
               define db_unique_name=${STDBYUNIQUENAME}
               define inst_name=${STDBYINSTANCENAME}
               define begin_snap=$bid
               define end_snap=$eid
               define report_name=${REPORT}
               alter session set cursor_sharing=EXACT;
               rem alter session set global_names=FALSE;
               @?/rdbms/admin/sbreport
               exit
EOF
          tar rf ${TEMPFILE} ${REPORT}
          rm ${REPORT}
done
}
function fstatspack
{
     for i in $(fstatspack_list)
     do
          echo $i
          timestmp=$(echo $i|cut -f 1 -d '@')
          bid=$(echo $i|cut -f 2 -d '@')
          eid=$(echo $i|cut -f 3 -d '@')
          REPORT=rep_${INSTANCENAME}_$timestmp.lst
          sqlplus  $CONNECTSTRING<< EOF   >/dev/null
               define begin_snap=$bid
               define end_snap=$eid
               define report_name=${REPORT}
               alter session set cursor_sharing=EXACT;
               @?/rdbms/admin/spreport
               exit
EOF
          tar rf ${TEMPFILE} ${REPORT}
          rm ${REPORT}
done
}
function fawr_list
{
     sqlplus -s "$CONNECTSTRING" <<EOF
     set heading off feedback off pages 0 lines 5000 trimspool on verify off
     alter session set nls_timestamp_format='YYYYMMDDHH24MISS';
     select END_INTERVAL_TIME||'@'||prev_snap_id||'@'||snap_id||'@'||'${DBNAME}'||'@'||to_number('${INSTANCENUMBER}')||'@'||to_number('${DBID}') from (
          select END_INTERVAL_TIME, first_value(snap_id) over (order by END_INTERVAL_TIME asc rows between 1 preceding and current row) prev_snap_id, snap_id
          from DBA_HIST_SNAPSHOT
          where dbid=${DBID} and instance_number = ${INSTANCENUMBER})
     where END_INTERVAL_TIME between to_date('${DAY}', '${DATEORAFMT}') and to_date('${DAY}', '${DATEORAFMT}') + 1 and prev_snap_id != snap_id;
     exit
EOF
}
function fawrglobal
{
     for i in $(fawr_list)
     do
          timestmp=$(echo $i|cut -f 1 -d '@')
          bid=$(echo $i|cut -f 2 -d '@')
          eid=$(echo $i|cut -f 3 -d '@')
          dbn=$(echo $i|cut -f 4 -d '@')
          vdbid=$(echo $i|cut -f 6 -d '@')
          REPORT=rep_${dbn}_$timestmp.${EXT}
          sqlplus  $CONNECTSTRING<< EOF   >/dev/null
              define  num_days     = 1;
              define  db_name      = $dbn;
              define  dbid         = $vdbid;
              define  begin_snap   = $bid;
              define  end_snap     = $eid;
              define  report_type  = ${FORMAT};
              define  report_name  = ${REPORT}
              define  instance_numbers_or_ALL = ALL;
              alter session set cursor_sharing=EXACT;
              @@?/rdbms/admin/awrgrpti
              exit
EOF
          tar rf ${TEMPFILE} ${REPORT}
          rm ${REPORT}
     done
}
function fawr
{
     for i in $(fawr_list)
     do
          timestmp=$(echo $i|cut -f 1 -d '@')
          bid=$(echo $i|cut -f 2 -d '@')
          eid=$(echo $i|cut -f 3 -d '@')
          dbn=$(echo $i|cut -f 4 -d '@')
          inu=$(echo $i|cut -f 5 -d '@')
          vdbid=$(echo $i|cut -f 6 -d '@')
          REPORT=rep_${LD_INSTANCENAME}_$timestmp.${EXT}
          sqlplus  -s "$CONNECTSTRING"<< EOF >/dev/null
              define  inst_num     = $inu;
              define  num_days     = 1;
              define  inst_name    = '$LD_INSTANCENAME';
              define  db_name      = $dbn;
              define  dbid         = $vdbid;
              define  begin_snap   = $bid;
              define  end_snap     = $eid;
              define  report_type  = ${FORMAT};
              define  report_name  = ${REPORT}
              alter session set cursor_sharing=EXACT;
              @@?/rdbms/admin/awrrpti
              exit
EOF
          tar rf ${TEMPFILE} ${REPORT}
          rm ${REPORT}
     done
     if [[ "$1" -ge "2" ]]
     then
          fawr2
     fi
     if [[ "$1" -ge "3" ]]
     then
          fawr3
     fi
}
function fawr2
{
     SEP1=":,"
     SEP2=":="
     REPORT=${LD_INSTANCENAME}_dbahistsqlstat_${DAY}.lst
     fheader ${SEP1} ${SEP2} > $REPORT
     echo 'TYPE ORAHQS plan_hash_value text' >>$REPORT
     echo 'TYPE ORAHQS optimizer_cost text' >>$REPORT
     echo 'TYPE ORAHQS optimizer_env_hash_value text' >>$REPORT
     echo 'TYPE ORAHQS force_matching_signature text' >>$REPORT
     echo 'TYPE ORAHQS parsing_schema_id text' >>$REPORT
     echo 'TYPE ORAHQS parsing_user_id text' >>$REPORT
     echo 'TYPE ORAHQS fetches_delta int' >>$REPORT
     echo 'TYPE ORAHQS end_of_fetch_count_delta int' >>$REPORT
     echo 'TYPE ORAHQS sorts_delta int' >>$REPORT
     echo 'TYPE ORAHQS executions_delta int' >>$REPORT
     echo 'TYPE ORAHQS px_servers_execs_delta int'>>$REPORT
     echo 'TYPE ORAHQS loads_delta int' >>$REPORT
     echo 'TYPE ORAHQS invalidations_delta int'>>$REPORT
     echo 'TYPE ORAHQS parse_calls_delta int' >>$REPORT
     echo 'TYPE ORAHQS disk_reads_delta int' >>$REPORT
     echo 'TYPE ORAHQS buffer_gets_delta int' >>$REPORT
     echo 'TYPE ORAHQS rows_processed_delta int' >>$REPORT
     echo 'TYPE ORAHQS cpu_time_delta int' >>$REPORT
     echo 'TYPE ORAHQS elapsed_time_delta int' >>$REPORT
     echo 'TYPE ORAHQS iowait_delta int' >>$REPORT
     echo 'TYPE ORAHQS clwait_delta int' >>$REPORT
     echo 'TYPE ORAHQS apwait_delta int' >>$REPORT
     echo 'TYPE ORAHQS ccwait_delta int' >>$REPORT
     echo 'TYPE ORAHQS direct_writes_delta int' >>$REPORT
     echo 'TYPE ORAHQS plsexec_time_delta int' >>$REPORT
     echo 'TYPE ORAHQS javexec_time_delta int' >>$REPORT
     echo 'TYPE ORAHQS io_offload_elig_bytes_delta int' >>$REPORT
     echo 'TYPE ORAHQS io_interconnect_bytes_delta int' >>$REPORT
     echo 'TYPE ORAHQS physical_read_requests_delta int' >>$REPORT
     echo 'TYPE ORAHQS physical_read_bytes_delta int' >>$REPORT
     echo 'TYPE ORAHQS physical_write_requests_delta int' >>$REPORT
     echo 'TYPE ORAHQS physical_write_bytes_delta int' >>$REPORT
     echo 'TYPE ORAHQS optimized_physical_reads_delta int' >>$REPORT
     echo 'TYPE ORAHQS cell_uncompressed_bytes_delta int' >>$REPORT
     echo 'TYPE ORAHQS io_offload_return_bytes_delta int' >>$REPORT
     echo 'TYPE ORAHQS con_dbid text' >>$REPORT
     echo 'TYPE ORAHQS con_id text' >>$REPORT
     fdbahistsqlstat ${SEP1} ${SEP2} >> $REPORT
     tar rf ${TEMPFILE} ${REPORT}
     rm ${REPORT}
     REPORT=${LD_INSTANCENAME}_dbahistsysmetric_${DAY}.lst
     fheader ${SEP1} ${SEP2} > $REPORT
     echo 'TYPE ORAHSM intsize int' >>$REPORT
     echo 'TYPE ORAHSM group_id text' >>$REPORT
     echo 'TYPE ORAHSM metric_id text' >>$REPORT
     echo 'TYPE ORAHSM metric_name text' >>$REPORT
     echo 'TYPE ORAHSM metric_unit text' >>$REPORT
     echo 'TYPE ORAHSM con_dbid text' >>$REPORT
     echo 'TYPE ORAHSM con_id text' >>$REPORT
     fsysmetric ${SEP1} ${SEP2} >> $REPORT
     tar rf ${TEMPFILE} ${REPORT}
     rm ${REPORT}
     SEP1="|>!!<|,"
     SEP2="=_||_="
     REPORT=${LD_INSTANCENAME}_dbahistsqltext_${DAY}.lst
     fheader ${SEP1} ${SEP2} > $REPORT
     echo 'TYPE ORAHQT command_type text' >>$REPORT
     echo 'TYPE ORAHQT con_dbid text' >>$REPORT
     echo 'TYPE ORAHQT con_id text' >>$REPORT
     fdbahistsqltext ${SEP1} ${SEP2} >> $REPORT
     tar rf ${TEMPFILE} ${REPORT}
     rm ${REPORT}
}
function fawr3
{
     SEP1=":,"
     SEP2=":="
     fdbahistactivesesshistory ${SEP1} ${SEP2} | split -l 10000 - kairos_extr_
     for f in kairos_extr_*
     do
          SUFFIX=$(echo $f|sed -e 's/kairos_extr_//')
          REPORT=${LD_INSTANCENAME}_dbahistactivesesshistory_${DAY}_$SUFFIX.lst
          fheader ${SEP1} ${SEP2} > $REPORT
          echo 'TYPE ORAHAS action text' >>$REPORT
          echo 'TYPE ORAHAS blocking_hangchain_info text' >>$REPORT
          echo 'TYPE ORAHAS blocking_inst_id text' >>$REPORT
          echo 'TYPE ORAHAS blocking_session text' >>$REPORT
          echo 'TYPE ORAHAS blocking_session_serial text' >>$REPORT
          echo 'TYPE ORAHAS blocking_session_status text' >>$REPORT
          echo 'TYPE ORAHAS capture_overhead text' >>$REPORT
          echo 'TYPE ORAHAS client_id text' >>$REPORT
          echo 'TYPE ORAHAS con_dbid text' >>$REPORT
          echo 'TYPE ORAHAS con_id text' >>$REPORT
          echo 'TYPE ORAHAS con_name text' >>$REPORT
          echo 'TYPE ORAHAS consumer_group_id text' >>$REPORT
          echo 'TYPE ORAHAS current_block text' >>$REPORT
          echo 'TYPE ORAHAS current_file text' >>$REPORT
          echo 'TYPE ORAHAS current_obj text' >>$REPORT
          echo 'TYPE ORAHAS current_row text' >>$REPORT
          echo 'TYPE ORAHAS dbop_exec_id text' >>$REPORT
          echo 'TYPE ORAHAS dbop_name text' >>$REPORT
          echo 'TYPE ORAHAS dbreplay_call_counter text' >>$REPORT
          echo 'TYPE ORAHAS dbreplay_file_id text' >>$REPORT
          echo 'TYPE ORAHAS delta_interconnect_io_bytes real' >>$REPORT
          echo 'TYPE ORAHAS delta_read_io_bytes real' >>$REPORT
          echo 'TYPE ORAHAS delta_read_io_requests real' >>$REPORT
          echo 'TYPE ORAHAS delta_time real' >>$REPORT
          echo 'TYPE ORAHAS delta_write_io_bytes real' >>$REPORT
          echo 'TYPE ORAHAS delta_write_io_requests real' >>$REPORT
          echo 'TYPE ORAHAS ecid text' >>$REPORT
          echo 'TYPE ORAHAS event text' >>$REPORT
          echo 'TYPE ORAHAS event_id text' >>$REPORT
          echo 'TYPE ORAHAS flags text' >>$REPORT
          echo 'TYPE ORAHAS force_matching_signature text' >>$REPORT
          echo 'TYPE ORAHAS in_bind text' >>$REPORT
          echo 'TYPE ORAHAS in_connection_mgmt text' >>$REPORT
          echo 'TYPE ORAHAS in_cursor_close text' >>$REPORT
          echo 'TYPE ORAHAS in_hard_parse text' >>$REPORT
          echo 'TYPE ORAHAS in_java_execution text' >>$REPORT
          echo 'TYPE ORAHAS in_parse text' >>$REPORT
          echo 'TYPE ORAHAS in_plsql_compilation text' >>$REPORT
          echo 'TYPE ORAHAS in_plsql_execution text' >>$REPORT
          echo 'TYPE ORAHAS in_plsql_rpc text' >>$REPORT
          echo 'TYPE ORAHAS in_sequence_load text' >>$REPORT
          echo 'TYPE ORAHAS in_sql_execution text' >>$REPORT
          echo 'TYPE ORAHAS is_captured text' >>$REPORT
          echo 'TYPE ORAHAS is_replayed text' >>$REPORT
          echo 'TYPE ORAHAS is_sqlid_current text' >>$REPORT
          echo 'TYPE ORAHAS machine text' >>$REPORT
          echo 'TYPE ORAHAS module text' >>$REPORT
          echo 'TYPE ORAHAS optimizer_env_hash_value text' >>$REPORT
          echo 'TYPE ORAHAS p1 text' >>$REPORT
          echo 'TYPE ORAHAS p1text text' >>$REPORT
          echo 'TYPE ORAHAS p2 text' >>$REPORT
          echo 'TYPE ORAHAS p2text text' >>$REPORT
          echo 'TYPE ORAHAS p3 text' >>$REPORT
          echo 'TYPE ORAHAS p3text text' >>$REPORT
          echo 'TYPE ORAHAS pga_allocated real' >>$REPORT
          echo 'TYPE ORAHAS plsql_entry_object_id text' >>$REPORT
          echo 'TYPE ORAHAS plsql_entry_subprogram_id text' >>$REPORT
          echo 'TYPE ORAHAS plsql_object_id text' >>$REPORT
          echo 'TYPE ORAHAS plsql_subprogram_id text' >>$REPORT
          echo 'TYPE ORAHAS port text' >>$REPORT
          echo 'TYPE ORAHAS program text' >>$REPORT
          echo 'TYPE ORAHAS qc_instance_id text' >>$REPORT
          echo 'TYPE ORAHAS qc_session_id text' >>$REPORT
          echo 'TYPE ORAHAS qc_session_serial text' >>$REPORT
          echo 'TYPE ORAHAS remote_instance text' >>$REPORT
          echo 'TYPE ORAHAS replay_overhead text' >>$REPORT
          echo 'TYPE ORAHAS sample_id text' >>$REPORT
          echo 'TYPE ORAHAS seq text' >>$REPORT
          echo 'TYPE ORAHAS service_hash text' >>$REPORT
          echo 'TYPE ORAHAS session_id text' >>$REPORT
          echo 'TYPE ORAHAS session_serial text' >>$REPORT
          echo 'TYPE ORAHAS session_state text' >>$REPORT
          echo 'TYPE ORAHAS session_type text' >>$REPORT
          echo 'TYPE ORAHAS sql_child_number text' >>$REPORT
          echo 'TYPE ORAHAS sql_exec_id text' >>$REPORT
          echo 'TYPE ORAHAS sql_exec_start text' >>$REPORT
          echo 'TYPE ORAHAS sql_id text' >>$REPORT
          echo 'TYPE ORAHAS sql_opcode text' >>$REPORT
          echo 'TYPE ORAHAS sql_opname text' >>$REPORT
          echo 'TYPE ORAHAS sql_plan_hash_value text' >>$REPORT
          echo 'TYPE ORAHAS sql_plan_line_id text' >>$REPORT
          echo 'TYPE ORAHAS sql_plan_operation text' >>$REPORT
          echo 'TYPE ORAHAS sql_plan_options text' >>$REPORT
          echo 'TYPE ORAHAS temp_space_allocated real' >>$REPORT
          echo 'TYPE ORAHAS time_model text' >>$REPORT
          echo 'TYPE ORAHAS time_waited real' >>$REPORT
          echo 'TYPE ORAHAS tm_delta_cpu_time real' >>$REPORT
          echo 'TYPE ORAHAS tm_delta_db_time real' >>$REPORT
          echo 'TYPE ORAHAS tm_delta_time real' >>$REPORT
          echo 'TYPE ORAHAS top_level_call text' >>$REPORT
          echo 'TYPE ORAHAS top_level_call_name text' >>$REPORT
          echo 'TYPE ORAHAS top_level_sql_id text' >>$REPORT
          echo 'TYPE ORAHAS top_level_sql_opcode text' >>$REPORT
          echo 'TYPE ORAHAS user_id text' >>$REPORT
          echo 'TYPE ORAHAS wait_class text' >>$REPORT
          echo 'TYPE ORAHAS wait_class_id text' >>$REPORT
          echo 'TYPE ORAHAS wait_time real' >>$REPORT
          echo 'TYPE ORAHAS xid text' >>$REPORT
          cat $f >>$REPORT
          tar rf ${TEMPFILE} ${REPORT}
          rm ${REPORT}
          rm $f
     done
}
function fdbahistsqlstat
{
     if [[ "$ORAVERS" = "10.2" ]]
     then
          fdbahistsqlstat111 $1 $2
     elif [[ "$ORAVERS" = "11.1" ]]
     then
          fdbahistsqlstat111 $1 $2
     elif [[ "$ORAVERS" = "11.2" ]]
     then
          fdbahistsqlstat111 $1 $2
     else
          fdbahistsqlstat121 $1 $2
     fi
}
function fdbahistsqlstat111
{
     sqlplus -s "$CONNECTSTRING" <<EOF
          set termout off heading off feedback off pages 0 lines ${COL} trimspool on verify off
          alter session set nls_timestamp_format='YYYYMMDDHH24MISS';
          define sep1=$1
          define sep2=$2
          select end_interval_time||' ORAHQS '||'sql_id'                         ||'&sep2'||sql_id
                                  ||'&sep1'   ||'plan_hash_value'                ||'&sep2'||plan_hash_value
                                  ||'&sep1'   ||'optimizer_cost'                 ||'&sep2'||optimizer_cost
                                  ||'&sep1'   ||'optimizer_mode'                 ||'&sep2'||optimizer_mode
                                  ||'&sep1'   ||'optimizer_env_hash_value'       ||'&sep2'||optimizer_env_hash_value
                                  ||'&sep1'   ||'sharable_mem'                   ||'&sep2'||sharable_mem
                                  ||'&sep1'   ||'loaded_versions'                ||'&sep2'||loaded_versions
                                  ||'&sep1'   ||'version_count'                  ||'&sep2'||version_count
                                  ||'&sep1'   ||'module'                         ||'&sep2'||module
                                  ||'&sep1'   ||'action'                         ||'&sep2'||action
                                  ||'&sep1'   ||'sql_profile'                    ||'&sep2'||sql_profile
                                  ||'&sep1'   ||'force_matching_signature'       ||'&sep2'||force_matching_signature
                                  ||'&sep1'   ||'parsing_schema_id'              ||'&sep2'||parsing_schema_id
                                  ||'&sep1'   ||'parsing_schema_name'            ||'&sep2'||parsing_schema_name
                                  ||'&sep1'   ||'fetches_delta'                  ||'&sep2'||fetches_delta
                                  ||'&sep1'   ||'end_of_fetch_count_delta'       ||'&sep2'||end_of_fetch_count_delta
                                  ||'&sep1'   ||'sorts_delta'                    ||'&sep2'||sorts_delta
                                  ||'&sep1'   ||'executions_delta'               ||'&sep2'||executions_delta
                                  ||'&sep1'   ||'px_servers_execs_delta'         ||'&sep2'||px_servers_execs_delta
                                  ||'&sep1'   ||'loads_delta'                    ||'&sep2'||loads_delta
                                  ||'&sep1'   ||'invalidations_delta'            ||'&sep2'||invalidations_delta
                                  ||'&sep1'   ||'parse_calls_delta'              ||'&sep2'||parse_calls_delta
                                  ||'&sep1'   ||'disk_reads_delta'               ||'&sep2'||disk_reads_delta
                                  ||'&sep1'   ||'buffer_gets_delta'              ||'&sep2'||buffer_gets_delta
                                  ||'&sep1'   ||'rows_processed_delta'           ||'&sep2'||rows_processed_delta
                                  ||'&sep1'   ||'cpu_time_delta'                 ||'&sep2'||cpu_time_delta
                                  ||'&sep1'   ||'elapsed_time_delta'             ||'&sep2'||elapsed_time_delta
                                  ||'&sep1'   ||'iowait_delta'                   ||'&sep2'||iowait_delta
                                  ||'&sep1'   ||'clwait_delta'                   ||'&sep2'||clwait_delta
                                  ||'&sep1'   ||'apwait_delta'                   ||'&sep2'||apwait_delta
                                  ||'&sep1'   ||'ccwait_delta'                   ||'&sep2'||ccwait_delta
                                  ||'&sep1'   ||'direct_writes_delta'            ||'&sep2'||direct_writes_delta
                                  ||'&sep1'   ||'plsexec_time_delta'             ||'&sep2'||plsexec_time_delta
                                  ||'&sep1'   ||'javexec_time_delta'             ||'&sep2'||javexec_time_delta
                                  ||'&sep1'   ||'gets_per_execs'                 ||'&sep2'||buffer_gets_total/decode(executions_total,0,1,nvl(executions_total,1))
          from dba_hist_snapshot sn, dba_hist_sqlstat sq
          where sn.dbid=${DBID} and sn.dbid = sq.dbid and sn.instance_number=${INSTANCENUMBER} and sn.instance_number= sq.instance_number and sn.end_interval_time between to_date('${DAY}', '${DATEORAFMT}') and to_date('${DAY}', '${DATEORAFMT}') + 1 and sn.snap_id=sq.snap_id;
          exit
EOF
}
function fdbahistsqlstat121
{
     sqlplus -s "$CONNECTSTRING" <<EOF
          set termout off heading off feedback off pages 0 lines ${COL} trimspool on verify off
          alter session set nls_timestamp_format='YYYYMMDDHH24MISS';
          define sep1=$1
          define sep2=$2
          select end_interval_time||' ORAHQS '||'sql_id'                         ||'&sep2'||sql_id
                                  ||'&sep1'   ||'plan_hash_value'                ||'&sep2'||plan_hash_value
                                  ||'&sep1'   ||'optimizer_cost'                 ||'&sep2'||optimizer_cost
                                  ||'&sep1'   ||'optimizer_mode'                 ||'&sep2'||optimizer_mode
                                  ||'&sep1'   ||'optimizer_env_hash_value'       ||'&sep2'||optimizer_env_hash_value
                                  ||'&sep1'   ||'sharable_mem'                   ||'&sep2'||sharable_mem
                                  ||'&sep1'   ||'loaded_versions'                ||'&sep2'||loaded_versions
                                  ||'&sep1'   ||'version_count'                  ||'&sep2'||version_count
                                  ||'&sep1'   ||'module'                         ||'&sep2'||module
                                  ||'&sep1'   ||'action'                         ||'&sep2'||action
                                  ||'&sep1'   ||'sql_profile'                    ||'&sep2'||sql_profile
                                  ||'&sep1'   ||'force_matching_signature'       ||'&sep2'||force_matching_signature
                                  ||'&sep1'   ||'parsing_schema_id'              ||'&sep2'||parsing_schema_id
                                  ||'&sep1'   ||'parsing_schema_name'            ||'&sep2'||parsing_schema_name
                                  ||'&sep1'   ||'parsing_user_id'                ||'&sep2'||parsing_user_id
                                  ||'&sep1'   ||'fetches_delta'                  ||'&sep2'||fetches_delta
                                  ||'&sep1'   ||'end_of_fetch_count_delta'       ||'&sep2'||end_of_fetch_count_delta
                                  ||'&sep1'   ||'sorts_delta'                    ||'&sep2'||sorts_delta
                                  ||'&sep1'   ||'executions_delta'               ||'&sep2'||executions_delta
                                  ||'&sep1'   ||'px_servers_execs_delta'         ||'&sep2'||px_servers_execs_delta
                                  ||'&sep1'   ||'loads_delta'                    ||'&sep2'||loads_delta
                                  ||'&sep1'   ||'invalidations_delta'            ||'&sep2'||invalidations_delta
                                  ||'&sep1'   ||'parse_calls_delta'              ||'&sep2'||parse_calls_delta
                                  ||'&sep1'   ||'disk_reads_delta'               ||'&sep2'||disk_reads_delta
                                  ||'&sep1'   ||'buffer_gets_delta'              ||'&sep2'||buffer_gets_delta
                                  ||'&sep1'   ||'rows_processed_delta'           ||'&sep2'||rows_processed_delta
                                  ||'&sep1'   ||'cpu_time_delta'                 ||'&sep2'||cpu_time_delta
                                  ||'&sep1'   ||'elapsed_time_delta'             ||'&sep2'||elapsed_time_delta
                                  ||'&sep1'   ||'iowait_delta'                   ||'&sep2'||iowait_delta
                                  ||'&sep1'   ||'clwait_delta'                   ||'&sep2'||clwait_delta
                                  ||'&sep1'   ||'apwait_delta'                   ||'&sep2'||apwait_delta
                                  ||'&sep1'   ||'ccwait_delta'                   ||'&sep2'||ccwait_delta
                                  ||'&sep1'   ||'direct_writes_delta'            ||'&sep2'||direct_writes_delta
                                  ||'&sep1'   ||'plsexec_time_delta'             ||'&sep2'||plsexec_time_delta
                                  ||'&sep1'   ||'javexec_time_delta'             ||'&sep2'||javexec_time_delta
                                  ||'&sep1'   ||'gets_per_execs'                 ||'&sep2'||buffer_gets_total/decode(executions_total,0,1,nvl(executions_total,1))
                                  ||'&sep1'   ||'io_offload_elig_bytes_delta'    ||'&sep2'||io_offload_elig_bytes_delta
                                  ||'&sep1'   ||'io_interconnect_bytes_delta'    ||'&sep2'||io_interconnect_bytes_delta
                                  ||'&sep1'   ||'physical_read_requests_delta'   ||'&sep2'||physical_read_requests_delta
                                  ||'&sep1'   ||'physical_read_bytes_delta'      ||'&sep2'||physical_read_bytes_delta
                                  ||'&sep1'   ||'physical_write_requests_delta'  ||'&sep2'||physical_write_requests_delta
                                  ||'&sep1'   ||'physical_write_bytes_delta'     ||'&sep2'||physical_write_bytes_delta
                                  ||'&sep1'   ||'optimized_physical_reads_delta' ||'&sep2'||optimized_physical_reads_delta
                                  ||'&sep1'   ||'cell_uncompressed_bytes_delta'  ||'&sep2'||cell_uncompressed_bytes_delta
                                  ||'&sep1'   ||'io_offload_return_bytes_delta'  ||'&sep2'||io_offload_return_bytes_delta
                                  ||'&sep1'   ||'con_dbid'                       ||'&sep2'||con_dbid
                                  ||'&sep1'   ||'con_id'                         ||'&sep2'||sq.con_id
                                  ||'&sep1'   ||'con_name'                       ||'&sep2'||decode(sq.con_id,1,'CDB\$ROOT',(select PDB_NAME from dba_pdbs where pdb_id=sq.con_id and dbid=con_dbid))
          from dba_hist_snapshot sn, dba_hist_sqlstat sq
          where sn.dbid=${DBID} and sn.dbid = sq.dbid and sn.instance_number=${INSTANCENUMBER} and sn.instance_number= sq.instance_number and sn.end_interval_time between to_date('${DAY}', '${DATEORAFMT}') and to_date('${DAY}', '${DATEORAFMT}') + 1 and sn.snap_id=sq.snap_id;
          exit
EOF
}
function fsysmetric
{
     if [[ "$ORAVERS" = "10.2" ]]
     then
          fsysmetric112 $1 $2
     elif [[ "$ORAVERS" = "11.1" ]]
     then
          fsysmetric112 $1 $2
     elif [[ "$ORAVERS" = "11.2" ]]
     then
          fsysmetric112 $1 $2
     else
          fsysmetric121 $1 $2
     fi
}
function fsysmetric112
{
     sqlplus -s "$CONNECTSTRING" <<EOF
          set termout off heading off feedback off pages 0 lines ${COL} trimspool on verify off
          alter session set nls_date_format='YYYYMMDDHH24MISS';
          define sep1=$1
          define sep2=$2
          select end_time||' ORAHSM '||'intsize'                     ||'&sep2'||intsize
                         ||'&sep1'   ||'group_id'                    ||'&sep2'||group_id
                         ||'&sep1'   ||'metric_id'                   ||'&sep2'||metric_id
                         ||'&sep1'   ||'metric_name'                 ||'&sep2'||metric_name
                         ||'&sep1'   ||'value'                       ||'&sep2'||value
                         ||'&sep1'   ||'metric_unit'                 ||'&sep2'||metric_unit
          from dba_hist_snapshot sn, dba_hist_sysmetric_history sh
          where sn.dbid=${DBID} and sn.dbid = sh.dbid and sn.instance_number=${INSTANCENUMBER} and sn.instance_number= sh.instance_number and sn.end_interval_time between to_date('${DAY}', '${DATEORAFMT}') and to_date('${DAY}', '${DATEORAFMT}') + 1 and sn.snap_id=sh.snap_id;
          exit
EOF
}
function fsesmetric112
{
     sqlplus -s "$CONNECTSTRING" <<EOF
          set termout off heading off feedback off pages 0 lines ${COL} trimspool on verify off
          alter session set nls_date_format='YYYYMMDDHH24MISS';
          define sep1=$1
          define sep2=$2
          select end_time||' ORAHSEM '||'intsize'                     ||'&sep2'||intsize
                         ||'&sep1'    ||'sessid'                      ||'&sep2'||sessid
                         ||'&sep1'    ||'serial'                      ||'&sep2'||serial#
                         ||'&sep1'    ||'group_id'                    ||'&sep2'||group_id
                         ||'&sep1'    ||'group_id'                    ||'&sep2'||group_id
                         ||'&sep1'    ||'metric_id'                   ||'&sep2'||metric_id
                         ||'&sep1'    ||'metric_name'                 ||'&sep2'||metric_name
                         ||'&sep1'    ||'value'                       ||'&sep2'||value
                         ||'&sep1'    ||'metric_unit'                 ||'&sep2'||metric_unit
          from dba_hist_snapshot sn, dba_hist_sessmetric_history sh
          where sn.dbid=${DBID} and sn.dbid = sh.dbid and sn.instance_number=${INSTANCENUMBER} and sn.instance_number= sh.instance_number and sn.end_interval_time between to_date('${DAY}', '${DATEORAFMT}') and to_date('${DAY}', '${DATEORAFMT}') + 1 and sn.snap_id=sh.snap_id;
          exit
EOF
}
function fsysmetric121
{
     sqlplus -s "$CONNECTSTRING" <<EOF
          set termout off heading off feedback off pages 0 lines ${COL} trimspool on verify off
          alter session set nls_date_format='YYYYMMDDHH24MISS';
          define sep1=$1
          define sep2=$2
          select end_time||' ORAHSM '||'intsize'                     ||'&sep2'||intsize
                         ||'&sep1'   ||'group_id'                    ||'&sep2'||group_id
                         ||'&sep1'   ||'metric_id'                   ||'&sep2'||metric_id
                         ||'&sep1'   ||'metric_name'                 ||'&sep2'||metric_name
                         ||'&sep1'   ||'value'                       ||'&sep2'||value
                         ||'&sep1'   ||'metric_unit'                 ||'&sep2'||metric_unit
                         ||'&sep1'   ||'con_dbid'                    ||'&sep2'||con_dbid
                         ||'&sep1'   ||'con_id'                      ||'&sep2'||sh.con_id
                         ||'&sep1'   ||'con_name'                    ||'&sep2'||decode(sh.con_id,1,'CDB\$ROOT',(select PDB_NAME from dba_pdbs where pdb_id=sh.con_id and dbid=con_dbid))
          from dba_hist_snapshot sn, dba_hist_sysmetric_history sh
          where sn.dbid=${DBID} and sn.dbid = sh.dbid and sn.instance_number=${INSTANCENUMBER} and sn.instance_number= sh.instance_number and sn.end_interval_time between to_date('${DAY}', '${DATEORAFMT}') and to_date('${DAY}', '${DATEORAFMT}') + 1 and sn.snap_id=sh.snap_id;
          exit
EOF
}
function fdbahistsqltext
{
     if [[ "$ORAVERS" = "10.2" ]]
     then
          fdbahistsqltext112 $1 $2
     elif [[ "$ORAVERS" = "11.1" ]]
     then
          fdbahistsqltext112 $1 $2
     elif [[ "$ORAVERS" = "11.2" ]]
     then
          fdbahistsqltext112 $1 $2
     else
          fdbahistsqltext121 $1 $2
     fi
}
function fdbahistsqltext112
{
     sqlplus -s "$CONNECTSTRING" <<EOF
          set termout off heading off feedback off pages 0 lines ${COL} trimspool on verify off long ${COL} longc ${COL}
          alter session set nls_timestamp_format='YYYYMMDDHH24MISS';
          define sep1=$1
          define sep2=$2
          select '00000000000000'||' ORAHQT '||'sql_id'         ||'&sep2'||sql_id
                                 ||'&sep1'   ||'sql_text'       ||'&sep2'||replace(sql_text,chr(10),'')
          from dba_hist_sqltext
          where sql_id in (
               select distinct sql_id
               from dba_hist_snapshot sn, dba_hist_sqlstat sq
               where sn.dbid=${DBID} and sn.dbid = sq.dbid and sn.instance_number=${INSTANCENUMBER} and sn.instance_number= sq.instance_number and sn.end_interval_time between to_date('${DAY}', '${DATEORAFMT}') and to_date('${DAY}', '${DATEORAFMT}') + 1 and sn.snap_id=sq.snap_id) and sql_text not like '%'||'&sep1'||'%';
          exit
EOF
}
function fdbahistsqltext121
{
     sqlplus -s "$CONNECTSTRING" <<EOF
          set termout off heading off feedback off pages 0 lines ${COL} trimspool on verify off long ${COL} longc ${COL}
          alter session set nls_timestamp_format='YYYYMMDDHH24MISS';
          define sep1=$1
          define sep2=$2
          select '00000000000000'||' ORAHQT '||'sql_id'         ||'&sep2'||sql_id
                                 ||'&sep1'   ||'command_type'   ||'&sep2'||command_type
                                 ||'&sep1'   ||'con_dbid'       ||'&sep2'||con_dbid
                                 ||'&sep1'   ||'con_id'         ||'&sep2'||con_id
                                 ||'&sep1'   ||'con_name'       ||'&sep2'||decode(con_id,1,'CDB\$ROOT',(select PDB_NAME from dba_pdbs where pdb_id=con_id and dbid=con_dbid))
                                 ||'&sep1'   ||'sql_text'       ||'&sep2'||replace(sql_text,chr(10),'')
          from dba_hist_sqltext
          where sql_id in (
               select distinct sql_id
               from dba_hist_snapshot sn, dba_hist_sqlstat sq
               where sn.dbid=${DBID} and sn.dbid = sq.dbid and sn.instance_number=${INSTANCENUMBER} and sn.instance_number= sq.instance_number and sn.end_interval_time between to_date('${DAY}', '${DATEORAFMT}') and to_date('${DAY}', '${DATEORAFMT}') + 1 and sn.snap_id=sq.snap_id) and sql_text not like '%'||'&sep1'||'%';
          exit
EOF
}
function fdbahistactivesesshistory
{
     if [[ "$ORAVERS" = "10.2" ]]
     then
          fdbahistactivesesshistory102 $1 $2
     elif [[ "$ORAVERS" = "11.1" ]]
     then
          fdbahistactivesesshistory111 $1 $2
     elif [[ "$ORAVERS" = "11.2" ]]
     then
          fdbahistactivesesshistory112 $1 $2
     else
          fdbahistactivesesshistory121 $1 $2
     fi
}
function fdbahistactivesesshistory102
{
     sqlplus -s "$CONNECTSTRING" <<EOF
          set termout off heading off feedback off pages 0 lines ${COL} trimspool on verify off
          alter session set nls_timestamp_format='YYYYMMDDHH24MISS';
          define sep1=$1
          define sep2=$2
          select       sample_time||' ORAHAS '||'sql_id'                  ||'&sep2'||sql_id
                                  ||'&sep1'   ||'sample_id'               ||'&sep2'||sample_id
                                  ||'&sep1'   ||'session_id'              ||'&sep2'||session_id
                                  ||'&sep1'   ||'session_serial'          ||'&sep2'||session_serial#
                                  ||'&sep1'   ||'user_id'                 ||'&sep2'||user_id
                                  ||'&sep1'   ||'sql_child_number'        ||'&sep2'||sql_child_number
                                  ||'&sep1'   ||'sql_plan_hash_value'     ||'&sep2'||sql_plan_hash_value
                                  ||'&sep1'   ||'force_matching_signature'||'&sep2'||force_matching_signature
                                  ||'&sep1'   ||'sql_opcode'              ||'&sep2'||sql_opcode
                                  ||'&sep1'   ||'service_hash'            ||'&sep2'||service_hash
                                  ||'&sep1'   ||'session_type'            ||'&sep2'||session_type
                                  ||'&sep1'   ||'session_state'           ||'&sep2'||session_state
                                  ||'&sep1'   ||'qc_session_id'           ||'&sep2'||qc_session_id
                                  ||'&sep1'   ||'qc_instance_id'          ||'&sep2'||qc_instance_id
                                  ||'&sep1'   ||'blocking_session'        ||'&sep2'||blocking_session
                                  ||'&sep1'   ||'blocking_session_status' ||'&sep2'||blocking_session_status
                                  ||'&sep1'   ||'blocking_session_serial' ||'&sep2'||blocking_session_serial#
                                  ||'&sep1'   ||'event'                   ||'&sep2'||event
                                  ||'&sep1'   ||'event_id'                ||'&sep2'||event_id
                                  ||'&sep1'   ||'seq'                     ||'&sep2'||seq#
                                  ||'&sep1'   ||'p1'                      ||'&sep2'||p1
                                  ||'&sep1'   ||'p1text'                  ||'&sep2'||p1text
                                  ||'&sep1'   ||'p2'                      ||'&sep2'||p2
                                  ||'&sep1'   ||'p2text'                  ||'&sep2'||p2text
                                  ||'&sep1'   ||'p3'                      ||'&sep2'||p3
                                  ||'&sep1'   ||'p3text'                  ||'&sep2'||p3text
                                  ||'&sep1'   ||'wait_class'              ||'&sep2'||wait_class
                                  ||'&sep1'   ||'wait_class_id'           ||'&sep2'||wait_class_id
                                  ||'&sep1'   ||'wait_time'               ||'&sep2'||wait_time
                                  ||'&sep1'   ||'time_waited'             ||'&sep2'||time_waited
                                  ||'&sep1'   ||'xid'                     ||'&sep2'||xid
                                  ||'&sep1'   ||'current_obj'             ||'&sep2'||current_obj#
                                  ||'&sep1'   ||'current_file'            ||'&sep2'||current_file#
                                  ||'&sep1'   ||'current_block'           ||'&sep2'||current_block#
                                  ||'&sep1'   ||'program'                 ||'&sep2'||program
                                  ||'&sep1'   ||'module'                  ||'&sep2'||module
                                  ||'&sep1'   ||'action'                  ||'&sep2'||action
                                  ||'&sep1'   ||'client_id'               ||'&sep2'||client_id
          from dba_hist_snapshot sn, dba_hist_active_sess_history sq
          where sn.dbid=${DBID} and sn.dbid = sq.dbid and sn.instance_number=${INSTANCENUMBER} and sn.instance_number= sq.instance_number and sn.end_interval_time between to_date('${DAY}', '${DATEORAFMT}') and to_date('${DAY}', '${DATEORAFMT}') + 1 and sn.snap_id=sq.snap_id;
          exit
EOF
}
function fdbahistactivesesshistory111
{
     sqlplus -s "$CONNECTSTRING" <<EOF
          set termout off heading off feedback off pages 0 lines ${COL} trimspool on verify off
          alter session set nls_timestamp_format='YYYYMMDDHH24MISS';
          define sep1=$1
          define sep2=$2
          select       sample_time||' ORAHAS '||'sql_id'                  ||'&sep2'||sql_id
                                  ||'&sep1'   ||'sample_id'               ||'&sep2'||sample_id
                                  ||'&sep1'   ||'session_id'              ||'&sep2'||session_id
                                  ||'&sep1'   ||'session_serial'          ||'&sep2'||session_serial#
                                  ||'&sep1'   ||'user_id'                 ||'&sep2'||user_id
                                  ||'&sep1'   ||'sql_child_number'        ||'&sep2'||sql_child_number
                                  ||'&sep1'   ||'sql_plan_hash_value'     ||'&sep2'||sql_plan_hash_value
                                  ||'&sep1'   ||'force_matching_signature'||'&sep2'||force_matching_signature
                                  ||'&sep1'   ||'sql_opcode'              ||'&sep2'||sql_opcode
                                  ||'&sep1'   ||'service_hash'            ||'&sep2'||service_hash
                                  ||'&sep1'   ||'session_type'            ||'&sep2'||session_type
                                  ||'&sep1'   ||'session_state'           ||'&sep2'||session_state
                                  ||'&sep1'   ||'qc_session_id'           ||'&sep2'||qc_session_id
                                  ||'&sep1'   ||'qc_instance_id'          ||'&sep2'||qc_instance_id
                                  ||'&sep1'   ||'blocking_session'        ||'&sep2'||blocking_session
                                  ||'&sep1'   ||'blocking_session_status' ||'&sep2'||blocking_session_status
                                  ||'&sep1'   ||'blocking_session_serial' ||'&sep2'||blocking_session_serial#
                                  ||'&sep1'   ||'event'                   ||'&sep2'||event
                                  ||'&sep1'   ||'event_id'                ||'&sep2'||event_id
                                  ||'&sep1'   ||'seq'                     ||'&sep2'||seq#
                                  ||'&sep1'   ||'p1'                      ||'&sep2'||p1
                                  ||'&sep1'   ||'p1text'                  ||'&sep2'||p1text
                                  ||'&sep1'   ||'p2'                      ||'&sep2'||p2
                                  ||'&sep1'   ||'p2text'                  ||'&sep2'||p2text
                                  ||'&sep1'   ||'p3'                      ||'&sep2'||p3
                                  ||'&sep1'   ||'p3text'                  ||'&sep2'||p3text
                                  ||'&sep1'   ||'wait_class'              ||'&sep2'||wait_class
                                  ||'&sep1'   ||'wait_class_id'           ||'&sep2'||wait_class_id
                                  ||'&sep1'   ||'wait_time'               ||'&sep2'||wait_time
                                  ||'&sep1'   ||'time_waited'             ||'&sep2'||time_waited
                                  ||'&sep1'   ||'xid'                     ||'&sep2'||xid
                                  ||'&sep1'   ||'current_obj'             ||'&sep2'||current_obj#
                                  ||'&sep1'   ||'current_file'            ||'&sep2'||current_file#
                                  ||'&sep1'   ||'current_block'           ||'&sep2'||current_block#
                                  ||'&sep1'   ||'program'                 ||'&sep2'||program
                                  ||'&sep1'   ||'module'                  ||'&sep2'||module
                                  ||'&sep1'   ||'action'                  ||'&sep2'||action
                                  ||'&sep1'   ||'client_id'               ||'&sep2'||client_id
                                  ||'&sep1'   ||'consumer_group_id'       ||'&sep2'||consumer_group_id
                                  ||'&sep1'   ||'current_row'             ||'&sep2'||current_row#
                                  ||'&sep1'   ||'in_bind'                 ||'&sep2'||in_bind
                                  ||'&sep1'   ||'in_connection_mgmt'      ||'&sep2'||in_connection_mgmt
                                  ||'&sep1'   ||'in_cursor_close'         ||'&sep2'||in_cursor_close
                                  ||'&sep1'   ||'in_hard_parse'           ||'&sep2'||in_hard_parse
                                  ||'&sep1'   ||'in_java_execution'       ||'&sep2'||in_java_execution
                                  ||'&sep1'   ||'in_parse'                ||'&sep2'||in_parse
                                  ||'&sep1'   ||'in_plsql_compilation'    ||'&sep2'||in_plsql_compilation
                                  ||'&sep1'   ||'in_plsql_execution'      ||'&sep2'||in_plsql_execution
                                  ||'&sep1'   ||'in_plsql_rpc'            ||'&sep2'||in_plsql_rpc
                                  ||'&sep1'   ||'in_sql_execution'        ||'&sep2'||in_sql_execution
                                  ||'&sep1'   ||'plsql_entry_object_id'   ||'&sep2'||plsql_entry_object_id
                                  ||'&sep1'   ||'plsql_entry_subprogram_id' ||'&sep2'||plsql_entry_subprogram_id
                                  ||'&sep1'   ||'plsql_object_id'         ||'&sep2'||plsql_object_id
                                  ||'&sep1'   ||'plsql_subprogram_id'     ||'&sep2'||plsql_subprogram_id
                                  ||'&sep1'   ||'qc_session_serial'       ||'&sep2'||qc_session_serial#
                                  ||'&sep1'   ||'remote_instance'         ||'&sep2'||remote_instance#
                                  ||'&sep1'   ||'sql_exec_id'             ||'&sep2'||sql_exec_id
                                  ||'&sep1'   ||'sql_exec_start'          ||'&sep2'||sql_exec_start
                                  ||'&sep1'   ||'sql_plan_line_id'        ||'&sep2'||sql_plan_line_id
                                  ||'&sep1'   ||'sql_plan_operation'      ||'&sep2'||sql_plan_operation
                                  ||'&sep1'   ||'sql_plan_options'        ||'&sep2'||sql_plan_options
          from dba_hist_snapshot sn, dba_hist_active_sess_history sq
          where sn.dbid=${DBID} and sn.dbid = sq.dbid and sn.instance_number=${INSTANCENUMBER} and sn.instance_number= sq.instance_number and sn.end_interval_time between to_date('${DAY}', '${DATEORAFMT}') and to_date('${DAY}', '${DATEORAFMT}') + 1 and sn.snap_id=sq.snap_id;
          exit
EOF
}
function fdbahistactivesesshistory112
{
     sqlplus -s "$CONNECTSTRING" <<EOF
          set termout off heading off feedback off pages 0 lines ${COL} trimspool on verify off
          alter session set nls_timestamp_format='YYYYMMDDHH24MISS';
          define sep1=$1
          define sep2=$2
          select       sample_time||' ORAHAS '||'sql_id'                  ||'&sep2'||sql_id
                                  ||'&sep1'   ||'sample_id'               ||'&sep2'||sample_id
                                  ||'&sep1'   ||'session_id'              ||'&sep2'||session_id
                                  ||'&sep1'   ||'session_serial'          ||'&sep2'||session_serial#
                                  ||'&sep1'   ||'user_id'                 ||'&sep2'||user_id
                                  ||'&sep1'   ||'sql_child_number'        ||'&sep2'||sql_child_number
                                  ||'&sep1'   ||'sql_plan_hash_value'     ||'&sep2'||sql_plan_hash_value
                                  ||'&sep1'   ||'force_matching_signature'||'&sep2'||force_matching_signature
                                  ||'&sep1'   ||'sql_opcode'              ||'&sep2'||sql_opcode
                                  ||'&sep1'   ||'service_hash'            ||'&sep2'||service_hash
                                  ||'&sep1'   ||'session_type'            ||'&sep2'||session_type
                                  ||'&sep1'   ||'session_state'           ||'&sep2'||session_state
                                  ||'&sep1'   ||'qc_session_id'           ||'&sep2'||qc_session_id
                                  ||'&sep1'   ||'qc_instance_id'          ||'&sep2'||qc_instance_id
                                  ||'&sep1'   ||'blocking_session'        ||'&sep2'||blocking_session
                                  ||'&sep1'   ||'blocking_session_status' ||'&sep2'||blocking_session_status
                                  ||'&sep1'   ||'blocking_session_serial' ||'&sep2'||blocking_session_serial#
                                  ||'&sep1'   ||'event'                   ||'&sep2'||event
                                  ||'&sep1'   ||'event_id'                ||'&sep2'||event_id
                                  ||'&sep1'   ||'seq'                     ||'&sep2'||seq#
                                  ||'&sep1'   ||'p1'                      ||'&sep2'||p1
                                  ||'&sep1'   ||'p1text'                  ||'&sep2'||p1text
                                  ||'&sep1'   ||'p2'                      ||'&sep2'||p2
                                  ||'&sep1'   ||'p2text'                  ||'&sep2'||p2text
                                  ||'&sep1'   ||'p3'                      ||'&sep2'||p3
                                  ||'&sep1'   ||'p3text'                  ||'&sep2'||p3text
                                  ||'&sep1'   ||'wait_class'              ||'&sep2'||wait_class
                                  ||'&sep1'   ||'wait_class_id'           ||'&sep2'||wait_class_id
                                  ||'&sep1'   ||'wait_time'               ||'&sep2'||wait_time
                                  ||'&sep1'   ||'time_waited'             ||'&sep2'||time_waited
                                  ||'&sep1'   ||'xid'                     ||'&sep2'||xid
                                  ||'&sep1'   ||'current_obj'             ||'&sep2'||current_obj#
                                  ||'&sep1'   ||'current_file'            ||'&sep2'||current_file#
                                  ||'&sep1'   ||'current_block'           ||'&sep2'||current_block#
                                  ||'&sep1'   ||'program'                 ||'&sep2'||program
                                  ||'&sep1'   ||'module'                  ||'&sep2'||module
                                  ||'&sep1'   ||'action'                  ||'&sep2'||action
                                  ||'&sep1'   ||'client_id'               ||'&sep2'||client_id
                                  ||'&sep1'   ||'blocking_hangchain_info' ||'&sep2'||blocking_hangchain_info
                                  ||'&sep1'   ||'blocking_inst_id'        ||'&sep2'||blocking_inst_id
                                  ||'&sep1'   ||'capture_overhead'        ||'&sep2'||capture_overhead
                                  ||'&sep1'   ||'consumer_group_id'       ||'&sep2'||consumer_group_id
                                  ||'&sep1'   ||'current_row'             ||'&sep2'||current_row#
                                  ||'&sep1'   ||'delta_interconnect_io_bytes' ||'&sep2'||delta_interconnect_io_bytes
                                  ||'&sep1'   ||'delta_read_io_bytes'     ||'&sep2'||delta_read_io_bytes
                                  ||'&sep1'   ||'delta_read_io_requests'  ||'&sep2'||delta_read_io_requests
                                  ||'&sep1'   ||'delta_time'              ||'&sep2'||delta_time
                                  ||'&sep1'   ||'delta_write_io_bytes'    ||'&sep2'||delta_write_io_bytes
                                  ||'&sep1'   ||'delta_write_io_requests' ||'&sep2'||delta_write_io_requests
                                  ||'&sep1'   ||'ecid'                    ||'&sep2'||ecid
                                  ||'&sep1'   ||'flags'                   ||'&sep2'||flags
                                  ||'&sep1'   ||'in_bind'                 ||'&sep2'||in_bind
                                  ||'&sep1'   ||'in_connection_mgmt'      ||'&sep2'||in_connection_mgmt
                                  ||'&sep1'   ||'in_cursor_close'         ||'&sep2'||in_cursor_close
                                  ||'&sep1'   ||'in_hard_parse'           ||'&sep2'||in_hard_parse
                                  ||'&sep1'   ||'in_java_execution'       ||'&sep2'||in_java_execution
                                  ||'&sep1'   ||'in_parse'                ||'&sep2'||in_parse
                                  ||'&sep1'   ||'in_plsql_compilation'    ||'&sep2'||in_plsql_compilation
                                  ||'&sep1'   ||'in_plsql_execution'      ||'&sep2'||in_plsql_execution
                                  ||'&sep1'   ||'in_plsql_rpc'            ||'&sep2'||in_plsql_rpc
                                  ||'&sep1'   ||'in_sequence_load'        ||'&sep2'||in_sequence_load
                                  ||'&sep1'   ||'in_sql_execution'        ||'&sep2'||in_sql_execution
                                  ||'&sep1'   ||'is_captured'             ||'&sep2'||is_captured
                                  ||'&sep1'   ||'is_replayed'             ||'&sep2'||is_replayed
                                  ||'&sep1'   ||'is_sqlid_current'        ||'&sep2'||is_sqlid_current
                                  ||'&sep1'   ||'machine'                 ||'&sep2'||machine
                                  ||'&sep1'   ||'pga_allocated'           ||'&sep2'||pga_allocated
                                  ||'&sep1'   ||'plsql_entry_object_id'   ||'&sep2'||plsql_entry_object_id
                                  ||'&sep1'   ||'plsql_entry_subprogram_id' ||'&sep2'||plsql_entry_subprogram_id
                                  ||'&sep1'   ||'plsql_object_id'         ||'&sep2'||plsql_object_id
                                  ||'&sep1'   ||'plsql_subprogram_id'     ||'&sep2'||plsql_subprogram_id
                                  ||'&sep1'   ||'port'                    ||'&sep2'||port
                                  ||'&sep1'   ||'qc_session_serial'       ||'&sep2'||qc_session_serial#
                                  ||'&sep1'   ||'remote_instance'         ||'&sep2'||remote_instance#
                                  ||'&sep1'   ||'replay_overhead'         ||'&sep2'||replay_overhead
                                  ||'&sep1'   ||'sql_exec_id'             ||'&sep2'||sql_exec_id
                                  ||'&sep1'   ||'sql_exec_start'          ||'&sep2'||sql_exec_start
                                  ||'&sep1'   ||'sql_opname'              ||'&sep2'||sql_opname
                                  ||'&sep1'   ||'sql_plan_line_id'        ||'&sep2'||sql_plan_line_id
                                  ||'&sep1'   ||'sql_plan_operation'      ||'&sep2'||sql_plan_operation
                                  ||'&sep1'   ||'sql_plan_options'        ||'&sep2'||sql_plan_options
                                  ||'&sep1'   ||'temp_space_allocated'    ||'&sep2'||temp_space_allocated
                                  ||'&sep1'   ||'time_model'              ||'&sep2'||time_model
                                  ||'&sep1'   ||'tm_delta_cpu_time'       ||'&sep2'||tm_delta_cpu_time
                                  ||'&sep1'   ||'tm_delta_db_time'        ||'&sep2'||tm_delta_db_time
                                  ||'&sep1'   ||'tm_delta_time'           ||'&sep2'||tm_delta_time
                                  ||'&sep1'   ||'top_level_call'          ||'&sep2'||top_level_call#
                                  ||'&sep1'   ||'top_level_call_name'     ||'&sep2'||top_level_call_name
                                  ||'&sep1'   ||'top_level_sql_id'        ||'&sep2'||top_level_sql_id
                                  ||'&sep1'   ||'top_level_sql_opcode'    ||'&sep2'||top_level_sql_opcode
          from dba_hist_snapshot sn, dba_hist_active_sess_history sq
          where sn.dbid=${DBID} and sn.dbid = sq.dbid and sn.instance_number=${INSTANCENUMBER} and sn.instance_number= sq.instance_number and sn.end_interval_time between to_date('${DAY}', '${DATEORAFMT}') and to_date('${DAY}', '${DATEORAFMT}') + 1 and sn.snap_id=sq.snap_id;
          exit
EOF
}
function fdbahistactivesesshistory121
{
     sqlplus -s "$CONNECTSTRING" <<EOF
          set termout off heading off feedback off pages 0 lines ${COL} trimspool on verify off
          alter session set nls_timestamp_format='YYYYMMDDHH24MISS';
          define sep1=$1
          define sep2=$2
          select       sample_time||' ORAHAS '||'sql_id'                  ||'&sep2'||sql_id
                                  ||'&sep1'   ||'sample_id'               ||'&sep2'||sample_id
                                  ||'&sep1'   ||'session_id'              ||'&sep2'||session_id
                                  ||'&sep1'   ||'session_serial'          ||'&sep2'||session_serial#
                                  ||'&sep1'   ||'user_id'                 ||'&sep2'||user_id
                                  ||'&sep1'   ||'sql_child_number'        ||'&sep2'||sql_child_number
                                  ||'&sep1'   ||'sql_plan_hash_value'     ||'&sep2'||sql_plan_hash_value
                                  ||'&sep1'   ||'force_matching_signature'||'&sep2'||force_matching_signature
                                  ||'&sep1'   ||'sql_opcode'              ||'&sep2'||sql_opcode
                                  ||'&sep1'   ||'service_hash'            ||'&sep2'||service_hash
                                  ||'&sep1'   ||'session_type'            ||'&sep2'||session_type
                                  ||'&sep1'   ||'session_state'           ||'&sep2'||session_state
                                  ||'&sep1'   ||'qc_session_id'           ||'&sep2'||qc_session_id
                                  ||'&sep1'   ||'qc_instance_id'          ||'&sep2'||qc_instance_id
                                  ||'&sep1'   ||'blocking_session'        ||'&sep2'||blocking_session
                                  ||'&sep1'   ||'blocking_session_status' ||'&sep2'||blocking_session_status
                                  ||'&sep1'   ||'blocking_session_serial' ||'&sep2'||blocking_session_serial#
                                  ||'&sep1'   ||'event'                   ||'&sep2'||event
                                  ||'&sep1'   ||'event_id'                ||'&sep2'||event_id
                                  ||'&sep1'   ||'seq'                     ||'&sep2'||seq#
                                  ||'&sep1'   ||'p1'                      ||'&sep2'||p1
                                  ||'&sep1'   ||'p1text'                  ||'&sep2'||p1text
                                  ||'&sep1'   ||'p2'                      ||'&sep2'||p2
                                  ||'&sep1'   ||'p2text'                  ||'&sep2'||p2text
                                  ||'&sep1'   ||'p3'                      ||'&sep2'||p3
                                  ||'&sep1'   ||'p3text'                  ||'&sep2'||p3text
                                  ||'&sep1'   ||'wait_class'              ||'&sep2'||wait_class
                                  ||'&sep1'   ||'wait_class_id'           ||'&sep2'||wait_class_id
                                  ||'&sep1'   ||'wait_time'               ||'&sep2'||wait_time
                                  ||'&sep1'   ||'time_waited'             ||'&sep2'||time_waited
                                  ||'&sep1'   ||'xid'                     ||'&sep2'||xid
                                  ||'&sep1'   ||'current_obj'             ||'&sep2'||current_obj#
                                  ||'&sep1'   ||'current_file'            ||'&sep2'||current_file#
                                  ||'&sep1'   ||'current_block'           ||'&sep2'||current_block#
                                  ||'&sep1'   ||'program'                 ||'&sep2'||program
                                  ||'&sep1'   ||'module'                  ||'&sep2'||module
                                  ||'&sep1'   ||'action'                  ||'&sep2'||action
                                  ||'&sep1'   ||'client_id'               ||'&sep2'||client_id
                                  ||'&sep1'   ||'blocking_hangchain_info' ||'&sep2'||blocking_hangchain_info
                                  ||'&sep1'   ||'blocking_inst_id'        ||'&sep2'||blocking_inst_id
                                  ||'&sep1'   ||'capture_overhead'        ||'&sep2'||capture_overhead
                                  ||'&sep1'   ||'consumer_group_id'       ||'&sep2'||consumer_group_id
                                  ||'&sep1'   ||'current_row'             ||'&sep2'||current_row#
                                  ||'&sep1'   ||'delta_interconnect_io_bytes' ||'&sep2'||delta_interconnect_io_bytes
                                  ||'&sep1'   ||'delta_read_io_bytes'     ||'&sep2'||delta_read_io_bytes
                                  ||'&sep1'   ||'delta_read_io_requests'  ||'&sep2'||delta_read_io_requests
                                  ||'&sep1'   ||'delta_time'              ||'&sep2'||delta_time
                                  ||'&sep1'   ||'delta_write_io_bytes'    ||'&sep2'||delta_write_io_bytes
                                  ||'&sep1'   ||'delta_write_io_requests' ||'&sep2'||delta_write_io_requests
                                  ||'&sep1'   ||'ecid'                    ||'&sep2'||ecid
                                  ||'&sep1'   ||'flags'                   ||'&sep2'||flags
                                  ||'&sep1'   ||'in_bind'                 ||'&sep2'||in_bind
                                  ||'&sep1'   ||'in_connection_mgmt'      ||'&sep2'||in_connection_mgmt
                                  ||'&sep1'   ||'in_cursor_close'         ||'&sep2'||in_cursor_close
                                  ||'&sep1'   ||'in_hard_parse'           ||'&sep2'||in_hard_parse
                                  ||'&sep1'   ||'in_java_execution'       ||'&sep2'||in_java_execution
                                  ||'&sep1'   ||'in_parse'                ||'&sep2'||in_parse
                                  ||'&sep1'   ||'in_plsql_compilation'    ||'&sep2'||in_plsql_compilation
                                  ||'&sep1'   ||'in_plsql_execution'      ||'&sep2'||in_plsql_execution
                                  ||'&sep1'   ||'in_plsql_rpc'            ||'&sep2'||in_plsql_rpc
                                  ||'&sep1'   ||'in_sequence_load'        ||'&sep2'||in_sequence_load
                                  ||'&sep1'   ||'in_sql_execution'        ||'&sep2'||in_sql_execution
                                  ||'&sep1'   ||'is_captured'             ||'&sep2'||is_captured
                                  ||'&sep1'   ||'is_replayed'             ||'&sep2'||is_replayed
                                  ||'&sep1'   ||'is_sqlid_current'        ||'&sep2'||is_sqlid_current
                                  ||'&sep1'   ||'machine'                 ||'&sep2'||machine
                                  ||'&sep1'   ||'pga_allocated'           ||'&sep2'||pga_allocated
                                  ||'&sep1'   ||'plsql_entry_object_id'   ||'&sep2'||plsql_entry_object_id
                                  ||'&sep1'   ||'plsql_entry_subprogram_id' ||'&sep2'||plsql_entry_subprogram_id
                                  ||'&sep1'   ||'plsql_object_id'         ||'&sep2'||plsql_object_id
                                  ||'&sep1'   ||'plsql_subprogram_id'     ||'&sep2'||plsql_subprogram_id
                                  ||'&sep1'   ||'port'                    ||'&sep2'||port
                                  ||'&sep1'   ||'qc_session_serial'       ||'&sep2'||qc_session_serial#
                                  ||'&sep1'   ||'remote_instance'         ||'&sep2'||remote_instance#
                                  ||'&sep1'   ||'replay_overhead'         ||'&sep2'||replay_overhead
                                  ||'&sep1'   ||'sql_exec_id'             ||'&sep2'||sql_exec_id
                                  ||'&sep1'   ||'sql_exec_start'          ||'&sep2'||sql_exec_start
                                  ||'&sep1'   ||'sql_opname'              ||'&sep2'||sql_opname
                                  ||'&sep1'   ||'sql_plan_line_id'        ||'&sep2'||sql_plan_line_id
                                  ||'&sep1'   ||'sql_plan_operation'      ||'&sep2'||sql_plan_operation
                                  ||'&sep1'   ||'sql_plan_options'        ||'&sep2'||sql_plan_options
                                  ||'&sep1'   ||'temp_space_allocated'    ||'&sep2'||temp_space_allocated
                                  ||'&sep1'   ||'time_model'              ||'&sep2'||time_model
                                  ||'&sep1'   ||'tm_delta_cpu_time'       ||'&sep2'||tm_delta_cpu_time
                                  ||'&sep1'   ||'tm_delta_db_time'        ||'&sep2'||tm_delta_db_time
                                  ||'&sep1'   ||'tm_delta_time'           ||'&sep2'||tm_delta_time
                                  ||'&sep1'   ||'top_level_call'          ||'&sep2'||top_level_call#
                                  ||'&sep1'   ||'top_level_call_name'     ||'&sep2'||top_level_call_name
                                  ||'&sep1'   ||'top_level_sql_id'        ||'&sep2'||top_level_sql_id
                                  ||'&sep1'   ||'top_level_sql_opcode'    ||'&sep2'||top_level_sql_opcode
                                  ||'&sep1'   ||'dbreplay_file_id'        ||'&sep2'||dbreplay_file_id
                                  ||'&sep1'   ||'dbreplay_call_counter'   ||'&sep2'||dbreplay_call_counter
                                  ||'&sep1'   ||'dbop_name'               ||'&sep2'||dbop_name
                                  ||'&sep1'   ||'dbop_exec_id'            ||'&sep2'||dbop_exec_id
                                  ||'&sep1'   ||'con_dbid'                ||'&sep2'||con_dbid
                                  ||'&sep1'   ||'con_id'                  ||'&sep2'||sq.con_id
                                  ||'&sep1'   ||'con_name'                ||'&sep2'||decode(sq.con_id,1,'CDB\$ROOT',(select PDB_NAME from dba_pdbs where pdb_id=sq.con_id and dbid=con_dbid))
          from dba_hist_snapshot sn, dba_hist_active_sess_history sq
          where sn.dbid=${DBID} and sn.dbid = sq.dbid and sn.instance_number=${INSTANCENUMBER} and sn.instance_number= sq.instance_number and sn.end_interval_time between to_date('${DAY}', '${DATEORAFMT}') and to_date('${DAY}', '${DATEORAFMT}') + 1 and sn.snap_id=sq.snap_id;
          exit
EOF
}
function fbashhistactivesesshistory
{
     sqlplus -s "$CONNECTSTRING" <<EOF
          set termout off heading off feedback off pages 0 lines ${COL} trimspool on verify off
          alter session set nls_timestamp_format='YYYYMMDDHH24MISS';
          define sep1=$1
          define sep2=$2
          select       sample_time||' ORAHAS '||'sql_id'                  ||'&sep2'||sql_id
                                  ||'&sep1'   ||'sample_id'               ||'&sep2'||sample_id
                                  ||'&sep1'   ||'session_id'              ||'&sep2'||session_id
                                  ||'&sep1'   ||'session_serial'          ||'&sep2'||session_serial#
                                  ||'&sep1'   ||'user_id'                 ||'&sep2'||user_id
                                  ||'&sep1'   ||'sql_child_number'        ||'&sep2'||sql_child_number
                                  ||'&sep1'   ||'sql_plan_hash_value'     ||'&sep2'||sql_plan_hash_value
                                  ||'&sep1'   ||'force_matching_signature'||'&sep2'||force_matching_signature
                                  ||'&sep1'   ||'sql_opcode'              ||'&sep2'||sql_opcode
                                  ||'&sep1'   ||'service_hash'            ||'&sep2'||service_hash
                                  ||'&sep1'   ||'session_type'            ||'&sep2'||session_type
                                  ||'&sep1'   ||'session_state'           ||'&sep2'||session_state
                                  ||'&sep1'   ||'qc_session_id'           ||'&sep2'||qc_session_id
                                  ||'&sep1'   ||'qc_instance_id'          ||'&sep2'||qc_instance_id
                                  ||'&sep1'   ||'blocking_session'        ||'&sep2'||blocking_session
                                  ||'&sep1'   ||'blocking_session_status' ||'&sep2'||blocking_session_status
                                  ||'&sep1'   ||'blocking_session_serial' ||'&sep2'||blocking_session_serial#
                                  ||'&sep1'   ||'event'                   ||'&sep2'||event
                                  ||'&sep1'   ||'event_id'                ||'&sep2'||event_id
                                  ||'&sep1'   ||'seq'                     ||'&sep2'||seq#
                                  ||'&sep1'   ||'p1'                      ||'&sep2'||p1
                                  ||'&sep1'   ||'p1text'                  ||'&sep2'||p1text
                                  ||'&sep1'   ||'p2'                      ||'&sep2'||p2
                                  ||'&sep1'   ||'p2text'                  ||'&sep2'||p2text
                                  ||'&sep1'   ||'p3'                      ||'&sep2'||p3
                                  ||'&sep1'   ||'p3text'                  ||'&sep2'||p3text
                                  ||'&sep1'   ||'wait_class'              ||'&sep2'||wait_class
                                  ||'&sep1'   ||'wait_class_id'           ||'&sep2'||wait_class_id
                                  ||'&sep1'   ||'wait_time'               ||'&sep2'||wait_time
                                  ||'&sep1'   ||'time_waited'             ||'&sep2'||time_waited
                                  ||'&sep1'   ||'xid'                     ||'&sep2'||xid
                                  ||'&sep1'   ||'current_obj'             ||'&sep2'||current_obj#
                                  ||'&sep1'   ||'current_file'            ||'&sep2'||current_file#
                                  ||'&sep1'   ||'current_block'           ||'&sep2'||current_block#
                                  ||'&sep1'   ||'program'                 ||'&sep2'||program
                                  ||'&sep1'   ||'module'                  ||'&sep2'||module
                                  ||'&sep1'   ||'action'                  ||'&sep2'||action
                                  ||'&sep1'   ||'client_id'               ||'&sep2'||client_id
                                  ||'&sep1'   ||'blocking_hangchain_info' ||'&sep2'||blocking_hangchain_info
                                  ||'&sep1'   ||'blocking_inst_id'        ||'&sep2'||blocking_inst_id
                                  ||'&sep1'   ||'capture_overhead'        ||'&sep2'||capture_overhead
                                  ||'&sep1'   ||'consumer_group_id'       ||'&sep2'||consumer_group_id
                                  ||'&sep1'   ||'current_row'             ||'&sep2'||current_row#
                                  ||'&sep1'   ||'delta_interconnect_io_bytes' ||'&sep2'||delta_interconnect_io_bytes
                                  ||'&sep1'   ||'delta_read_io_bytes'     ||'&sep2'||delta_read_io_bytes
                                  ||'&sep1'   ||'delta_read_io_requests'  ||'&sep2'||delta_read_io_requests
                                  ||'&sep1'   ||'delta_time'              ||'&sep2'||delta_time
                                  ||'&sep1'   ||'delta_write_io_bytes'    ||'&sep2'||delta_write_io_bytes
                                  ||'&sep1'   ||'delta_write_io_requests' ||'&sep2'||delta_write_io_requests
                                  ||'&sep1'   ||'ecid'                    ||'&sep2'||ecid
                                  ||'&sep1'   ||'flags'                   ||'&sep2'||flags
                                  ||'&sep1'   ||'in_bind'                 ||'&sep2'||in_bind
                                  ||'&sep1'   ||'in_connection_mgmt'      ||'&sep2'||in_connection_mgmt
                                  ||'&sep1'   ||'in_cursor_close'         ||'&sep2'||in_cursor_close
                                  ||'&sep1'   ||'in_hard_parse'           ||'&sep2'||in_hard_parse
                                  ||'&sep1'   ||'in_java_execution'       ||'&sep2'||in_java_execution
                                  ||'&sep1'   ||'in_parse'                ||'&sep2'||in_parse
                                  ||'&sep1'   ||'in_plsql_compilation'    ||'&sep2'||in_plsql_compilation
                                  ||'&sep1'   ||'in_plsql_execution'      ||'&sep2'||in_plsql_execution
                                  ||'&sep1'   ||'in_plsql_rpc'            ||'&sep2'||in_plsql_rpc
                                  ||'&sep1'   ||'in_sequence_load'        ||'&sep2'||in_sequence_load
                                  ||'&sep1'   ||'in_sql_execution'        ||'&sep2'||in_sql_execution
                                  ||'&sep1'   ||'is_captured'             ||'&sep2'||is_captured
                                  ||'&sep1'   ||'is_replayed'             ||'&sep2'||is_replayed
                                  ||'&sep1'   ||'is_sqlid_current'        ||'&sep2'||is_sqlid_current
                                  ||'&sep1'   ||'machine'                 ||'&sep2'||machine
                                  ||'&sep1'   ||'pga_allocated'           ||'&sep2'||pga_allocated
                                  ||'&sep1'   ||'plsql_entry_object_id'   ||'&sep2'||plsql_entry_object_id
                                  ||'&sep1'   ||'plsql_entry_subprogram_id' ||'&sep2'||plsql_entry_subprogram_id
                                  ||'&sep1'   ||'plsql_object_id'         ||'&sep2'||plsql_object_id
                                  ||'&sep1'   ||'plsql_subprogram_id'     ||'&sep2'||plsql_subprogram_id
                                  ||'&sep1'   ||'port'                    ||'&sep2'||port
                                  ||'&sep1'   ||'qc_session_serial'       ||'&sep2'||qc_session_serial#
                                  ||'&sep1'   ||'remote_instance'         ||'&sep2'||remote_instance#
                                  ||'&sep1'   ||'replay_overhead'         ||'&sep2'||replay_overhead
                                  ||'&sep1'   ||'sql_exec_id'             ||'&sep2'||sql_exec_id
                                  ||'&sep1'   ||'sql_exec_start'          ||'&sep2'||sql_exec_start
                                  ||'&sep1'   ||'sql_opname'              ||'&sep2'||sql_opname
                                  ||'&sep1'   ||'sql_plan_line_id'        ||'&sep2'||sql_plan_line_id
                                  ||'&sep1'   ||'sql_plan_operation'      ||'&sep2'||sql_plan_operation
                                  ||'&sep1'   ||'sql_plan_options'        ||'&sep2'||sql_plan_options
                                  ||'&sep1'   ||'temp_space_allocated'    ||'&sep2'||temp_space_allocated
                                  ||'&sep1'   ||'time_model'              ||'&sep2'||time_model
                                  ||'&sep1'   ||'tm_delta_cpu_time'       ||'&sep2'||tm_delta_cpu_time
                                  ||'&sep1'   ||'tm_delta_db_time'        ||'&sep2'||tm_delta_db_time
                                  ||'&sep1'   ||'tm_delta_time'           ||'&sep2'||tm_delta_time
                                  ||'&sep1'   ||'top_level_call'          ||'&sep2'||top_level_call#
                                  ||'&sep1'   ||'top_level_call_name'     ||'&sep2'||top_level_call_name
                                  ||'&sep1'   ||'top_level_sql_id'        ||'&sep2'||top_level_sql_id
                                  ||'&sep1'   ||'top_level_sql_opcode'    ||'&sep2'||top_level_sql_opcode
                                  ||'&sep1'   ||'dbreplay_file_id'        ||'&sep2'||dbreplay_file_id
                                  ||'&sep1'   ||'dbreplay_call_counter'   ||'&sep2'||dbreplay_call_counter
          from bash\$hist_active_sess_history sq
          where sq.instance_number=${INSTANCENUMBER} and sq.sample_time between to_date('${DAY}', '${DATEORAFMT}') and to_date('${DAY}', '${DATEORAFMT}') + 1;
          exit
EOF
}
function fbash
{
     SEP1=":,"
     SEP2=":="
     fbashhistactivesesshistory ${SEP1} ${SEP2} | split -l 10000 - kairos_extr_
     for f in kairos_extr_*
     do
          SUFFIX=$(echo $f|sed -e 's/kairos_extr_//')
          REPORT=${LD_INSTANCENAME}_bashhistactivesesshistory_${DAY}_$SUFFIX.lst
          fheader ${SEP1} ${SEP2} > $REPORT
          echo 'TYPE ORAHAS action text' >>$REPORT
          echo 'TYPE ORAHAS session_id text' >>$REPORT
          echo 'TYPE ORAHAS sample_id text' >>$REPORT
          echo 'TYPE ORAHAS session_serial text' >>$REPORT
          echo 'TYPE ORAHAS user_id text' >>$REPORT
          echo 'TYPE ORAHAS sql_child_number text' >>$REPORT
          echo 'TYPE ORAHAS sql_plan_hash_value text' >>$REPORT
          echo 'TYPE ORAHAS optimizer_env_hash_value text' >>$REPORT
          echo 'TYPE ORAHAS force_matching_signature text' >>$REPORT
          echo 'TYPE ORAHAS sql_opcode text' >>$REPORT
          echo 'TYPE ORAHAS service_hash text' >>$REPORT
          echo 'TYPE ORAHAS qc_session_id text' >>$REPORT
          echo 'TYPE ORAHAS qc_instance_id text' >>$REPORT
          echo 'TYPE ORAHAS qc_session_serial text' >>$REPORT
          echo 'TYPE ORAHAS blocking_session text' >>$REPORT
          echo 'TYPE ORAHAS blocking_session_serial text' >>$REPORT
          echo 'TYPE ORAHAS event_id text' >>$REPORT
          echo 'TYPE ORAHAS p1 text' >>$REPORT
          echo 'TYPE ORAHAS p2 text' >>$REPORT
          echo 'TYPE ORAHAS p3 text' >>$REPORT
          echo 'TYPE ORAHAS xid text' >>$REPORT
          echo 'TYPE ORAHAS current_obj text' >>$REPORT
          echo 'TYPE ORAHAS current_file text' >>$REPORT
          echo 'TYPE ORAHAS current_block text' >>$REPORT
          echo 'TYPE ORAHAS current_row text' >>$REPORT
          echo 'TYPE ORAHAS flags text' >>$REPORT
          echo 'TYPE ORAHAS top_level_sql_opcode text' >>$REPORT
          echo 'TYPE ORAHAS sql_plan_line_id text' >>$REPORT
          echo 'TYPE ORAHAS sql_exec_id text' >>$REPORT
          echo 'TYPE ORAHAS sql_exec_start text' >>$REPORT
          echo 'TYPE ORAHAS plsql_entry_object_id text' >>$REPORT
          echo 'TYPE ORAHAS plsql_entry_subprogram_id text' >>$REPORT
          echo 'TYPE ORAHAS plsql_object_id text' >>$REPORT
          echo 'TYPE ORAHAS plsql_subprogram_id text' >>$REPORT
          echo 'TYPE ORAHAS seq text' >>$REPORT
          echo 'TYPE ORAHAS wait_class_id text' >>$REPORT
          echo 'TYPE ORAHAS blocking_inst_id text' >>$REPORT
          echo 'TYPE ORAHAS top_level_call text' >>$REPORT
          echo 'TYPE ORAHAS consumer_group_id text' >>$REPORT
          echo 'TYPE ORAHAS remote_instance text' >>$REPORT
          echo 'TYPE ORAHAS time_model text' >>$REPORT
          echo 'TYPE ORAHAS port text' >>$REPORT
          echo 'TYPE ORAHAS dbreplay_file_id text' >>$REPORT
          echo 'TYPE ORAHAS dbop_exec_id text' >>$REPORT
          echo 'TYPE ORAHAS con_dbid text' >>$REPORT
          echo 'TYPE ORAHAS con_id text' >>$REPORT
          echo 'TYPE ORAHAS pga_allocated real' >>$REPORT
          echo 'TYPE ORAHAS temp_space_allocated real' >>$REPORT
          cat $f >>$REPORT
          tar rf ${TEMPFILE} ${REPORT}
          rm ${REPORT}
          rm $f
     done
}
function finalize_output
{
     if [[ ${ARCHIVE_TYP} = 'tgz' ]]
     then
          OUTFILE=$PREFIX.tgz
          cat $TEMPFILE|gzip>$OUTFILE
     else
          OUTFILE=$PREFIX.zip
          rm -f $OUTFILE
          TEMPDIR=$DIR/kairos_$$
          mkdir $TEMPDIR
          cd $TEMPDIR
          tar xf $TEMPFILE
          zip $PREFIX.zip *
          cd ..
          rm -fr $TEMPDIR
     fi
     rm $TEMPFILE
}
function fsar
{
     SARPATH=/var/adm/sa
     case $(uname -s) in
          Linux) SARPATH=/var/log/sa ;;
     esac
     export LANG=en_US
     SARFILE=sa$(echo $DAY|sed -e 's:........::')
     REPORT=sa${DAY}.txt
     sar -A -f ${SARPATH}/${SARFILE} >${REPORT}
     tar rf ${TEMPFILE} ${REPORT}
     rm ${REPORT}
}
function fnmon
{
     YMD=$(echo $DAY|sed -e 's:^..::' -e 's:^..:&@:' -e 's:@.*$::')$(echo $DAY|sed -e 's:^.....::' -e 's:^..:&@:' -e 's:@.*$::')$(echo $DAY|sed -e 's:^........::')
     cd ${NMON}
     if [[ $1 -eq 0 ]]
     then
        NMONFILE=$(hostname -s)_${YMD}_*.nmon
     else
        NMONINPUT=$(hostname -s)_${YMD}.topas
        NMONFILE=$(hostname -s)_${YMD}_*.topas_01
        topasout -a ${NMONINPUT}
     fi
     tar rf ${TEMPFILE} ${NMONFILE}
}
function fheader
{
        echo "REPORT TYPE: GENERIC SEP1="\"$1\"",SEP2="\"$2\"""
}
###############################################################################
## DEBUT DU PROGRAMME
###############################################################################

finit_variables $0
fanalyze_parameters $*
if [[ ${HELP} -eq 1 ]]
then
     fdisplay_help
     exit 0
fi
fcheck_parameters
LD_INSTANCENAME=$(fld_instancename)
printf "LD_INSTANCENAME=$LD_INSTANCENAME\n"
if [[ ${ORAENV} -ne 1 ]]
then
   fenv
else
   foraenv
fi
CONNECTSTRING=$(fconnectstring)
printf "CONNECTSTRING=$CONNECTSTRING\n"
fcheckconnect
ORAVERS=$(foravers)
printf "ORAVERS=$ORAVERS\n"
DAY=$(fday)
printf "DAY=$DAY\n"
WEEKDAY=$(fweekday)
printf "WEEKDAY=$WEEKDAY\n"
DBID=$(fdbid)
printf "DBID=$DBID\n"
INSTANCENUMBER=$(finstancenumber)
printf "INSTANCENUMBER=$INSTANCENUMBER\n"
STDBYUNIQUENAME=$(fstdbyuniquename)
printf "STDBYUNIQUENAME=$STDBYUNIQUENAME\n"
DBNAME=$(fdbname)
printf "DBNAME=$DBNAME\n"
if [[ ${GLOBAL} -ne 1 ]]
then
   if [[ ${STDBY} -ne 1 ]]
   then
     PREFIX=$DIR/kairos_${GROUP}_${LD_INSTANCENAME}_${WEEKDAY}
   else
     PREFIX=$DIR/kairos_${GROUP}_${STDBYINSTANCENAME}_${WEEKDAY}
   fi
else
     PREFIX=$DIR/kairos_${GROUP}_${DBNAME}_${WEEKDAY}
fi
printf "PREFIX=$PREFIX\n"
if [[ ${ORAVERS} = "10.1" ]]
then
     FORMAT=text
elif [[ ${ORAVERS} = "10.2" ]]
then
     FORMAT=text
else
     FORMAT=html
fi
TEMPFILE=$PREFIX.tar
fversion
if [[ ${AWR} -ne 1 ]]
then
     if [[ ${STDBY} -ne 1 ]]
     then
          fstatspack
     else
          fstatspackstandby
     fi
else
     if [[ ${GLOBAL} -ne 1 ]]
     then
          fawr $LVL
     else
          fawrglobal
     fi
fi
if [[ ${BASH} -eq 1 ]]
then
     fbash
fi
if [[ ${LD_INSTANCENAME} = ${INSTANCENAME} ]]
then
     if [[ ${SAR} -eq 1 ]]
     then
          fsar
     fi
     if [[ "${NMON}" != "0" ]]
     then
          fnmon $TOPAS
     fi
fi
finalize_output
