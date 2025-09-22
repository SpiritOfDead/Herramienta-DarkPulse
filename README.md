# DarkPulseV11: Herramienta de Ciberseguridad Ofensiva ⚡️

Una potente herramienta en Python diseñada para automatizar el reconocimiento de red, el escaneo de vulnerabilidades y la explotación de sistemas. **DarkPulseV11** utiliza Nmap y Metasploit para identificar y comprometer objetivos, proporcionando a los pentesters una solución eficiente para evaluar la seguridad de la red.

## Preview
```python
# ¡Así es como se ve DarkPulseV11 al inicio!
---------------------------------------------------------------------
  __                     __  
____/ /_  ___  ____  _   __/ /_  ___  __  
/ __  / / / / |/_/ / / | / / __ \/ _ \/ / /
/ /_/ / /_/ />  </ / /| |/ / /_/ /  __/ /_/ 
\__,_/\__,_/_/\_\/_/_/ |_/ /_.___/\___/\__, /
                                   /____/
---------------------------------------------------------------------
      ⚡️ DarkPulseV11: Escáner de Red y Explotación ⚡️
      🔓 Buscando vulnerabilidades | Creado por: SpiritNetGhost 🔍
---------------------------------------------------------------------

## Primeros Pasos

Para obtener una copia de la herramienta DarkPulse, clona el repositorio a tu máquina local:

#habre tu terminal:
#bash
git clone [https://github.com/SpiritOfDead/Herramienta-DarkPulse.git](https://github.com/SpiritOfDead/Herramienta-DarkPulse.git)

-------------------------------------------------------------------------------------------------------------------------------------------------
⚠️ Advertencia: Uso con Fines Educativos y Éticos ⚠️

Esta herramienta, DarkPulseV11, ha sido creada exclusivamente para fines educativos y de investigación. Su propósito es ayudar a estudiantes y profesionales a comprender mejor los procesos de escaneo, análisis de vulnerabilidades y pruebas de penetración en entornos controlados y autorizados.

Queda estrictamente prohibido su uso en sistemas, redes o dispositivos de los que no seas propietario o para los que no tengas un permiso explícito por escrito del dueño.

El desarrollador no se hace responsable por el uso malintencionado, ilegal o no autorizado de esta herramienta. Al descargar y utilizar este software, el usuario asume toda la responsabilidad de sus acciones y se compromete a utilizarlo de manera ética y legal.
--------------------------------------------------------------------------------------------------------------------------------------------------------------
. Requisitos de Software

    Python: El script está escrito en Python 3, por lo que debes tenerlo instalado en tu sistema. Puedes verificarlo con el comando python3 --version.

    Nmap: La herramienta utiliza Nmap para los escaneos de red. Asegúrate de tenerlo instalado y accesible desde la línea de comandos. Puedes descargarlo desde nmap.org.

    Metasploit Framework: Para la fase de explotación, es indispensable tener una instalación de Metasploit Framework y un servidor RPC en ejecución. Puedes obtenerlo con la instalación de Kali Linux o a través de su sitio oficial.

2. Librerías de Python

El script depende de varias librerías de Python que no vienen por defecto. Puedes instalarlas todas de una vez usando pip:
Bash

pip install requests python-nmap

    requests: Se usa para realizar las consultas a la API de Vulners.com.

    python-nmap: Es la librería que permite al script interactuar con Nmap.

Además, para que la función de explotación funcione, necesitas la librería python-msfrpc. Aunque el script puede ejecutarse sin ella, la funcionalidad de Metasploit no estará disponible.
Bash

pip install python-msfrpc

3. Configuración Adicional

    API de Vulners.com: El script realiza búsquedas de vulnerabilidades a través de su API. Aunque no se requiere una clave para las consultas básicas, es importante que tengas conexión a internet para que esta funcionalidad trabaje.

    Servidor Metasploit RPC: Antes de ejecutar el script, debes iniciar el servicio de Metasploit RPC. Esto permite que el script se conecte a Metasploit de forma remota para ejecutar los exploits. Puedes iniciar el servidor RPC con un comando similar a este:

Bash

msfconsole -x "load msgrpc ServerPassword=micontraseña"

Nota: El script está configurado para conectarse con la contraseña que establezcas en el comando de ejecución.

Cómo Ejecutar el Script

Una vez que tengas todos los requisitos, puedes ejecutar la herramienta con el siguiente comando, asegurándote de proporcionar el rango de IP objetivo y la contraseña de Metasploit RPC:

Bash
-------------------------------------------------------------------------------------
python DarkPulseV1.py --rango_ip "192.168.1.0/24" --metasploit_pass "micontraseña"
---------------------------------------------------------------------------------------
metodo 2 para ejecutar el scrip:
Abrir tu terminal
dirigete a la carpeta donde esta el scrip DarkPulseV1.py
Abrir el archivo DarkPulseV1.py  con nano [nano DarkPulseV1.Py]
busca la ultima linea algo como ""darkpulse = DarkPulseV11(rango_ip="IP VICTIMA", metasploit_pass="tu_contraseña", max_threads=10)"
Agregas la IP Y GUARDAS Y VUELVES A EJECUTAR  Y LISTO.
-------------------------------------------------------------------------------------------------------------------------------------------
