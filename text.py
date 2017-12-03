import time, threading, math
from rgbmatrix import RGBMatrix, RGBMatrixOptions, graphics


class Display(threading.Thread):
	def __init__(self):
		threading.Thread.__init__(self)



		# Configure LED matrix driver
		# Configuration for the matrix
		options = RGBMatrixOptions()
		options.rows = 16
		options.chain_length = 1
		options.parallel = 1
		options.hardware_mapping = 'adafruit-hat'
		options.gpio_slowdown = 3
		options.disable_hardware_pulsing = True

		self._matrix = RGBMatrix(options = options)
		self._matrix.pwmBits = 11
		self._matrix.brightness = 45


		# Load fonts
		self._font_tiny = graphics.Font()
		self._font_tiny.LoadFont("rpi-rgb-led-matrix/fonts/4x6.bdf")
		self.currentX = 0
		# Define colors
		self._white  = graphics.Color(255, 255, 255)
		self._red    = graphics.Color(255, 32, 32)
		self._green  = graphics.Color(64, 255, 64)
		self._yellow = graphics.Color(255, 255, 0)
		# Timer Variables
		self._totaltime = 0
		self._secs = -1
		self._slidet = 0
		self._sliderange = 0
		self._overtime = False
		self._greentime = True
		self._yellowtime = False
		self._redtime = False
		self._sname = 'mySurvey'
		self.running = False

	def _draw(self, canvas, timer, slidetime):
		canvas.Clear()

		## Yellow Time
		if self._overtime:
			for x in range(22, 32):
					canvas.SetPixel(x, 0, 255, 32, 32)
					canvas.SetPixel(x, 1, 255, 32, 32)
					canvas.SetPixel(x, 2, 255, 32, 32)
					canvas.SetPixel(x, 3, 255, 32, 32)
			if self._secs % 2 == 0:
				graphics.DrawText(canvas, self._font_tiny, 0, 11, self._white, timer)
			else:
				graphics.DrawText(canvas, self._font_tiny, 0, 11, self._red, timer)
		else:
			if self._yellowtime:
				for x in range(11, 21):
					canvas.SetPixel(x, 0, 255, 255, 0)
					canvas.SetPixel(x, 1, 255, 255, 0)
					canvas.SetPixel(x, 2, 255, 255, 0)
					canvas.SetPixel(x, 3, 255, 255, 0)
				graphics.DrawText(canvas, self._font_tiny, 0, 11, self._white, timer)

			## Red Time
			if self._redtime:
				for x in range(22, 32):
					canvas.SetPixel(x, 0, 255, 32, 32)
					canvas.SetPixel(x, 1, 255, 32, 32)
					canvas.SetPixel(x, 2, 255, 32, 32)
					canvas.SetPixel(x, 3, 255, 32, 32)
				graphics.DrawText(canvas, self._font_tiny, 0, 11, self._white, timer)

			## Green Time
			if self._greentime:
				for x in range(0, 10):
					canvas.SetPixel(x, 0, 64, 255, 64)
					canvas.SetPixel(x, 1, 64, 255, 64)
					canvas.SetPixel(x, 2, 64, 255, 64)
					canvas.SetPixel(x, 3, 64, 255, 64)
				graphics.DrawText(canvas, self._font_tiny, 0, 11, self._white, timer)

		## Slider
		for x in range(0, slidetime):
			ytime = self._sliderange / 2
			rtime =  ytime + ytime / 2
			if self._slidet < ytime:
				canvas.SetPixel(x, 13, 255, 255, 255)
				canvas.SetPixel(x, 14, 255, 255, 255)
				canvas.SetPixel(x, 15, 255, 255, 255)
			if self._slidet >= ytime and self._slidet < rtime:
				canvas.SetPixel(x, 13, 255, 255, 0)
				canvas.SetPixel(x, 14, 255, 255, 0)
				canvas.SetPixel(x, 15, 255, 255, 0)
			if self._slidet >= rtime:
				canvas.SetPixel(x, 13, 255, 32, 32)
				canvas.SetPixel(x, 14, 255, 32, 32)
				canvas.SetPixel(x, 15, 255, 32, 32)

	def sessionSet(self, arg1, arg2):
		self._secs = sum(int(x) * 60 ** i for i,x in enumerate(reversed(arg1.split(":"))))
		self._sliderange = int(arg2)
		self._totaltime = self._secs
		self._slidet = 0
		self._overtime = False

	def stop(self):
		self._draw(canvas, "00:00:00", 0)
		self.running = False

	def setColorFlag(self):
		## set color flag
		ytime = self._totaltime / 2
		rtime =  ytime - ytime / 2
		if self._secs > ytime:
			self._greentime = True
			self._yellowtime = False
			self._redtime = False
		if self._secs <= ytime and self._secs > rtime:
			self._greentime = False
			self._yellowtime = True
			self._redtime = False
		if self._secs <= rtime:
			self._greentime = False
			self._yellowtime = False
			self._redtime = True

	def buildTimeString(self):
		# Timer Calculations
		if self._overtime:
			self._secs += 1
		else:
			self._secs -= 1

		m, s = divmod(self._secs, 60)
		h, m = divmod(m, 60)

		# Return Assembled Time String
		return ("%02.f:%02.f:%02.f" % (h,m,s))

	def calculateSlideTime(self):
		# Calculate slide timer
		if self._slidet > 0 and self._slidet < self._sliderange:
			oldrange = (int(self._sliderange) - 0)
			newval = math.floor(((int(self._slidet+1) * 32) / oldrange))
		else:
			self._slidet = 0
			newval = 0
		self._slidet += 1
		return newval

	def run(self):

		canvas = self._matrix.CreateFrameCanvas()
		print ("Thread running")
		while True:
			if self.running and self._secs >= 0:
				timer = self.buildTimeString()
				newval = self.calculateSlideTime()
				self.setColorFlag()

				# Send data to LED display
				self._draw(canvas, timer, newval)
				time.sleep(0.05)
				canvas = self._matrix.SwapOnVSync(canvas)
				time.sleep(1)
				if self._secs == 0:
					self._overtime = True
			else:
				self._draw(canvas, " READY! " , 0)
				time.sleep(0.05)
				canvas = self._matrix.SwapOnVSync(canvas)
				#print("Not running")


if __name__ == '__main__':
	displaytext = Display()
	displaytext.run()
