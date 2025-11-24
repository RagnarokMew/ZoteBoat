import arcade

class FadingText(arcade.Text):
    def __init__(self, text,
                 x=0,
                 y=0,
                 color=arcade.color.BLACK,
                 font_size=12,
                 duration=5,
                 trans_duration=1,
                 multiline=True):

        super().__init__(
            text,
            x = x,
            y = y,
            color = color,
            font_size = font_size,
            multiline = multiline,
            width = 500,
        )

        self.max_duration = duration
        self.duration = duration
        self.trans_max_duration = trans_duration
        self.trans_duration = trans_duration
        self.r, self.g, self.b, self.alpha= color
        self.cur_alpha = self.alpha

    def update(self, delta_time):
        if self.duration > 0:
            self.duration -= delta_time
        elif self.trans_duration > 0:
            self.trans_duration -= delta_time

        self.cur_alpha = max(0, int(self.alpha * (self.trans_duration / self.trans_max_duration)))
        self.color = (self.r, self.g, self.b, self.cur_alpha)

    def reset(self):
        self.duration = self.max_duration
        self.trans_duration = self.trans_max_duration

