// include the library code:
#include <LiquidCrystal.h>
using namespace std;

// initialize the library with the numbers of the interface pins
LiquidCrystal lcd(12, 11, 5, 4, 3, 2);
int yellowLED = 7;
int redLED = 6;
int buzzer = 9;

bool isHigh = false;
bool isLow = false;
bool lowBeep = false;
bool highBeep = false;
int lowFreq = 1000;
int highFreq = 1000;

void setup() {
  //LED SETUP
  pinMode(yellowLED, OUTPUT);
  pinMode(redLED, OUTPUT);
  pinMode(buzzer, OUTPUT);
  
  // set up the LCD's number of columns and rows:
  lcd.begin(16, 2);
  lcd.print("Connecting...");
  Serial.begin(9600);
}

void loop() {
  if(Serial.available() > 0) {    //if new data
    /* LCD SCREEN AND INPUT CODE */
    isHigh = false;
    isLow = false;
    highBeep = false;
    lowBeep = false;
    //TODO: python input and newline code
    lcd.clear();
    lcd.setCursor(0,0);
    char str[17]; //max amount of chars that would fit
    int index = 0;
    while(Serial.available() > 0){
    char data = Serial.read();
        if(data == '*'){      //char for high BS
          isHigh = true;
          Serial.print("HIGH");
        }
        else if(data == '-'){   //char for low BS
          isLow = true;
          Serial.print("LOW");
        }
        else if(data == '{'){   //char for high beep
          highBeep = true;
        }
        else if(data == '}'){   //char for low beep
          lowBeep = true;
        }
        else if(data == '\n'){ 
           str[index] = '\0';
           lcd.print(str);
           lcd.setCursor(0,1);
           index = 0;      
        }
        else{
          str[index] = data;
          index++;
          if(index >= 32){
            break;
          }
        }
    }
    str[index] = '\0';
    Serial.print(str);
    lcd.print(str);           //print data from python to the LCD
    
    ///////////////////////////////
  
    /* LED AND BUZZER CODE */
    if(isHigh){
      digitalWrite(yellowLED, HIGH);    //turn on yellow light
    }else{
      digitalWrite(yellowLED, LOW);     //turn off yellow light
    }
    if(highBeep){
      tone(buzzer, highFreq);   //beeeeeeep
      delay(500);
    }

    if(isLow){  
      digitalWrite(redLED, HIGH);       //turn on red light
    }else{
      digitalWrite(redLED, LOW);        //turn off red light
    }
    if(lowBeep){
      tone(buzzer, lowFreq);    //beep beep beep
      delay(300);
      noTone(buzzer);
      delay(300);
      tone(buzzer, lowFreq);
      delay(300);
      noTone(buzzer);
      delay(300);
      tone(buzzer, lowFreq);
      delay(300);
    }

    noTone(buzzer);
    /////////////////////////
  }
  delay(1000);
}
 