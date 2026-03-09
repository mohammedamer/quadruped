import time
import board
import busio

from adafruit_pca9685 import PCA9685
from adafruit_motor import servo

JOINTS = {
    "l11": {"drive": 1, "ch": 10},
    "l12": {"drive": 1, "ch": 11},
    "l13": {"drive": 1, "ch": 12},
    "l21": {"drive": 1, "ch": 13},
    "l22": {"drive": 1, "ch": 14},
    "l23": {"drive": 1, "ch": 15},
    "l31": {"drive": 0, "ch": 13},
    "l32": {"drive": 0, "ch": 14},
    "l33": {"drive": 0, "ch": 15},
    "r11": {"drive": 1, "ch": 6},
    "r12": {"drive": 1, "ch": 5},
    "r13": {"drive": 1, "ch": 4},
    "r21": {"drive": 1, "ch": 9},
    "r22": {"drive": 1, "ch": 8},
    "r23": {"drive": 1, "ch": 7},
    "r31": {"drive": 0, "ch": 2},
    "r32": {"drive": 0, "ch": 1},
    "r33": {"drive": 0, "ch": 0},
}

# 1) I2C bus (Feather SDA/SCL pins)
i2c = busio.I2C(board.SCL, board.SDA)


def list_address():

    while not i2c.try_lock():
        pass

    try:
        print([hex(x) for x in i2c.scan()])
    finally:
        i2c.unlock()


list_address()


PCA = []

for address in [0x40, 0x41]:
    pca = PCA9685(i2c, address=address)
    pca.frequency = 50
    PCA.append(pca)


SERVOS = {}

for k, v in JOINTS.items():
    pca = PCA[v["drive"]]
    ch = pca.channels[v["ch"]]
    s = servo.Servo(ch, min_pulse=500, max_pulse=2500)

    SERVOS[k] = s


def set_neutral():

    for _, servo in SERVOS.items():
        servo.angle = 90


while True:
    set_neutral()
    time.sleep(5)


# print("Starting servo calibration")

# STEP = 1
# DEFAULT_ANGLE = 0

# current_servo = None
# servo_key = None
# current_angle = DEFAULT_ANGLE

# min_angle = max_angle = neutral_angle = None


# def write_angle(angle):

#     global current_servo, current_angle

#     if current_servo is not None:
#         current_angle = angle
#         current_servo.angle = current_angle
#         print(f"current angle: {current_angle}")
#         time.sleep(0.1)
#     else:
#         print("choose a servo first")


# while True:
#     cmd = input("> ").strip()

#     if cmd.startswith("servo"):
#         key = cmd.split(" ")[1]

#         if key not in SERVOS:
#             print("Unknown servo")
#             continue

#         servo_key = key
#         current_servo = SERVOS[servo_key]
#         write_angle(DEFAULT_ANGLE)

#         print(f"selected servo: {servo_key}")

#     elif cmd == "w":
#         write_angle(current_angle+STEP)
#     elif cmd == "s":
#         write_angle(current_angle-STEP)
#     elif cmd == "W":
#         write_angle(current_angle+5*STEP)
#     elif cmd == "S":
#         write_angle(current_angle-5*STEP)
#     elif cmd == "r":
#         write_angle(DEFAULT_ANGLE)
#     elif cmd == "p":
#         print(f"current angle: {current_angle}")
#     elif cmd == "min":
#         min_angle = current_angle
#         print(f"min: {min_angle}")
#     elif cmd == "max":
#         max_angle = current_angle
#         print(f"max: {max_angle}")
#     elif cmd == "neutral":
#         neutral_angle = current_angle
#         print(f"neutral: {neutral_angle}")
#     elif cmd == "save":
#         print({
#             "servo": servo_key,
#             "min": min_angle,
#             "neutral": neutral_angle,
#             "max": max_angle,
#         })
#     elif cmd == "q":
#         break
#     else:
#         print("Unknown command")

# print("Done.")
