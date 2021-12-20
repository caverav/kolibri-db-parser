# kolibri-db-parser
Procesador de base de datos en instalación de Kolibri.

## Uso

Se debe dar permisos de ejecución al programa y posteriormente ejecutarlo junto al nombre de la base de datos global de Kolibri.

```
chmod +x kolibri-conversor-base-de-datos.py
./kolibri-conversor-base-de-datos.py <nombre de base de datos>
```
![image](https://user-images.githubusercontent.com/66751764/146845476-890cecbd-ba19-48bb-9858-252bf9dcd744.png)

## Consideraciones adicionales

El archivo CSV generado tendrá las siguientes columnas:

```
id, title, content_id, channel_id, description, sort_order, license_owner, author, kind, available, lft, rght, tree_id, level, lang_id, license_description, license_name, coach_content, num_coach_contents, on_device_resources, options, parent_id, local_file_id, local_file_id_thumb, parents, tags
```

Respecto a las dos últimas (parents y tags) hay un par de consideraciones:

__parents:__ estará en el formato *p1/p2/p3/p4*, donde p1 es el padre principal y p4 es el padre directo del nodo/recurso actual, en caso de no tener padre estará vacío

__tags:__ estará en el formato *tag1/tag2/tag3*, el orden es el mismo de la base de datos, en caso de no tener también estará vacío

