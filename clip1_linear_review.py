# clip1_linear_review.py
from manim import *
import numpy as np

class Clip1LinearReview(Scene):
    def construct(self):
        # 1. Transition Text
        title = Text("Linear Regression").scale(1.5)
        self.play(FadeIn(title, shift=UP))
        self.wait(1)
        self.play(FadeOut(title, shift=UP))
        self.wait(0.5)

        # 2. Setup Axes
        axes = Axes(
            x_range=[-4, 4, 1],
            y_range=[-3, 6, 1],
            x_length=8,
            y_length=6,
            axis_config={"include_tip": False},
        ).add_coordinates()
        axes_labels = axes.get_axis_labels(x_label="x", y_label="y")
        self.play(Create(axes), Write(axes_labels))
        self.wait(0.5)

        # 3. Show Various Functions
        # Define functions and labels
        func_defs = [
            (lambda x: x**3 / 4, "y = \\frac{1}{4}x^3", RED), # Cubic scaled
            (lambda x: np.exp(x/2) - 1, "y = e^{x/2} - 1", GREEN), # Exponential scaled
            (lambda x: 2 * np.sin(x), "y = 2 \\sin(x)", BLUE), # Sine scaled
            (lambda x: 0.8 * x + 1.5, "y = mx + b", YELLOW) # Linear
        ]

        current_graph = None
        current_label = None

        for i, (func, label_tex, color) in enumerate(func_defs):
            graph = axes.plot(func, color=color)
            label = MathTex(label_tex, color=color).scale(0.8).to_corner(UL).shift(RIGHT*0.5 + DOWN*0.5)

            if current_graph: # If not the first function
                self.play(
                    ReplacementTransform(current_graph, graph),
                    ReplacementTransform(current_label, label)
                )
            else: # First function
                self.play(Create(graph), Write(label))

            current_graph = graph
            current_label = label
            self.wait(1.5 if i < len(func_defs) - 1 else 0.5) # Pause longer on non-linear

        # 4. Highlight Linear Function
        linear_graph = current_graph # It's the last one plotted
        linear_label = current_label

        self.play(
            linear_graph.animate.set_stroke(width=6).set_color(YELLOW), # Thicker and ensure color
            Wiggle(linear_label) # Briefly wiggle the label
        )
        self.wait(1)

        # --- Slope and Intercept Explanation ---
        # Initial values for the linear function shown
        m_initial = 0.8
        b_initial = 1.5

        # Use ValueTrackers for smooth animation later
        m = ValueTracker(m_initial)
        b = ValueTracker(b_initial)

        # Redraw the linear graph based on trackers - crucial for animation
        linear_graph_dynamic = always_redraw(
            lambda: axes.plot(
                lambda x: m.get_value() * x + b.get_value(),
                color=YELLOW,
                stroke_width=6 # Keep highlighted width
            )
        )
        # Remove the static graph and add the dynamic one
        self.remove(linear_graph)
        self.add(linear_graph_dynamic)
        # Keep the label, maybe update it if needed, but y=mx+b is fine for now
        self.add(linear_label.set_z_index(1)) # Ensure label is on top

        # 5. Explain Slope (m)
        x_start = 1.0
        x_end = x_start + 1.0 # Run = 1

        # Create slope triangle components - these need to update if m changes during explanation
        slope_triangle = always_redraw(lambda: axes.get_secant_slope_group(
            x=x_start,
            graph=linear_graph_dynamic, # Use the dynamic graph here
            dx=1.0, # Run = 1
            dx_line_color=WHITE,
            dy_line_color=WHITE,
            dx_label="run = 1",
            dy_label="rise = m",
            secant_line_color=None, # Don't draw the secant line itself
            secant_line_length=0,
        ).set_z_index(0)) # Behind the line

        m_label = always_redraw(lambda:
            MathTex("m = \\text{slope} = \\frac{\\text{rise}}{\\text{run}}")
            .scale(0.7)
            .next_to(slope_triangle, DOWN, buff=0.2)
        )

        self.play(Create(slope_triangle), Write(m_label))
        self.wait(2.5)

        # 6. Explain Intercept (b)
        intercept_dot = always_redraw(lambda:
            Dot(axes.c2p(0, b.get_value()), color=PINK, radius=0.1)
            .set_z_index(2) # Make sure dot is visible on top
        )
        b_label = always_redraw(lambda:
             MathTex(f"b = \\text{{y-intercept}} = {b.get_value():.1f}")
            .scale(0.7)
            .next_to(intercept_dot, RIGHT if b.get_value() < 0 else LEFT, buff=0.2)
        )

        self.play(FadeIn(intercept_dot, scale=0.5), Write(b_label))
        self.wait(2.5)

        # 7. Animate Parameter Changes
        # Fade out slope explanation for clarity during animation
        self.play(FadeOut(slope_triangle), FadeOut(m_label))
        self.wait(0.5)

        # Animate slope 'm'
        m_change_label = Text("Changing slope 'm'", font_size=28).to_corner(DR)
        self.play(Write(m_change_label))
        self.play(m.animate.set_value(2.0), run_time=2) # Increase slope
        self.wait(0.5)
        self.play(m.animate.set_value(-1.0), run_time=3) # Decrease slope to negative
        self.wait(0.5)
        self.play(m.animate.set_value(m_initial), run_time=2) # Return to original slope
        self.play(FadeOut(m_change_label))
        self.wait(0.5)

        # Animate intercept 'b'
        b_change_label = Text("Changing intercept 'b'", font_size=28).to_corner(DR)
        self.play(Write(b_change_label))
        self.play(b.animate.set_value(4.0), run_time=2) # Increase intercept
        self.wait(0.5)
        self.play(b.animate.set_value(-1.0), run_time=3) # Decrease intercept
        self.wait(0.5)
        self.play(b.animate.set_value(b_initial), run_time=2) # Return to original intercept
        self.play(FadeOut(b_change_label), FadeOut(intercept_dot), FadeOut(b_label)) # Fade out b explanation too
        self.wait(1)

        # Optional: Fade out everything before next clip
        self.play(FadeOut(linear_graph_dynamic), FadeOut(linear_label), FadeOut(axes), FadeOut(axes_labels))
        self.wait(1) 