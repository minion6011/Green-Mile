from ursina import *

from ursina.scripts.property_generator import generate_properties_for_class

@generate_properties_for_class()
class StaminaBar(Button):

    def __init__(self, max_value=100, value=Default, roundness=0, bar_color=color.yellow.tint(-.2), highlight_color=color.black66, animation_duration=.1, show_text=True, show_lines=False, text_size=.7, scale=(.5,.025), origin=(-.5,.5), name='stamina_bar', **kwargs):
        super().__init__(name=name, position=(-.45*window.aspect_ratio,.45), origin=origin, scale=scale, text='stamina', text_size=text_size, radius=roundness, ignore=True, highlight_color=highlight_color, color=highlight_color)
        # - barra quadrata
        self.bar = Entity(parent=self, model=Quad(radius=roundness), origin=origin, z=-.005, color=bar_color, highlight_color=highlight_color, ignore=True)
        # - barra colorata
        self.lines = Entity(parent=self.bar, y=-1, color=color.black33, ignore=True, enabled=show_lines, z=-.05)

        self.status = "OFF"

        self.max_value = max_value
        self.clamp = True
        self.roundness = roundness
        self.animation_duration = animation_duration
        self.show_lines = show_lines
        self.show_text = show_text
        self.value = self.max_value if value == Default else value

        for key, value in kwargs.items():
            setattr(self, key, value)

        self.text_entity.enabled = show_text


    def value_setter(self, n):
        if self.clamp:
            n = clamp(n, 0, self.max_value)

        self._value = n

        self.bar.animate_scale_x(n/self.max_value, duration=self.animation_duration, curve=curve.in_out_bounce)
        self.text_entity.text = f'{n} / {self.max_value} Stamina - {self.status}'

        if self.lines.enabled:
            self.lines.model = Grid(n, 1)
            self.lines.origin = (-.5,-.5)

        if n / self.max_value >= self.scale_y / self.scale_x:
            aspect_ratio = n/self.max_value*self.scale_x / self.scale_y
            self.bar.model = Quad(radius=self.roundness, aspect=aspect_ratio)
        else:
            self.bar.model = 'quad'
        self.bar.origin = self.bar.origin



    def show_text_getter(self):
        return self.text_entity.enabled
    def show_text_setter(self, value):
        self.text_entity.enabled = value

    def show_lines_getter(self):
        return self.lines.enabled
    def show_lines_setter(self, value):
        self.lines.enabled = value

    def bar_color_getter(self):
        return self.bar.color
    def bar_color_setter(self, value):
        self.bar.color = value



    def __setattr__(self, name, value):
        if name == 'scale' and hasattr(self, 'model') and self.model:  # update rounded corners of background when scaling
            self.model.aspect = self.world_scale_x / self.world_scale_y
            self.model.generate()
            if hasattr(self, 'bar'):
                self.bar.model = Quad(aspect=self.world_scale_x/self.world_scale_y, radius=self.roundness)
                self.bar.origin = self.origin
            
            if hasattr(self, 'text_entity') and self.text_entity:
                self.text_entity.world_scale = 25 * self.text_size

        super().__setattr__(name, value)
