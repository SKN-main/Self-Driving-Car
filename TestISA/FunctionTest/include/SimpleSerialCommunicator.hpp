#pragma once
#include <Arduino.h>
#include <TeensyTimerTool.h>
#include <vector>

// DO NOT USE IN PR$ODUCTION CODE
// Simple, non-blocking serial communication protocol quickstart
// https://www.pjrc.com/teensy/td_serial.html
// https://www.pjrc.com/teensy/td_uart.html
class SimpleSerialCommunicator
{

private:

    bool m_isInitialized = false;
    bool m_serialTimeoutInMiliseconds = 3000;
    bool m_hasNewMessage = false;
    String m_message = "";
    std::vector<char> m_messageBuffer;
    const int m_messageBufferMaxSize = 128;
    String m_messageStartMarker = "";
    String m_messageEndMarker = "";

public:
    SimpleSerialCommunicator()
    {

    }

    //Serial on Teensy - baud rate is ignored; always communicates with max USB speed
    SimpleSerialCommunicator(int baudRate, String startMarker = "", String endMarker = "" ) : m_messageStartMarker{startMarker}, m_messageEndMarker{endMarker}
    {
        Initialize(baudRate);
    }


    void Initialize(int baudRate)
    {
        uint32_t elapsedTime = 0;
        uint32_t startTime = millis();
        Serial.begin(baudRate);
        while (!Serial && elapsedTime < m_serialTimeoutInMiliseconds) 
        {
            // wait up to Timeout seconds for Serial Monitor initialization
            elapsedTime = startTime + millis();
        }

        if (Serial) 
        {
            m_messageBuffer = std::vector<char>(m_messageBufferMaxSize);
            m_isInitialized = true;
            Serial.println("Serial Communication Initialized");
        }

    }


    bool HasData()
    {
        CheckForNewData();
        return m_hasNewMessage;
    }

    String GetMessage()
    {
        if (m_hasNewMessage)
        {
            
            m_hasNewMessage = false;
            String returnedMessage = m_message.trim().toLowerCase();
            m_message = "";
            return returnedMessage;
        }
        else
        {
            return "";
        }
    }

private:

    void CheckForNewData()
    {
        while(Serial.available())
        {
            char incomingByte = Serial.read();  // will not be -1;
            if (incomingByte == '\n')
            {
                m_hasNewMessage = true;
            }
            else 
            {
                m_hasNewMessage = false;
            }
            m_message += (char)incomingByte;
        }

    }

};

