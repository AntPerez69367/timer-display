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
		options.hardware_mapping = 'adafruit-hat'  # If you have an Adafruit HAT: 'adafruit-hat'

		self._matrix = RGBMatrix(options = options)
		self._matrix.pwmBits = 11
		self._matrix.brightness = 32


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

	def _draw(self, canvas, timer, slidet):
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

		for x in range(0, slidet):
			canvas.SetPixel(x, 13, 255, 32, 32)
			canvas.SetPixel(x, 14, 255, 32, 32)
			canvas.SetPixel(x, 15, 255, 32, 32)
			canvas.SetPixel(x, 16, 255, 32, 32)


	def run(self):
		canvas = self._matrix.CreateFrameCanvas()

		while True:
			hours = int(0)
			minutes = int(10)
			seconds = int(25)
			slidet = 0
			while hours > -1:
				while minutes > -1:
					while seconds > 0:
						seconds=seconds-1
						time.sleep(1)
						sec = ('%02.f' % seconds)
						min = ('%02.f' % minutes)
						hr = ('%02.f' % hours)
						timer = (str(hr)+':'+str(min)+':'+str(sec))
						self._draw(canvas, timer, slidet)
						slidet += 1
						time.sleep(0.05)
						canvas = self._matrix.SwapOnVSync(canvas)

					minutes=minutes-1
					seconds=60
				hours=hours-1
				minutes=59


if __name__ == '__main__':
	displaytext = Display()
	displaytext.run()
