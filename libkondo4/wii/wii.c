/**
 * Nintendo Wiimote-control demo.
 * Requires libwiiuse installed: http://wiiuse.sourceforge.net
 *
 * Copyright 2010 - Christopher Vo (cvo1@cs.gmu.edu)
 * George Mason University - Autonomous Robotics Laboratory
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *    http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 */

#include <stdio.h>
#include <stdlib.h>
#include <wiiuse.h>
#include <rcb4.h>

// motion numbers
#define MOT_HOME 1
#define MOT_ONE 30 
#define MOT_ONE_B 28
#define MOT_TWO 31
#define MOT_TWO_B 27
#define MOT_MINUS 0
#define MOT_PLUS 4
#define MOT_A 17
#define MOT_CALIBRATE 49
#define MOT_FREE 2 
#define MOT_HOLD 3

KondoInstance ki;

void clear_buttons() {
	kondo_krc3_buttons(&ki, 0, 0, 0, 0, 0);
}

void set_button_state(int u, int d, int l, int r, int b) {
	unsigned int s = 0;
	if(u) s |= RCB4_BTN_LU;
	if(d) s |= RCB4_BTN_LD;
	if(l && !b) s |= RCB4_BTN_LL;
	if(r && !b) s |= RCB4_BTN_LR;
	if(l && b) s |= RCB4_BTN_RL;
	if(r && b) s |= RCB4_BTN_RR;
	kondo_krc3_buttons(&ki, s, 0, 0, 0, 0);
}

void play_motion(int m) {
	clear_buttons();
	printf("playing motion %d\n", m);
	kondo_play_motion(&ki, m, 0);
}	

void handle_event(struct wiimote_t* wm) {

	static int freed = 0;

	// b pressed?
	int b_pressed = 0;
	if(IS_PRESSED(wm, WIIMOTE_BUTTON_B))
		b_pressed = 1;

	// basic motion mapping
	if(!b_pressed) {
		if(IS_JUST_PRESSED(wm, WIIMOTE_BUTTON_HOME))
			play_motion(MOT_HOME);
		if (IS_JUST_PRESSED(wm, WIIMOTE_BUTTON_ONE))
			play_motion(MOT_ONE);
		if (IS_JUST_PRESSED(wm, WIIMOTE_BUTTON_TWO))
			play_motion(MOT_TWO);
		if (IS_JUST_PRESSED(wm, WIIMOTE_BUTTON_MINUS))
			play_motion(MOT_MINUS);
		if (IS_JUST_PRESSED(wm, WIIMOTE_BUTTON_PLUS))
			play_motion(MOT_PLUS);
		if (IS_JUST_PRESSED(wm, WIIMOTE_BUTTON_A))
			play_motion(MOT_A);
	} else {
		if(IS_JUST_PRESSED(wm, WIIMOTE_BUTTON_HOME))
			play_motion(MOT_CALIBRATE);
		if (IS_JUST_PRESSED(wm, WIIMOTE_BUTTON_ONE))
			play_motion(MOT_ONE_B);
		if (IS_JUST_PRESSED(wm, WIIMOTE_BUTTON_TWO))
			play_motion(MOT_TWO_B);
		if (IS_JUST_PRESSED(wm, WIIMOTE_BUTTON_A))
			if(freed) {
				play_motion(MOT_HOLD);
				freed = 0;
			} else {
				play_motion(MOT_FREE);
				freed = 1;
			}

	}

	// direction keys
	int su = IS_PRESSED(wm, WIIMOTE_BUTTON_UP);
	int sd = IS_PRESSED(wm, WIIMOTE_BUTTON_DOWN);
	int sl = IS_PRESSED(wm, WIIMOTE_BUTTON_LEFT);
	int sr = IS_PRESSED(wm, WIIMOTE_BUTTON_RIGHT);
	set_button_state(su, sd, sl, sr, b_pressed);
}

int main(int argc, char** argv) {
	wiimote** wiimotes;
	int found, connected;

	// init
	printf("[INFO] Looking for wiimotes (5 seconds)...\n");
	wiimotes =  wiiuse_init(1);

	// find wii (wait for 5 seconds)
	found = wiiuse_find(wiimotes, 1, 5);
	if (!found) {
		printf ("[INFO] No wiimotes found.\n");
		return 0;
	}

	// connect
	connected = wiiuse_connect(wiimotes, 1);
	if (connected)
		printf("[INFO] Connected to %i wiimotes (of %i found).\n", connected, found);
	else {
		printf("[ERROR] Failed to connect to any wiimote.\n");
		return 0;
	}

	// rumble and set leds
	wiiuse_set_leds(wiimotes[0], WIIMOTE_LED_1);
	wiiuse_rumble(wiimotes[0], 1);
	usleep(200000);
	wiiuse_rumble(wiimotes[0], 0);

	// set up kondo
	int ret = kondo_init(&ki);
	if (ret < 0) {
		printf("%s", ki.error);
		exit(-1);
	}

	// continuously poll wiimote and handle events
	while (1) {
		if (wiiuse_poll(wiimotes, 1)) {
			switch (wiimotes[0]->event) {
				case WIIUSE_EVENT:
					handle_event(wiimotes[0]);
					break;
				case WIIUSE_DISCONNECT:
				case WIIUSE_UNEXPECTED_DISCONNECT:
					goto exit;
					break;

				default:
					break;
			}
		}
	}
exit:
	wiiuse_cleanup(wiimotes, 1);
	ret = kondo_close(&ki);
	if (ret < 0)
		printf("%s", ki.error);
	return 0;
}
