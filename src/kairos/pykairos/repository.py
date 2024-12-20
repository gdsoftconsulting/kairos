#    This file is part of Kairos.
#
#    Kairos is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    Kairos is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with Kairos.  If not, see <http://www.gnu.org/licenses/>.
#
import json, psycopg2, psycopg2.extensions, psycopg2.extras
from datetime import datetime
from loguru import logger

class Repository:

    def __init__(self, db=None):
        self.database = db
        postgresstr = f"host='localhost' user='postgres' dbname='{db}'" if db != None else "host='localhost' user='postgres'"
        self.postgres = psycopg2.connect(postgresstr)
        self.cursor =  self.postgres.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        self.setschema()
        self.postgres.set_isolation_level(psycopg2.extensions.ISOLATION_LEVEL_AUTOCOMMIT)
    
    def setschema(self, schema=None):
        self.schema = 'public' if schema == None else schema
        self.execute(f'set search_path={self.schema}')

    def execute(self,*req):
        logger.debug(f'Database: {self.database}, schema: {self.schema}, request: {req[0]}')
        self.cursor.execute(*req)
        return self.cursor

    def executep(self,req,prm):
        logger.debug(f'Database: {self.database}, schema: {self.schema}, request: {req}')
        c = self.postgres.cursor()
        c.execute(req, prm)
        return c

    def copy(self, buffer, table, description):
        logger.debug(f'Database: {self.database}, schema: {self.schema}, copy into: {table} using: {description}')
        c = self.postgres.cursor()
        c.copy_from(buffer, table.lower(), columns=description)

    def exists(self, table):
        result = False
        x = self.execute(f"select 1 from information_schema.tables where table_schema = '{self.schema}' and table_name = '{table}'")
        for _ in x.fetchall(): result = True
        return result

    def disconnect(self):
        self.cursor.close()
        self.postgres.close()
