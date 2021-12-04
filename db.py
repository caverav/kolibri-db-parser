#!/usr/bin/env python3
import sqlite3

conn = sqlite3.connect('databases/8b6ea1c2fd8754209845311625a7d8e9.sqlite3')

c = conn.cursor()
c.execute("SELECT title FROM content_contentnode")
res = c.fetchall()
for i in range(len(res)):
    print("["+str(i)+"]"+res[i][0])
inn = int(input("Ingrese el número del documento que desea buscar: "))
# print the local_file_id of the content node
c.execute("SELECT id FROM content_contentnode WHERE title = '" + res[inn][0]+"'")
res = c.fetchall()
if c.execute("SELECT local_file_id FROM content_file WHERE contentnode_id = \"" + str(res[0][0])+"\" AND preset NOT LIKE '%thumbnail%'"):
    rec = c.fetchall()[0][0]
    print("El recurso se encuentra en storage/" +str(rec[0]) + "/" + str(rec[1]) + "/" + str(rec))
if c.execute("SELECT local_file_id FROM content_file WHERE contentnode_id = \"" + str(res[0][0])+"\" AND preset LIKE '%thumbnail%'"):
    thumb = c.fetchall()[0][0]
    print("La miniatura se encuentra en storage/" +str(thumb[0]) + "/" + str(thumb[1]) + "/" + str(thumb))


