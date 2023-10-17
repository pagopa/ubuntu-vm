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
mapping = []
i = 0
sqlQuery = str("""
                    SELECT 
	                    p.ID_PSP,
	                    p.ABI
                    FROM 
	                    NODO4_CFG.PSP p
                    WHERE 
                        p.ID_PSP NOT LIKE '%CHARITY%'
                    ORDER BY p.ID_PSP
                   """)

for row in cursor.execute(sqlQuery):
    mapping.append(row)
    i += 1

connection.close()

print("Found {} bundles that match the query".format(i))
