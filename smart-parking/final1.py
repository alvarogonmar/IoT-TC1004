import RPi.GPIO as GPIO
import time
import firebase_admin
from firebase_admin import credentials, firestore

# Inicializar Firestore
cred = credentials.Certificate("ruta_json")
firebase_admin.initialize_app(cred)
db = firestore.client()

GPIO.setmode(GPIO.BOARD)

# Pines de sensores de los cajones
IR_PINS = {
    "P-01": 11,
    "P-02": 12,
    "P-03": 13,
    "P-04": 15,
    "P-05": 16,
    "P-06": 18
}

# Sensor y servo de entrada
ENTRADA_IR_PIN = 21
SERVO_ENTRADA_PIN = 19

# Sensor y servo de salida
SALIDA_IR_PIN = 24
SERVO_SALIDA_PIN = 23

# Configurar sensores
for slot, pin in IR_PINS.items():
    GPIO.setup(pin, GPIO.IN)

GPIO.setup(ENTRADA_IR_PIN, GPIO.IN)
GPIO.setup(SALIDA_IR_PIN, GPIO.IN)

# Configurar servos
GPIO.setup(SERVO_ENTRADA_PIN, GPIO.OUT)
GPIO.setup(SERVO_SALIDA_PIN, GPIO.OUT)

servo_entrada = GPIO.PWM(SERVO_ENTRADA_PIN, 50)
servo_salida = GPIO.PWM(SERVO_SALIDA_PIN, 50)

# Iniciar servos abajo
servo_entrada.start(7.5)
servo_salida.start(7.5)

def levantar_pluma(servo):
    print("Levantando pluma...")
    servo.ChangeDutyCycle(2.5)
    time.sleep(4)

def bajar_pluma(servo):
    print("Bajando pluma...")
    servo.ChangeDutyCycle(7.5)
    time.sleep(1)

# Estados
estados_anteriores = {slot: None for slot in IR_PINS}
tiempo_acumulado = {slot: 0 for slot in IR_PINS}

ultima_actualizacion = time.time()

try:
    while True:
        ahora = time.time()

        # Entrada del estacionamiento
        if GPIO.input(ENTRADA_IR_PIN) == 0:
            print("Carro ENTRANDO")
            levantar_pluma(servo_entrada)
            bajar_pluma(servo_entrada)

        # Salida del estacionamiento
        if GPIO.input(SALIDA_IR_PIN) == 0:
            print("Carro SALIENDO")
            levantar_pluma(servo_salida)
            bajar_pluma(servo_salida)

        # Lectura de cajones
        for slot, pin in IR_PINS.items():
            valor = GPIO.input(pin)
            estado_texto = "ocupado" if valor == 0 else "libre"

            if valor != estados_anteriores[slot]:
                print("Slot", slot, estado_texto.upper())
                doc_ref = db.collection("parking-slots").document(slot)
                doc_ref.update({"isOccupied": valor == 0})

                if estados_anteriores[slot] == 1 and valor == 0:
                    slot_data = doc_ref.get().to_dict()
                    nuevo_valor = slot_data.get("usageFrequency", 0) + 1
                    doc_ref.update({"usageFrequency": nuevo_valor})

                estados_anteriores[slot] = valor

            # Tiempo acumulado
            if valor == 0 and ahora - ultima_actualizacion >= 5:
                tiempo_acumulado[slot] += 5
                db.collection("parking-slots").document(slot).update({
                    "totalOccupiedSeconds": tiempo_acumulado[slot]
                })

        if ahora - ultima_actualizacion >= 5:
            ultima_actualizacion = ahora

        time.sleep(0.1)

except KeyboardInterrupt:
    print("Finalizando programa...")

finally:
    servo_entrada.stop()
    servo_salida.stop()
    GPIO.cleanup()
