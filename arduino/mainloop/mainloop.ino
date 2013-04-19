#include "LedControl.h"
#define DIN 11
#define CS 12
#define CLOCK 13

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

LedControl lc = LedControl(DIN,CLOCK,CS,1); 
char display_buffer[8];

void setup(){
  lc.shutdown(0,false);
  lc.setIntensity(0,15);
  Serial.begin(9600);
}

void loop(){
  print8bit();
  delay(300);
  Serial.println("8bit Display is ready!");
  while(1){
    if(Serial.available()>=8){
      Serial.readBytes(display_buffer,8);
      Serial.print("New string received: ");
      printBuffer();
    }
  }
}

void print8bit(){
  lc.setDigit(0,7,8,false);
  lc.setRow(0,6,0b000011111);
  lc.setRow(0,5,0b100);
  lc.setRow(0,4,0b111);
  lc.setRow(0,3,0x00);
  lc.setRow(0,2,0b000011111);
  lc.setDigit(0,1,0xa,false);
  lc.setRow(0,0,0b101);
}

void printBuffer(){
  for(int i =7; i>=0; --i){
    lc.setRow(0,i,display_buffer[7-i]);
    Serial.write(display_buffer[7-i]);
  }
}






