#include <Arduino.h>
#include "helper_functions.hpp"
#include <Chassis.hpp>
#include <SimpleSerialCommunicator.hpp>
#include <fstream>
#include <iostream>
#include <Ethernet.h>
#include <cstring>

// Main chassis definition
Chassis traxxas4_tec;
SimpleSerialCommunicator comm;
bool left = 0;
bool down = 0;
bool up = 0;
bool right = 0;


void printHelp()
{
	Serial.println("Help:");
	
	Serial.println("  mD p   - set the motor speed and direction");
	Serial.println("  	  D (direction): 'F'-forwards, 'R'-reverse, 'S'-stop");
	Serial.println("   	  p (level/speed): 0-100");
	
	Serial.println("  sD p   - set the steering level");
	Serial.println("  	  D (direction): 'L'-left, 'R'-right");
	Serial.println("   	  p (level): 0-100");
	
	Serial.println("  reset   - reset");
	Serial.println("  selftest   - perform a full self-test. WARNING - WILL MOVE MOTORS FULL SPEED");
}

void resetTeensy()
{
	Serial.println("Ok.");
	_softRestart();
	while(1);
}


int parseMotorsCommand(String command)
{
	String s = command;

	if (s.length() < 2) {
		Serial.println("Command 'm': command syntax error");
		return 0;
	}
	
	int direction = tolower(s[1]);
	int power = 0;
	if (s.indexOf(" ") != -1) {
		s = s.substring(s.lastIndexOf(" ") + 1);
		char *endptr = NULL;
		power = strtol(s.c_str(), &endptr, 10);
		if (*endptr != '\0') {
			Serial.println("Command 'm': error in power level syntax");
			return 0;
		}
	}
	power = constrain(power, 0, 100);
	
	if (strchr("frs", direction) == NULL) {
		Serial.println("Command 'm': error in direction syntax");
		return 0;
	}
	
	if (direction != 's' && power == 0) {
		Serial.println("Command 'm': power level not set properly");
		return 0;
	}
		

	if (direction == 'r')
	{
		power *= -1;
	}

	return power;

}

int parseSteeringCommand(String command)
{
	String s = command;
	if (s.length() < 2) {
		Serial.println("Command 's': command syntax error");
		return 0;
	}
	
	int direction = tolower(s[1]);
	int level = -1000;

	if (s.indexOf(" ") != -1) {
		s = s.substring(s.lastIndexOf(" ") + 1);
		char *endptr = NULL;
		level = strtol(s.c_str(), &endptr, 10);
		if (*endptr != '\0') {
			Serial.println("Command 's': servo position syntax error");
			return 0;
		}
	}
	
	if (level == -1000) {
		Serial.println("Command 's': level not set properly");
		return 0;
	}
	level = constrain(level, 0, 100);

	if (strchr("lr", direction) == NULL) {
		Serial.println("Command 's': direction syntax error");
		return 0;
	}

	if (direction == 'l')
	{
		level*=-1;
	}

	return level;
}

void setup() {
  	// put your setup code here, to run once:
	delay(1000);
	Serial.begin(115200);
  	Serial.setTimeout(1.5);
	for (int i = 0; i < 10; i++)
	{
		Serial.print((char)(43+2*(i&1)));
		delay(200);
	}
	Serial.println("");
	
	// Initialize Serial communication
    // initSerial();
	comm.Initialize(115200);

	//initialize builtin LED
    initLED();

	// Initialize Chassis
	traxxas4_tec.Initialize();
	//make sure that motors and servos are in neutral position
	traxxas4_tec.SetNeutral();
    delay(500);

    Serial.println("Initalization ended");


 	Serial.println();
	Serial.println("#========================================================#");
	Serial.println("# Inteligentne Systemy Autonomiczne IIS                  #");
	Serial.println("# Platform tester v3.0 by Pawel Kapusta                  #");
	Serial.println("# original code by Tomasz Jaworski                       #");
	Serial.println("#========================================================#");
	Serial.print("  Kompilacja: ");
	Serial.print(__DATE__);
	Serial.print(", ");
	Serial.println(__TIME__);
	
	Serial.println("Commands must end with character: '\\n'.");
	Serial.println("ARDUINO IDE: Change 'No line ending' to 'Newline' in the lower portion of console window...\n");
	traxxas4_tec.SetSteering(0);
	delay(2000);
}

int SPEED_VALUE = 0;
int TURN_VALUE = 0;

void loop() 
{
  	String command_value = "";
	String command = "";
	String turn_value = "";

	if (Serial.available())
	{
		command_value = Serial.readString();

		int split_index = 1;
		command = command_value[0];

		// Serial.println(split_index);

		for (int i = split_index + 1; i < (int)command_value.length(); i++){
			turn_value += command_value[i];
		}
		
		TURN_VALUE = turn_value.toInt();

		// Serial.println(command);
		// Serial.println(turn_value);
		if(command == 'r')
		{
			left = 0;
			right = 0; 
			up = 0;
			down = 0;
			traxxas4_tec.SetSteering(0);
			traxxas4_tec.SetSpeed(0);
			//traxxas4_tec.SetNeutral();
		}
		if(command == 'a')
		{
			//traxxas4_tec.SetSteering(-80);
			//if(TURN_VALUE != -80)
			{
				left = 1;
				right = 0;
				// TURN_VALUE = -80;
				TURN_VALUE *= -1; 
			}
			
		}
		if(command == 'd')
		{
			//traxxas4_tec.SetSteering(80);
			//if(TURN_VALUE != 80)
			{
				right = 1;
				left = 0;
				// TURN_VALUE = 80;
			}
			
		}
		if(command == "w")
		{
			//traxxas4_tec.SetSpeed(30);
			if(down)
			{
				traxxas4_tec.SetSpeed(0);
				//delay(100);
			}
			traxxas4_tec.SetSteering(0);
			delay(50);
			left = 0;
			right = 0;
			up = 1;
			down = 0;
			SPEED_VALUE = 10;
			
			
		}
		if(command == "s")
		{
			if(up)
			{
				//delay(10);
				traxxas4_tec.SetSteering(0);
				delay(10);
				traxxas4_tec.SetSpeed(0);
				//delay(100);
				
			}
			//if(SPEED_VALUE!=-10)
			{
				down = 1;
				up = 0;
				SPEED_VALUE = -10;
			}
			
		}
	}
	if(left )
	{
		// traxxas4_tec.SetSteering(-80);
		traxxas4_tec.SetSteering(TURN_VALUE);
	}
	if(right )
	{
		// traxxas4_tec.SetSteering(80);
		traxxas4_tec.SetSteering(TURN_VALUE);
	}
	if(up)
	{
		traxxas4_tec.SetSpeed(11);
	}
	if(down )
	{
		traxxas4_tec.SetSpeed(-30);
	}
	//Serial.print(x + 1);
	if (comm.HasData())
	{
		String s = comm.GetMessage();
		Serial.println(s);

		if (s == "help")
		{
			printHelp();

		}
		else if (s == "reset") 
		{
			resetTeensy();
		}
		
		else if (s == "selftest")
		{
			Serial.println("Starting self-test.");
			Serial.println("Testing steering");
			
			delay(1000);
			Serial.println("Max left");
			traxxas4_tec.SetSteering(-100);
			delay(2000);
			Serial.println("Half left");
			traxxas4_tec.SetSteering(-50);
			delay(2000);
			Serial.println("Neutral");
			traxxas4_tec.SetSteering(0);
			delay(2000);
			Serial.println("Half right");
			traxxas4_tec.SetSteering(50);
			delay(2000);
			Serial.println("Max right");
			traxxas4_tec.SetSteering(100);
			delay(2000);
			Serial.println("Neutral");
			traxxas4_tec.SetNeutral();
		    delay(1000);
			
			Serial.println("Testing motors");
			delay(1000);
			Serial.println("Neutral");
			traxxas4_tec.SetSpeed(0);
			delay(2000);
			Serial.println("20 \% speed");
			traxxas4_tec.SetSpeed(20);
			delay(2000);
			Serial.println("50 \% speed");
			traxxas4_tec.SetSpeed(50);
			delay(2000);
			Serial.println("100 \% speed");
			traxxas4_tec.SetSpeed(100);
			delay(2000);
			Serial.println("Neutral");
			traxxas4_tec.SetSpeed(0);
			delay(2000);
			Serial.println("20 \% reverse");
			traxxas4_tec.SetSpeed(-20);
			delay(2000);
			traxxas4_tec.SetSpeed(-30);
			delay(2000);
			traxxas4_tec.SetSpeed(-40);
			delay(2000);
			Serial.println("50 \% reverse");
			traxxas4_tec.SetSpeed(-50);
			delay(2000);
			Serial.println("100 \% reverse");
			traxxas4_tec.SetSpeed(-100);
			delay(2000);
			Serial.println("Neutral");
			traxxas4_tec.SetNeutral();

			delay(1000);
			Serial.println("Self-test DONE");

		}

		else if (s == "distance")
		{

			auto distances = traxxas4_tec.ultrasonicSensors.GetDistancesInCentimeters();
			auto descriptions = traxxas4_tec.ultrasonicSensors.GetSensorNames();

			for (unsigned int i = 0; i< distances.size(); i++ )
			{
				Serial.println("Sensor: " + descriptions.at(i) + "; Distance: " + distances.at(i) + " cm");
			}
			
		}

		else if (s.startsWith("m")) 
		{
			int motorsPower = parseMotorsCommand(s);
			char msg[128];
			sprintf(msg, "Motor settings: power=%d\n", motorsPower);
			Serial.print(msg);
			traxxas4_tec.SetSpeed(motorsPower);
		}
		
		else if (s.startsWith("s")) 
		{
			int steeringLevel = parseSteeringCommand(s);
			char msg[128];
			sprintf(msg, "Steering servo setting: position/level=%d\n", steeringLevel);
			Serial.print(msg);
			traxxas4_tec.SetSteering(steeringLevel);

		}
		else
		{
			Serial.print(" Command '");
			Serial.print(s);
			Serial.print(" is unknown; Maybe try 'help'?\n");
		}

	}
}