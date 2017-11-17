import threading
from rgbmatrix import graphics
from rgbmatrix import RGBMatrix


class Display(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)

        # Configure LED matrix driver
        self._matrix = RGBMatrix(32, 2, 1)
        self._matrix.pwmBits = 11
        self._matrix.brightness = 25

        # Load fonts
        self._font_large = graphics.Font()
        self._font_large.LoadFont("rpi-rgb-led-matrix/fonts/10x20.bdf")
        self._font_small = graphics.Font()
        self._font_small.LoadFont("rpi-rgb-led-matrix/fonts/6x10.bdf")
        self._font_tiny = graphics.Font()
        self._font_tiny.LoadFont("rpi-rgb-led-matrix/fonts/4x6.bdf")

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

        # example to print time
        #graphics.DrawText(canvas, self._font_large, 1, 13, self._white, time.strftime("%-2I:%M"))
        graphics.DrawText(canvas, self._font_small, 1, 4, self._white, "00:00:00")
        #graphics.DrawText(canvas, self._font_small, 2, 22, self._white, time.strftime("%a %b %-d"))


    def run(self):
        canvas = self._matrix.CreateFrameCanvas()

        while True:
            self._draw(canvas)
            time.sleep(0.05)
            canvas = self._matrix.SwapOnVSync(canvas)

if __name__ == '__main__':
    displaytext = Display()
