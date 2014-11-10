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
       
       
To display a one "1", you need to light up segments 5,6
=> in binary: 0b00110000

*/

#define SEGM_CLEAR 0b00000000
#define SEGM_N 0b01000000
#define SEGM_NW 0b00000010
#define SEGM_NE 0b00100000
#define SEGM_SW 0b00000100
#define SEGM_MID 0b00000001
#define SEGM_SE 0b00010000
#define SEGM_S 0b00001000
#define SEGM_DOT 0b10000000

#define CHAR_0 0b01111110
#define CHAR_1 0b00110000
#define CHAR_2 0b01101101
#define CHAR_3 0b01111001
#define CHAR_4 0b00110011
#define CHAR_5 0b01011011
#define CHAR_6 0b01011111
#define CHAR_7 0b01110000
#define CHAR_8 0b01111111
#define CHAR_9 0b01111011
#define CHAR_a 0b01110111
#define CHAR_b 0b00011111
#define CHAR_c 0b00001101
#define CHAR_C 0b01001110
#define CHAR_d 0b00111101
#define CHAR_e 0b01001111
#define CHAR_f 0b01000111
#define CHAR_g 0b01111011
#define CHAR_h 0b00010111
#define CHAR_H 0b00110111
#define CHAR_i 0b00000100
#define CHAR_I 0b00000110
#define CHAR_j 0b00111000
#define CHAR_k 0b00001101
#define CHAR_l 0b00001110
#define CHAR_m 0b01110110
#define CHAR_n 0b00010101
#define CHAR_o 0b00011101
#define CHAR_O 0b01111110
#define CHAR_ouml 0b01011101
#define CHAR_p 0b01100111
#define CHAR_q 0b01110011
#define CHAR_r 0b00000101
#define CHAR_s 0b01011011
#define CHAR_t 0b00001111
#define CHAR_u 0b00011100
#define CHAR_U 0b00111110
#define CHAR_uuml 0b01011100
#define CHAR_y 0b00110011
#define CHAR_z 0b01101101
#define CHAR_SPACE 0b00000000
#define CHAR_DOT 0b10000000
#define CHAR_MINUS 0b00000001
#define CHAR_UNDERSCORE 0b00001000
#define CHAR_EQUAL 0b00001001
#define CHAR_EXCLAMATION 0b10100000
#define CHAR_COMMA 0b10000000
