#!/usr/bin/env python3
import os
import time

import Adafruit_BBIO.ADC as ADC
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM  as PWM

# Direction control
FLEX_DIR_CW    = "AIN3"
FLEX_DIR_CCW   = "AIN4"
# Motor triggers
FLEX_TRIG_1    = "AIN5"   # triggers Motor 1
FLEX_TRIG_2    = "AIN6"   # triggers Motor 2

BEND_THRESHOLD    = 2900    # raw < this → bent
UNBEND_THRESHOLD  = 3600    # raw > this → unbent

M1_EN,  M1_IN1,  M1_IN2 = "P1_36", "P1_34", "P1_32"
M2_EN,  M2_IN1,  M2_IN2 = "P1_33", "P1_35", "P1_31"
ADC.setup()

os.system(f"config-pin {M1_EN} pwm")
os.system(f"config-pin {M2_EN} pwm")
for pin in (M1_IN1, M1_IN2, M2_IN1, M2_IN2):
    os.system(f"config-pin {pin} gpio")
    GPIO.setup(pin, GPIO.OUT)

PWM.start(M1_EN, 0, 1000)   # 1 kHz, 0% duty (off)
PWM.start(M2_EN, 0, 1000)

def motor_on_dir(en, in1, in2, direction, speed_pct=100):
    """Run motor in CW or CCW at speed_pct%."""
    if direction == "CW":
        GPIO.output(in1, GPIO.HIGH)
        GPIO.output(in2, GPIO.LOW)
    else:  # CCW
        GPIO.output(in1, GPIO.LOW)
        GPIO.output(in2, GPIO.HIGH)
    PWM.set_duty_cycle(en, speed_pct)

def motor_off(en, in1, in2, coast=True):
    """Stop motor; if coast=False, actively brake."""
    PWM.set_duty_cycle(en, 0)
    if not coast:
        GPIO.output(in1, GPIO.HIGH)
        GPIO.output(in2, GPIO.HIGH)

if __name__ == "__main__":
    direction_flag = "CW"       
    dir3_bent = False             
    dir4_bent = False              
    motor1_active = False
    motor2_active = False

    print("Starting demo (Ctrl-C to quit)...")
    try:
        while True:
            # Read all four flex sensors
            raw3 = ADC.read_raw(FLEX_DIR_CW)
            raw4 = ADC.read_raw(FLEX_DIR_CCW)
            raw5 = ADC.read_raw(FLEX_TRIG_1)
            raw6 = ADC.read_raw(FLEX_TRIG_2)

            if (not dir3_bent) and raw3 < BEND_THRESHOLD:
                dir3_bent = True
                direction_flag = "CW"
                print("→ Direction set to CW")
            elif dir3_bent and raw3 > UNBEND_THRESHOLD:
                dir3_bent = False
            # Sensor4 bent → set CCW
            if (not dir4_bent) and raw4 < BEND_THRESHOLD:
                dir4_bent = True
                direction_flag = "CCW"
                print("→ Direction set to CCW")
            elif dir4_bent and raw4 > UNBEND_THRESHOLD:
                dir4_bent = False

            if (not motor1_active) and raw5 < BEND_THRESHOLD:
                motor1_active = True
                print("→ MOTOR 1 ON")
                motor_on_dir(M1_EN, M1_IN1, M1_IN2, direction_flag)
            elif motor1_active and raw5 > UNBEND_THRESHOLD:
                motor1_active = False
                print("→ MOTOR 1 OFF")
                motor_off(M1_EN, M1_IN1, M1_IN2)

            if (not motor2_active) and raw6 < BEND_THRESHOLD:
                motor2_active = True
                print("→ MOTOR 2 ON")
                motor_on_dir(M2_EN, M2_IN1, M2_IN2, direction_flag)
            elif motor2_active and raw6 > UNBEND_THRESHOLD:
                motor2_active = False
                print("→ MOTOR 2 OFF")
                motor_off(M2_EN, M2_IN1, M2_IN2)

            status = (
                f"Raw3:{raw3:4d}  Raw4:{raw4:4d}  "
                f"Raw5:{raw5:4d}  Raw6:{raw6:4d}  "
                f"Dir:{direction_flag}  "
                f"M1:{'ON' if motor1_active else 'OFF'}  "
                f"M2:{'ON' if motor2_active else 'OFF'}"
            )
            print(status)

            time.sleep(0.1)

    except KeyboardInterrupt:
        print("\nInterrupted; shutting down...")
        # Ensure motors off
        motor_off(M1_EN, M1_IN1, M1_IN2)
        motor_off(M2_EN, M2_IN1, M2_IN2)
        # Stop & cleanup PWM/GPIO
        PWM.stop(M1_EN)
        PWM.stop(M2_EN)
        PWM.cleanup()
        GPIO.cleanup()
        print("Done.")
