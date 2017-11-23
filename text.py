import time
import threading
from rgbmatrix import graphics
from rgbmatrix import RGBMatrix, RGBMatrixOptions


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
		options.gpio_slowdown = 1
		options.disable_hardware_pulsing = True

		self._matrix = RGBMatrix(options = options)
		self._matrix.pwmBits = 11
		self._matrix.brightness = 25


		# Load fonts
		self._font_large = graphics.Font()
		self._font_large.LoadFont("rpi-rgb-led-matrix/fonts/10x20.bdf")
		self._font_small = graphics.Font()
		self._font_small.LoadFont("rpi-rgb-led-matrix/fonts/5x7.bdf")
		self._font_tiny = graphics.Font()
		self._font_tiny.LoadFont("rpi-rgb-led-matrix/fonts/4x6.bdf")
		self.currentX = 0
		# Define colors
		self._white  = graphics.Color(255, 255, 255)
		self._red    = graphics.Color(255, 32, 32)
		self._green  = graphics.Color(64, 255, 64)
		self._yellow = graphics.Color(255, 255, 0)
		# Timer Variables
		self._hours = 0
		self._mins = 0
		self._secs = 0
		self._slidet = 0
		self._sname = 'mySurvey'
		#--------------------------------#
		# Important Locations            #
		#--------------------------------#
		#                                #
		#  Row 1:                        #
		#        Top Left        0,0     #
		#        Top Middle     11,0     #
		#        Top Right      22,0     #
		#                                #
		#  Row 2:                        #
		#        Text Start      1,4     #
		#                                #
		#  Row 3:                        #
		#        Bar Start  0, 12-15     #
		#        Bar End   31, 12-15     #
		#                                #
		#--------------------------------#

	def _draw(self, canvas, timer, slidetime):
		canvas.Clear()

		for x in range(0, 10):
			canvas.SetPixel(x, 0, 64, 255, 64)
			canvas.SetPixel(x, 1, 64, 255, 64)
			canvas.SetPixel(x, 2, 64, 255, 64)
			canvas.SetPixel(x, 3, 64, 255, 64)
		#for x in range(11, 21):
		#	canvas.SetPixel(x, 0, 255, 255, 0)
		#	canvas.SetPixel(x, 1, 255, 255, 0)
		#	canvas.SetPixel(x, 2, 255, 255, 0)
		#	canvas.SetPixel(x, 3, 255, 255, 0)
		#for x in range(22, 32):
		#	canvas.SetPixel(x, 0, 255, 32, 32)
		#	canvas.SetPixel(x, 1, 255, 32, 32)
		#	canvas.SetPixel(x, 2, 255, 32, 32)
		#	canvas.SetPixel(x, 3, 255, 32, 32)

		# example to print time
		#graphics.DrawText(canvas, self._font_large, 1, 13, self._white, time.strftime("%-2I:%M"))
		graphics.DrawText(canvas, self._font_tiny, 0, 11, self._white, timer)
		#graphics.DrawText(canvas, self._font_small, 2, 22, self._white, time.strftime("%a %b %-d"))

		for x in range(0, slidetime):
			canvas.SetPixel(x, 13, 255, 32, 32)
			canvas.SetPixel(x, 14, 255, 32, 32)
			canvas.SetPixel(x, 15, 255, 32, 32)
			canvas.SetPixel(x, 16, 255, 32, 32)

	def sessionSet(self, arg1, arg2):
		ledtime = arg1.split(':')
		self._hours = int(ledtime[0])
		self._mins = int(ledtime[1])
		self._secs = int(ledtime[2])
		self._slidet = int(arg2)

	def stop(self):
		self.alive = False
		self.join()

	def run(self):
		canvas = self._matrix.CreateFrameCanvas()
		self.alive = True
		print ("Thread running")
		try:
			print ("2nd part thread")
			while True:
				print ("THis happened")
				if self._secs == 0:
					if self._mins == 0:
						if self._hours == 0:
							break
						else:
							self._hours -= 1
							self._mins = 59
					else:
						self._mins -= 1
						self._secs = 60


				print ("Should display here")
				sec = ('%02.f' % self._secs)
				min = ('%02.f' % self._mins)
				hr = ('%02.f' % self._hours)
				timer = (str(hr)+':'+str(min)+':'+str(sec))
				self._draw(canvas, timer, self._slidet)
				self._slidet += 1
				time.sleep(0.05)
				canvas = self._matrix.SwapOnVSync(canvas)
				self._secs = self._secs - 1
				time.sleep(1)
		except:
			print ("final")

if __name__ == '__main__':
	displaytext = Display()
	displaytext.run()
