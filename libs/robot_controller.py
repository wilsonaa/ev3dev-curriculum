"""
  Library of EV3 robot functions that are useful in many different applications. For example things
  like arm_up, arm_down, driving around, or doing things with the Pixy camera.

  Add commands as needed to support the features you'd like to implement.  For organizational
  purposes try to only write methods into this library that are NOT specific to one tasks, but
  rather methods that would be useful regardless of the activity.  For example, don't make
  a connection to the remote control that sends the arm up if the ir remote control up button
  is pressed.  That's a specific input --> output task.  Maybe some other task would want to use
  the IR remote up button for something different.  Instead just make a method called arm_up that
  could be called.  That way it's a generic action that could be used in any task.
"""

import ev3dev.ev3 as ev3
import math
import time


class Snatch3r(object):
    """Commands for the Snatch3r robot that might be useful in many different programs."""

    # TODO: Implement the Snatch3r class as needed when working the sandox exercises
    # (and delete these comments)
    def __init__(self):


        # Connect two large motors on output ports B and C
        self.left_motor = ev3.LargeMotor(ev3.OUTPUT_B)
        self.right_motor = ev3.LargeMotor(ev3.OUTPUT_C)
        self.arm_motor = ev3.MediumMotor(ev3.OUTPUT_A)
        self.touch_sensor = ev3.TouchSensor()
        self.color_sensor = ev3.ColorSensor()
        self.ir_sensor = ev3.InfraredSensor()
        self.beacon_seeker = ev3.BeaconSeeker()
        self.pixy = ev3.Sensor(driver_name="pixy-lego")

        assert self.pixy
        assert self.beacon_seeker
        assert self.ir_sensor
        assert self.color_sensor
        assert self.touch_sensor
        assert self.arm_motor.connected
        assert self.left_motor.connected
        assert self.right_motor.connected

    def drive_forward(self,left_speed,right_speed):
        assert self.right_motor
        assert self.left_motor

        self.left_motor.run_forever(speed_sp=left_speed)
        self.right_motor.run_forever(speed_sp=right_speed)

    def turn_left(self,right_speed):
        assert self.right_motor

        self.left_motor.stop()
        self.right_motor.run_forever(speed_sp = right_speed)

    def turn_right(self,left_speed):
        assert self.left_motor
        self.right_motor.stop()
        self.left_motor.run_forever(speed_sp = left_speed)

    def drive_left_motor(self,speed):
        self.left_motor.run_forever(speed_sp = speed)

    def drive_right_motor(self,speed):
        self.right_motor.run_forever(speed_sp = speed)

    def stop(self):
        self.right_motor.stop(stop_action = ev3.Motor.STOP_ACTION_BRAKE)
        self.left_motor.stop(stop_action = ev3.Motor.STOP_ACTION_BRAKE)


    def drive_inches(self,Distance,speed):

        self.left_motor.wait_while(ev3.Motor.STATE_RUNNING)
        self.left_motor.run_to_rel_pos(position_sp=Distance * 90,
                                  speed_sp=speed,
                                  stop_action=ev3.Motor.STOP_ACTION_BRAKE)

        self.right_motor.run_to_rel_pos(position_sp=Distance * 90,
                                   speed_sp=speed,
                                   stop_action=ev3.Motor.STOP_ACTION_BRAKE)

        self.right_motor.wait_while(ev3.Motor.STATE_RUNNING)

    def turn_degrees(self, degrees_to_turn, turn_speed_sp):


        self.left_motor.wait_while(ev3.Motor.STATE_RUNNING)
        self.left_motor.run_to_rel_pos(position_sp=degrees_to_turn * -11/2*turn_speed_sp/(turn_speed_sp+10),
                                       speed_sp=turn_speed_sp,
                                       stop_action=ev3.Motor.STOP_ACTION_BRAKE)

        self.right_motor.run_to_rel_pos(position_sp=degrees_to_turn * 11/2*turn_speed_sp/(turn_speed_sp+10),
                                        speed_sp=turn_speed_sp,
                                        stop_action=ev3.Motor.STOP_ACTION_BRAKE)

    def arm_calibration(self):

        self.arm_motor.run_forever(speed_sp=900)
        while not self.touch_sensor.is_pressed:
            time.sleep(0.01)
        self.arm_motor.stop(stop_action=ev3.Motor.STOP_ACTION_BRAKE)
        ev3.Sound.beep().wait()
        arm_revolutions_for_full_range = 14.2 * 360
        self.arm_motor.run_to_rel_pos(position_sp=-arm_revolutions_for_full_range,stop_action = ev3.Motor.STOP_ACTION_BRAKE)
        self.arm_motor.wait_while(ev3.Motor.STATE_RUNNING)
        ev3.Sound.beep().wait()
        self.arm_motor.position = 0  # Calibrate the down position as 0 (this line is correct as is).

    def arm_up(self):

        self.arm_motor.run_forever(speed_sp=900)
        while not self.touch_sensor.is_pressed:
            time.sleep(0.01)
        self.arm_motor.stop(stop_action=ev3.Motor.STOP_ACTION_BRAKE)
        self.arm_motor.wait_while(ev3.Motor.STATE_RUNNING)
        self.arm_motor.stop(stop_action=ev3.Motor.STOP_ACTION_BRAKE)
        ev3.Sound.beep().wait()

    def arm_down(self):

        arm_revolutions_for_full_range = 14.2 * 360
        self.arm_motor.run_to_rel_pos(position_sp=-arm_revolutions_for_full_range)
        self.arm_motor.wait_while(ev3.Motor.STATE_HOLDING)  # Blocks until the motor finishes running
        ev3.Sound.beep().wait()

    def led(self,side,color):

        ev3.Leds.set_color(side, color)

    def ir_sensor_dist(self):
        if self.ir_sensor.proximity <=10:

            ev3.Sound.beep().wait()
            time.sleep(1.5)

    def seek_beacon(self):
        while not self.touch_sensor.is_pressed:
            # The touch sensor can be used to abort the attempt (sometimes handy during testing)

            # DONE: 3. Use the beacon_seeker object to get the current heading and distance.
            current_heading = self.beacon_seeker.heading  # use the beacon_seeker heading
            current_distance = self.beacon_seeker.distance  # use the beacon_seeker distance
            if current_distance == -128:
                # If the IR Remote is not found just sit idle for this program until it is moved.
                self.drive_right_motor(150)
                self.drive_left_motor(-150)
            elif current_distance == 100:
                self.drive_right_motor(150)
                self.drive_left_motor(-150)
            else:

                if math.fabs(current_heading) < 2:
                    # Close enough of a heading to move forward
                    print("On the right heading. Distance: ", current_distance)
                    # You add more!
                if current_distance == 0:
                    self.stop()
                    return True
                if current_heading < -2:
                    if current_heading < -20:
                        self.drive_right_motor(150)
                        self.drive_left_motor(-150)
                    self.drive_right_motor(150)
                    self.drive_left_motor(-150)
                elif current_heading > 2:
                    if current_heading > 20:
                        self.drive_right_motor(-150)
                        self.drive_left_motor(150)
                    self.drive_left_motor(150)
                    self.drive_right_motor(-150)
                else:
                    self.drive_right_motor(150)
                    self.drive_left_motor(150)


    def loop_forever(self):
        # This is a convenience method that I don't really recommend for most programs other than m5.
        #   This method is only useful if the only input to the robot is coming via mqtt.
        #   MQTT messages will still call methods, but no other input or output happens.
        # This method is given here since the concept might be confusing.
        self.running = True
        while self.running:
            time.sleep(0.1)  # Do nothing (except receive MQTT messages) until an MQTT message calls shutdown.

    def shutdown(self):
        # Modify a variable that will allow the loop_forever method to end. Additionally stop motors and set LEDs green.
        # The most important part of this method is given here, but you should add a bit more to stop motors, etc.
        self.running = False

    def find_color(self,signature):


        if signature == "SIG1":
            ev3.Sound.speak("Finding Green")
        if signature == "SIG2":
            ev3.Sound.speak("Finding Red")
        if signature == "SIG3":
            ev3.Sound.speak("Finding Black")
        if signature == "SIG4":
            ev3.Sound.speak("Finding Yellow")
        turn_speed = 50

        while not self.touch_sensor.is_pressed:

            print("value1:X", self.pixy.value(1))
            print("value2:Y", self.pixy.value(2))

            if self.pixy.value(1) < 150:
                self.drive_left_motor(-turn_speed)
                self.drive_right_motor(turn_speed)
            elif self.pixy.value(1) > 170:
                self.drive_left_motor(turn_speed)
                self.drive_right_motor(-turn_speed)
            else:
                self.stop()
                break
            time.sleep(0.25)

        if signature == "SIG1":
            ev3.Sound.speak("Found Green").wait()
        if signature == "SIG2":
            ev3.Sound.speak("Found Red").wait()
        if signature == "SIG3":
            ev3.Sound.speak("Found Black").wait()
        if signature == "SIG4":
            ev3.Sound.speak("Found Yellow").wait()
        ev3.Sound.speak("Waiting for next command").wait()

    def PlayingCatch(self):
        print("--------------------------------------------")
        print(" Playing Catch")
        print("--------------------------------------------")
        ev3.Sound.speak("Playing Catch").wait()
        print("Press the touch sensor to exit this program.")


        self.pixy.mode = "SIG1"
        turn_speed = 300

        while not self.touch_sensor.is_pressed:

            sa = self.pixy.value(3) * self.pixy.value(4)
            if self.pixy.value(1) < 150:
                self.drive_left_motor(-turn_speed)
                self.drive_right_motor(turn_speed)
            elif self.pixy.value(1) > 170:
                self.drive_left_motor(turn_speed * .5)
                self.drive_right_motor(-turn_speed * .5)
            else:
                if sa > 2500:
                    print("Caught Object")
                    ev3.Sound.speak("Caught Object").wait()
                    self.stop()
                    break
                elif sa > 1800:
                    self.drive_forward(turn_speed * .25, turn_speed * .25)

                elif sa > 800:
                    self.drive_forward(turn_speed * .5, turn_speed * .5)

                elif sa > 500:
                    self.drive_forward(turn_speed * .75, turn_speed * .75)

                elif sa < 100:
                    self.drive_forward(turn_speed, turn_speed)
                time.sleep(0.25)

        print("Goodbye!")
        ev3.Sound.speak("Goodbye").wait()