# Resumen

# Clase 1: Introducción a Git y Unix/Linux

## 1. Introducción a Git y Control de Versiones
Git es un sistema de control de versiones distribuido utilizado en el desarrollo de software. Su propósito principal es rastrear cambios en archivos y facilitar la colaboración entre desarrolladores. A diferencia de otros sistemas de control de versiones centralizados, Git permite trabajar de manera descentralizada, proporcionando ventajas como mayor flexibilidad, historial completo de cambios y la posibilidad de trabajar sin conexión.

### Comandos básicos:
> git --version  # Verifica si Git está instalado  
> git config --global user.name "Tu Nombre"  # Configura el nombre de usuario  
> git config --global user.email "tuemail@example.com"  # Configura el correo electrónico  

## 2. Creación y Configuración de un Repositorio Git
Un repositorio Git es el espacio donde Git rastrea los cambios en los archivos de un proyecto. Puede ser local (en tu máquina) o remoto (en GitHub, GitLab, etc.).
Pasos para crear un repositorio local:

- Crear una carpeta para el proyecto y acceder a ella con cd.
- Inicializar Git en el directorio con:
> git init  

- Verificar el estado del repositorio con:
> git status  

## 3. Estructura del Repositorio del Curso
Organizar correctamente la estructura de un repositorio es fundamental para el mantenimiento y colaboración en el proyecto.
Estructura recomendada:

README.md  
/TP_1  
/TP_2  
/Clases  
    /Clase_1  
        /Apuntes  
        /Ejercicios  
        /Resumen_pedagógico  
...  
/TRABAJO_FINAL  

(El archivo README.md incluiye información sobre el proyecto, expectativas y objetivos de la materia.)

## 4. Flujo de Trabajo en Git
Git maneja los archivos en tres áreas principales:

- Working Directory: Archivos en la carpeta local.
- Staging Area: Archivos preparados para ser confirmados (commit).
- Repository: Donde se almacenan los commits.

### Comandos clave:
git add .  # Añade todos los cambios al área de preparación  
git commit -m "Mensaje descriptivo"  # Guarda los cambios en el historial  
git log --oneline  # Muestra el historial de commits en una línea por cada uno  

## 5. Conexión con un Repositorio Remoto
Los repositorios remotos permiten colaborar con otros desarrolladores y mantener copias de seguridad.

Pasos para conectar el repositorio local con GitHub:
- Crear un repositorio en GitHub.

- Vincularlo con el repositorio local con:
> git remote add origin https://github.com/usuario/repositorio.git  

- Subir los cambios con:
> git push -u origin main  

## 6. Conceptos Básicos de Terminal Unix/Linux
Entrada/Salida Estándar (E/S):

- stdin: Entrada estándar (teclado).
- stdout: Salida estándar (pantalla).
- stderr: Salida de errores.


### Redirección de comandos:
> comando > archivo  # Redirige la salida a un archivo (sobrescribe)  
> comando >> archivo  # Agrega la salida a un archivo sin sobrescribir  
> comando < archivo  # Toma la entrada desde un archivo  
> comando 2> archivo  # Redirige errores a un archivo  

### Uso de Pipes (|):
Los pipes permiten encadenar comandos para procesar datos.
> ls | grep "archivo"  

## 7. Ejercicios Prácticos
- Crear un repositorio Git, hacer commits y subirlos a GitHub.
- Usar redirecciones (>, >>, <, 2>) y pipes (|) en la terminal.

## Conclusión
En esta clase aprendimos los fundamentos del control de versiones con Git y la terminal de Unix/Linux. Se establecieron las bases para la gestión eficiente de proyectos, la colaboración en repositorios remotos y la manipulación de archivos mediante la línea de comandos. 

