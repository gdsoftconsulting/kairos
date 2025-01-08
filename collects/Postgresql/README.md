Within this directory, a lot of scripts to collect data on production systems. The result is a zip or a tar.gz file to be uploaded into Kairos

## Data collection for PostgreSQL

In the PostgreSQL universe, data collection is done by adding an extension to a PostgreSQL database.

The software is delivered as  a "tar" archive. The name is "pgkairos.tar". This tar file must be copied on a system where PostgreSQL is running for exemple in the "/tmp" directory. From there, the administrator has to identify the directory where extensions are stored.

To identify the directory where the extension must be installed, run the following command:

```
$ psql -c "create extension very_improbable_name"
ERROR:  could not open extension control file "/usr/share/postgresql/9.5/extension/very_improbable_name.control": No such file or directory
```

The error message indicates the directory where the tar file must be extracted. In this example: "/usr/share/postgresql/9.5/extension"

So to install properly this PostgreSQL extension you have to:

```
$ cd /usr/share/postgresql/9.5/extension
$ tar xvf /tmp/pgkairos.tar
```

After that step, the extension is available. You can check the availability by running:

```
$ psql -c "select * from pg_available_extensions" | grep kairos
```

This extension must be then created in a new PostgreSQL database named "kairos"

```
$ psql -c "create database kairos"
$ psql -d kairos -c "create extension kairos"
$ psql -d kairos -c "\dp"
```

The last command lists all tables created through the extension. An exmaple of the list is:

```
                                      Access privileges
 Schema |          Name           | Type  | Access privileges | Column privileges | Policies 
--------+-------------------------+-------+-------------------+-------------------+----------
 public | config                  | table |                   |                   | 
 public | kairos_pg_stat_activity | table |                   |                   | 
 public | kairos_sql_text         | table |                   |                   | 
(3 rows)

```

From there, the extension is operational. A lot of functions are available to collect, purge or export data.

The "config" table keeps in mind the global parameters to control this process:

```
$ psql -d kairos -c "select * from config"
   param   | value 
-----------+-------
 enable    | true
 retention | 15.0
 directory | /tmp
(3 rows)
```

The kairos extension collects statistics if the "enable" poarameter is set to "true". Controlling the "enable" parameter allows to enable or disable the collect of statistics

The "retention" parameter specifies the number of days statistics are retained in the kairos database. When the purge is activated, it removes data older than "retention" days.

The "directory" parameter specifies the directory in which "exports" are generated.

All parameters of the config table can be read using the "get_param" function.
