#pragma once
#include <NewPing.h>
#include <array>
#include <chassis_defines.h>

class UltrasonicSensor
{
private:
    NewPing m_internalSensor;
    unsigned int m_pingIntervalInMiliseconds = chassis_defines::ULTRASONIC_PING_INTERVAL;

    unsigned int m_latestDistance = 0;

public:
    String sensorDescription = "";
    std::array<int,3> positionOffsetXYZFromOriginInMilimeters;


public:

    UltrasonicSensor(uint8_t triggerPin, uint8_t echoPin, unsigned int maxDistanceInCentimeters, String sensorDescription, std::array<int, 3> positionOffsetXYZFromOriginInMilimeters) : 
                                    m_internalSensor(NewPing(triggerPin, echoPin, maxDistanceInCentimeters)),
                                    sensorDescription{sensorDescription}, 
                                    positionOffsetXYZFromOriginInMilimeters {positionOffsetXYZFromOriginInMilimeters}
    {

    }


    void Initialize()
    {

    }



    unsigned int GetDistanceInCentimeters()
    {
        return TriggerSensor_Blocking();
    }


    void SetPingInterval(unsigned int pingInterval)
    {
        m_pingIntervalInMiliseconds = pingInterval;
    }


private: 
    int TriggerSensor_Blocking()
    {
        int distance = m_internalSensor.ping_cm();
        delay(m_pingIntervalInMiliseconds); // necessary to eliminate sensor crosstalk (echo/sound bounces?)
        return distance;
    }

};