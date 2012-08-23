from SimpleCV import *
from time import localtime, strftime

cam = Camera()
num_outage_frames = 0
color_threshhold = (10, 10, 10)
outage_threshold = 300

while(1):
	img = cam.getImage()
	miv = img.meanColor()
	color_outage = false
	if miv < color_threshold:
		color_outage = true
	if color_outage:
		num_outage_frames += 1
	else:
		num_outage_frames = 0
	if (num_outage_frames > outage_threshold):
		outage_notify()
		num_outage_frames = 0

def outage_notify():
	print "An Outage has occurred at: " + strftime("%Y-%m-%d %H:%M:%S", localtime())
