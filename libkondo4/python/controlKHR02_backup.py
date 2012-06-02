#! /usr/bin/env python

import Blender
import sys
from pykondo import *

def play_motion( ki, motion_num ):
	
	# play motion
	max_wait = 50 * 1000000;
	ret = kondo_play_motion(ki, motion_num, max_wait)
	if ret < 0:
		 print(ki.error)

# def set_servo( ki, servo, pos )


def init(ki):
	
	# initialize
	ki = KondoInstance()
	ret = kondo_init(ki)
	if ret < 0:
		print(ki.error)
	
def set_servo(ki, servo_id, armature):
	
	bones = armature.getData().bones
	for bone in bones:
		bone.get	
	servo_value = 7500
	kondo_set_servo_pos(ki,servo_id,servo_value) 
	
def close(ki):
	# clean up
	ret = kondo_close(ki)
	if ret < 0:
		print(ki.error)
	
# initialize
print "init Kondo instance.."
ki = KondoInstance()
ret = kondo_init(ki)
if ret < 0:
	print(ki.error)
print "init done"

print "setting servo pos.."
if Blender.bylink and Blender.event == 'Redraw':
  set_servo(ki, 0, Blender.link)
print "set pos done"

close(ki)
print "Kondo instance closed"

