from manim import *
from manim.opengl import *

class Test(Scene):
    def construct(self):
        iterations = 5
        ax = ThreeDAxes(
            x_range=[-3, 3, 0.25],
            y_range=[-2.5, 2.5, 0.25],
            z_range=[0, 25, ((25/iterations) if iterations < 100 else 25)],

            x_length=6*2,
            y_length=5*2,

            tips=False,
            x_axis_config={"include_numbers": True, "font_size": 14},
        )

        self.play(Write(ax))

        self.play(
            self.camera.animate.set_euler_angles(
                phi=45 * DEGREES,
                theta=30 * DEGREES
            )
        )
        self.play(self.camera.animate.set(width=25))
        self.zScale = 50

        self.cTrack = ValueTracker(0)

        def f(t):
            if (t == 1):
                return [(self.cTrack.get_value()), RED]
            return [t*(self.cTrack.get_value()), WHITE]
        
        dots = OpenGLVGroup()

        def updateDot(d, i):
            [val, clr] = f(i)

            newCAx = [val, i, (25/iterations)*i * self.zScale/50]
            newCScene = ax.c2p(*newCAx)

            d.move_to(newCScene)
            d.set_color(clr)
        
        for i in range(iterations + 1):
            [_, clr] = f(i)

            dots.add(Dot3D(radius=0.02, color=clr))

            dots[i].add_updater(lambda d, i=i: updateDot(d, i))
        self.add(dots)
        
        lines = OpenGLVGroup()

        def makeLine(d, i):
            [endVal, clr] = f(i+1)
            [startVal, _] = f(i)

            newCAxStart = [startVal, i, (25/iterations)*i * self.zScale/50]
            newCAxEnd = [endVal, i+1, (25/iterations)*(i+1) * self.zScale/50]
            newCSceneStart = ax.c2p(*newCAxStart)
            newCSceneEnd = ax.c2p(*newCAxEnd)

            d.set_start_and_end_attrs(newCSceneStart, newCSceneEnd)
            d.set_color(clr)

        for i in range(iterations):
            lines.add(Line3D(color=dots[i+1].get_color()))
            lines[i].add_updater(
                lambda d, i=i: makeLine(d, i)
            )
        self.add(lines)

        self.wait(frozen_frame=False)

        self.play(self.cTrack.animate.set_value(2))

        self.interactive_embed()