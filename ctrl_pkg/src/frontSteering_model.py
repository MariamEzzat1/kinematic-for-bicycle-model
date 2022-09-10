#!/usr/bin/env python3
import time 
import rospy
from geometry_msgs.msg import Twist
from turtlesim.msg import Pose
from math import atan,cos,sin,pi,tan

'''from yaml'''
Lr=2 #rospy.get_param("/Lr")
Lf=5#rospy.get_param("/Lf")

'''----------------------------------subscriber--------------------------------------'''
'''once the subscriber get a new data save it in current position'''
current_pose=Pose()
def callback_pose(data):
    current_pose.x=data.x
    current_pose.y=data.y
    current_pose.theta=data.theta


'''subscriber node to get the current pose of the turtle from the /turtle1/pose topic'''
def listener():
    rospy.init_node("position_listener",anonymous=True)
    pose_listener=rospy.Subscriber("/turtle1/pose",Pose,callback_pose)
'''----------------------------------publisher------------------------------------------'''
'''publisher node which publishes the linear and angle velociety to turtle1/cmd_vel topic'''
def publishing(beta,delta,sim_time):
    start_time=time.time()
    vel_publisher=rospy.Publisher("/turtle1/cmd_vel",Twist,queue_size=10)
    '''h publish lw l goal bta3y ab3d mn mkan mo3yn so ana mhtaga min dis lets se it 0.5'''
    while (1):
        msg=Twist()
        msg.linear.x,msg.linear.y=linear_velociety(beta)
        msg.linear.z=0
        msg.angular.x=0
        msg.angular.y=0
        msg.angular.z=angular_velociety(beta,delta)
        vel_publisher.publish(msg)
        if(time.time()-start_time-sim_time>0.2):
           break
     


'''function to calculate the X and Y components of the linear velocity''' 
def linear_velociety (beta):
    Vx=lin_vel*cos(beta+current_pose.theta)
    Vy=lin_vel *sin(beta+current_pose.theta)
    return Vx,Vy

    
'''----------------------fuction to calc the angular velocity-------------------------------------'''
def angular_velociety (beta,delta):
    ang =(lin_vel*cos(beta)*tan(delta))/(Lf+Lr)
    return ang


'''--------------------------------------main function i------------------------------------------ '''
if __name__=="__main__":
    try:
        "-----------Inputs and arguments preparation------------"
        lin_vel=float(input("Enter the car velocity\n") )#where lin_vel=0.5r(wl+wr) as the radius of each wheel is the same 
        delta= float(input("Enter the steering angle: \n"))
        time_of_simulation=float(input("And the time of simulation"))
        beta=atan((Lr/(Lf+Lr))*tan(delta))
        

        listener()
        publishing(beta,delta,time_of_simulation)
    except rospy.ROSInterruptException:
        pass