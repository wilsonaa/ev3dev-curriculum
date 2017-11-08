#Code Written by Benjamin Dreikosen

import ev3dev.ev3 as ev3
import time

import robot_controller as robo


def main():
    print("--------------------------------------------")
    print(" Color tracking")
    print("--------------------------------------------")
    ev3.Sound.speak("Color tracking").wait()
    print("Press the touch sensor to exit this program.")

    robot = robo.Snatch3r()
    robot.pixy.mode = "SIG1"
    turn_speed = 600

    while not robot.touch_sensor.is_pressed:

        # TODO: 2. Read the Pixy values for x and y
        # Print the values for x and y
        print("value1:X", robot.pixy.value(1))
        print("value2:Y", robot.pixy.value(2))
        print("value3:Width",robot.pixy.value(3))
        print("value3:Hiegth", robot.pixy.value(4))
        print("surface Area",(robot.pixy.value(3)*robot.pixy.value(4)))
        sa = robot.pixy.value(3)*robot.pixy.value(4)
        if sa > 1000:
            print("Caught Object")
            ev3.Sound.speak("Caught Object").wait()
            robot.stop()
            break
        elif sa > 850:
            robot.drive_forward(turn_speed*.25,turn_speed*.25)

        elif sa > 500:
            robot.drive_forward(turn_speed*.5, turn_speed*.5)

        elif sa > 150:
            robot.drive_forward(turn_speed*.75, turn_speed*.75)

        elif sa < 50:
            robot.drive_forward(turn_speed, turn_speed)
        time.sleep(0.25)

    print("Goodbye!")
    ev3.Sound.speak("Goodbye").wait()
main()