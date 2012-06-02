#! /usr/bin/env python

#
# run_motion.py example for Python SWIG bindings
#
# Copyright 2010 - Christopher Vo (cvo1@cs.gmu.edu)
# George Mason University - Autonomous Robotics Laboratory
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#

import sys
from pykondo import *

def main():
	
	# initialize
	ki = KondoInstance()
	print ("Create KondoInstance OK",ki)	
	ret = kondo_init(ki)
	print ("Init KondoInstance OK", ret)
	if ret < 0:
		sys.exit(ki.error)
	
	# play motion
	motion_num = 0
	max_wait = 50 * 1000000;
	ret = kondo_play_motion(ki, motion_num, max_wait)
	if ret < 0:
		sys.exit(ki.error)

	# set_servo_pos
	#servos = array('B', [0,0,0,0,0])
	#kondo_send_ics_pos(ki, 7500, array('B', [0,0,0,0,0]))
	#kondo_set_servo_pos(ki,0,7500)


	# clean up
	ret = kondo_close(ki)
	print("KondoInstance killed", ret)
	if ret < 0:
		sys.exit(ki.error)

if __name__ == "__main__":
	main()
