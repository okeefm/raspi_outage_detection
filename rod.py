from SimpleCV import *
import time
from time import strftime, localtime
import smtplib
import string
import ConfigParser
import io

config = ConfigParser.SafeConfigParser()
config.read("rod.cfg")

server = smtplib.SMTP_SSL(config.get("email", "host"), config.getint("email", "port"))
print "connected"
server.login(config.get("email", "user"), config.get("email", "password"))
FROM = config.get("email", "from")
TO = config.get("email", "to").split(",")
SUBJECT = config.get("email", "subject")
text = config.get("email", "text")

cam = Camera()
num_outage_frames = 0
color_threshold = (config.getint("outage_params", "red_threshold"), config.getint("outage_params", "blue_threshold"), config.getint("outage_params", "green_threshold"))
outage_threshold = config.getint("outage_params", "outage_frames")
i = 0
num_iters = 300.0

def outage_notify():
	print "An Outage has occurred at: " + strftime("%Y-%m-%d %H:%M:%S", localtime())
	BODY = string.join((
	"From: %s" % FROM,
	"To: %s" % TO,
	"Subject: %s" % SUBJECT + " " + strftime("%Y-%m-%d %H:%M:%S", localtime()),
	"",
	text + " " + strftime("%Y-%m-%d %H:%M:%S", localtime())), "\r\n")
	server.sendmail(FROM, TO, BODY)

#t1 = time.time()
while(1):
	#get the current frame from the camera
	img = cam.getImage()
	#i = i + 1
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
	else:
		time.sleep(0.03)
#t2 = time.time()

#print '%d iterations took %0.3f ms, or %0.5f ms per iteration' % (num_iters, (t2-t1)*1000.0, (t2-t1)*1000.0 / num_iters)

server.quit()
