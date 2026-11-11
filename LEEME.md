# Taller de temperatura y humedad

Semáforo con sensor DHT22 y pulsador en un Arduino UNO simulado en Wokwi. Las lecturas se capturan con RealTerm y con Python, que además genera las gráficas.

## Requisitos

Necesitas instalar todo lo siguiente. No hace falta un Arduino ni un sensor físico.

| Herramienta | Para qué se usa | Descarga |
|---|---|---|
| Visual Studio Code (o Cursor) | Abrir el proyecto y correr la simulación | [code.visualstudio.com](https://code.visualstudio.com/) |
| Extensión **Wokwi Simulator** | Simular el Arduino, el DHT22 y el semáforo. Requiere cuenta de Wokwi y licencia | [Marketplace](https://marketplace.visualstudio.com/items?itemName=Wokwi.wokwi-vscode) |
| Arduino IDE 2 | Compilar el código y generar el `.hex` | [arduino.cc/en/software](https://www.arduino.cc/en/software) |
| Librerías **DHT sensor library** y **Adafruit Unified Sensor** | Leer el DHT22 desde el código | Desde Arduino IDE, en **Sketch → Include Library → Manage Libraries** |
| RealTerm | Grabar al menos 100 filas del puerto serial | [sourceforge.net/projects/realterm](https://sourceforge.net/projects/realterm/) |
| Python 3, con "Add Python to PATH" marcado | Capturar 500 lecturas y graficarlas | [python.org/downloads](https://www.python.org/downloads/) |

Para activar Wokwi en VS Code, abre la paleta con **F1**, ejecuta **Wokwi: Request a New License** e inicia sesión con tu cuenta de Wokwi en el navegador.

## Arrancar el circuito

1. Descarga el proyecto con `git clone https://github.com/ChristianAguilar2006/Semaforo-DHT22-Wokwi.git`, o desde GitHub con **Code → Download ZIP**. Abre la carpeta en VS Code con **File → Open Folder**.
2. En Arduino IDE abre `SemaforoDHT22/SemaforoDHT22.ino` y selecciona la placa **Arduino UNO**. Instala las dos librerías de Adafruit de la tabla anterior si aún no las tienes.
3. Usa **Sketch → Export Compiled Binary**. El archivo esperado es `SemaforoDHT22/build/arduino.avr.uno/SemaforoDHT22.ino.hex`. Si el IDE lo deja en otra ruta, ajusta `firmware` en `wokwi.toml` con la ruta relativa y barras `/`. Repite este paso cada vez que cambies el `.ino`.
4. Regresa a VS Code, abre la paleta con **F1** y ejecuta **Wokwi: Start Simulator**. La terminal de Wokwi debe mostrar una línea con temperatura y humedad cada 2,1 segundos aproximadamente. Haz clic en el DHT22 para variar sus valores.

## Probar el semáforo

El pulsador va de D3 a GND. Los LEDs verde, amarillo y rojo usan D6, D7 y D8 respectivamente, con una resistencia de 220 Ω por LED. El DHT22 usa D2, 5 V y GND.

Mantén presionado el pulsador con el ratón o con la tecla **B** mientras el diagrama tiene el foco. En Wokwi, **Ctrl + clic** deja el pulsador presionado hasta el siguiente clic, lo que facilita las capturas. El semáforo alterna cada tres segundos entre temperatura y humedad. El LED integrado **L** se enciende en la fase de humedad. Al soltar el pulsador, se apagan los LEDs. La salida serial sigue capturando ambas variables cada 2,1 segundos.

| Temperatura | Humedad | LED con L apagado | LED con L encendido |
|---|---|---|---|
| 15 °C | 60 % | Verde | Rojo |
| 25 °C | 20 % | Amarillo | Verde |
| 36,3 °C | 40 % | Rojo | Amarillo |

Los límites se aplican literalmente. Los valores sin color asignado por el enunciado dejan apagado el semáforo. Para tus capturas usa los valores de la tabla y deja pasar una lectura después de mover los controles del DHT22.

## Capturar 100 filas en RealTerm

1. Deja Wokwi corriendo y visible. Su puerto serial simulado se expone en `127.0.0.1:4000`.
2. En RealTerm, entra en **Port**, escribe `127.0.0.1:4000` en el campo **Port**, selecciona **Telnet** en **Winsock** y pulsa **Open**. Busca líneas con dos números separados por coma.
3. Ve a **Capture**, elige un archivo llamado `realterm.txt` y pulsa **Start Overwrite**. Tras cuatro minutos, detén la captura y verifica que haya al menos 100 líneas con dos números. Guarda una captura de RealTerm y otra del archivo. Luego cierra la conexión de RealTerm.

Wokwi acepta una sola conexión a la vez en el puerto 4000. Cierra RealTerm antes de ejecutar Python, o Python no podrá conectarse.

## Capturar 500 filas y graficar con Python

`graficas.py` es el script de clase modificado. Conserva la conexión a `rfc2217://localhost:4000` y las dos gráficas en tiempo real, y además guarda cada lectura en `data.txt`, se detiene al llegar a 500 lecturas y guarda la figura en `graficas.png`.

La primera vez, crea el entorno virtual e instala los paquetes desde PowerShell en la carpeta del proyecto.

```powershell
py -m venv .venv
.\.venv\Scripts\python -m pip install pyserial matplotlib
```

Con la simulación corriendo y visible, ejecuta el script.

```powershell
.\.venv\Scripts\python graficas.py
```

La captura dura unos 20 minutos. Mueve los controles del DHT22 varias veces durante la captura. Al terminar, `data.txt` tiene un encabezado y 500 filas con número de muestra, tiempo, temperatura y humedad. Cierra la ventana de las gráficas para finalizar. Si la cierras o pulsas Ctrl+C antes, `data.txt` conserva las lecturas tomadas hasta ese momento.

## Preparar la entrega

Incluye en el PDF el código Arduino, capturas del circuito, los cambios del semáforo para ambas variables y evidencia de RealTerm. Agrega la ejecución de Python, una vista del archivo de datos y ambas gráficas. Pon el enlace del video en el PDF.

En el video muestra cómo cambias los valores del DHT22, cómo responde el semáforo mientras presionas el pulsador y dónde quedan los datos y las gráficas.
