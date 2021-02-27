#include <ros/ros.h>
#include <wiringPi.h>
#include <iostream>
#include <string>
#include <ros/console.h>

#define LED_PIN 25 // change pin number here

int main (int argc, char **argv)
{
    ros::init(argc, argv, "pid1");
    ros::NodeHandle nh;
//    begin = begin + 5;
    wiringPiSetupGpio();
    pinMode(LED_PIN, OUTPUT);
    ROS_INFO("GPIO has been set as OUTPUT.");

    //time = rospy.get_time()
    //TIME_INC = 0.05
    while (ros::ok())
    {
        ///if (rospy.get_time() > time)
        //    ... time = time + TIME_INC 
        std::cout << 12 << "whatever text" << std::endl;    
        digitalWrite(LED_PIN, HIGH);
        ROS_INFO("Set GPIO IGH");
        ros::Duration(1.0).sleep();
        digitalWrite(LED_PIN, LOW);
        ROS_INFO("Set GPIO LOW");
        ros::Duration(1.0).sleep();
    }
}
