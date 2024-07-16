int data;

void setup() { 
  Serial.begin(9600);                               //initialize serial COM at 9600 baudrate
  pinMode(9, OUTPUT); 
  pinMode(10, OUTPUT);
  pinMode(11, OUTPUT);
  pinMode(12, OUTPUT);
  pinMode(13, OUTPUT);//declare the LED pin (13) as output
  digitalWrite (9, LOW);   
  digitalWrite (10, LOW);
  digitalWrite (11, LOW);
  digitalWrite (12, LOW);
  digitalWrite (13, LOW);//Turn OFF the Led in the beginning
  
  Serial.println("Hello!,How are you Python ?");
}
void loop() {
  while (Serial.available())    //whatever the data that is coming in serially and assigning the value to the variable “data”
  { 
  data = Serial.read();
  }
  if (data == '0')
  {
  digitalWrite (9, 0);                  //Turn On the Led
  digitalWrite (10, 0); 
  digitalWrite (11, 0); 
  digitalWrite (12, 0); 
  digitalWrite (13, 0); 
  }
  else if (data == '1')
  {
  digitalWrite (9, 1);                  //Turn On the Led
  digitalWrite (10, 0); 
  digitalWrite (11, 0); 
  digitalWrite (12, 0); 
  digitalWrite (13, 0);                  //Turn OFF the Led
  }
  else if (data == '2')
  {
  digitalWrite (9, 1);                  //Turn On the Led
  digitalWrite (10, 1); 
  digitalWrite (11, 0); 
  digitalWrite (12, 0); 
  digitalWrite (13, 0);
  }
  else if (data == '3')
  {
  digitalWrite (9, 1);                  //Turn On the Led
  digitalWrite (10, 1); 
  digitalWrite (11, 1); 
  digitalWrite (12, 0); 
  digitalWrite (13, 0);
  }
  else if (data == '4')
  {
  digitalWrite (9, 1);                  //Turn On the Led
  digitalWrite (10, 1); 
  digitalWrite (11, 1); 
  digitalWrite (12, 1); 
  digitalWrite (13, 0);
  }
  else if (data == '5')
  {
  digitalWrite (9, 1);                  //Turn On the Led
  digitalWrite (10, 1); 
  digitalWrite (11, 1); 
  digitalWrite (12, 1); 
  digitalWrite (13, 1);
  }
  else 
  {
  digitalWrite (9, 0);                  //Turn On the Led
  digitalWrite (10, 0); 
  digitalWrite (11, 0); 
  digitalWrite (12, 0); 
  digitalWrite (13, 0); 
  }
}
