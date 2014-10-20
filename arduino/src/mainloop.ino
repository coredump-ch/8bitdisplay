#include "LedControl.h"
#include <src/charmap.h>
#define DIN 11
#define CS 12
#define CLOCK 13
#define ADDR 0

#define SERIAL_INTERFACE false

/*
Segment numbering:
       7
    --------
   |        |
 2 |        | 6
   |    1   |
    --------
   |        |
 3 |        | 5
   |        |
    --------   . 8
       4
	   
	   
To display a one "1", you need to light up segments 5,6 => in binary: 0b00110000
*/

// Initialization

LedControl lc = LedControl(DIN,CLOCK,CS,1); 
char display_buffer[8];


// Function declarations

static void print8bit();
static void printCoredump();
static void printBuffer();


// Setup & Loop

void setup() {
    lc.shutdown(0,false);
    lc.setIntensity(0,15);
#ifdef SERIAL_INTERFACE
    Serial.begin(9600);
#endif
}

void loop() {
    printCoredump();

#ifdef SERIAL_INTERFACE
    Serial.println("8bit Display is ready!");
    while (1){
        if (Serial.available() >= 8){
            Serial.readBytes(display_buffer, 8);
            Serial.print("New string received: ");
            printBuffer();
        }
    }
#endif
}


// Output functions

void print8bit() {
    lc.setDigit(ADDR, 7, 8, false);
    lc.setRow(ADDR, 6, 0b000011111);
    lc.setRow(ADDR, 5, 0b100);
    lc.setRow(ADDR, 4, 0b111);
    lc.setRow(ADDR, 3, 0x00);
    lc.setRow(ADDR, 2, 0b000011111);
    lc.setDigit(ADDR, 1, 0xa, false);
    lc.setRow(ADDR, 0, 0b101);
}

void printBuffer() {
    for(int i =7; i>=0; --i){
        lc.setRow(0, i, display_buffer[7-i]);
        Serial.write(display_buffer[7-i]);
    }
}

void printCoredump() {
    lc.setRow(ADDR, 7, CHAR_C);
    lc.setRow(ADDR, 6, CHAR_o);
    lc.setRow(ADDR, 5, CHAR_r);
    lc.setRow(ADDR, 4, CHAR_e);
    lc.setRow(ADDR, 3, CHAR_d);
    lc.setRow(ADDR, 2, CHAR_u);
    lc.setRow(ADDR, 1, CHAR_m);
    lc.setRow(ADDR, 0, CHAR_p);
}
