# In-Hand Palm 2DoF Manipulator
In-the-palm 2DoF manipulator that will be worn on both the forearm and hand. This device will be comprised of an active surface (i.e. a pulley belt) and turntable that will be actuated by two micro DC motors. The control of this device will be actuated by four pressure sensors that will be inlaid along the wrist to measure the bend of the wrist. Depending on the bend of the wrist, either the turntable or active surface will turn on and move.

## Installation

Download the .io file labelled "main.py" as well as the ADAFruit BBIO libraries. Once installed, push the "main.py" file to your local microprocessor (This project was ran using a Pocket Beagle) and will run automatically as it awaits flex sensor data assuming everything is wired correctly.

## Usage

With the glove installed and looking down on it in a supinated position, the following movements control the manipulator. A forward flick changes the active surface direction (CW or CCW) and a backwards hold turns the active surface on until returned to a neutral position. A right flick toggles the turntable direction (CW or CCW) and a left hold turns the turntable on until returned to a neutral position. Tolerances for the flex sensors can be set within the script to ensure they work correctly.
Note: This device was constructed without encoders and thus the turntable does not have built in limits for movement. For personal use, either pay attention to wire limit during operation or add in encoder motor stops to prevent wire tangle and/or detachment.

## Testing

If needed to, a flex sensor and motor test script (flex_test and motor_test respectively) are given to confirm that both systems are functioning correctly. Simply wiring and connecting either to the microprocessor is sufficient for these tests.

## Physical Construction

To learn more about the physical build for this project, please follow [this link](https://www.hackster.io/haydenwebb/in-hand-palm-2dof-manipulator-6d990e) to the associated Hackster page. There you'll find more information regarding the construction and steps taken to create this manipulator.

## License

[MIT](https://choosealicense.com/licenses/mit/)
