from machine import Pin
import dht
import time

# ========================================
# CONFIGURAÇÃO
# ========================================

DHT_PIN = 27
CHUVA_PIN = 25

# ========================================
# SENSORES
# ========================================

sensor = dht.DHT11(Pin(DHT_PIN))
sensor_chuva = Pin(CHUVA_PIN, Pin.IN)

# ========================================
# INÍCIO
# ========================================

print()
print("========================================")
print("     DHT11 + SENSOR DE CHUVA + ESP32")
print("========================================")
print()
print("DHT11 DATA  -> GPIO 27")
print("CHUVA DO    -> GPIO 25")
print()
print("Iniciando leituras...")
print()

registro = 0

# ========================================
# LOOP
# ========================================

while True:

    try:

        # ----------------------------------------
        # LER DHT11
        # ----------------------------------------

        sensor.measure()

        temperatura = sensor.temperature()
        umidade = sensor.humidity()

        # ----------------------------------------
        # LER SENSOR DE CHUVA
        # ----------------------------------------

        chuva = sensor_chuva.value()

        if chuva == 1:
            status_chuva = "CHUVA DETECTADA"
        else:
            status_chuva = "SEM CHUVA"

        # ----------------------------------------
        # REGISTRO
        # ----------------------------------------

        registro += 1

        # ----------------------------------------
        # MOSTRAR
        # ----------------------------------------

        print("----------------------------------------")
        print("Registro:", registro)
        print("Temperatura:", temperatura, "°C")
        print("Umidade:", umidade, "%")
        print("Chuva:", status_chuva)
        print("----------------------------------------")
        print()

    except Exception as erro:

        print("----------------------------------------")
        print("ERRO AO LER SENSOR")
        print("Erro:", erro)
        print("----------------------------------------")
        print()

    time.sleep(2)