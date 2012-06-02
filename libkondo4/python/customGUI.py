import Blender
from Blender import Draw, BGL

mystring = ""
mymsg = ""
toggle = 0

def event(evt, val):    # the function to handle input events
  global mystring, mymsg

  if not val:  # val = 0: it's a key/mbutton release
    if evt in [Draw.LEFTMOUSE, Draw.MIDDLEMOUSE, Draw.RIGHTMOUSE]:
      mymsg = "You released a mouse button."
      Draw.Redraw(1)
    return

  if evt == Draw.ESCKEY:
    Draw.Exit()                 # exit when user presses ESC
    return

  elif Draw.AKEY <= evt <= Draw.ZKEY: mystring += chr(evt)
  elif evt == Draw.SPACEKEY: mystring += ' '
  elif evt == Draw.BACKSPACEKEY and len(mystring):
    mystring = mystring[:-1]
  else: return # no need to redraw if nothing changed

  Draw.Redraw(1)

def button_event(evt):  # the function to handle Draw Button events
  global mymsg, toggle
  if evt == 1:
    mymsg = "You pressed the toggle button."
    toggle = 1 - toggle
    Draw.Redraw(1)

def gui():              # the function to draw the screen
  global mystring, mymsg, toggle
  if len(mystring) > 90: mystring = ""
  BGL.glClearColor(0,0,1,1)
  BGL.glClear(BGL.GL_COLOR_BUFFER_BIT)
  BGL.glColor3f(1,1,1)
  Draw.Toggle("Toggle", 1, 10, 10, 55, 20, toggle,"A toggle button")
  Draw.Toggle("Toggle2", 1, 10, 30, 55, 20, toggle,"A toggle button")
  Draw.Toggle("Toggle3", 1, 10, 60, 55, 20, toggle,"A toggle button")
  Draw.Toggle("Toggle4", 1, 10, 90, 55, 20, toggle,"A toggle button")
  BGL.glRasterPos2i(72, 16)
  if toggle: toggle_state = "down"
  else: toggle_state = "up"
  Draw.Text("The toggle button is %s." % toggle_state, "small")
  BGL.glRasterPos2i(10, 230)
  Draw.Text("Type letters from a to z, ESC to leave.")
  BGL.glRasterPos2i(20, 200)
  Draw.Text(mystring)
  BGL.glColor3f(1,0.4,0.3)
  BGL.glRasterPos2i(340, 70)
  Draw.Text(mymsg, "tiny")

Draw.Register(gui, event, button_event)  # registering the 3 callbacks
