#include <LedControl.h>
#include "segments.h"
#define DIN 11
#define CS 12
#define CLOCK 13
#define ADDR 0

#define SERIAL_LOOP false

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
long randomNumber;


// Function declarations

static void print_8bit();
static void print_coredump();
static void print_buffer();
static void print_snake(char);
static void print_number(unsigned long number);
static void print_count_up();
static void print_press_it();
static void print_random();


// Setup & Loop

void setup() {
    lc.shutdown(0,false);
    lc.setIntensity(0,15);
    Serial.begin(9600);

    pinMode(2,INPUT_PULLUP);

    // if analog input pin 0 is unconnected, random analog
    // noise will cause the call to randomSeed() to generate
    // different seed numbers each time the sketch runs.
    // randomSeed() will then shuffle the random function.
    randomSeed(analogRead(0));

    lc.clearDisplay(ADDR);
}

void loop() {
    //Serial.println("8bit Display is ready!");

    /*
    print_coredump();
    delay(random(3000, 30000));  // Sleep between 3s and 30s
    print_snake(random(3, 5));  // Do 3 to 5 loops
    */

    enum State {
        GotoShowNumber,
        ShowNumber,
        GotoShowMessage,
        ShowMessage,
    };
    static State state = GotoShowNumber;
    static unsigned long timer_start = 0;
    static unsigned long count = 0;
    static int old_switch = 1;

    int new_switch = digitalRead(2);
    bool flank = old_switch == 1 && new_switch == 0;
    old_switch = new_switch;

    if (flank) {
        count++;
        state = GotoShowNumber;
    }

    switch (state) {
        case GotoShowNumber:
            print_number(count);
            state = ShowNumber;
            timer_start = millis();
            break;
        case ShowNumber:
            if ((millis() - timer_start) > 3000) {
                state = GotoShowMessage;
            }
            break;

        case GotoShowMessage:
            print_random();
            state = ShowMessage;
            timer_start = millis();
            break;
        case ShowMessage:
            if ((millis() - timer_start) > 3000) {
                state = GotoShowNumber;
            }
            break;
    }
    delay(10);

#if (SERIAL_LOOP == true)
    Serial.println("Waiting for serial commands...");
    while (1){
        if (Serial.available() >= 8){
            Serial.readBytes(display_buffer, 8);
            Serial.print("New string received: ");
            print_buffer();
        }
    }
#endif
}


// Output functions
static void print_8bit() {
    lc.setDigit(ADDR, 7, 8, false);
    lc.setRow(ADDR, 6, 0b000011111);
    lc.setRow(ADDR, 5, 0b100);
    lc.setRow(ADDR, 4, 0b111);
    lc.setRow(ADDR, 3, 0x00);
    lc.setRow(ADDR, 2, 0b000011111);
    lc.setDigit(ADDR, 1, 0xa, false);
    lc.setRow(ADDR, 0, 0b101);
}

static void print_buffer() {
    for(int i =7; i>=0; --i){
        lc.setRow(0, i, display_buffer[7-i]);
        Serial.write(display_buffer[7-i]);
    }
}

static void print_coredump() {
    lc.clearDisplay(ADDR);
    lc.setRow(ADDR, 7, CHAR_C);
    lc.setRow(ADDR, 6, CHAR_o);
    lc.setRow(ADDR, 5, CHAR_r);
    lc.setRow(ADDR, 4, CHAR_e);
    lc.setRow(ADDR, 3, CHAR_d);
    lc.setRow(ADDR, 2, CHAR_u);
    lc.setRow(ADDR, 1, CHAR_m);
    lc.setRow(ADDR, 0, CHAR_p);
}

static void print_random() {
    switch (random() % 3) {
        case 0:
            print_coredump();
            break;
        case 1:
            print_count_up();
            break;
        case 2:
            print_press_it();
            break;
    }
}

static void print_press_it() {
    lc.clearDisplay(ADDR);
    lc.setRow(ADDR, 7, CHAR_p);
    lc.setRow(ADDR, 6, CHAR_r);
    lc.setRow(ADDR, 5, CHAR_e);
    lc.setRow(ADDR, 4, CHAR_s);
    lc.setRow(ADDR, 3, CHAR_s);
    lc.setRow(ADDR, 2, CHAR_SPACE);
    lc.setRow(ADDR, 1, CHAR_i);
    lc.setRow(ADDR, 0, CHAR_t);
}

static void print_count_up() {
    lc.clearDisplay(ADDR);
    lc.setRow(ADDR, 7, CHAR_C);
    lc.setRow(ADDR, 6, CHAR_o);
    lc.setRow(ADDR, 5, CHAR_u);
    lc.setRow(ADDR, 4, CHAR_n);
    lc.setRow(ADDR, 3, CHAR_t);
    lc.setRow(ADDR, 2, CHAR_SPACE);
    lc.setRow(ADDR, 1, CHAR_u);
    lc.setRow(ADDR, 0, CHAR_p);
}

static void print_number(unsigned long number) {
    for(int i=0; i<8; ++i) {
        if (number == 0 && i != 0) {
            lc.setRow(ADDR, i, CHAR_SPACE);
        } else {
            lc.setDigit(ADDR, i, number%10, false);
            number /= 10;
        }
    }
}


#define SNAKE_DELAY 100
char i, digit;
static void print_snake(char nof_loops) {
    Serial.println("Printing snake...");
    lc.clearDisplay(ADDR);

    for (i = 0; i < nof_loops; i++) {
        for (digit = 7; digit >= 0; digit--) {
            Serial.print("Digit is ");
            Serial.print((char)(((int)'0')+digit));
            Serial.print("\n\r");
            if (digit % 2 == 1) {
                lc.setRow(ADDR, digit, SEGM_SW);
                delay(SNAKE_DELAY);

                if (digit == 7) {
                    lc.setRow(ADDR, 0, SEGM_CLEAR);
                } else {
                    lc.setRow(ADDR, digit + 1, SEGM_CLEAR);
                }
                lc.setRow(ADDR, digit, SEGM_SW | SEGM_NW);
                delay(SNAKE_DELAY);

                lc.setRow(ADDR, digit, SEGM_NW | SEGM_N);
                delay(SNAKE_DELAY);

                lc.setRow(ADDR, digit, SEGM_N);
            } else {
                lc.setRow(ADDR, digit, SEGM_NW);
                delay(SNAKE_DELAY);

                lc.setRow(ADDR, digit + 1, SEGM_CLEAR);
                lc.setRow(ADDR, digit, SEGM_NW | SEGM_SW);
                delay(SNAKE_DELAY);

                lc.setRow(ADDR, digit, SEGM_SW | SEGM_S);
                delay(SNAKE_DELAY);

                lc.setRow(ADDR, digit, SEGM_S);
            }
        }
    }
    Serial.println("Snake done.");
}
