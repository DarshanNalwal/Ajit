#!/usr/bin/env python
# license removed for brevity
import rospy
from std_msgs.msg import String
from geometry_msgs.msg import Twist
from numpy import interp

left = 0.0
right = 0.0
w = 0.27  # distance between wheels in meters


def callback(msg):
    global vx, vy, vr, pub
    # max pwm = 200   min pwm = 46
    # max linear vel = 0.44  min linear vel = 0.17
    # max angular vel = 0.4619  min angular vel = 0.1619
    vx = msg.linear.x
    vz = msg.angular.z

    if((vx != 0) or (vz != 0)):
        if(vx != 0):
            if (vx > 0.17 and vx < 0.44):
                vx = int(interp(vx,[0.17,0.44],[46,200]))
                pub.publish("w,"+str(vx))
            elif(vx < -0.17 and vx > -0.44):
                vx = int(interp(vx,[-0.44,-0.17],[200,46]))
                pub.publish("s,"+str(vx))

        if(vz != 0):
            if(vz > 0.16 and vz < 0.46):
                vz = int(interp(vz,[0.16,0.46],[83,200]))
                pub.publish("a,"+str(vz))
            elif(vz < -0.16 and vz > -0.46):
                vz = int(interp(vz,[-0.46,-0.16],[200,83]))
                pub.publish("d,"+str(vz))
    else:
        pub.publish("c,0")

    print(vx)

if __name__ == '__main__':
    rospy.init_node('twist_motors', anonymous=True)
    pub = rospy.Publisher('base_cmd', String, queue_size=10)
    rospy.Subscriber("cmd_vel", Twist, callback)

    rate = rospy.Rate(10)
    while not rospy.is_shutdown():

        rate.sleep()
