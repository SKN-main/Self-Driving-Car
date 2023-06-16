#pragma once
// #include <elapsedMillis.h>
// #include <Servo.h>
#include <Wire.h>

#define SCB_AIRCR (*(volatile uint32_t *)0xE000ED0C) // Application Interrupt and Reset Control location

//Timing
// elapsedMillis elapsedTime;
// elapsedMillis blinkTime;


// constants for motor driver
// const uint8_t IN1=25;
// const uint8_t IN2=26;
// const uint8_t ENA=23;

// const uint8_t IN3=27;
// const uint8_t IN4=28;
// const uint8_t ENB=22;

// enum direction {
//     dirForward,
//     dirBackwards,
//     dirRotatingLeft,
//     dirRotatingRight
// };

// direction currentDirection;
// bool isBreaking = false;


//constants for ESP8266
// const uint8_t ESP8266_RST = 29, ESP8266_CH_PD = 30;


//Constants for Lidar 
// VL53L1X distanceSensor;

const uint8_t Lidar_XSHUT = 36;
enum LidarDistanceMode 
{
    near = 0,
    medium = 1,
    far = 2
};


// enum class EngineSelector
// {
// 	Left,
// 	Right
// };

// enum class ServoSelector{
//     Yaw,
//     Pitch
// };


//constants for debug LED
const uint8_t LED_BUILTIN_TEENSY = 13;
// boolean ledState = HIGH;


//constants for servos
//left-right
// Servo servoYaw;
// int yawMin = 45, yawMax = 135, yawCenter = 90;
// //up-down
// Servo servoPitch;
// int pitchMin = 45, pitchMax = 135, pitchCenter = 90;





