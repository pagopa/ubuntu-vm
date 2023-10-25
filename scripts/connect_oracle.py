import os
import csv
import oracledb


connection = oracledb.connect(
    dsn="db-nodo-pagamenti.d.db-nodo-pagamenti.com/NDPSPCT_PP_NODO4_CFG",
    port=1522,
    user=os.environ['SPRING_DATASOURCE_USERNAME'],
    password=os.environ['SPRING_DATASOURCE_PASSWORD']
)
print("Successfully connected to Oracle Database")


with open('psp.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    values = []
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            tax_code = row[8]
            psp_codes = row[2]
            for psp_code in psp_codes.split(','):
                print(f'\t PSP {psp_code} set taxcode {tax_code}')
                line_count += 1
                values.append((tax_code, psp_code))

    print("Executing query...")
    cursor = connection.cursor()
    cursor.prepare("UPDATE NODO4_CFG.PSP  SET PSP.CODICE_FISCALE= :1  WHERE PSP.ID_PSP = :2")
    cursor.executemany(None, values)
    connection.commit()

    print(f'Processed {line_count} lines.')

connection.close()
print("Done")
