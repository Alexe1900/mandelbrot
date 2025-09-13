from manimlib import *
import numpy as np

class ExampleScene(InteractiveScene):
    def construct(self):
        nmp = NumberPlane(
            x_range=(-30, 30),
            y_range=(-30, 30),
            width=30,
            height=30,
        )
        ax = ThreeDAxes(
            x_range=(-30, 30),
            y_range=(-30, 30),
            z_range=(-30, 30),
            width=30,
            height=30,
            depth=30,
        )
        self.play(
            Write(nmp),
            Write(ax),
        )
        self.play(self.frame.animate.reorient(45, 60))
        self.play(self.frame.animate.set_width(7 * FRAME_WIDTH).move_to(15 * OUT))

        itsPerDir = 70
        spcs = np.linspace(-0.05, 0.05, itsPerDir)
        points = np.array([[x, y, z] for x in spcs for y in spcs for z in spcs])

        scale = 3 #imp: lorenz only 1

        def lorenz(x, y, z):
            sigma, rho, beta = 10, 28, 8/3

            dx = sigma * (y - x)
            dy = x * (rho - z) - y
            dz = x * y - beta * z

            return dx, dy, dz
        
        def roessler(x, y, z):
            a, b, c = 0.2, 0.2, 5.7

            dx = -y - z
            dy = x + (a * y)
            dz = b + z * (x - c)

            return dx, dy, dz
        
        def gener(calcFun):
            x = points[:, 0]
            y = points[:, 1]
            z = points[:, 2]

            dx, dy, dz = calcFun(x, y, z)

            x += dx / (60 / scale)
            y += dy / (60 / scale)
            z += dz / (60 / scale)

            return DotCloud(
                ax.c2p(*points.T),
                color=BLUE,
                radius=0.075,
                glow_factor=0.7
            ).make_3d(reflectiveness=0.8)

        dc1 = always_redraw(lambda: gener(roessler))

        self.add(dc1)