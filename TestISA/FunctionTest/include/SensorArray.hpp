#pragma once
#include <vector>
#include <UltrasonicSensor.hpp>
#include <chassis_defines.h>


class SensorArray
{
private:
    std::vector<UltrasonicSensor> sensors;
    bool m_isInitialized = false;
    // unsigned long pingTimer[SONAR_NUM]; // Holds the times when the next ping should happen for each sensor.
    // unsigned int distances[SONAR_NUM];         // Where the ping distances are stored.
    // uint8_t currentSensor = 0;          // Keeps track of which sensor is active.
    // bool isObstacle[SONAR_NUM] = {false};

public:
    SensorArray()
    {

    }

    void Initialize()
    {
        InitializeSensors();
        m_isInitialized = true;
    }


    std::vector<unsigned int> GetDistancesInCentimeters()
    {
        std::vector<unsigned int> distances;

        for (auto &sensor : sensors)
        {
            distances.push_back(sensor.GetDistanceInCentimeters());

        } 
        return distances;
    }

    std::vector<String> GetSensorNames()
    {
        std::vector<String> names;

        for (auto & sensor : sensors)
        {
            names.push_back(sensor.sensorDescription);
        }
        return names;
    }


private:
    void InitializeSensors()
    {
        sensors.reserve(chassis_defines::ULTRASONIC_NUMBER_OF_SENSORS);
        for (int i = 0; i < chassis_defines::ULTRASONIC_NUMBER_OF_SENSORS; i++)
        {
            sensors.emplace_back(UltrasonicSensor(chassis_defines::ultrasonicTriggerPins[i], 
                                 chassis_defines::ultrasonicEchoPins[i], 
                                 chassis_defines::ULTRASONNIC_MAX_DISTANCE, 
                                 chassis_defines::sensorDescriptions[i],
                                 chassis_defines::sensorOffsetsXYZFromOriginInMilimeters[i] ));

        }

    }
};