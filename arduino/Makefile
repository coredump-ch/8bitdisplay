# System configuration
ARDUINO_DIR   = /usr/share/arduino
ARDMK_DIR     = arduino-makefile
AVR_TOOLS_DIR = /usr

# Arduino config
BOARD_TAG        = nano  # use "make show_boards" to list all
BOARD_SUB        = atmega328
ARDUINO_PORT     = /dev/ttyUSB0
ARDUINO_LIBS     = LedControl
USER_LIB_PATH    = $(realpath libs)
MONITOR_BAUDRATE = 9600

# Filesystem config
LOCAL_C_SRCS   ?= $(wildcard src/*.c)
LOCAL_CPP_SRCS ?= $(wildcard src/*.cpp)
LOCAL_CC_SRCS  ?= $(wildcard src/*.cc)
LOCAL_PDE_SRCS ?= $(wildcard src/*.pde)
LOCAL_INO_SRCS ?= $(wildcard src/*.ino)
LOCAL_AS_SRCS  ?= $(wildcard src/*.s)

# Compiler config
CFLAGS_STD = -std=c11

include arduino-makefile/Arduino.mk
