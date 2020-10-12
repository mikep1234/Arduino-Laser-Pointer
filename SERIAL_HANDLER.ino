#include <Servo.h>
Servo Bottom;
Servo Top;
int Bottom_pos = 90;
int Top_pos = 90;

void setup() {
  Bottom.attach(12);
  Top.attach(11);
  Serial.begin(115200);
  pinMode(13, OUTPUT);
}

void loop() {
  while(Serial.available()){
    char x = Serial.read();
    if(x == 'F'){
      digitalWrite(13, HIGH);
    }
    else if(x == 'S'){
      digitalWrite(13, LOW);
    }
    else if(x == 'U'){
      if(Top_pos + 5 >= 180){
        Top_pos = 180;
        Top.write(Top_pos);
      }
      else{
        Top_pos += 5;
        Top.write(Top_pos);
      }
    }
    else if(x == 'D'){
      if(Top_pos - 5 <= 0){
        Top_pos = 0;
        Top.write(Top_pos);
      }
      else{
        Top_pos -= 5;
        Top.write(Top_pos);
      }
    }
    else if(x == 'L'){
      if(Bottom_pos - 5 <= 0){
        Bottom_pos = 0;
        Bottom.write(Bottom_pos);
      }
      else{
        Bottom_pos -= 5;
        Bottom.write(Bottom_pos);
      }
    }
    else if(x == 'R'){
      if(Bottom_pos + 5 >= 180){
        Bottom_pos = 180;
        Bottom.write(Bottom_pos);
      }
      else{
        Bottom_pos += 5;
        Bottom.write(Bottom_pos);
      }
    }
  }
}
