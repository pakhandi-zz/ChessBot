#include<SoftwareSerial.h>
SoftwareSerial esp(0,1);
char c;
void setup() {
  // put your setup code here, to run once:
esp.begin(9600);
Serial.begin(9600);
}

void loop() {
  // put your main code here, to run repeatedly:
  if(esp.available()>0){
  c=esp.read();
  Serial.print(c);}
  //if(c>='0'&&c<='9')
    //  Serial.print(c);
}
