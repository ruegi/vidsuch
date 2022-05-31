import vidarchdb
import datetime

vidarchdb.dbconnect()

vidarchdb.set_config("letzterSync", datetime.datetime.now())


