#!/usr/bin/env python3
import Adafruit_BBIO.ADC as ADC
import time

ADC.setup()
FLEX_CHANNEL      = "AIN5"

# Raw-ADC thresholds; tune these to your actual sensor:
BEND_THRESHOLD    = 2900    # raw < this → bent
UNBEND_THRESHOLD  = 3600    # raw > this → unbent

def read_raw():
    """Reads data for flex sensor"""
    return int(ADC.read_raw(FLEX_CHANNEL))

if __name__ == "__main__":
    print("Reading flex sensor on", FLEX_CHANNEL)
    state_bent = False

    try:
        while True:
            raw = read_raw()

            # Hysteresis logic with no smoothing
            if not state_bent and raw < BEND_THRESHOLD:
                state_bent = True
                print("→ BENT detected!")
            elif state_bent and raw > UNBEND_THRESHOLD:
                state_bent = False
                print("← UNBENT detected!")

            status = "BENT" if state_bent else "unbent"
            print(f" Raw: {raw:4d}   Status: {status}")
            time.sleep(0.1)

    except KeyboardInterrupt:
        print("\nExiting.")

