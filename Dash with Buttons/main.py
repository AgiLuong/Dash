import os
import struct
import threading
import time
from enum import Enum

import can
from gpiozero import Button as gpioButton
from gpiozero import LED as gpioLED
from kivy import Config
from kivy.app import App
from kivy.clock import Clock
from kivy.lang import Builder
from kivy.properties import (NumericProperty,
                             StringProperty, BooleanProperty)
from kivy.uix.screenmanager import NoTransition
from kivy.uix.screenmanager import ScreenManager, Screen


class Button_Enum(Enum):
    BLANK = 0
    ENTER = 1
    RIGHT = 2
    LEFT = 3
    UP = 4
    DOWN = 5


class Button_states(Enum):
    SELECTED = 'down'
    NOT_SELECTED = 'normal'


class inputManager:
    # This class will handle creating physical buttons
    def __init__(self):
        pass

    def buttonEnterPressed(self):
        global isPressed
        # global led
        if isPressed == Button_Enum.BLANK:
            isPressed = Button_Enum.ENTER
            # led.on()
            main.kivy_manager.key_down(Button_Enum.ENTER)

    def buttonEnterReleased(self):
        global isPressed
        # global led
        if isPressed == Button_Enum.ENTER:
            # led.off()
            main.kivy_manager.key_up(Button_Enum.ENTER)
            isPressed = Button_Enum.BLANK

    def buttonRightPressed(self):
        global isPressed
        # global led
        if isPressed == Button_Enum.BLANK:
            isPressed = Button_Enum.RIGHT
            main.kivy_manager.key_down(Button_Enum.RIGHT)

    def buttonRightReleased(self):
        global isPressed
        # global led
        if isPressed == Button_Enum.RIGHT:
            main.kivy_manager.key_up(Button_Enum.RIGHT)
            isPressed = Button_Enum.BLANK

    def buttonLeftPressed(self):
        global isPressed
        # global led
        if isPressed == Button_Enum.BLANK:
            isPressed = Button_Enum.LEFT
            main.kivy_manager.key_down(Button_Enum.LEFT)

    def buttonLeftReleased(self):
        global isPressed
        # global led
        if isPressed == Button_Enum.LEFT:
            main.kivy_manager.key_up(Button_Enum.LEFT)
            isPressed = Button_Enum.BLANK

    def buttonUpPressed(self):
        global isPressed
        # global led
        if isPressed == Button_Enum.BLANK:
            isPressed = Button_Enum.UP
            main.kivy_manager.key_down(Button_Enum.UP)

    def buttonUpReleased(self):
        global isPressed
        # global led
        if isPressed == Button_Enum.UP:
            main.kivy_manager.key_up(Button_Enum.UP)
            isPressed = Button_Enum.BLANK

    def buttonDownPressed(self):
        global isPressed
        # global led
        if isPressed == Button_Enum.BLANK:
            isPressed = Button_Enum.DOWN
            main.kivy_manager.key_down(Button_Enum.DOWN)

    def buttonDownReleased(self):
        global isPressed
        # global led
        if isPressed == Button_Enum.DOWN:
            main.kivy_manager.key_up(Button_Enum.DOWN)
            isPressed = Button_Enum.BLANK


class kivyScreenManager:
    # TODO button calls will call to here and update ScreenManager
    #   * Manage Selected attributes of buttons on screens
    #   * Change Screen based on touch or button input
    def __init__(self):
        self.current_screen = 'MainScreen'
        self.screen_obj = MainScreen
        self.reg_screens = ['MainScreen', 'SuspensionScreen', 'SettingsScreen']
        self.Fuel_level = 0
        self.Throttle_level = 0
        self.Traction_level = 0
        self.Launch_level = 0
        self.Gearbox_level = 0
        # Maybe have the screenManager reference saved to directly call upon.

    def change_screen(self, name):
        global screens
        if name == 'MainScreen':
            self.current_screen = 'MainScreen'
            self.screen_obj = MainScreen
        elif name == 'SuspensionScreen':
            self.current_screen = 'SuspensionScreen'
            self.screen_obj = SuspensionScreen
        elif name == 'SettingsScreen':
            self.current_screen = 'SettingsScreen'
            self.screen_obj = SettingsScreen

        screens.current = self.current_screen
        self.screen_obj.ids[self.screen_obj.button_keys[self.screen_obj.selected_pos[0]][
            self.screen_obj.selected_pos[1]]].state = 'down'

    def key_down(self, direction):
        pass

    def key_up(self, direction, *kwargs):
        if self.current_screen == 'MainScreen':
            self.screen_key_event(direction=direction, screen_obj=MainScreen)
        elif self.current_screen == 'SuspensionScreen':
            self.screen_key_event(direction=direction, screen_obj=SuspensionScreen)
        elif self.current_screen == 'SettingsScreen':
            self.screen_key_event(direction=direction, screen_obj=SettingsScreen)

    def screen_key_event(self, direction, screen_obj):
        if direction == Button_Enum.RIGHT:
            if len(screen_obj.button_keys[screen_obj.selected_pos[0]]) \
                    > screen_obj.selected_pos[1] + 1:  # if it can move right

                screen_obj.ids[screen_obj.button_keys[screen_obj.selected_pos[0]][screen_obj.selected_pos[1]]].state \
                    = 'normal'
                screen_obj.selected_pos[1] += 1
            else:  # Cannot move right
                screen_obj.ids[
                    screen_obj.button_keys[screen_obj.selected_pos[0]][screen_obj.selected_pos[1]]].state = 'normal'
                screen_obj.selected_pos[1] = 0

        elif direction == Button_Enum.LEFT:
            if 0 <= screen_obj.selected_pos[1] - 1:  # if it can move Left
                screen_obj.ids[
                    screen_obj.button_keys[screen_obj.selected_pos[0]][screen_obj.selected_pos[1]]].state = 'normal'
                screen_obj.selected_pos[1] -= 1
            else:  # Cannot move Left
                screen_obj.ids[
                    screen_obj.button_keys[screen_obj.selected_pos[0]][screen_obj.selected_pos[1]]].state = 'normal'
                screen_obj.selected_pos[1] = len(screen_obj.button_keys[screen_obj.selected_pos[0]]) - 1

        elif direction == Button_Enum.UP:
            if 0 <= screen_obj.selected_pos[0] - 1:  # if it can move Up
                screen_obj.ids[
                    screen_obj.button_keys[screen_obj.selected_pos[0]][screen_obj.selected_pos[1]]].state = 'normal'
                screen_obj.selected_pos[0] -= 1
            else:  # Cannot move Up
                screen_obj.ids[
                    screen_obj.button_keys[screen_obj.selected_pos[0]][screen_obj.selected_pos[1]]].state = 'normal'
                screen_obj.selected_pos[0] = len(screen_obj.button_keys) - 1
            while len(screen_obj.button_keys[screen_obj.selected_pos[0]]) - 1 < screen_obj.selected_pos[1]:
                screen_obj.selected_pos[1] -= 1

        elif direction == Button_Enum.DOWN:
            if len(screen_obj.button_keys) - 1 >= screen_obj.selected_pos[0] + 1:  # if it can move Down
                screen_obj.ids[
                    screen_obj.button_keys[screen_obj.selected_pos[0]][screen_obj.selected_pos[1]]].state = 'normal'
                screen_obj.selected_pos[0] += 1
            else:  # Cannot move Down
                screen_obj.ids[
                    screen_obj.button_keys[screen_obj.selected_pos[0]][screen_obj.selected_pos[1]]].state = 'normal'
                screen_obj.selected_pos[0] = 0
            while len(screen_obj.button_keys[screen_obj.selected_pos[0]]) - 1 < screen_obj.selected_pos[1]:
                screen_obj.selected_pos[1] -= 1

        elif direction == Button_Enum.ENTER:
            screen_obj.ids[
                screen_obj.button_keys[screen_obj.selected_pos[0]][screen_obj.selected_pos[1]]].trigger_action()
            self.Clear_button_row(screen_obj.button_keys[screen_obj.selected_pos[0]], screen_obj=screen_obj)

        screen_obj.ids[screen_obj.button_keys[screen_obj.selected_pos[0]][screen_obj.selected_pos[1]]].state = 'down'

    def Clear_button_row(self, array, screen_obj):
        for x in array:
            screen_obj.ids[x].background_color = (1, 1, 1, 1)


Config.set('graphics', 'width', 1920)
Config.set('graphics', 'height', 1080)
Config.set('graphics', 'fbo', 'hardware')
Config.set('graphics', 'multisamples', -2)
Config.set('graphics', 'fullscreen', 1)
Config.set('graphics', 'window_state', 'maximized')

Builder.load_file('main.kv')

# initialize global variables
global_rpm = 0
global_speed = 0
global_gear = 0
global_coolant_temperature = 0.0
global_head_temperature = 0.0
global_coolant_pressure = 0.0
global_lambda_value = 0.00
global_oil_temperature = 0.0
global_oil_pressure = 0.0
global_battery_voltage = 0.0
global_fuel_pressure = 0.0
global_throttle_percent = 0
global_clutch_percent = 0
global_odo = 0
global_tune_mode = 'Null'
global_BSE_status = False
global_BSEA_status = False
global_front_left_wheel_speed = 0.0
global_front_right_wheel_speed = 0.0
global_front_left_lin_pot = 0.0
global_front_right_lin_pot = 0.0
global_steering_angle = 0
# Tune modes
global_tune1 = -1
global_tune2 = -1


class MainScreen(Screen):
    selected_pos = [0, 0]  # y,x
    button_keys = [['Suspension']]

    # Screen variables
    rpm = NumericProperty(0)
    speed = NumericProperty(0)
    gear = NumericProperty(0)
    coolant_temperature = NumericProperty(0.0)
    head_temperature = NumericProperty(0.0)
    coolant_pressure = NumericProperty(0.0)
    lambda_value = NumericProperty(0.00)
    oil_temperature = NumericProperty(0.0)
    oil_pressure = NumericProperty(0.0)
    battery_voltage = NumericProperty(0.0)
    fuel_pressure = NumericProperty(0.0)
    throttle_percent = NumericProperty(0)
    clutch_percent = NumericProperty(0)
    time_text = StringProperty(time.strftime("%H:%M"))
    odo = NumericProperty(0)
    tune_mode = StringProperty('Null')
    BSE_status = BooleanProperty(False)
    BSEA_status = BooleanProperty(False)


class SuspensionScreen(Screen):
    selected_pos = [0, 0]  # y,x
    button_keys = [['Return']]

    # Screen variables
    front_left_wheel_speed = NumericProperty(0.0) # front left wheel speed
    front_right_wheel_speed = NumericProperty(0.0) # front right wheel speed
    front_left_lin_pot = NumericProperty(0.0)
    front_right_lin_pot = NumericProperty(0.0)
    steering_angle = NumericProperty(0)


class SettingsScreen(Screen):
    selected_pos = [2, 0]  # y,x
    button_keys = [['Launch_Terminal'], ['Restart_Dash'], ['Return']]

    ip_address = StringProperty('IP: ')

screens = ScreenManager(transition=NoTransition())
screens.add_widget(MainScreen(name='MainScreen'))
screens.add_widget(SuspensionScreen(name='SuspensionScreen'))
screens.add_widget(SettingsScreen(name='SettingsScreen'))

MainScreen = screens.get_screen('MainScreen')
SuspensionScreen = screens.get_screen('SuspensionScreen')
SettingsScreen = screens.get_screen('SettingsScreen')


# CanBus = can.ThreadSafeBus(interface='socketcan', channel='can0', bitrate=1000000)  # TODO

running_flag = True

# def CANComm():
#
#     global global_rpm
#     global global_speed
#     global global_gear
#     global global_coolant_temperature
#     global global_head_temperature
#     global global_coolant_pressure
#     global global_lambda_value
#     global global_oil_temperature
#     global global_oil_pressure
#     global global_battery_voltage
#     global global_fuel_pressure
#     global global_throttle_percent
#     global global_clutch_percent
#     global global_odo
#     global global_tune_mode
#     global global_BSE_status
#     global global_front_left_wheel_speed
#     global global_front_right_wheel_speed
#     global global_front_left_lin_pot
#     global global_front_right_lin_pot
#     global global_steering_angle
#     BYTEORDER_CONSTANT = 'big'
#
#     while running_flag:
#
#         try:
#
#             msg = CanBus.recv(timeout=0.5)
#
#             if msg != None:  # msg is not None:
#
#                 if msg.arbitration_id == 0x100:
#                     if screens.current_screen == MainScreen:
#                         global_rpm = int.from_bytes(msg.data[0:2], byteorder=BYTEORDER_CONSTANT, signed=False)
#                         global_gear = int.from_bytes(msg.data[2:3], byteorder=BYTEORDER_CONSTANT, signed=False)
#                         global_speed = int.from_bytes(msg.data[3:4], byteorder=BYTEORDER_CONSTANT, signed=False)
#                         global_throttle_percent = int.from_bytes(msg.data[4:5], byteorder=BYTEORDER_CONSTANT, signed=False)
#                         global_clutch_percent = int.from_bytes(msg.data[6:7], byteorder=BYTEORDER_CONSTANT, signed=False)
#                     elif screens.current_screen == SuspensionScreen:
#                         global_steering_angle = int.from_bytes(msg.data[5:6], byteorder=BYTEORDER_CONSTANT, signed=True)
#
#                 elif msg.arbitration_id == 0x101:
#                     global_fuel_pressure = int.from_bytes(msg.data[4:6], byteorder=BYTEORDER_CONSTANT, signed=False) / 10.0
#                     global_oil_pressure = int.from_bytes(msg.data[6:8], byteorder=BYTEORDER_CONSTANT, signed=False) / 10.0
#
#                 elif msg.arbitration_id == 0x102:
#                     global_coolant_temperature = int.from_bytes(msg.data[0:2], byteorder=BYTEORDER_CONSTANT, signed=True) / 10.0
#                     global_head_temperature = int.from_bytes(msg.data[2:4], byteorder=BYTEORDER_CONSTANT, signed=True) / 10.0
#                     global_battery_voltage = int.from_bytes(msg.data[6:7], byteorder=BYTEORDER_CONSTANT, signed=False) / 10.0
#                     global_lambda_value = int.from_bytes(msg.data[7:8], byteorder=BYTEORDER_CONSTANT, signed=False) / 100.0
#
#                 elif msg.arbitration_id == 0x103:
#                     global_front_left_wheel_speed = int.from_bytes(msg.data[0:2], byteorder=BYTEORDER_CONSTANT, signed=True) / 10.0
#                     global_front_left_lin_pot = int.from_bytes(msg.data[2:4], byteorder=BYTEORDER_CONSTANT, signed=True) / 10.0
#                     global_front_right_wheel_speed = int.from_bytes(msg.data[4:6], byteorder=BYTEORDER_CONSTANT, signed=True) / 10.0
#                     global_front_right_lin_pot = int.from_bytes(msg.data[6:8], byteorder=BYTEORDER_CONSTANT, signed=True) / 10.0
#
#                 elif msg.arbitration_id == 0x104:
#                     global_odo = int.from_bytes(msg.data[0:2], byteorder=BYTEORDER_CONSTANT, signed=False)
#                     status = int.from_bytes(msg.data[2:3], byteorder=BYTEORDER_CONSTANT, signed=False)
#                     global_BSE_status = status & 0b01000000
#                     global_BSEA_status = status & 0b00000100 #added BAGR
#                     global_tune1 =  int.from_bytes(msg.data[3:4], byteorder = BYTEORDER_CONSTANT, signed = False) #added
#                     global_tune2 = status & 0b00000001 #added changed
#
#                     if global_tune1 == 0:
#                         global_tune_mode = 'F'
#                     elif global_tune1 == 1:
#                         global_tune_mode = 'M'
#                     elif global_tune1 == 2:
#                         if global_tune2 == 0:
#                             global_tune_mode = 'A'
#                         elif global_tune2 == 1:
#                             global_tune_mode = 'D'
#                         else:
#                             global_tune_mode = 'F2'
#
#         except:  # Whats giving the error
#             pass


# CANCommThread = threading.Thread(target=CANComm)

isPressed = Button_Enum.BLANK


# # led = gpioLED("board35")
# buttonEnter = gpioButton("board33")
# buttonLeft = gpioButton("board31")
# buttonRight = gpioButton("board37")
# buttonUp = gpioButton("board40")
# buttonDown = gpioButton("board38")
# buttonEnter.when_pressed = inputManager.buttonEnterPressed
# buttonEnter.when_released = inputManager.buttonEnterReleased
# buttonLeft.when_pressed = inputManager.buttonLeftPressed
# buttonLeft.when_released = inputManager.buttonLeftReleased
# buttonRight.when_pressed = inputManager.buttonRightPressed
# buttonRight.when_released = inputManager.buttonRightReleased
# buttonUp.when_pressed = inputManager.buttonUpPressed
# buttonUp.when_released = inputManager.buttonUpReleased
# buttonDown.when_pressed = inputManager.buttonDownPressed
# buttonDown.when_released = inputManager.buttonDownReleased


class main(App):
    kivy_manager = kivyScreenManager()

    # def sendCanMsg(self, func, msg_data):
    #
    #     try:
    #         if func == 'ThrottleMap':
    #             msg = can.Message(arbitration_id = 0xFF, is_extended_id = False, data = [0,msg_data])
    #
    #
    #         elif func == 'RideHeight':
    #             msg = can.Message(arbitration_id = 0xFF, is_extended_id = False, data = [2] + list(struct.pack("!f", msg_data)))
    #
    #         elif func == 'TractionSlipMap':
    #             msg = can.Message(arbitration_id = 0xFF, is_extended_id = False, data = [3,msg_data])
    #
    #         elif func == 'TractionRangeMap':
    #             msg = can.Message(arbitration_id = 0xFF, is_extended_id = False, data = [4,msg_data])
    #
    #         elif func == 'LaunchMap':
    #             msg = can.Message(arbitration_id = 0xFF, is_extended_id = False, data = [5,msg_data])
    #
    #         elif func == 'ShiftMode':
    #             msg = can.Message(arbitration_id = 0xFF, is_extended_id = False, data = [6,msg_data])
    #
    #         elif func == 'EngineMap':
    #             msg = can.Message(arbitration_id = 0xFF, is_extended_id = False, data = [7,msg_data])
    #
    #         CanBus.send(msg)
    #     except:
    #         pass

    def stopApp(self):
        os._exit(0)

    def updateTime(self, *args):
        MainScreen.time_text = time.strftime("%H:%M")

    def updateIpAddress(self, *args):
        try:
            SettingsScreen.ip_address = "IP: " + \
                                        os.popen('/sbin/ip addr show wlan0').read().split("inet ")[1].split("/")[
                                            0]  # TODO uncomment later.
        except:  # Whats giving the error
            pass

    def updateScreen(self, *args):
        if screens.current_screen == MainScreen:
            MainScreen.rpm = global_rpm
            MainScreen.speed = global_speed
            MainScreen.gear = global_gear
            MainScreen.coolant_temperature = global_coolant_temperature
            MainScreen.head_temperature = global_head_temperature
            MainScreen.coolant_pressure = global_coolant_pressure
            MainScreen.lambda_value = global_lambda_value
            MainScreen.oil_temperature = global_oil_temperature
            MainScreen.oil_pressure = global_oil_pressure
            MainScreen.battery_voltage = global_battery_voltage
            MainScreen.fuel_pressure = global_fuel_pressure
            MainScreen.throttle_percent = global_throttle_percent
            MainScreen.clutch_percent = global_clutch_percent
            MainScreen.odo = global_odo
            MainScreen.tune_mode = global_tune_mode
            MainScreen.BSE_status = global_BSE_status
            MainScreen.BSEA_status = global_BSEA_status  # added 5-22-21

        elif screens.current_screen == SuspensionScreen:
            SuspensionScreen.front_left_wheel_speed = global_front_left_wheel_speed
            SuspensionScreen.front_right_wheel_speed = global_front_right_wheel_speed
            SuspensionScreen.front_left_lin_pot = global_front_left_lin_pot
            SuspensionScreen.front_right_lin_pot = global_front_right_lin_pot
            SuspensionScreen.steering_angle = global_steering_angle

    def on_start(self):
        Clock.schedule_interval(self.updateTime, 1)
        Clock.schedule_interval(self.updateIpAddress, 3)
        Clock.schedule_interval(self.updateScreen, 0.02)
        # CANCommThread.start()

    def on_stop(self):
        global running_flag
        running_flag = False

    def restart(self):
        os.system('sudo reboot')

    def build(self):
        return screens


if __name__ == "__main__":
    main().run()
