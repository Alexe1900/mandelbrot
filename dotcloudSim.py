from manimlib import *
import numpy as np

from pyglet.window import key

#def: custom np.linspace() with rounding
def lspace(start, stop, n):
    res = []
    counter = start
    spacing = str((stop - start) / n)
    spacingdecs = len(spacing) - 2
    spacing = float(spacing)
    for _ in range(n):
        res.append(counter)
        counter += spacing
        counter = np.float32(counter)
        counter = np.around(counter, spacingdecs)
    res.append(counter)
    return res

#debug function
def printurn(x):
    print(x)
    return x

#def: mand = mandelbrot
#def: dotc = DotCloud

#def: rcs = real component
#def: ics = imaginary component

class sc(InteractiveScene):
    #def: check colors for orbit dots
    def colorTest(self, p):
        point = self.ax.p2n(p)
        if (abs(point) > 2):
            return hex2rgb(RED)
        else:
            return hex2rgb(BLUE)

    #imp: deprecated, uses math instead of dict
    #imp: still works (when npax = npay), keeping just in case
    def mandColorTestOld(self, p): 
        point = self.ax.p2n(p)
        x = point.real
        y = point.imag
        a = int((2 * x * self.npax + self.r * self.npax) / (2 * self.r))
        b = int((2 * y * self.npay + self.r * self.npay) / (2 * self.r))
        if (abs(self.points[(a * self.npay + b)][0]) > 2):
            return hex2rgb(BLUE_E)
        else:
            return hex2rgb(GREY_D)
    
    #def: updating the "out since" counter. done on every step
    def updOutSince(self):
        for i in range(len(self.points)):
            if (abs(self.points[i][0]) > 2):
                self.outSince[i] += 1

    #def: check colors for mand dots (boolean coloring)
    def mandColorTest(self, p):
        i = self.indexing[tuple(p)]
        if (abs(self.points[i][0]) > 2):
            return hex2rgb(BLUE_E)
        else:
            return hex2rgb(GREY_D)
    
    #def: check colors for mand dots (speed coloring)
    def mandColorTestSpeed(self, p):
        i = self.indexing[tuple(p)]
        
        return color_to_rgb(self.gradient[self.outSince[i]])
    
    #def: recolor + move around dotc
    def updateDotc(self):
        # insert line 72 for dot separation
        # .make_3d(
        #             reflectiveness=0.3,
        #             gloss=0.3
        #         )
        self.play(
            Transform(
                self.dotc,
                DotCloud(
                    self.c2ps(self.points[:, 0]),
                    radius=self.rad
                ).set_color_by_rgb_func(self.colorTest)
            )
        )
    
    #def: recolor manddotc
    def updateMandDotc(self):
        self.mandDotc.set_color_by_rgb_func(self.mandColorTestSpeed)
        # self.mandDotc.make_3d(reflectiveness=0.3, gloss=0.3)

    #def: animate 1 orbit step, inst=0 if slow, inst=1 if instant
    def orbitStep(self, inst=0):
        self.points[:, 0] **= 2
        self.points[:, 0] += self.points[:, 1]

        #def: move points way too far closer but still off screen to avoid overflow
        #problem: points in the negatives get dragged across the screen
        #solution: 10-unit vector
        # self.points[:, 0][abs(self.points[:, 0]) > 15] = self.points[:, 0][abs(self.points[:, 0]) > 15]

        self.points[:, 0] = np.where(abs(self.points[:, 0]) > 400, self.points[:, 0] / abs(self.points[:, 0]) * 10, self.points[:, 0])

        #def: updating slowly if inst=0, instantly if inst=1
        if (inst == 0): self.updateDotc()
        else:
            self.dotc.set_points(self.c2ps(self.points[:, 0]))
            self.dotc.set_color_by_rgb_func(self.colorTest)
        
        self.updOutSince()

    def construct(self):
        #section: configuration
        conf = open('config.txt', 'r')
        self.mode = conf.readline().strip()
        self.npax = int(conf.readline())
        self.npay = int(conf.readline())
        self.c = complex(conf.readline())
        initial = int(conf.readline())
        self.rad = float(conf.readline())

        #section: config reminder
        self.reminderOpen = True

        remind = Text('Check config!').scale(2).set_color(RED)
        self.play(FadeIn(remind))
        self.wait_until(lambda: not self.reminderOpen, 600)
        self.play(FadeOut(remind))

        #section: important functions vectorization
        self.rcs = np.frompyfunc(lambda x: x.real, 1, 1)
        self.ics = np.frompyfunc(lambda x: x.imag, 1, 1)
        self.p2ns = np.frompyfunc(lambda x: self.ax.p2n(x), 1, 1)
        self.c2ps = lambda x: self.ax.c2p(self.rcs(x), self.ics(x))

        #section: custom zoom
        self.l = -3
        self.r = 3
        self.d = -3
        self.u = 3

        self.ax = ComplexPlane(
            x_range=(self.l, self.r),
            y_range=(self.d, self.u),
            width=self.r - self.l,
            height=self.u - self.d,
        )
        self.play(FadeIn(self.ax))

        #section: generating important arrays
        spcsHor = lspace(int(self.l), int(self.r), self.npax)
        spcsVer = lspace(int(self.d), int(self.u), self.npay)
        fullspcs = [tuple([x, y, 0]) for x in spcsHor for y in spcsVer]
        self.points = None
        if (self.mode == 'm'):
            self.points = np.array([[self.c, complex(x, y)] for x in spcsHor for y in spcsVer])
        else:
            self.points = np.array([[complex(x, y), self.c] for x in spcsHor for y in spcsVer])

        self.dotc = DotCloud()
        self.mandDotc = DotCloud(fullspcs, radius=self.rad)

        self.indexing = dict(
            zip(
                fullspcs,
                [(x * (self.npay+1) + y) for x in range(self.npax+1) for y in range(self.npay+1)]
            )
        )

        self.outSince = [0] * len(fullspcs)

        self.gradient = color_gradient([BLUE_E, RED_E, GREEN_E, ORANGE, MAROON_E, YELLOW_E, TEAL_E, PURPLE_E], 50)
        self.gradient.insert(0, BLACK)

        #section: starting the animation
        self.updateDotc()
        self.add(self.dotc)

        for _ in range(initial):
            self.orbitStep(inst=1)
            self.wait(1)

    #section: hotkeys
    def on_key_press(self, symbol, modifiers):
        match symbol:
            case key.SPACE:
                if (self.reminderOpen):
                    self.reminderOpen = False
                else:
                    self.orbitStep()
            case key.DOLLAR:
                self.orbitStep(inst=1)
            case key.M:
                self.play(FadeOut(self.dotc))
                self.updateMandDotc()
                self.play(FadeIn(self.mandDotc))
            case key.O:
                self.play(FadeOut(self.mandDotc))
                self.play(FadeIn(self.dotc))

        super().on_key_press(symbol, modifiers)