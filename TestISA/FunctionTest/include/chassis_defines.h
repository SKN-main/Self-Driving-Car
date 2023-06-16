#pragma once
#include <array>


namespace chassis_defines
{
    // Defines/constants for V3 chassis - based on Traxxas 4-tec 3.0 (Corvette Stingray body)

    const int TRAXXAX_PWM_MICROSECONDS_MIN = 1000;
    const int TRAXXAS_PWM_MICROSECONDS_MAX = 2000;
    const int TRAXXAS_PWM_MICROSECONDS_ZERO = 1500;
    // const int STEERING_SERVO_TRIM_IN_MILISECONDS = 0;
    const int STEERING_SERVO_TRIM_IN_MILISECONDS = -300; // - TEMPORARY - for old platform and straight ahead (pitch)


    const int WATCHDOG_MAX_TIME_BETWEEN_COMMANDS_IN_MILISECONDS = 3500;  // was 1500
    const int MOTOR_PIN = 23; // Temporary - Yaw (mf 50 - slightly left, mr 50 - slightly right)
    const int STEERING_PIN = 22; //Temporary - Pitch (sl 80 is front (NEVER GO ABOVE 90); sr 80 is up)
    const float MOTOR_POWER_LEVEL_DEFAULT_CONSTRAINT_FORWARD = 1.0f; 
    const float MOTOR_POWER_LEVEL_DEFAULT_CONSTRAINT_BACKWARD = -1.0f; 
    const float STEERING_SWING_DEFAULT_CONSTRAING_LEFT = -1.0f; 
    const float STEERING_SWING_DEFAULT_CONSTRAING_RIGHT = 1.0f; 



    const int ULTRASONIC_NUMBER_OF_SENSORS = 3; // Number of sensors.
    const std::array<uint8_t, ULTRASONIC_NUMBER_OF_SENSORS> ultrasonicTriggerPins = {11, 9, 24};
    const std::array<uint8_t, ULTRASONIC_NUMBER_OF_SENSORS> ultrasonicEchoPins = {10, 8, 12};

    const std::array<std::array<int, 3>, ULTRASONIC_NUMBER_OF_SENSORS> sensorOffsetsXYZFromOriginInMilimeters = {{{0, 0, 0}, {0, 0, 0}, {0, 0, 0}}};
    const std::array<String, ULTRASONIC_NUMBER_OF_SENSORS> sensorDescriptions = {"Left Front", "Right Front", "Rear"};

    const int ULTRASONNIC_MAX_DISTANCE = 200; // Maximum distance (in cm) to ping.
    const int ULTRASONIC_PING_INTERVAL = 30; // Milliseconds between sensor pings (29ms is about the min to avoid cross-sensor echo).

}

