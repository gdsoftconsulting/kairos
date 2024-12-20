from pykairos.vdollartemplate import UserObject as Template
class UserObject(Template):

    def __init__(self):
        Template.ID = 'derived_from_vdollartemplate'
        Template.INCLUDEINPATH = False
        Template.IPADDRESS = 'localhost'
        Template.PORT = '1521'
        Template.CONTAINER = 'ORCLCDB'
        Template.USER = 'system'
        Template.PASSWORD = 'manager'
    
        Template.MINDATE = "select to_char(sysdate - 1, 'YYYYMMDDHH24MISS') as mindate from dual"
        Template.MAXDATE = "select to_char(sysdate, 'YYYYMMDDHH24MISS') as maxdate from dual"
        Template.RETENTION = 300
        super(UserObject, self).__init__()
