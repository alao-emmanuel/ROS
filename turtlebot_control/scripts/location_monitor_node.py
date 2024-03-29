#!/usr/bin/env python
import math
import rospy
from nav_msgs.msg import Odometry
from turtlebot_control.msg import LandmarkDistance


def distance(x1,y1,x2,y2):
	xd = x1-x2
	yd = y1-y2
	return math.sqrt(xd*xd+yd*yd)
	
class LandmarkMonitor(object):
	def __init__(self, pub, landmarks):
		self._pub = pub
		self._landmarks = landmarks

	def callback(self, msg):
		x = msg.pose.pose.position.x
		y = msg.pose.pose.position.y
		closest_name = None
		closest_distance = None
		for l_name, l_x, l_y in self._landmarks:
			dist = distance(x,y,l_x,l_y)
			if closest_distance is None or dist < closest_distance:
				closest_name = l_name
				closest_distance = dist
		ld = LandmarkDistance()
		ld.name = closest_name
		ld.distance = closest_distance
		self._pub.publish(ld)
		
		if closest_distance < 0.5:
			rospy.loginfo('I\'m near the {}'.format(closest_name))
			
		#rospy.loginfo('x: {}, y: {}'.format(x,y))
		#rospy.loginfo('Closest: {}'.format(closest_name))

def main():
	rospy.init_node('location_monitor')
	
	landmarks = []
	landmarks.append(("Cube", 0.31, -0.99));
	landmarks.append(("Dumpster", 0.11, -2.42));
	landmarks.append(("Cylinder", -1.14, -2.88));
	landmarks.append(("Barrier", -2.59, -0.83));
	landmarks.append(("Bookshelf", -0.09, 0.53));
	
	pub = rospy.Publisher('closest_landmark', LandmarkDistance, queue_size=10)
	monitor = LandmarkMonitor(pub, landmarks)
	
	rospy.Subscriber("/odom", Odometry, monitor.callback)
	
	rospy.spin()

if __name__ == '__main__':
	main()
