"""
User settings for NeoPixel demo.
"""

# --------------------------------------------------------------------------------------------------
# Device settings
# --------------------------------------------------------------------------------------------------
# LED_NUM       | 1 to 164          | Number of LEDs connected to the SPI LED strip |
# MAX_BRIGHTNESS| 0(Off) to 100[%]  | Brightness MAX limit of the LEDs.             |
# Depends on power supply current and SPI bus frequency
# In a experiment, 164 LEDs worked at 5V, 1.8A.
# --------------------------------------------------------------------------------------------------
LED_NUM = 164
MAX_BRIGHTNESS = 5

# --------------------------------------------------------------------------------------------------
# LED settings
# --------------------------------------------------------------------------------------------------
# START_POSITION    | 0 to LED_NUM - 1  | Initial starting position of the lit area.|
# LED_ON_NUM        | 0 to LED_NUM      | The number of LEDs to use.                |
# --------------------------------------------------------------------------------------------------
START_POSITION = 0
LED_ON_NUM = 100

# --------------------------------------------------------------------------------------------------
# Blink timing
# --------------------------------------------------------------------------------------------------
# TIME_INTERVAL | 0 to x.xxxx   | Main loop cycle time [seconds]                |
# CYCLE_SEC     | 0 to x.xx     | Time to stay at current LED position [seconds]|
# ON_TIME       | 0 to x        | LED ON duration [seconds]                     |
# OFF_TIME      | 0 to x        | LED OFF duration[seconds]                     |
# FADE_IN_RATE  | 0 to 100      | Fade-in duration = ON_TIME  * rate / 100      |
# FADE_OUT_RATE | 0 to 100      | Fade-out duration = OFF_TIME * rate / 100     |
# MOVE_REVERSE  | True or False | False: forward / True: reverse                |
# --------------------------------------------------------------------------------------------------
TIME_INTERVAL = 0.1
CYCLE_SEC = 0.5
ON_TIME = 1.5
OFF_TIME = 0.5
FADE_IN_RATE = 80
FADE_OUT_RATE = 80
MOVE_REVERSE = False
PATTERN_FREQ = 10

# --------------------------------------------------------------------------------------------------
# LED Animation Timing Chart
# --------------------------------------------------------------------------------------------------
#   |<- one cycle ------------------------------------>|
#   |<---------- ON_TIME -------------><-- OFF_TIME -->|
#   |<-FADE_IN_->|                     |<- FADE_OUT_ ->|
#   |   _RATE[%] |                     |    _RATE[%]   |
#   |            +---------------------+               |
#   |          /                          \            |
#   |       /                                 \        |
#   |    /                                        \    |
#   | /                                              \ |
#   +------------+---------------------+---------------+--> time
#   ^            ^                     ^               ^
#   |            |                     |               |
#   ON start    Fade-in end           OFF start       OFF end
#
# Position
# ==============================================================================
#
# [MOVE_REVERSE = False] LED 0               LED 1                LED 2
#   ●                    ●                    ●                    ●
#   +-----CYCLE_SEC------>-----CYCLE_SEC------>-----CYCLE_SEC------>  time
#   ●                    ●                    ●                    ●
# [MOVE_REVERSE =  True] LED 2                LED 1                LED 0
# =============================================================================
