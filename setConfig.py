from manimlib import *

from subprocess import run

class conf(InteractiveScene):
    def writeResults(self, _):
        conf = open('config.txt', 'w')
        conf.write('')
        conf.close()

        conf = open('config.txt', 'a')

        if (self.juliaCheck.get_value()):
            conf.write('j\n')
        else:
            conf.write('m\n')
        
        conf.write(self.npaxInp.get_value() + '\n')
        conf.write(self.npayInp.get_value() + '\n')

        conf.write(self.cInp.get_value() + '\n')

        conf.write(self.initInp.get_value() + '\n')

        conf.write(self.radInp.get_value() + '\n')
        
        conf.close()

        self.clear()

    def construct(self):
        bText = Text('Start Sim', font_size=12)
        ebContent = Group(
            RoundedRectangle(
                bText.get_width() + 0.5,
                bText.get_height() + 0.5,
                corner_radius=0.2
            ),
        bText)
        self.endButton = Button(ebContent, self.writeResults)

        self.juliaCheck = Checkbox(value=False)
        juliaLabel = Text('Julia Toggle', font_size=12).next_to(self.juliaCheck, LEFT)
        julia = Group(self.juliaCheck, juliaLabel)

        self.npaxInp = Textbox(value='600', box_kwargs={'height': 0.5})
        npaxLabel = Text('Numbers Per X Axis', font_size=12).next_to(self.npaxInp, LEFT)
        npax = Group(self.npaxInp, npaxLabel)

        self.npayInp = Textbox(value='600', box_kwargs={'height': 0.5})
        npayLabel = Text('Numbers Per Y Axis', font_size=12).next_to(self.npayInp, LEFT)
        npay = Group(self.npayInp, npayLabel)

        self.cInp = Textbox(value='0', box_kwargs={'height': 0.5})
        cLabel = Text('C for julia / Start for mand', font_size=12).next_to(self.cInp, LEFT)
        c = Group(self.cInp, cLabel)

        self.initInp = Textbox(value='0', box_kwargs={'height': 0.5})
        initLabel = Text('Initial epoch number', font_size=12).next_to(self.initInp, LEFT)
        initial = Group(self.initInp, initLabel)

        self.radInp = Textbox(value='0.01', box_kwargs={'height': 0.5})
        radLabel = Text('Dot radius', font_size=12).next_to(self.radInp, LEFT)
        rad = Group(self.radInp, radLabel)

        controls = Group(julia, npax, npay, c, initial, rad, self.endButton).arrange(DOWN)
        self.add(controls)