#!/usr/bin/env python3
import sqlite3
import sys
import csv

if len(sys.argv) != 2:
    print("Uso: kolibri-conversor-base-de-datos.py <base de datos>")
    sys.exit(1)

# CONEXION A LA BASE DE DATOS
db = str(sys.argv[1].strip())
conn = sqlite3.connect(db)
c = conn.cursor()


# CREACION DEL CSV

# Columnas
fieldnames = ['id', 'title', 'content_id', 'channel_id', 'description', 'sort_order', 'license_owner', 'author', 'kind', 'available', 'lft', 'rght', 'tree_id', 'level', 'lang_id', 'license_description', 'license_name', 'coach_content', 'num_coach_contents', 'on_device_resources', 'options', 'parent_id', 'local_file_id', 'local_file_id_thumb', 'parents', 'tags']

with open('content_contentnode.tsv', 'w', newline='') as csvfile:

    # Creacion del archivo
    csvwriter = csv.writer(csvfile, delimiter='\t')
    csvwriter.writerow(fieldnames)


    # Conexión auxiliar
    conn2 = sqlite3.connect(db)
    c2 = conn2.cursor()
    cnt = 0
    # Iterar por cada fila de content_contentnode
    for row in c.execute('SELECT * FROM content_contentnode'):

        # Mostrar el progreso
        flag = True
        if cnt % 4050 == 0 or cnt == 40401:
            print(str(round((cnt/40401)*100))+"%")
        cnt+=1

        # local file id
        local_file_id = c2.execute('SELECT local_file_id FROM content_file WHERE contentnode_id = "' + str(row[0]) + '" AND thumbnail = 0').fetchone()
        local_file_id_thumb = c2.execute('SELECT local_file_id FROM content_file WHERE contentnode_id = "' + str(row[0]) + '" AND thumbnail = 1').fetchone()

        if not (local_file_id is None):
            local_file_id = local_file_id[0]

        if not (local_file_id_thumb is None):
            local_file_id_thumb = local_file_id_thumb[0]

        # parent_id
        parent_id_str = ''
        parent_id = c2.execute('SELECT parent_id FROM content_contentnode WHERE id = "' + str(row[0]) + '"').fetchone()[0]
        if parent_id is None:
            flag = False
            parent_id_str = ''
        else:
            parent_id_str += str(parent_id)
            parent_id = c2.execute('SELECT title FROM content_contentnode WHERE id = "' + str(parent_id) + '"').fetchone()[0]
            while flag:
                parent_id = c2.execute('SELECT title FROM content_contentnode WHERE id = "' + str(parent_id).replace('\"', '\'') + '"').fetchone()
                if parent_id is not None:
                    parent_id = parent_id[0]
                    if parent_id == parent_id_str:
                        parent_id = ''
                        continue
                    else:
                        parent_id_str += '|' + str(parent_id)
                else:
                    flag = False


        # Revertir el orden de los padres
        parent_id_str = parent_id_str.split('|')
        parent_id_str.reverse()
        parent_id_str = '|'.join(parent_id_str)


        # tags
        tags = c2.execute('SELECT contenttag_id FROM content_contentnode_tags WHERE contentnode_id = "' + str(row[0]) + '"').fetchall()

        # obtener los nombres de las tags
        tags_str = ''
        for tag in tags:
            tag_name = c2.execute('SELECT tag_name FROM content_contenttag WHERE id = "' + str(tag[0]) + '"').fetchone()[0]
            tags_str += tag_name + '|'
        if len(tags_str) > 0 and tags_str[-1] == '|':
            tags_str = tags_str[:-1]
        # escribir la fila en el csv
        csvwriter.writerow(tuple(list(row)+[local_file_id]+[local_file_id_thumb]+[parent_id_str]+[tags_str]))

# cerrar conexiones y archivos
conn.close()
conn2.close()
csvfile.close()
