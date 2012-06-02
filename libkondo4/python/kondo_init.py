	
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
#if Blender.bylink and Blender.event == 'Redraw':
print "redraw detected" 
set_servo(ki, Blender.link)
print "set pos done"

close(ki)
print "Kondo instance closed"
