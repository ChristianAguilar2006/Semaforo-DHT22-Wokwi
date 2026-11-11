#include <DHT.h>

const uint8_t PIN_DHT = 2;
const uint8_t PIN_PULSADOR = 3;
const uint8_t PIN_VERDE = 6;
const uint8_t PIN_AMARILLO = 7;
const uint8_t PIN_ROJO = 8;
const unsigned long INTERVALO_LECTURA_MS = 2100;
const unsigned long DURACION_MODO_MS = 3000;

enum Color { APAGADO, VERDE, AMARILLO, ROJO };

Color clasificar(float valor, float finVerde, float finAmarillo);

DHT sensor(PIN_DHT, DHT22);
float temperatura = NAN;
float humedad = NAN;
unsigned long ultimaLectura = 0;
unsigned long inicioPulsacion = 0;
bool pulsadorAnterior = false;

Color clasificar(float valor, float finVerde, float finAmarillo) {
  if (valor >= 10 && valor <= finVerde) {
    return VERDE;
  }
  if (valor >= finVerde + 1 && valor <= finAmarillo) {
    return AMARILLO;
  }
  if (valor > finAmarillo + 1) {
    return ROJO;
  }
  return APAGADO;
}

void setup() {
  Serial.begin(9600);
  sensor.begin();

  pinMode(PIN_PULSADOR, INPUT_PULLUP);
  pinMode(PIN_VERDE, OUTPUT);
  pinMode(PIN_AMARILLO, OUTPUT);
  pinMode(PIN_ROJO, OUTPUT);
  pinMode(LED_BUILTIN, OUTPUT);
}

void loop() {
  unsigned long ahora = millis();
  bool pulsado = digitalRead(PIN_PULSADOR) == LOW;

  if (pulsado && !pulsadorAnterior) {
    inicioPulsacion = ahora;
  }
  pulsadorAnterior = pulsado;

  if (ahora - ultimaLectura >= INTERVALO_LECTURA_MS) {
    ultimaLectura = ahora;
    temperatura = sensor.readTemperature();
    humedad = sensor.readHumidity();

    if (!isnan(temperatura) && !isnan(humedad)) {
      Serial.print(temperatura, 1);
      Serial.print(',');
      Serial.println(humedad, 1);
    }
  }

  Color color = APAGADO;
  bool modoHumedad = false;

  if (pulsado) {
    modoHumedad = (ahora - inicioPulsacion) / DURACION_MODO_MS % 2 == 1;
    color = modoHumedad ? clasificar(humedad, 30, 50) : clasificar(temperatura, 20, 30);
  }

  digitalWrite(PIN_VERDE, color == VERDE);
  digitalWrite(PIN_AMARILLO, color == AMARILLO);
  digitalWrite(PIN_ROJO, color == ROJO);
  digitalWrite(LED_BUILTIN, modoHumedad);
}
