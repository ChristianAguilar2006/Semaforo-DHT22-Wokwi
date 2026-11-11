import time
import math
from pathlib import Path

import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
import serial

URL = "rfc2217://localhost:4000"
BAUDIOS = 9600
MUESTRAS = 500
CARPETA = Path(__file__).resolve().parent
ARCHIVO_DATOS = CARPETA / "data.txt"
ARCHIVO_GRAFICAS = CARPETA / "graficas.png"

tiempos = []
temperaturas = []
humedades = []

plt.ion()
fig, (ax_temp, ax_hum) = plt.subplots(2, 1, figsize=(9, 7))
fig.tight_layout(pad=3)
plt.show(block=False)

try:
    with serial.serial_for_url(URL, baudrate=BAUDIOS, timeout=0.1) as conexion, \
            ARCHIVO_DATOS.open("w", encoding="utf-8") as datos:
        print("Conectado. Esperando lecturas del simulador...")
        datos.write("muestra,tiempo_s,temperatura_c,humedad_pct\n")
        inicio = time.monotonic()
        pendiente = b""
        # La conexión puede empezar a mitad de una línea.
        primera_linea = True

        while plt.fignum_exists(fig.number) and len(temperaturas) < MUESTRAS:
            # Conserva los fragmentos hasta recibir un salto de línea.
            pendiente += conexion.read(256)
            while b"\n" in pendiente and len(temperaturas) < MUESTRAS:
                linea, pendiente = pendiente.split(b"\n", 1)
                if primera_linea:
                    primera_linea = False
                    continue
                partes = linea.decode("utf-8", errors="replace").strip().split(",")
                if len(partes) != 2:
                    continue
                try:
                    temperatura = float(partes[0])
                    humedad = float(partes[1])
                except ValueError:
                    continue
                if not (math.isfinite(temperatura) and math.isfinite(humedad)):
                    continue

                tiempos.append(time.monotonic() - inicio)
                temperaturas.append(temperatura)
                humedades.append(humedad)
                datos.write(f"{len(temperaturas)},{tiempos[-1]:.2f},"
                            f"{temperatura:.2f},{humedad:.2f}\n")
                datos.flush()
                print(f"[{len(temperaturas)}/{MUESTRAS}] "
                      f"Temperatura: {temperatura:.2f} °C | "
                      f"Humedad: {humedad:.2f} %", flush=True)

                ax_temp.clear()
                ax_temp.plot(tiempos, temperaturas, "r.-")
                ax_temp.set_title(f"Temperatura ({len(temperaturas)} muestras)")
                ax_temp.set_ylabel("Temperatura (°C)")
                ax_temp.grid(True)

                ax_hum.clear()
                ax_hum.plot(tiempos, humedades, "b.-")
                ax_hum.set_title(f"Humedad relativa ({len(humedades)} muestras)")
                ax_hum.set_xlabel("Tiempo transcurrido (s)")
                ax_hum.set_ylabel("Humedad relativa (%)")
                ax_hum.grid(True)
                fig.canvas.draw_idle()

            if len(pendiente) > 4096:
                pendiente = b""  # Descarta un fragmento inesperadamente largo.
            plt.pause(0.05)

    if temperaturas:
        fig.savefig(ARCHIVO_GRAFICAS, dpi=150)
        print(f"Se guardaron {len(temperaturas)} lecturas en {ARCHIVO_DATOS.name} "
              f"y las gráficas en {ARCHIVO_GRAFICAS.name}.")
    if len(temperaturas) >= MUESTRAS:
        print("Captura completa. Cierra la ventana de las gráficas para terminar.")
        plt.ioff()
        plt.show()

except KeyboardInterrupt:
    print("Lectura detenida por el usuario.")
except serial.SerialException as error:
    print(f"No se pudo conectar al simulador: {error}")
finally:
    plt.close(fig)
    print("Programa finalizado.")
