#!/usr/bin/env python3
import os
import time
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.PWM  as PWM

M2_EN,  M2_IN1,  M2_IN2 = "P1_33", "P1_35", "P1_31"
M1_EN,  M1_IN1,  M1_IN2 = "P1_36", "P1_34", "P1_32"

os.system(f"config-pin {M1_EN} pwm")
os.system(f"config-pin {M2_EN} pwm")
for pin in (M1_IN1, M1_IN2, M2_IN1, M2_IN2):
    os.system(f"config-pin {pin} gpio")
    GPIO.setup(pin, GPIO.OUT)

PWM.start(M1_EN, 0, 1000)   # 1 kHz, 0% duty (off)
PWM.start(M2_EN, 0, 1000)

def motor_on(en, in1, in2, speed_pct=100):
    """Run motor in CW or CCW at speed_pct%."""
    GPIO.output(in1, GPIO.HIGH)
    GPIO.output(in2, GPIO.LOW)
    PWM.set_duty_cycle(en, speed_pct)


def motor_off(en, in1, in2, coast=True):
    """Stop motor; if coast=False, actively brake."""
    PWM.set_duty_cycle(en, 0)
    if not coast:
        # active brake: tie both inputs together
        GPIO.output(in1, GPIO.HIGH)
        GPIO.output(in2, GPIO.HIGH)

if __name__ == "__main__":
    print("Starting alternating motor test (Ctrl-C to quit)...")
    try:
        while True:
            print("→ MOTOR 1 ON")
            try:
                motor_on(M1_EN, M1_IN1, M1_IN2)
            except Exception as e:
                print("Error in motor_on(M1):", repr(e))
            time.sleep(2.0)

            print("→ MOTOR 1 OFF (coast)")
            try:
                motor_off(M1_EN, M1_IN1, M1_IN2, coast=True)
            except Exception as e:
                print("Error in motor_off(M2):", repr(e))
            time.sleep(2.0)

            print("→ MOTOR 2 ON (coast)")
            try:
                motor_on(M2_EN, M2_IN1, M2_IN2, coast=True)
            except Exception as e:
                print("Error in motor_off(M1):", repr(e))
            time.sleep(0.5)

            print("→ MOTOR 2 OFF")
            try:
                motor_off(M2_EN, M2_IN1, M2_IN2)
            except Exception as e:
                print("Error in motor_on(M2):", repr(e))
            time.sleep(2)

    except KeyboardInterrupt:
        print("\nInterrupted; shutting down motors and cleaning up.")
        # Ensure motors are off
        motor_off(M1_EN, M1_IN1, M1_IN2)
        motor_off(M2_EN, M2_IN1, M2_IN2)
        # Stop and cleanup PWM/GPIO
        PWM.stop(M1_EN)
        PWM.stop(M2_EN)
        PWM.cleanup()
        GPIO.cleanup()
        print("Done.")
