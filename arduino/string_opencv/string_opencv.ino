#include <Servo.h>
#define numofvalsRec 5
#define digitsPerVal 1

Servo servoThumb;
Servo servoIndex;
Servo servoMiddle;
Servo servoRing;
Servo servoPinky;


int valRec[numofvalsRec];
int stringlngth = numofvalsRec * digitsPerVal + 1; //$00000
int counter = 0;
bool counterStart = false;
String recString;

void setup() {
  Serial.begin(115200);
  servoThumb.attach(50);
  servoIndex.attach(52);
  servoMiddle.attach(9);
  servoRing.attach(7);
  servoPinky.attach(10);

}
void recData(){
  while (Serial.available())
  {
    char c = Serial.read();
    if(c == '$'){
      counterStart = true;
    }
    if (counterStart){
      if(counter < stringlngth){
        recString = String(recString + c);
        counter++;
      }
      if (counter >= stringlngth){
        for(int i = 0; i<numofvalsRec; i++){
        int num = (i*digitsPerVal)+1;
        valRec[i] = recString.substring(num,num + digitsPerVal).toInt();
      }
      recString = "";
      counter = 0;
      counterStart = false;
    }
  }
}
}
void loop() {
  recData();
  if (valRec[0] == 1){servoThumb.write(180);}else{servoThumb.write(0);}
  if (valRec[1] == 1){servoIndex.write(180);}else{servoIndex.write(0);}
  if (valRec[2] == 1){servoMiddle.write(180);}else{servoMiddle.write(0);}
  if (valRec[3] == 1){servoRing.write(180);}else{servoRing.write(0);}
  if (valRec[4] == 1){servoPinky.write(180);}else{servoPinky.write(0);}


}
