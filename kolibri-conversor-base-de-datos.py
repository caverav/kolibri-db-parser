#!/usr/bin/env python3
import sqlite3
import sys

if len(sys.argv) != 2:
    print("Uso: kolibri-conversor-base-de-datos.py <base de datos>")
    sys.exit(1)

# CONEXION A LA BASE DE DATOS
db = str(sys.argv[1].strip())
conn = sqlite3.connect(db)
c = conn.cursor()


# CREACION DEL CSV
import csv
fieldnames = ['id', 'title', 'content_id', 'channel_id', 'description', 'sort_order', 'license_owner', 'author', 'kind', 'available', 'lft', 'rght', 'tree_id', 'level', 'lang_id', 'license_description', 'license_name', 'coach_content', 'num_coach_contents', 'on_device_resources', 'options', 'parent_id', 'local_file_id', 'local_file_id_thumb']
with open('content_contentnode.csv', 'w', newline='') as csvfile:
    csvwriter = csv.writer(csvfile)
    csvwriter.writerow(fieldnames)
    conn2 = sqlite3.connect(db)
    c2 = conn2.cursor()
    c = conn.cursor()
    for row in c.execute('SELECT * FROM content_contentnode'):
        local_file_id = c2.execute('SELECT local_file_id FROM content_file WHERE contentnode_id = "' + str(row[0]) + '" AND thumbnail = 0').fetchone()
        local_file_id_thumb = c2.execute('SELECT local_file_id FROM content_file WHERE contentnode_id = "' + str(row[0]) + '" AND thumbnail = 1').fetchone()
        print("Row: ")
        print(row)
        print("Local_file_id: ")
        if local_file_id is None:
            print("None")
        else:
            print(local_file_id[0])
            local_file_id = local_file_id[0]
        if local_file_id_thumb is None:
            print("None")
        else:
            print(local_file_id_thumb[0])
            local_file_id_thumb = local_file_id_thumb[0]
        csvwriter.writerow(tuple(list(row)+[local_file_id]+[local_file_id_thumb]))

conn.close()
conn2.close()
csvfile.close()

# c.execute("SELECT id FROM content_contentnode WHERE title = '" + res[inn][0]+"'")
# res = c.fetchall()
# if c.execute("SELECT local_file_id FROM content_file WHERE contentnode_id = \"" + str(res[0][0])+"\" AND preset NOT LIKE '%thumbnail%'"):
#     rec = c.fetchall()[0][0]
#     print("El recurso se encuentra en storage/" +str(rec[0]) + "/" + str(rec[1]) + "/" + str(rec))
# if c.execute("SELECT local_file_id FROM content_file WHERE contentnode_id = \"" + str(res[0][0])+"\" AND preset LIKE '%thumbnail%'"):
#     thumb = c.fetchall()[0][0]
#     print("La miniatura se encuentra en https://truful.newtenberg.com/kolibri/content/storage/" +str(thumb[0]) + "/" + str(thumb[1]) + "/" + str(thumb))



