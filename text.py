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

    def _draw(self, canvas):
        canvas.Clear()

        if (self.currentX > 32):
            self.currentX = 0
        else:
            self.currentX += 1

        for x in range(0, 10):
            canvas.SetPixel(x, 0, 64, 255, 64)
            canvas.SetPixel(x, 1, 64, 255, 64)
            canvas.SetPixel(x, 2, 64, 255, 64)
            canvas.SetPixel(x, 3, 64, 255, 64)
        for x in range(11, 21):
            canvas.SetPixel(x, 0, 255, 255, 0)
            canvas.SetPixel(x, 1, 255, 255, 0)
            canvas.SetPixel(x, 2, 255, 255, 0)
            canvas.SetPixel(x, 3, 255, 255, 0)
        for x in range(22, 32):
            canvas.SetPixel(x, 0, 255, 32, 32)
            canvas.SetPixel(x, 1, 255, 32, 32)
            canvas.SetPixel(x, 2, 255, 32, 32)
            canvas.SetPixel(x, 3, 255, 32, 32)

        # example to print time
        #graphics.DrawText(canvas, self._font_large, 1, 13, self._white, time.strftime("%-2I:%M"))
        graphics.DrawText(canvas, self._font_tiny, 0, 11, self._white, "00:00:00")
        #graphics.DrawText(canvas, self._font_small, 2, 22, self._white, time.strftime("%a %b %-d"))

        for x in range(0, self.currentX):
            canvas.SetPixel(x, 13, 255, 32, 32)
            canvas.SetPixel(x, 14, 255, 32, 32)
            canvas.SetPixel(x, 15, 255, 32, 32)
            canvas.SetPixel(x, 16, 255, 32, 32)

    def run(self):
        canvas = self._matrix.CreateFrameCanvas()

        while True:
            self._draw(canvas)
            time.sleep(0.05)
            canvas = self._matrix.SwapOnVSync(canvas)

if __name__ == '__main__':
    displaytext = Display()
    displaytext.run()
