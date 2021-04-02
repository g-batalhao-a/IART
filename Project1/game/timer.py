import time




##########################################################################
############################# Timer Class ################################
##########################################################################

class Timer:
	def __init__(self,timer):
		self.time=timer
		self.timer=time.time()

	def startTimer(self):
		self.timer=time.time()+self.time

	def updateTimer(self,newTime):
		self.time=newTime
		self.timer=time.time()+self.time

	def checkTimer(self):
		if self.timer < time.time():
			self.timer=time.time()+self.time
			return True
		return False