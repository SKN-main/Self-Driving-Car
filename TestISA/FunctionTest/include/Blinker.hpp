#pragma once
#include <Arduino.h>
#include <TeensyTimerTool.h>

class Blinker
{
 public:
    Blinker(unsigned _pin, unsigned _period) // add blink period to the constructor
    {
        pin = _pin;
        period = _period;
    }

    void begin()  // better not initalizie peripherals in constructors
    {
        pinMode(pin, OUTPUT);
        timer.begin([this] { this->blink(); }, period);
    }

 protected:
    void blink() const // this will be called by the timer
    {
        digitalWriteFast(pin, !digitalReadFast(pin));
    }

    unsigned pin, period;
    TeensyTimerTool::PeriodicTimer timer;
};