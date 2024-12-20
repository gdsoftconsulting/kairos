Within this directory, a lot of scripts to collect Oracle data on production systems. The result is a zip or a tar.gz file to be uploaded into Kairos

## Data collection for Oracle

Starting from Oracle version 10 and upper, there are AWR and ASH availables but they must be used only if the the pack "Oracle diagnostic pack" has been bought by the customer.

So KAIROS can collect data above AWR and ASH if the customer has the right to use them, but KAIROS can collect data above STATSPACK and another Free Software (B-ASH, see https://marcusmonnig.wordpress.com/bash/) if the customer doesn't have the right to use "Oracle diagnostic pack".

There are 2 ways to collect Oracle data for KAIROS:

a) through a provided Korn-shell script: kairosora.ksh
b) through a python script runnable under JYTHON (Preferred method when available)

#### Oracle Data Collection for Kairos with kairosora.ksh

The script must be transfered to a system where the Oracle Database resides. Some Oracle installations don't use the "oraenv" mechanism to switch between Oracle contexts.

If "oraenv" is used, it's better tu use the collect script with the flag "-oraenv".

If "oraenv" isn't used or doesn't work for any reason, the Oracle data collection script for KAIROS must be used when the Oracle context has been setup manually.

Oracle data Collection when AWR is allowed

The general form of the command to be run to capture a day of activity is:

```
ksh /TOOLDIR/kairosora.ksh -sid:MYINSTANCE -day:YYYY-MM-DD -awr -lvl:3 -zip -grp:GGGG -dir:DDDD
```

where

TOOLDIR is the directory in which the data collection script has been put

MYINSTANCE is the name of the Oracle instance

YYYY-MM-DD is the day to be extracted (ex : 2016-08-20 for August 2016, 20)

GGGG (not mandatory, default value UNKNOWN is a symbol identifying the company)

DDDD is the directory in which the result (tar file or zip file) will be written.


If the -day parameter is not specified, data is extracted from the day before. This is especially useful when the command is triggered through a scheduler like "cron". In this case, the same command executed every day will produce a different result each day. This is a way to automate the data collection.

Oracle data Collection when AWR is NOT allowed

In this case, the general form of the command is:

```
ksh /TOOLDIR/kairosora.ksh -sid:MYINSTANCE -day:YYYY-MM-DD -pwd:PPPP -bash -zip -grp:GGGG -dir:DDDD
```

The difference with the invocation in the AWR context is:

-awr and -lvl have been removed (meaning STATSPACK is required)

-bash is a flag to indicate that collection over B-ASH is required

PPPP is the PERFSTAT password is the case of STATSPACK. The default value is PERFSTAT.

If the PERSTAT password is not PERFSTAT and if the customer don't want to pass the password as an argument of the command, the default password must be changed in the provided KAIROS script.

#### Oracle Data Collection for Kairos with kairosora.py

This method supposes that JAVA is available on the system where the collect must be done.

Steps to be realized:

###### a) find a java executable

```
find / -name 'java' 2> /dev/null
```
Several lines can be displayed. Example:

```
/etc/pki/java
/etc/pki/ca-trust/extracted/java
/oracle/12.2.0/jdk/bin/java
/oracle/12.2.0/jdk/jre/bin/java
/oracle/12.2.0/xdk/doc/java
/oracle/12.2.0/OPatch/jre/bin/java
```

The third line (/oracle/12.2.0/jdk/bin/java) seems to be a good candidate...

Check the java version like this:

```
/oracle/12.2.0/jdk/bin/java -version
```

Something like the following result will be displayed:

```
java version "1.8.0_91"
Java(TM) SE Runtime Environment (build 1.8.0_91-b14)
Java HotSpot(TM) 64-Bit Server VM (build 25.91-b14, mixed mode)
```

###### b) find an "ojdbc.jar" file 

```
find / -name '*ojdbc*jar' 2> /dev/null
```

An example of result:

```
/oracle/12.2.0/suptools/tfa/release/tfa_home/jlib/ojdbc5.jar
/oracle/12.2.0/jdbc/lib/ojdbc8dms.jar
/oracle/12.2.0/jdbc/lib/ojdbc8dms_g.jar
/oracle/12.2.0/jdbc/lib/ojdbc8.jar
/oracle/12.2.0/jdbc/lib/ojdbc8_g.jar
/oracle/12.2.0/sqldeveloper/sqlcl/lib/ojdbc7.jar
/oracle/12.2.0/sqldeveloper/jdbc/lib/ojdbc7.jar
/oracle/12.2.0/md/property_graph/lib/ojdbc7.jar
/oracle/12.2.0/dmu/jlib/ojdbc6.jar
/oracle/12.2.0/inventory/Scripts/ext/jlib/ojdbc8.jar
/oracle/12.2.0/inventory/Scripts/ext/jlib/._ojdbc8.jar
/oracle/12.2.0/inventory/backup/2017-10-10_04-21-57PM/Scripts/ext/jlib/ojdbc8.jar
/oracle/12.2.0/inventory/backup/2017-10-10_04-21-57PM/Scripts/ext/jlib/._ojdbc8.jar
/oracle/sqlcl/lib/ojdbc8.jar
```
ojdbc6.jar or ojdbc8.jar are good candidates

###### c) make jython available for use

Transfer the jar file "jython-standalone.jar" to any directory (for example: /tmp)

Create an alias for jython (example)

```
alias jython='/oracle/12.2.0/jdk/bin/java -classpath /tmp/jython-standalone.jar:/oracle/12.2.0/jdbc/lib/ojdbc8.jar org.python.util.jython'
```

This alias is made of several things:
a) it contains the full path to the "JAVA" executable
b) it contains the full path of "JYTHON" jar file
c) it contains the full path of "OJDBC" jar file

Check that jython is available:

```
jython
```

The following result should be displayed:

```
Jython 2.7.0 (default:9987c746f838, Apr 29 2015, 02:25:11) 
[Java HotSpot(TM) 64-Bit Server VM (Oracle Corporation)] on java1.8.0_91
Type "help", "copyright", "credits" or "license" for more information.
>>> 
```

###### d) copy kairosora.py to the target system and check the available options

kairosora.py can be transfered anywhere (for example /tmp)

```
jython kairosora.py -h   
usage: kairosora.py [-h] [--version] [--awr] [--host HOST] [--port PORT]
                    [--service SERVICE] [--user USER] [--password PASSWORD]
                    [--instance INSTANCE] [--level LEVEL] [--from FROM]
                    [--to TO] [--directory DIRECTORY] [--bash]

optional arguments:
  -h, --help            show this help message and exit
  --version             show program's version number and exit
  --awr                 True: AWR extract, False: STATSPACK extract
  --host HOST           Host to connect to using SQL*Net. Default: current
                        host name
  --port PORT           Port number. Default 1521
  --service SERVICE     Service to connect to. Default: value of ORACLE_SID
  --user USER           Schema from which STATSPACK data is extracted.
                        Default: PERFSTAT
  --password PASSWORD   PERFSTAT schema password in case of STATSPACK, SYS
                        password in case of AWR
  --instance INSTANCE   Instance from which to retrieve data. Default: value
                        of ORACLE_SID
  --level LEVEL         Level 1: Extract AWR, level 2: Detailed info on
                        requests, level 3: ASH
  --from FROM           Extract data generated from this date
  --to TO               Extract data generated until this date
  --directory DIRECTORY
                        Directory to store the result. Default: /tmp
  --bash                True: B-ash extract
  ```

At this point, the extraction can be realized.

###### e) perform the extraction 

With this method (python script with jython), data extraction is not necessarily done on the target system where the database resides.
It can be done on any system with an Oracle client installed if java is available and if the target database can be reached through SQL*Net.

Examples of use with STATSPACK

```
jython kairosora.py --password PERFSTAT
```

In this case, you are adressing the current host and the Oracle instance identified by environment variable ORACLE_SID. The connection to the database is done with SQL*Net through the port value = 1521. 
The target schema is PERFSTAT and the password is provided on the command line.
There are no filter on time so that everything will be captured from the PERFSTAT schema

```
jython kairosora.py --host MYHOST --port 15211 --service TARGETDB --instance ABCD --user PERFSTAT_X --password PERFSTAT_X --from YESTERDAY --to TODAY --directory /mydirectory --bash
```

In this case, you are adressing the listener hosted on MYHOST and listening on port 15211. Your requirement is to connect to the service TARGETDB with user PERFSTAT_X and password PERFSTAT_X.
You are requiring B-ASH data. You want an extract of the previous day (--from YESTERDAY and --to TODAY).
The result of the extract will be stored in the directory /mydirectory

```
jython kairosora.py --password PERFSTAT --from 2018-02-05
```

In this example, you are requiring data where snap times are greater than 2018-02-05

```
jython kairosora.py --password PERFSTAT --from "2018-02-05 08:30" --to "2018-02-05 17:30"
```

In this example, you are requiring data where snap times are between "2018-02-05 08:30" and "2018-02-05 17:30"

#### STATSPACK installation

STASTSPACK is always available in Oracle 10, 11, 12, even if all STATSPACK functionalities have been replaced by AWR.

The documentation to install and configure Statspack is available at this address: https://docs.oracle.com/cd/B10501_01/server.920/a96533/statspac.htm

For example, on UNIX:

```
SQL>  CONNECT / AS SYSDBA
SQL>  define default_tablespace='TOOLS'
SQL>  define temporary_tablespace='TEMP'
SQL>  define perfstat_password='my_perfstat_password'
SQL>  @?/rdbms/admin/spcreate
```

We suggest to use SYSAUX as the default tablespace.

To automate the production of snapshots, the SPAUTO script must be used. The default value of one hour between each snapshot is enough if B-ASH is used in addition.

```
SQL>  CONNECT perfstat/my_perfstat_password
SQL>  @?/rdbms/admin/spauto
````

#### B-ASH installation

The package to install and configure B-ASH is provided in attachment.

Within the zip archive, there is a bashcreate_V8.sql to be run to activate B-ASH. In the header of the script there are comments to use the script.

We suggest to use SYSAUX as the default tablespace and start the B-ASH data collector immediately.

Once bashcreate_v8.sql has been completed, open a sql*plus session under bash/password_of_bash and issue the following request:

```
grant select on bash$hist_active_sess_history to perfstat;
```

B-ASH installation must be done after STATSPACK installation
