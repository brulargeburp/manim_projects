from manim_imports_ext import *


class TrigRepresentationsScene(Scene):
    CONFIG = {
        "unit_length": 1.5,
        "arc_radius": 0.5,
        "axes_color": WHITE,
        "circle_color": RED,
        "theta_color": YELLOW,
        "theta_height": 0.3,
        "theta_value": np.pi / 5,
        "x_line_colors": MAROON_B,
        "y_line_colors": BLUE,
    }

    def setup(self):
        self.init_axes()
        self.init_circle()
        self.init_theta_group()

    def init_axes(self):
        self.axes = Axes(unit_size=self.unit_length)
        self.axes.set_color(self.axes_color)
        self.add(self.axes)

    def init_circle(self):
        self.circle = Circle(radius=self.unit_length, color=self.circle_color)
        self.add(self.circle)

    def init_theta_group(self):
        self.theta_group = self.get_theta_group()
        self.add(self.theta_group)

    def add_trig_lines(self, *funcs, **kwargs):
        lines = VGroup(*[self.get_trig_line(func, **kwargs) for func in funcs])
        self.add(*lines)

    def get_theta_group(self):
        arc = Arc(self.theta_value, radius=self.arc_radius, color=self.theta_color)
        theta = OldTex("\\theta")
        theta.shift(1.5 * arc.point_from_proportion(0.5))
        theta.set_color(self.theta_color)
        theta.set_height(self.theta_height)
        line = Line(ORIGIN, self.get_circle_point())
        dot = Dot(line.get_end(), radius=0.05)
        return VGroup(line, arc, theta, dot)

    def get_circle_point(self):
        return rotate_vector(self.unit_length * RIGHT, self.theta_value)

    def get_trig_line(self, func_name="sin", color=None):
        assert func_name in ["sin", "tan", "sec", "cos", "cot", "csc"]
        is_co = func_name in ["cos", "cot", "csc"]
        if color is None:
            if is_co:
                color = self.y_line_colors
            else:
                color = self.x_line_colors

        # Establish start point
        if func_name in ["sin", "cos", "tan", "cot"]:
            start_point = self.get_circle_point()
        else:
            start_point = ORIGIN

        # Establish end point
        if func_name == "sin":
            end_point = start_point[0] * RIGHT
        elif func_name == "cos":
            end_point = start_point[1] * UP
        elif func_name in ["tan", "sec"]:
            end_point = (1.0 / np.cos(self.theta_value)) * self.unit_length * RIGHT
        elif func_name in ["cot", "csc"]:
            end_point = (1.0 / np.sin(self.theta_value)) * self.unit_length * UP
        return Line(start_point, end_point, color=color)


class TrigAnimation(TrigRepresentationsScene):
    def construct(self):
        self.add_trig_lines("sin", "cos", "tan", "sec", "csc", "cot")

        # Animate theta from 0 to 2pi
        self.animate_theta(0, 2 * np.pi)

    def animate_theta(self, start_theta, end_theta, run_time=5):
        def update_theta_group(group, alpha):
            theta = interpolate(start_theta, end_theta, alpha)
            self.theta_value = theta
            new_group = self.get_theta_group()
            group.become(new_group)
            return group

        def update_trig_lines(group, alpha):
            theta = interpolate(start_theta, end_theta, alpha)
            self.theta_value = theta
            new_group = VGroup(
                *[self.get_trig_line(func) for func in ["sin", "cos", "tan", "sec", "csc", "cot"]]
            )

            group.become(new_group)

        trig_lines = VGroup(*[self.get_trig_line(func) for func in ["sin", "cos", "tan", "sec", "csc", "cot"]])
        self.add(trig_lines)
        self.play(
            UpdateFromAlphaFunc(self.theta_group, update_theta_group),
            UpdateFromAlphaFunc(trig_lines, update_trig_lines),

            run_time=run_time,
        )
