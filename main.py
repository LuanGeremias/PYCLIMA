from machine import Pin
import dht
import time
import network
import urequests

# ========================================
# CONFIGURAÇÃO
# ========================================

DHT_PIN = 27
CHUVA_PIN = 25

WIFI_SSID = "LUCAS"
WIFI_SENHA = "senh@999"

API_URL = "http://192.168.3.103:8000/sensores"

# ========================================
# SENSORES
# ========================================

sensor = dht.DHT11(Pin(DHT_PIN))
sensor_chuva = Pin(CHUVA_PIN, Pin.IN)

# ========================================
# WIFI
# ========================================

wifi = network.WLAN(network.STA_IF)
wifi.active(True)

print()
print("========================================")
print("           PYCLIMA - ESP32")
print("========================================")

print("Conectando ao Wi-Fi...")

wifi.connect(WIFI_SSID, WIFI_SENHA)

tentativas = 0

while not wifi.isconnected() and tentativas < 20:
    time.sleep(1)
    tentativas += 1
    print("Tentativa:", tentativas)

if wifi.isconnected():
    print("Wi-Fi conectado!")
    print("IP do ESP32:", wifi.ifconfig()[0])
else:
    print("ERRO: não foi possível conectar ao Wi-Fi.")

# ========================================
# LOOP
# ========================================

registro = 0

while True:

    try:

        sensor.measure()

        temperatura = sensor.temperature()
        umidade = sensor.humidity()

        chuva = sensor_chuva.value()

        if chuva == 1:
            status_chuva = "CHUVA DETECTADA"
        else:
            status_chuva = "SEM CHUVA"

        registro += 1

        print("----------------------------------------")
        print("Registro:", registro)
        print("Temperatura:", temperatura, "°C")
        print("Umidade:", umidade, "%")
        print("Chuva:", status_chuva)

        # ========================================
        # ENVIAR PARA API
        # ========================================

        if wifi.isconnected():

            dados = {
                "temperatura": temperatura,
                "umidade": umidade,
                "chuva": bool(chuva)
            }

            resposta = urequests.post(
                API_URL,
                json=dados
            )

            print("Resposta da API:", resposta.status_code)

            resposta.close()

        else:
            print("Wi-Fi desconectado.")

        print("----------------------------------------")
        print()

    except Exception as erro:

        print("----------------------------------------")
        print("ERRO")
        print("Erro:", erro)
        print("----------------------------------------")

    time.sleep(5)