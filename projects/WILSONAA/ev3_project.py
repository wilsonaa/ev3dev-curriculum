"""
Author: Aaron A. Wilson
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
    green_button['command'] = lambda: find_color(mqtt_client, "SIG1")

    blue_button = ttk.Button(main_frame, text="Find Blue")
    blue_button.grid(row=1, column=0)
    blue_button['command'] = lambda: find_color(mqtt_client, "SIG2")

    pink_button = ttk.Button(main_frame, text="Find Pink")
    pink_button.grid(row=0, column=1)
    pink_button['command'] = lambda: find_color(mqtt_client, "SIG3")

    yellow_button = ttk.Button(main_frame, text="Find Yellow",)
    yellow_button.grid(row=1, column=1)
    yellow_button['command'] = lambda: find_color(mqtt_client, "SIG4")

    q_button = ttk.Button(main_frame, text="Exit")
    q_button.grid(row=14, column=2)
    q_button['command'] = (lambda: quit_program(mqtt_client, False))

    left_speed_label = ttk.Label(main_frame, text="Left")
    left_speed_label.grid(row=8, column=0)
    left_speed_entry = ttk.Entry(main_frame, width=8)
    left_speed_entry.insert(0, "600")
    left_speed_entry.grid(row=9, column=0)

    right_speed_label = ttk.Label(main_frame, text="Right")
    right_speed_label.grid(row=8, column=2)
    right_speed_entry = ttk.Entry(main_frame, width=8, justify=tkinter.RIGHT)
    right_speed_entry.insert(0, "600")
    right_speed_entry.grid(row=9, column=2)

    forward_button = ttk.Button(main_frame, text="Forward")
    forward_button.grid(row=10, column=1)
    # forward_button and '<Up>' key is done for your here...
    forward_button['command'] = lambda: handle_forward_button(mqtt_client, left_speed_entry, right_speed_entry)
    root.bind('<Up>', lambda event: handle_forward_button(mqtt_client, left_speed_entry, right_speed_entry))

    left_button = ttk.Button(main_frame, text="Left")
    left_button.grid(row=11, column=0)
    left_button['command'] = lambda: handle_left_button(mqtt_client, right_speed_entry)
    root.bind('<Left>', lambda event: handle_left_button(mqtt_client, right_speed_entry))
    # left_button and '<Left>' key

    right_button = ttk.Button(main_frame, text="Right")
    right_button.grid(row=11, column=2)
    right_button['command'] = lambda: handle_right_button(mqtt_client, left_speed_entry)
    root.bind('<Right>', lambda event: handle_right_button(mqtt_client, left_speed_entry))
    # right_button and '<Right>' key

    back_button = ttk.Button(main_frame, text="Back")
    back_button.grid(row=12, column=1)
    back_button['command'] = lambda: handle_back_button(mqtt_client, left_speed_entry, right_speed_entry)
    root.bind('<Down>', lambda event: handle_back_button(mqtt_client, left_speed_entry, right_speed_entry))
    # back_button and '<Down>' key

    up_button = ttk.Button(main_frame, text="Up")
    up_button.grid(row=0, column=2)
    up_button['command'] = lambda: send_up(mqtt_client)
    root.bind('<u>', lambda event: send_up(mqtt_client))

    down_button = ttk.Button(main_frame, text="Down")
    down_button.grid(row=1, column=2)
    down_button['command'] = lambda: send_down(mqtt_client)
    root.bind('<j>', lambda event: send_down(mqtt_client))

    stop_button = ttk.Button(main_frame, text="Stop")
    stop_button.grid(row=11, column=1)
    left_button['command'] = lambda: handle_stop(mqtt_client)
    root.bind('<space>', lambda event: handle_stop(mqtt_client))
    # stop_button and '<space>' key (note, does not need left_speed_entry, right_speed_entry)

    root.mainloop()


def find_color(mqtt_client, signature):
    if signature == "SIG1":
        print('Finding Green')
        mqtt_client.send_message("find_color", [signature])
    elif signature == "SIG2":
        print('Finding Blue')
        mqtt_client.send_message("find_color", [signature])
    elif signature == "SIG3":
        print('Finding Pink')
        mqtt_client.send_message("find_color", [signature])
    elif signature == "SIG4":
        print('Finding Yellow')
        mqtt_client.send_message("find_color", [signature])


def quit_program(mqtt_client, shutdown_ev3):
    if shutdown_ev3:
        print("shutdown")
        mqtt_client.send_message("shutdown")
    mqtt_client.close()
    exit()


def handle_forward_button(mqtt_client, left_speed_entry, right_speed_entry):
    left = int(left_speed_entry.get())
    right = int(right_speed_entry.get())
    print('Going forward')
    mqtt_client.send_message('drive_forward', [left, right])


def handle_left_button(mqtt_client, right_speed_entry):
    right = int(right_speed_entry.get())
    print('Going left')
    mqtt_client.send_message('turn_left', [right])


def handle_right_button(mqtt_client, left_speed_entry):
    left = int(left_speed_entry.get())
    print('Going right')
    mqtt_client.send_message('turn_right', [left])


def handle_back_button(mqtt_client, left_speed_entry, right_speed_entry):
    left = -int(left_speed_entry.get())
    right = -int(right_speed_entry.get())
    print('Going backwards')
    mqtt_client.send_message('drive_forward', [left, right])


def send_up(mqtt_client):
    print("Arm going up")
    mqtt_client.send_message("arm_up")


def handle_stop(mqtt_client):
    print('Stopping')
    mqtt_client.send_message("stop")


def send_down(mqtt_client):
    print("Arm going down")
    mqtt_client.send_message("arm_down")


main()
