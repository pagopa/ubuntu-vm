import os

import oracledb

connection = oracledb.connect(
    dsn="db-nodo-pagamenti.d.db-nodo-pagamenti.com/NDPSPCT_PP_NODO4_CFG",
    port=1522,
    user=os.environ['SPRING_DATASOURCE_USERNAME'],
    password=os.environ['SPRING_DATASOURCE_PASSWORD']
)

print("Successfully connected to Oracle Database")

print("Creating cursor...")
cursor = connection.cursor()
print("Cursor created")

print("Executing query...")
sqlQuery = str("""
                    UPDATE NODO4_CFG.PSP
                    SET  NODO4_CFG.PSP='ABC'
                    WHERE NODO4_CFG.PSP.ID_PSP = 'JACOPO'
                   """)

cursor.execute(sqlQuery)
connection.close()

print("Done")
