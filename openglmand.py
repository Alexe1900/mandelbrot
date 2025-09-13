from manim import *
from manim.opengl import *

class Orbits3d(ThreeDScene):
    def construct(self):
        self.rotating = False
        iterations = 30
        self.zScale = 50
        ax = ThreeDAxes(
            x_range=[-3, 3, 0.25],
            y_range=[-2.5, 2.5, 0.25],
            z_range=[0, 25, ((25/iterations) if iterations < 100 else 25)],

            x_length=6*2,
            y_length=5*2,

            tips=False,
            x_axis_config={"include_numbers": True, "font_size": 12}
        )

        mandImg = OpenGLImageMobject("imgMand.png")
        mandImg.height = ax.c2p(0, 4, 0)[1] - ax.c2p(0, 0, 0)[1]
        self.add(mandImg)

        self.play(Write(ax))

        self.play(
            self.camera.animate.set_euler_angles(
                phi=45 * DEGREES,
                theta=30 * DEGREES
            )
        )
        self.play(self.camera.animate.set(width=25))
        
        self.cTrack = ComplexValueTracker(0)

        memo = {}

        def f(t):
            c = self.cTrack.get_value()

            if (t == 0):
                return [0, GREEN]
            
            if (t == 1):
                return [c, BLUE]
            
            if ((c, t) in memo):
                return memo[(c, t)]
            
            a = f(t-1)[0]
            r = (a * a) + c
            if (abs(r.real) > 2.5 or abs(r.imag) > 2.5):
                memo[(c, t)] = [2.5*((r.real)/abs(r.real))+2.5j*((r.imag)/abs(r.imag)), RED]
            else:
                memo[(c, t)] = [r, GREEN]
            return memo[(c, t)]

        self.add(ax)

        dots = OpenGLVGroup()

        def updateDot(d, i):
            [val, clr] = f(i)

            newCAx = [val.real, val.imag, (25/iterations)*i * self.zScale/50]
            newCScene = ax.c2p(*newCAx)

            d.move_to(newCScene)
            d.set_color(clr)
        
        for i in range(iterations + 1):
            [_, clr] = f(i)

            dots.add(Dot3D(radius=0.02, color=clr))

            dots[i].add_updater(lambda d, i=i: updateDot(d, i))
        self.add(dots)

        # lines = OpenGLVGroup()

        # def makeLine(d, i):
        #     [endVal, clr] = f(i+1)
        #     [startVal, _] = f(i)

        #     newCAxStart = [startVal.real, startVal.imag, (25/iterations)*i * self.zScale/50]
        #     newCAxEnd = [endVal.real, endVal.imag, (25/iterations)*(i+1) * self.zScale/50]
        #     newCSceneStart = ax.c2p(*newCAxStart)
        #     newCSceneEnd = ax.c2p(*newCAxEnd)

        #     d.set_start_and_end_attrs(newCSceneStart, newCSceneEnd)
        #     d.set_color(clr)

        # for i in range(iterations):
        #     lines.add(Line3D(color=dots[i+1].get_color()))
        #     lines.add_updater(
        #         lambda d, i=i: makeLine(d, i)
        #     )
        # self.add(lines)

        self.interactive_embed()
    
    def setC(self, newC):
        self.play(
            self.cTrack.animate.set_value(newC)
        )
    
    def on_key_press(self, symbol, modifiers):
        from pyglet.window import key

        if (symbol == key.W):
            self.cTrack.set_value(self.cTrack.get_value() + 0.03j)
        if (symbol == key.S):
            self.cTrack.set_value(self.cTrack.get_value() - 0.03j)
        if (symbol == key.D):
            self.cTrack.set_value(self.cTrack.get_value() + 0.03)
        if (symbol == key.A):
            self.cTrack.set_value(self.cTrack.get_value() - 0.03)
        
        if (symbol == key.UP):
            self.cTrack.set_value(self.cTrack.get_value() + 0.01j)
        if (symbol == key.DOWN):
            self.cTrack.set_value(self.cTrack.get_value() - 0.01j)
        if (symbol == key.RIGHT):
            self.cTrack.set_value(self.cTrack.get_value() + 0.01)
        if (symbol == key.LEFT):
            self.cTrack.set_value(self.cTrack.get_value() - 0.01)
        
        if (symbol == key.U):
            self.zScale = min(self.zScale+1, 50)
        if (symbol == key.J):
            self.zScale = max(self.zScale-1, 0)
        if (symbol == key.M):
            self.zScale = 0
        
        if (symbol == key.H):
            self.cTrack.set_value(0)
        
        if (symbol == key.DOLLAR):
            if (self.rotating):
                self.stop_ambient_camera_rotation()
            else:
                self.begin_ambient_camera_rotation(0.25)
            self.rotating = not self.rotating

        super().on_key_press(symbol, modifiers)