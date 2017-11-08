"""
Author: Aaron Wilson
"""
import ev3dev.ev3 as ev3
import time

import robot_controller as robo
import tkinter
from tkinter import ttk
import mqtt_remote_method_calls as com



def main():
    mqtt_client = com.MqttClient()
    mqtt_client.connect_to_ev3()

    root = tkinter.Tk()
    root.title("MQTT Remote")

    main_frame = ttk.Frame(root, padding=20, relief='raised')
    main_frame.grid()

    green_button = ttk.Button(main_frame, text="Find Green")
    green_button.grid(row=0, column=0)
    green_button['command'] = lambda: find_color(mqtt_client,"SIG1")

    red_button = ttk.Button(main_frame, text = "Find Red")
    red_button.grid(row = 1, column = 0)

    black_button = ttk.Button(main_frame, text = "Find Black")
    black_button.grid(row = 0, column = 1)

    yellow_button = ttk.Button(main_frame, text = "Find Yellow",)
    yellow_button.grid(row = 1, column = 1)
    yellow_button['command'] = lambda: find_color(mqtt_client, "SIG4")

    q_button = ttk.Button(main_frame, text="Quit")
    q_button.grid(row=5, column=2)
    q_button['command'] = (lambda: quit_program(mqtt_client, False))

    root.mainloop()

def find_color(mqtt_client,signature):
    if signature == "SIG1":
        mqtt_client.send_message("find_color",[signature])
    elif signature == "SIG4":
        mqtt_client.send_message("find_color", [signature])

def quit_program(mqtt_client, shutdown_ev3):
    if shutdown_ev3:
        print("shutdown")
        mqtt_client.send_message("shutdown")
    mqtt_client.close()
    exit()

main()