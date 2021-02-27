#include <ros/ros.h>
#include <wiringPi.h>
#include <stdio.h>
#include <string.h>
#include <errno.h>
#include <stdlib.h>

#define BUTTON_PIN 25

int deg = 0;

volatile int eventCounter = 0;

void myInterrupt(void)
     {
	eventCounter++;
     }

int main (int argc, char **argv)
{
    if (wiringPiSetup() > 0){
	printf(stderr, "unable to setup wiring: %s\n", strerror(errno));
	return 1;	
    }
    if (wiringPiISR (BUTTON_PIN, INT_EDGE_FALLING, &myInterrupt)  < 0) {
	printf(stderr, "Unable to setup isr: %s\n",stderror(errno));
	return 1;

    }
	
    while (1) {
	printf("%d\n", eventCounter);
	eventCounter = 0;
	delay(1000);
    }


    ros::init(argc, argv, "tacho1");
/*
    ros::NodeHandle nh;
    // publish the interrupt (deg) into topic / tacho1
    // msg: std_msgs int64
     
    while (ros::ok())
    {

    }
    
*/
}
