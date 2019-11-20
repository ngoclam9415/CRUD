
import os
db_type = (os.getenv('DB_TYPE') or 'default').lower()
if db_type == "mysql":
    from database.mysql_access.AccessFactory import AccessFactory
elif db_type == "mongo":
    from database.mongo_access.AccessFactory import AccessFactory


else:
    from database.mysql_access.AccessFactory import AccessFactory

access_factory = AccessFactory()