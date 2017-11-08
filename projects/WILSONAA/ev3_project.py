"""
Author: Aaron Wilson
"""
import ev3dev.ev3 as ev3
import time

import robot_controller as robo
import tkinter
from tkinter import ttk
import mqtt_remote_method_calls as com


class MyDelegate(object):
    def print_message(self, message):
        print("Message received:", message)




def main():
    my_delegate = MyDelegate()
    mqtt_client = com.MqttClient(my_delegate)
    mqtt_client.connect("topic_name", "topic_name")

    root = tkinter.Tk()
    root.title("MQTT Remote")

    main_frame = ttk.Frame(root, padding=20, relief='raised')
    main_frame.grid()

    green_button = ttk.Button(main_frame, text="Find Green")
    green_button.grid(row=0, column=0)

    red_button = ttk.Button(main_frame, text = "Find Red")
    red_button.grid(row = 1, column = 0)

    black_button = ttk.Button(main_frame, text = "Find Black")
    black_button.grid(row = 0, column = 1)

    yellow_button = ttk.Button(main_frame, text = "Find Yellow")
    yellow_button.grid(row = 1, column = 1)

    root.mainloop()

main()