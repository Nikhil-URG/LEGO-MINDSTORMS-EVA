#!/usr/bin/env micropython
from time import sleep
import sys
import math 
from ev3dev2.motor import LargeMotor, OUTPUT_A, OUTPUT_B, OUTPUT_C, OUTPUT_D, SpeedPercent, MoveTank
from ev3dev2.sensor import INPUT_1, INPUT_2, INPUT_3, INPUT_4
from ev3dev2.sound import Sound
from ev3dev2.button import Button

WHEEL_DIAMETER = 5.6 # cm
MAIN_AXIS_LENGTH = 12.0 # cm

buttons = Button()
move = MoveTank(OUTPUT_A, OUTPUT_D)
spkr = Sound()
motor_1 = LargeMotor(OUTPUT_A)
motor_2 = LargeMotor(OUTPUT_D)
last_pose = ()

def final_data(x, y, orientation):
    
    with open('final_poses.csv','a') as final_poses:
        final_poses.write("{:.2f},{:.2f},{:.2f}\n".format(robot_position_x, robot_position_y, (math.pi / 2) - robot_orientation))
        

for loop in range(1,30):
    motor_1_path = [] # in rad
    motor_2_path = [] # in rad

    motor_1_path.append(motor_1.position)
    motor_2_path.append(motor_2.position)

    robot_orientation = 0.0 # in rad
    robot_position_x  = 0.0 # in cm
    robot_position_y  = 0.0 # in cm

    distance_traveled_wheel_1 = 0.0 # in cm
    distance_traveled_wheel_2 = 0.0 # in cm

    spkr.speak('Press a button')
    while True:
        if buttons.right:
            move.on_for_seconds(SpeedPercent(-40), SpeedPercent(-30), 2.2, block=False)

        elif buttons.down:
            move.on_for_seconds(SpeedPercent(-38), SpeedPercent(-38), 2.2, block=False)

        elif buttons.left:
            move.on_for_seconds(SpeedPercent(-30), SpeedPercent(-40), 2.2, block=False)

        if (motor_1.is_running): motor_1_path.append((motor_1.position * math.pi) / 180.0)
        if (motor_2.is_running): motor_2_path.append((motor_2.position * math.pi) / 180.0)

        if (motor_1.is_holding and motor_2.is_holding):
            data_length = min(len(motor_1_path), len(motor_2_path))
            

            with open('both_motors_path_{}.csv'.format(loop), "w") as f_wheels_path:
                for i in range(data_length):
                    f_wheels_path.write(str(str(motor_1_path[i]) + " " + str(motor_2_path[i]) + "\n")) # in rad

            with open('robot_path_{}.csv'.format(loop), "w") as f_robot_path:
                for i in range(data_length):
                    if i is 0:
                        distance_traveled_wheel_1 = (WHEEL_DIAMETER * math.pi * motor_1_path[0]) / (2 * math.pi)
                        distance_traveled_wheel_2 = (WHEEL_DIAMETER * math.pi * motor_2_path[0]) / (2 * math.pi)
                    else:
                        distance_traveled_wheel_1 = (WHEEL_DIAMETER * math.pi * (motor_1_path[i] - motor_1_path[i - 1])) / (2 * math.pi)
                        distance_traveled_wheel_2 = (WHEEL_DIAMETER * math.pi * (motor_2_path[i] - motor_2_path[i - 1])) / (2 * math.pi)

                    delta_distance = (distance_traveled_wheel_1 + distance_traveled_wheel_2) / 2
                    delta_angle    = (distance_traveled_wheel_1 - distance_traveled_wheel_2) / MAIN_AXIS_LENGTH

                    robot_orientation = robot_orientation + delta_angle
                    robot_position_x  = robot_position_x  + delta_distance * math.sin(robot_orientation)
                    robot_position_y  = robot_position_y  + delta_distance * math.cos(robot_orientation)
                    f_robot_path.write("{},{},{}\n".format(robot_position_x, robot_position_y, (math.pi / 2) - robot_orientation))  # in cm and rad
                    last_pose = (robot_position_x, robot_position_y, robot_orientation)

            final_data(last_pose[0], last_pose[1], last_pose[2])
            number = str(loop)
            spkr.speak('Motion completed' + number)         
            motor_1.stop(stop_action="coast")
            motor_2.stop(stop_action="coast")
            motor_1.reset()
            motor_2.reset()
            break

    # don't let this loop use 100% CPU
    sleep(0.001)


