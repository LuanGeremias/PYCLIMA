from machine import Pin
import dht
import time
import network
import urequests
import ujson


# ========================================
# CONFIGURAÇÃO
# ========================================

DHT_PIN = 26
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


# Verifica se já está conectado
if not wifi.isconnected():

    try:
        wifi.connect(WIFI_SSID, WIFI_SENHA)
    except Exception as erro:
        print("Erro ao iniciar conexão:", erro)


    tentativas = 0

    while not wifi.isconnected() and tentativas < 20:

        time.sleep(1)

        tentativas += 1

        print("Tentativa:", tentativas)


# Resultado da conexão
if wifi.isconnected():

    print()
    print("Wi-Fi conectado!")
    print("IP do ESP32:", wifi.ifconfig()[0])
    print("Máscara:", wifi.ifconfig()[1])
    print("Gateway:", wifi.ifconfig()[2])
    print("DNS:", wifi.ifconfig()[3])

else:

    print()
    print("ERRO: Wi-Fi não conectado.")
    print("Verifique o nome e a senha do Wi-Fi.")


# ========================================
# LOOP PRINCIPAL
# ========================================

registro = 0

while True:

    try:

        # ========================================
        # LER DHT11
        # ========================================

        sensor.measure()

        temperatura = sensor.temperature()
        umidade = sensor.humidity()


        # ========================================
        # LER SENSOR DE CHUVA
        # ========================================

        chuva = sensor_chuva.value()

        if chuva == 1:
            status_chuva = "CHUVA DETECTADA"
        else:
            status_chuva = "SEM CHUVA"


        # ========================================
        # REGISTRO
        # ========================================

        registro += 1

        print()
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

            json_dados = ujson.dumps(dados)

            print("Enviando para API...")

            try:

                resposta = urequests.post(
                    API_URL,
                    data=json_dados,
                    headers={
                        "Content-Type": "application/json"
                    }
                )

                print("Resposta da API:", resposta.status_code)

                resposta.close()

            except Exception as erro_api:

                print("Erro ao enviar para API:", erro_api)


        else:

            print("Wi-Fi desconectado.")
            print("Os dados não foram enviados.")


        print("----------------------------------------")


    except Exception as erro:

        print()
        print("----------------------------------------")
        print("ERRO:", erro)
        print("----------------------------------------")


    # Aguarda 5 segundos
    time.sleep(200)