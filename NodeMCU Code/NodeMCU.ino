/*
▪ * Team Id: 2317
▪ * Author List: Aniket Pratap Singh
▪ * Filename: NodeMCUCode
▪ * Theme: eYRC-NT
▪ * Functions: laser_pointer,servo_rotate,find_laser_angle, find_axial_angle, cellchange, callback
▪ */
#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <Servo.h>
#include<string.h>
 
Servo myservo;  // create servo object to control a servo 
Servo myservo1;

const char* ssid = "RPi-2317";
const char* password = "firebird";
const char* mqtt_server = "192.168.10.1";

WiFiClient espClient;
PubSubClient client(espClient);
long lastMsg = 0;
char msg[50];
int value = 0;
char* message;
// twelve servo objects can be created on most boards
void servo_rotate(Servo myservo,int start_angle,int end_angle){
  int pos;
  if(start_angle<end_angle){
    for(pos = start_angle; pos <= end_angle; pos += 1) // goes from 0 degrees to 180 degrees 
      {                                  // in steps of 1 degree 
        myservo.write(pos);              // tell servo to go to position in variable 'pos' 
        delay(15);                       // waits 15ms for the servo to reach the position 
      }
    }
  else
    for(pos = start_angle; pos >= end_angle; pos -= 1) // goes from 0 degrees to 180 degrees 
    {                                  // in steps of 1 degree 
       myservo.write(pos);              // tell servo to go to position in variable 'pos' 
       delay(15);                       // waits 15ms for the servo to reach the position 
    }
}

void laser_pointer(int level, int cellnum){
  int t,axial_angle,laser_angle;
  if(level == 1){
    t=360/4;
    laser_angle = 30.219;
  }
  else if(level==2){
    t=360/10;
    laser_angle = 45.127;
  }
  else if(level == 3){
    t=360/15;
    laser_angle = 60.33;
  }
  else if(level== 4){
    t=360/20;
   laser_angle = 75.22;
  }
   axial_angle = cellnum*t;

   if(axial_angle < 180){
    myservo.write(axial_angle);
    myservo1.write(90-laser_angle);
    delay(15);
   }
   else if(axial_angle > 180){
    myservo.write(axial_angle-180);
    myservo1.write(90+laser_angle);
    delay(15);
   }
   
}
float find_laser_angle(int level){
  float laser_angle;
  if(level == 0){
    laser_angle = 0;
  }
  if(level == 1){
    laser_angle = 30.219;
  }
  else if(level==2){
    laser_angle = 45.127;
  }
  else if(level == 3){
    laser_angle = 60.33;
  }
  else if(level== 4){
   laser_angle = 75.22;
  }
  return laser_angle;
}

int find_axial_angle(int level,int cellnum){
  int t,axial_angle,laser_angle;
  if(level == 1){
    t=360/4;
    laser_angle = 30.219;
  }
  else if(level==2){
    t=360/10;
    laser_angle = 45.127;
  }
  else if(level == 3){
    t=360/15;
    laser_angle = 60.33;
  }
  else if(level== 4){
    t=360/20;
   laser_angle = 75.22;
  }
   axial_angle = cellnum*t;
  return axial_angle;
}
int cell_change(int sl,int sc,int el, int ec){
  int find_axial_angle(int level,int cellnum);
  float find_laser_angle(int level);
  int saa,sla,eaa,ela;
  saa = find_axial_angle(sl,sc);
  sla = find_laser_angle(sl);
  eaa = find_axial_angle(el,ec);
  ela = find_laser_angle(el);
  int pos1,pos2;
  if(sl!=el){
    if(saa>eaa){
  for(pos1=saa,pos2=sla; pos1<=eaa,pos2<=ela; pos1+=1,pos2+=1){
    if(pos1<180){
    myservo.write(pos1);
    myservo1.write(90-pos2);
    delay(100);
    }
    if(pos1==180){
    myservo.write(pos1-180);
    myservo1.write(90+pos2);
    delay(1000);
    }
    if(pos1>180){
    myservo.write(pos1-180);
    myservo1.write(90+pos2);
    delay(100);
    }
   }
  }
  else if(saa<eaa){
    for(pos1=saa,pos2=sla; pos1<=eaa/2,pos2<=ela/2; pos1+=1,pos2+=1){
    if(pos1<180){
    myservo.write(pos1);
    myservo1.write(90-pos2);
    delay(100);
    }
    if(pos1==180){
    myservo.write(pos1-180);
    myservo1.write(90+pos2);
    delay(1000);
    }
    if(pos1>180){
    myservo.write(pos1-180);
    myservo1.write(90+pos2);
    delay(100);
    }
   }

   for(pos1=eaa/2,pos2=ela/2; pos1<=eaa,pos2<=ela; pos1+=1,pos2+=1){
    if(pos1<180){
    myservo.write(pos1);
    myservo1.write(90-pos2);
    delay(100);
    }
    if(pos1==180){
    myservo.write(pos1-180);
    myservo1.write(90+pos2);
    delay(1000);
    }
    if(pos1>180){
    myservo.write(pos1-180);
    myservo1.write(90+pos2);
    delay(100);
    }
   }
  }
  }
  else if(sl==el){
    for(pos1=saa; pos1<=eaa; pos1+=1){
    if(pos1<180){
    myservo.write(pos1);
    delay(100);
    }
    if(pos1==180){
    myservo.write(pos1-180);
    delay(1000);
    }
    if(pos1>180){
    myservo.write(pos1-180);
    delay(100);
    }
   }
  }
  }

void setup() 
{ Serial.begin(115200);
  myservo.attach(2);  // attaches the servo on GIO2 to the servo object 
  myservo1.attach(15);
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
} 
void setup_wifi() {

  delay(10);
  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

/*
▪ * Function Name:callback
▪ * Input: topic, payload,lentgh
▪ * Output: it runs the 
▪ * Logic: <Description of the function performed and the logic used
▪ * in the function>
▪ * Example Call: <Example of how to call this function>
▪ */ 
void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  int i;
  message = "";
  for (i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
    message[i] = (char)payload[i];
  }
  message[i+1] = '\0';
  Serial.println();
}
void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Attempt to connect
    if (client.connect("ESP8266Client")) {
      Serial.println("connected");
      // Once connected, publish an announcement...
      //client.publish("outTopic", "hello world");
      // ... and resubscribe
      client.subscribe("toNodeMCU");
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}
void loop() 
{ 
  if (!client.connected()) {
    reconnect();
  }
  client.loop();

  int cell_change(int sl,int sc,int el, int ec);
  void servo_rotate(Servo myservo,int start_angle,int end_angle);
  myservo.write(0);
  myservo1.write(0);
  char* str;
  /*myservo1.write(90-45.757);
  delay(1000);
  servo_rotate(myservo,0,190);*/
  if (message[0] == '['){
    strcpy(str,message);
    Serial.println(str);
  }
  if (message == "")
  {
    Serial.println("Path not received");
  }
  if(str){
    client.publish("toRPi", "follow");
  int i,l,c,pl=4,pc=1,d1,d2,ppl,ppc,pppl,pppc;
  for(i=0;str[i]!='\0';i+=1){
    if(str[i]=='['&& str[i+1]=='['){
      l=str[i+3]-48;
      if(str[i+7]==')'){
      c=str[i+6]-48;
      i+=6;
      }
      else{
        d1 = str[i+6]-48;
        d2 = str[i+7]-48;
        c = d1*10 + d2;
        i+=7;
      }
    }
    if(str[i]==')'&& str[i+1]==','){
      l=str[i+4]-48;
      if(str[i+8]==')'){
      c=str[i+7]-48;
      i+=7;
      }
      else{
        d1 = str[i+7]-48;
        d2 = str[i+8]-48;
        c = d1*10 + d2;
        i+=8;
      }
    }
    if(str[i]==']'&& str[i+1]==','){
      //send message to read the checkpoint
      client.publish("toRPi", "stop");
      client.publish("toRPi", "detect_checkpoint");
      delay(1000);
      client.publish("toRPi", "follow");
      l=str[i+5]-48;
      if(str[i+9]==')'){
      c=str[i+8]-48;
      i+=8;
      }
     else{
        d1 = str[i+8]-48;
        d2 = str[i+9]-48;
        c = d1*10 + d2;
        i+=9;
      }
    }
    if(str[i]==')' && str[i+1]==']' && str[i+2]==']'){
      client.publish("toRPi", "stop");
      break;
    }
    if(l==pl && pl == ppl && ppl == pppl && pppc==c && ppc ==pc){
      client.publish("toRPi", "turn_around");
      delay(2000);
      client.publish("toRPi", "follow");
    } 
    cell_change(pl,pc,l,c);
    pl=l;
    pc=c;
    ppc=pc;
    ppl=pl;
    pppc=ppc;
    pppc=ppl;
    Serial.print(l);
    //Serial.println(l,",",c);
    Serial.print(",");
    Serial.print(c);
    Serial.print("\n");
    }
  }
  }
  
  /*servo_rotate(myservo,180,0);
  servo_rotate(myservo1,0,180);
  servo_rotate(myservo1,180,0);*/

