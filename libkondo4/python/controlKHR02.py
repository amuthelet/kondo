#! /usr/bin/env python

#############
# Blender script writtten by Arnaud Muthelet / Nov 2010
# Contact: amuthelet at gmail dot com
# Prereq: 
#   Blender v2.49, Python 2.6, libkondo4 from Christopher Vo
# Desc:
#   Interactive command of Kondo KHR3 servos via RCB4
#   controller, given
#   orientations of virtual robot bones.
# WARNINGS:
#   SERVOS CAN BE DAMAGED IF FORCED TO INVALID VALUES, 
#   PLEASE CHECK DATA SENT TO SERVOS BEFORE PLUGGING YOUR 
#   ROBOT (verbose = 1). 
#################################################

import Blender
import sys
import math
from pykondo import *

SERVO_NEUTRAL = 7500
SERVO_MAX = 10000
SERVO_MIN = 5000
SERVO_DIFF = 30

VERBOSE = 1
KONDO_PLUGGED = 0

def init_registry(arm):
	values = Blender.Registry.GetKey('servo_values')
	if values:
		if VERBOSE:
			print "REGISTRY entry 'servo_value' already exists"
	else:
		values = {}
		pose = arm.getPose()
		poseBones = pose.bones
		staticBones = arm.getData().bones
		for boneT in staticBones.items():
			bone_name = boneT[0]
			values[bone_name] = 0
		Blender.Registry.SetKey('servo_values',values,0)
		if VERBOSE:
			print "REGISTRY entry 'servo_values' created"
	
def set_servo(ki, arm):
	
	previousValues = Blender.Registry.GetKey('servo_values')

	sepID = "_#"
	sepAxis = "_A"
	sepSign = "_S"
		
	pose = arm.getPose()
	poseBones = pose.bones
	staticBones = arm.getData().bones
	for boneT in staticBones.items():
		bone_name = boneT[0]
		bone = poseBones[bone_name]
	
		idIndex = bone_name.find(sepID) + len(sepID)
		if(idIndex > len(sepID)-1):
			servo_id = int(bone_name[idIndex:idIndex+2])
			
			axisIndex = bone_name.find(sepAxis) + len(sepAxis)
			axis = bone_name[axisIndex]
			
			signIndex = bone_name.find(sepSign) + len(sepSign)
			sign = bone_name[signIndex]
			signFactor = 1
						
			if( sign == "P" ):
				signFactor = -1

			if( axis == 'X'):
				servo_value = int(SERVO_NEUTRAL + signFactor * math.floor(SERVO_DIFF*bone.quat.toEuler().x))
			elif (axis == "Y"):
				servo_value = int(SERVO_NEUTRAL + signFactor * math.floor(SERVO_DIFF*bone.quat.toEuler().y))
			elif(axis == "Z"):
				servo_value = int(SERVO_NEUTRAL + signFactor * math.floor(SERVO_DIFF*bone.quat.toEuler().z))
			else:
				servo_value = int(SERVO_NEUTRAL + signFactor * math.floor(SERVO_DIFF*bone.quat.toEuler().y))
				if VERBOSE:
					print	"ERROR: No Axis found in servo name, defaulted to Y"
				
			previousValue = previousValues[bone_name]
					 
			if( (servo_value < SERVO_MAX) & (servo_value > SERVO_MIN) & (previousValue != servo_value)):
				kondo_set_servo_pos(ki,servo_id,servo_value) 
				if VERBOSE:
					print bone_name, "ServoID:",servo_id, "Sign:",sign,"Value:",servo_value, "Axis:", axis		
			elif VERBOSE:
					print bone_name, "did not move, or moved out of range"
		
			previousValues[bone_name] = servo_value
			Blender.Registry.SetKey('robot_data',previousValues,0)
		elif VERBOSE:
			print "ERROR: no ID found in", bone_name
			

if Blender.bylink:
	# Initialize Kondo lib
	ki = KondoInstance()
	if KONDO_PLUGGED:
		ret = kondo_init(ki)
		if ret < 0:
			print(ki.error)
		if VERBOSE:
			print "Kondo lib init done"
	init_registry(Blender.link)
	set_servo(ki, Blender.link)

	ret = kondo_close(ki)
	if ret < 0:
		print(ki.error)

else:
	print "MANUAL LAUNCH"