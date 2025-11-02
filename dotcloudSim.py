from manimlib import *
from pyglet.window import key

import numpy as np
from copy import deepcopy

from playsound import playsound

def hue2rgb(h):
    x = h / 60

    if h < 60:
        r, g, b = 1, x, 0
    elif h < 120:
        r, g, b = 2-x, 1, 0
    elif h < 180:
        r, g, b = 0, 1, x-2
    elif h < 240:
        r, g, b = 0, 4-x, 1
    elif h < 300:
        r, g, b = x-4, 0, 1
    else:
        r, g, b = 1, 0, 6-x

    return (r, g, b)

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
    
    #def: check colors for mand dots (angle coloring)
    def mandColorTestAngle(self, p):
        i = self.indexing[tuple(p)]

        if (abs(self.points[i][0]) > 2):
            return hex2rgb(BLACK)
        else:
            firstP = self.prev2[0][i] - self.prev2[1][i]
            lastP = self.points[i][0] - self.prev2[1][i]

            angle = float(np.angle(firstP, True) - np.angle(lastP, True))
            angle += 720
            angle %= 360

            # print(angle)
            # print(tuple(p))

            return hue2rgb((angle * 5) % 360)
    
    #def: move around dotc
    def updateDotc(self):
        self.play(
            Transform(
                self.dotc,
                DotCloud(
                    self.c2ps(self.points[:, 0]),
                    radius=self.rad
                )
            )
        )
    
    #def: recolors dotc
    def colorDotc(self):
        self.dotc.set_color_by_rgb_func(self.colorTest)
    
    #def: recolor manddotc
    def updateMandDotc(self):
        self.mandDotc.set_color_by_rgb_func(self.mandColorTestAngle)
        # self.mandDotc.make_3d(reflectiveness=0.3, gloss=0.3)

    #def: animate 1 orbit step, inst=0 if slow, inst=1 if instant
    def orbitStep(self, inst=0):
        self.prev2[0] = deepcopy(self.prev2[1])
        self.prev2[1] = deepcopy(self.points[:, 0])

        self.points[:, 0] **= 2
        self.points[:, 0] += self.points[:, 1]

        #def: move points way too far closer but still off screen to avoid overflow
        # self.points[:, 0][abs(self.points[:, 0]) > 15] = self.points[:, 0][abs(self.points[:, 0]) > 15]
        #problem: points in the negatives get dragged across the screen
        #solution: 10-unit vector

        self.points[:, 0] = np.where(abs(self.points[:, 0]) > 400, self.points[:, 0] / abs(self.points[:, 0]) * 10, self.points[:, 0])

        #def: updating slowly if inst=0, instantly if inst=1
        if (inst == 0): self.updateDotc()
        else:
            self.dotc.set_points(self.c2ps(self.points[:, 0]))
        
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
        #todo: make usable
        self.l = -2
        self.r = 2
        self.d = -2
        self.u = 2

        self.ax = ComplexPlane(
            x_range=(-2, 2),
            y_range=(-2, 2),
            width=4,
            height=4,
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
        self.prev2 = [[0] * len(fullspcs)] * 2

        self.gradient = color_gradient([BLUE_E, RED_E, GREEN_E, ORANGE, MAROON_E, YELLOW_E, TEAL_E, PURPLE_E], 50)
        self.gradient.insert(0, BLACK)

        #section: starting the animation
        self.updateDotc()
        self.add(self.dotc)

        for _ in range(initial):
            self.orbitStep(inst=1)
            self.wait(1)
        
        playsound('ready.mp3')

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
            case key.C:
                self.colorDotc()
        
        if (50 <= symbol and symbol <= 57):
            #section: number key pressed, doing that many iters

            iters = symbol - 48

            for _ in range(iters):
                self.orbitStep(inst=1)
                self.wait(0.5)

        super().on_key_press(symbol, modifiers)