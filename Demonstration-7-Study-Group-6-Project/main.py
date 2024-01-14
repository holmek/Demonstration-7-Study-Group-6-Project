from lcd_menu import DisplayMenu
from rotary_encoder import RotaryEncoder
from lmt84 import LMT84
from machine import Pin
from gpio_lcd import GpioLcd


# Alle variabler
temperature_sensor = LMT84()
rotaryencoder = RotaryEncoder()
red_light = Pin(26, Pin.OUT)
rotary_button = Pin(14, Pin.IN, Pin.PULL_UP)
display = GpioLcd(rs_pin=Pin(27), enable_pin=Pin(25),
                  d4_pin=Pin(33), d5_pin=Pin(32),
                  d6_pin=Pin(21), d7_pin=Pin(22),
                  num_lines=4, num_columns=20)
display_menu = DisplayMenu(display, rotaryencoder, rotary_button)


# Viser rød lampe
def display_led():
    red_light.value(not red_light.value())

# Viser temperatur på display
def display_temperature(unit_function, unit_symbol):
    update_display_temperature(unit_function(), unit_symbol)

# Opdatere temperaturen på display
def update_display_temperature(unit, unit_symbol):
    #linje 33 laver et enkelt ryk (1) så _ symbolet kan ses
    display.move_to(1, display_menu.selected)
    display.putstr(f"Value: {unit:.1f}")


# Lav menu items til display, altså første navnet og så hvad den skal vise
display_menu.items("Red Button", display_led)
display_menu.items("Celsius", lambda: display_temperature(temperature_sensor.celsius_temperature, "C"))
display_menu.items("Fahrenheit", lambda: display_temperature(temperature_sensor.fahrenheit_temperature, "F"))
display_menu.items("Kelvin", lambda: display_temperature(temperature_sensor.kelvin_temperature, "K"))


# Menu startes og vises som loop på display
display_menu.show_menu()
display_menu.run()

