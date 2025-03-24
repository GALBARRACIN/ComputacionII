### 6. Conceptos de Entrada/Salida en Unix/Linux
1- Crea un archivo de texto con la salida de un comando:
> ls > lista_archivos.txt

2- Agrega contenido sin sobrescribir:
> echo "Nuevo contenido" >> lista_archivos.txt

3- Redirige errores a un archivo:
> ls /carpeta_inexistente 2> error.log

4- Usa un pipe para filtrar resultados:
> ls | grep "archivo"
