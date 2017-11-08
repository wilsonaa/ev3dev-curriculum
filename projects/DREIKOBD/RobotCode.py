#Code Written by Benjamin Dreikosen

import ev3dev.ev3 as ev3
import time

import robot_controller as robo


def main():
    print("--------------------------------------------")
    print(" Playing Catch")
    print("--------------------------------------------")
    ev3.Sound.speak("Playing Catch").wait()
    print("Press the touch sensor to exit this program.")

    robot = robo.Snatch3r()
    robot.pixy.mode = "SIG1"
    turn_speed = 300

    while not robot.touch_sensor.is_pressed:


        sa = robot.pixy.value(3)*robot.pixy.value(4)
        if robot.pixy.value(1) < 150:
            robot.drive_left_motor(-turn_speed)
            robot.drive_right_motor(turn_speed)
        elif robot.pixy.value(1) > 170:
            robot.drive_left_motor(turn_speed*.5)
            robot.drive_right_motor(-turn_speed*.5)
        else:
            if sa > 2500:
                print("Caught Object")
                ev3.Sound.speak("Caught Object").wait()
                robot.stop()
                break
            elif sa > 1800:
                robot.drive_forward(turn_speed*.25,turn_speed*.25)

            elif sa > 800:
                robot.drive_forward(turn_speed*.5, turn_speed*.5)

            elif sa > 500:
                robot.drive_forward(turn_speed*.75, turn_speed*.75)

            elif sa < 100:
                robot.drive_forward(turn_speed, turn_speed)
            time.sleep(0.25)

    print("Goodbye!")
    ev3.Sound.speak("Goodbye").wait()
main()