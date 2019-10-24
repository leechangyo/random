#!/usr/bin/env python

import rospy, tf, rospkg
from gazebo_msgs.srv import SpawnModel
import time
from geometry_msgs.msg import *
from gazebo_msgs.msg import ModelState, ModelStates
import os
from os.path import expanduser

rospack = rospkg.RosPack()
Home = rospack.get_path('multi_ur5')
path = Home + '/models/object/model.sdf'

class Spawn():
	def __init__(self, model_name, Spawning, x_pose, y_pose):
		self.pub_model = rospy.Publisher('gazebo/set_model_state', ModelState, queue_size=1)
		self.model_name = model_name
		self.rate = rospy.Rate(10)
		self.x_model_pose = x_pose
		self.y_model_pose = y_pose
		self.Spawning = Spawning 
		self.flag = 0
		self.flag1 = 0


	def spawning(self,):
		with open(path) as f:
			product_xml = f.read()
		item_name   =   "product_{0}_0".format(0)
		print("Spawning model:%s", self.model_name)
		item_pose   =   Pose(Point(x=self.x_model_pose, y=self.y_model_pose,    z=1.0),   Quaternion(0.,0.,0.,0.))
		# item_pose   =   Pose(Point(x=self.x_model_pose, y=self.y_model_pose,    z=2))
		self.Spawning(self.model_name, product_xml, "", item_pose, "world")

def main():
	rospy.init_node('moving_obstacle')
	Spawning = rospy.ServiceProxy("gazebo/spawn_sdf_model", SpawnModel)
	rospy.wait_for_service("gazebo/spawn_sdf_model")
	object1 = Spawn("object", Spawning, 0.65, -0.25)
	object1.spawning()

if __name__ == '__main__':
	main()
    #   <pose frame=''>0.6 1 2 0 0.785 -1.57</pose>  -->
