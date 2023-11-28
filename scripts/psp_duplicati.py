import os
import csv
import oracledb
import numpy as np


connection = oracledb.connect(
    dsn=os.environ['SPRING_DATASOURCE_HOST'],
    port=int(os.environ['SPRING_DATASOURCE_PORT']),
    user=os.environ['SPRING_DATASOURCE_USERNAME'],
    password=os.environ['SPRING_DATASOURCE_PASSWORD']
)
print("Successfully connected to Oracle Database")


print("Executing query...")
cursor = connection.cursor()
cursor.execute("""
-- PSP duplicati diretti
select distinct PSP.ID_PSP, PSP.CODICE_FISCALE
from PSP,
     CANALE_TIPO_VERSAMENTO,
     CANALI,
     PSP_CANALE_TIPO_VERSAMENTO
WHERE CANALI.OBJ_ID = CANALE_TIPO_VERSAMENTO.FK_CANALE
  and PSP_CANALE_TIPO_VERSAMENTO.FK_PSP = PSP.OBJ_ID
  and PSP_CANALE_TIPO_VERSAMENTO.FK_CANALE_TIPO_VERSAMENTO = CANALE_TIPO_VERSAMENTO.OBJ_ID
  and CANALI.ID_CANALE like concat(PSP.CODICE_FISCALE, '_%')
  and PSP.OBJ_ID in (select PSP.OBJ_ID
                     from NODO4_CFG.PSP
                     where PSP.CODICE_FISCALE in (select PSP.CODICE_FISCALE
                                                  from NODO4_CFG.PSP
                                                  group by PSP.CODICE_FISCALE
                                                  having count(*) > 1));
""")

res = cursor.fetchall()
a = np.asarray(res)
np.savetxt('./psp_diretti.csv', a, delimiter=',', fmt='%s')


cursor.execute("""
-- PSP duplicati diretti
select distinct PSP.ID_PSP, PSP.CODICE_FISCALE
from PSP,
     CANALE_TIPO_VERSAMENTO,
     CANALI,
     PSP_CANALE_TIPO_VERSAMENTO
WHERE CANALI.OBJ_ID = CANALE_TIPO_VERSAMENTO.FK_CANALE
  and PSP_CANALE_TIPO_VERSAMENTO.FK_PSP = PSP.OBJ_ID
  and PSP_CANALE_TIPO_VERSAMENTO.FK_CANALE_TIPO_VERSAMENTO = CANALE_TIPO_VERSAMENTO.OBJ_ID
  and CANALI.ID_CANALE not like concat(PSP.CODICE_FISCALE, '_%')
  and PSP.OBJ_ID in (select PSP.OBJ_ID
                     from NODO4_CFG.PSP
                     where PSP.CODICE_FISCALE in (select PSP.CODICE_FISCALE
                                                  from NODO4_CFG.PSP
                                                  group by PSP.CODICE_FISCALE
                                                  having count(*) > 1));
""")

res = cursor.fetchall()
a = np.asarray(res)
np.savetxt('./psp_indiretti.csv', a, delimiter=',', fmt='%s')

cursor.close()
connection.close()
