import time
import board
import busio

from adafruit_pca9685 import PCA9685
from adafruit_motor import servo

JOINTS = {
    "l11":  {"ch": 0, "dir": -1},
    "l12":  {"ch": 1, "dir": -1},
    "l21":  {"ch": 2, "dir": -1},
    "l22":  {"ch": 3, "dir": -1},
    "r11":  {"ch": 4, "dir": 1},
    "r12":  {"ch": 5, "dir": -1},
    "r21":  {"ch": 6, "dir": 1},
    "r22":  {"ch": 7, "dir": -1},
}

# 1) I2C bus (Feather SDA/SCL pins)
i2c = busio.I2C(board.SCL, board.SDA)
pca = PCA9685(i2c, address=0x41)
pca.frequency = 50


SERVOS = {}

for k, v in JOINTS.items():
    ch = pca.channels[v["ch"]]
    s = servo.Servo(ch, min_pulse=500, max_pulse=2500)

    SERVOS[k] = s


DEFAULT_ANGLE = 90


def set_neutral():

    for _, servo in SERVOS.items():
        servo.angle = DEFAULT_ANGLE


set_neutral()


def calibrate():

    STEP = 1

    current_servo = None
    servo_key = None
    current_angle = DEFAULT_ANGLE

    min_angle = max_angle = neutral_angle = None

    def write_angle(angle):

        global current_servo, current_angle

        if current_servo is not None:
            current_angle = angle
            current_servo.angle = current_angle
            print(f"current angle: {current_angle}")
            time.sleep(0.1)
        else:
            print("choose a servo first")

    while True:
        cmd = input("> ").strip()

        if cmd.startswith("servo"):
            key = cmd.split(" ")[1]

            if key not in SERVOS:
                print("Unknown servo")
                continue

            servo_key = key
            current_servo = SERVOS[servo_key]
            write_angle(DEFAULT_ANGLE)

            print(f"selected servo: {servo_key}")

        elif cmd == "w":
            write_angle(current_angle+STEP)
        elif cmd == "s":
            write_angle(current_angle-STEP)
        elif cmd == "W":
            write_angle(current_angle+5*STEP)
        elif cmd == "S":
            write_angle(current_angle-5*STEP)
        elif cmd == "r":
            write_angle(DEFAULT_ANGLE)
        elif cmd == "p":
            print(f"current angle: {current_angle}")
        elif cmd == "min":
            min_angle = current_angle
            print(f"min: {min_angle}")
        elif cmd == "max":
            max_angle = current_angle
            print(f"max: {max_angle}")
        elif cmd == "neutral":
            neutral_angle = current_angle
            print(f"neutral: {neutral_angle}")
        elif cmd == "save":
            print({
                "servo": servo_key,
                "min": min_angle,
                "neutral": neutral_angle,
                "max": max_angle,
            })
        elif cmd == "q":
            break
        else:
            print("Unknown command")

    print("Starting servo calibration")


def dance():

    dtheta = 5

    for key in ["l12", "l22"]:
        SERVOS[key].angle = DEFAULT_ANGLE - JOINTS[key]["dir"]*dtheta

    for key in ["r12", "r22"]:
        SERVOS[key].angle = DEFAULT_ANGLE + JOINTS[key]["dir"]*dtheta

    time.sleep(0.5)

    for key in ["l12", "l22"]:
        SERVOS[key].angle = DEFAULT_ANGLE + JOINTS[key]["dir"]*dtheta

    for key in ["r12", "r22"]:
        SERVOS[key].angle = DEFAULT_ANGLE - JOINTS[key]["dir"]*dtheta

    time.sleep(0.5)


# while True:
#     dance()


print("Done.")
