from manim import *

iterations = 50
def compute(x, it, c):
    val = x
    for _ in range(it):
        val = val*val + c
    return val

class Graph(Scene):
    def construct(self):
        ax = Axes(
            x_range=[-1.5, 1.5, 0.25],
            y_range=[-3, 0, 0.25],
            tips=False,
            axis_config={"include_numbers": True},
        )

        graphx = ax.plot(lambda x:x, use_smoothing=True, color=GREEN)
        graphy = ax.plot(lambda x:-0.525, use_smoothing=True, color=GREEN)
        self.add(ax, graphx, graphy)
        self.wait(1)

        graphs = []

        for i in range(iterations):
            graph = ax.plot(
                lambda x: compute(x, i+1, 0),
                use_smoothing=True,
                color=BLUE,
                stroke_width=0.4
            )
            self.add(graph)
            self.wait(0.5)
            graphs.append(graph)

        graph = ax.plot(
            lambda x: compute(x, 100000, 0),
            use_smoothing=True,
            color=PURE_RED,
            stroke_width=0.8
        )
        self.add(graph)
        graphs.append(graph)
        self.wait(5)


class testMandelbrotFix(Scene):
    def construct(self):
        coords = []
        coordg = Group()
        points = []
        pointg = VGroup()

        [x1, w, y1, h, step] = [-4, 8, -4, 8, 1/32]

        c = 0.5j

        plane = ComplexPlane().add_coordinates()
        self.play(Write(plane))

        for y in range(int(h/step)+1):
            coords.append([])
            points.append([])
            for x in range(int(w/step)+1):
                coords[y].append('blub')
                normal = y*step+y1
                imaginary = x*step+x1

                coords[y][x] = ComplexValueTracker(normal+imaginary*1j)
                points[-1].append(Dot(coords[y][x].points, radius=0.007))

                coordg.add(coords[y][x])

                pointg.add(points[-1][-1])
        
        self.play(LaggedStart(*[Write(dot) for dot in pointg], lag_ratio=0))
        
        self.wait()
        
        for _ in range(10):
            for i in range((int(h/step)+1)*(int(w/step)+1)):
                    if (abs(coordg[i].get_value().real) < 20 and abs(coordg[i].get_value().imag) < 20):
                        coordg[i].set_value(coordg[i].get_value() ** 2 + c)
            
            self.play(LaggedStart(*[
                Transform(pointg[i],
                          Dot(coordg[i].points, radius=0.007)
                ) for i in range((int(h/step)+1)*(int(w/step)+1))
            ], lag_ratio=0))
                    
            self.wait(2)

        for _ in range(10):
            for _ in range(5):
                for i in range((int(h/step)+1)*(int(w/step)+1)):
                        if (abs(coordg[i].get_value().real) < 20 and abs(coordg[i].get_value().imag) < 20):
                            coordg[i].set_value(coordg[i].get_value() ** 2 + c)
            
            self.play(LaggedStart(*[
                Transform(pointg[i],
                          Dot(coordg[i].points, radius=0.007)
                ) for i in range((int(h/step)+1)*(int(w/step)+1))
            ], lag_ratio=0))
                    
            self.wait(2)

class mandelbrotR(Scene):
    def construct(self):
        ax = Axes(
            x_range=[-2.5, 1.25, 0.25],
            y_range=[-2.5, 2.5, 0.25],
            tips=False,
            axis_config={"include_numbers": True},
        )

        self.play(Write(ax))

        dotg = Group()

        for i in range(750):
            dotg.add(Dot(point=ax.coords_to_point(-2.5 + (i*0.005), 0), radius=0.007))

        for it in range(10):
            self.play(*[
                Transform(dotg[i],
                          Dot(ax.coords_to_point(-2.5 + (i*0.005), compute(0, it, -2.5 + (i*0.005))), radius=0.007)
                ) for i in range(750)
            ])

            self.wait(0.5)

class realCanim(Scene):
    def construct(self):
        iterations = 500
        ax = Axes(
            x_range=[-2.5, 3, 0.25],
            y_range=[0, iterations, (1 if iterations < 100 else iterations)],
            tips=False,
            x_axis_config={"include_numbers": True, "font_size": 18},
        )

        c = 0.5

        memo = {}

        def f(t):
            if (t == 0):
                return [0, WHITE]
            
            if (t == 1):
                return [c.get_value(), BLUE]
            
            if ((c.get_value(), t) in memo):
                return memo[(c.get_value(), t)]
            
            a = f(t-1)[0]
            r = (a * a) + c.get_value()
            if (r > 2.5):
                memo[(c.get_value(), t)] = [2.5, RED]
                return [2.5, RED]
            memo[(c.get_value(), t)] = [r, WHITE]
            return [r, WHITE]

        self.add(ax)

        dots = VGroup()
        
        for i in range(iterations + 1):
            [val, clr] = f(i)
            dot = Dot(
                point=ax.coords_to_point(val, i),
                radius=0.05,
                color=clr
            )

            dots.add(dot)
        
        self.add(dots)
        
        while (c.get_value() > -2.25):
            c.set_value(c.get_value() - 0.0025)
            animations = []
            for j in range(iterations+1):
                [val, clr] = f(j)

                animations.append(
                    Transform(
                        dots[j],
                        Dot(
                            ax.coords_to_point(val, j),
                            radius=0.05,
                            color=clr
                        ),
                        run_time=0.1,
                        rate_func=linear
                    )
                )
            
            self.play(
                LaggedStart(*animations, lag_ratio=0)
            )

class realCpic(Scene):
    def construct(self):
        iterations = 1000
        ax = Axes(
            x_range=[-2.5, 3, 0.25],
            y_range=[0, iterations, (1 if iterations < 100 else iterations)],
            tips=False,
            x_axis_config={"include_numbers": True, "font_size": 18},
        )

        c = ValueTracker(-2)

        memo = {}

        def f(t):
            if (t == 0):
                return [0, WHITE]
            
            if (t == 1):
                return [c.get_value(), BLUE]
            
            if ((c.get_value(), t) in memo):
                return memo[(c.get_value(), t)]
            
            a = f(t-1)[0]
            r = (a * a) + c.get_value()
            if (r > 2.5):
                memo[(c.get_value(), t)] = [2.5, RED]
                return [2.5, RED]
            memo[(c.get_value(), t)] = [r, WHITE]
            return [r, WHITE]

        self.add(ax)

        dots = VGroup()
        
        for i in range(iterations + 1):
            [val, clr] = f(i)
            dot = Dot(
                point=ax.coords_to_point(val, i),
                radius=0.05,
                color=clr
            )

            dots.add(dot)
        
        self.add(dots)