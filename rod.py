from SimpleCV import *
import time
from time import strftime, localtime

cam = Camera()
num_outage_frames = 0
color_threshold = (20, 20, 20)
outage_threshold = 30
i = 0
num_iters = 10000.0

def outage_notify():
	print "An Outage has occurred at: " + strftime("%Y-%m-%d %H:%M:%S", localtime())

t1 = time.time()
while(i < num_iters):
	i = i + 1
	#get the current frame from the camera
	img = cam.getImage()
	#img.show()
	#find the mean pixel color (RGB) for the camera
	miv = img.meanColor()
	#print miv
	#If the mean image value is below some threshold set as a constant, declare an outage for black levels
	outage = False
	if miv < color_threshold:
		outage = True
	#if there's an outage for this frame, add one to the outage counter	
	if outage:
		num_outage_frames += 1
	else:
		num_outage_frames = 0
	#if the outage counter is above some threshold, notify somehow
	if (num_outage_frames > outage_threshold):
		outage_notify()
		num_outage_frames = 0
t2 = time.time()

print '%d iterations took %0.3f ms, or %0.5f ms apiece' % (num_iters, (t2-t1)*1000.0, (t2-t1)*1000.0 / num_iters)
