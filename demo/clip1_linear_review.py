# clip1_linear_review.py
from manim import *

class Clip1LinearReview(Scene):
    def construct(self):
        # 1. Transition Text
        title = Text("Linear Regression").scale(1.5)
        self.play(FadeIn(title, direction=UP))
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
            #(lambda x: x**3, "y = x^3", RED), # Cubic scaled
            # (lambda x: np.exp(x), "y = e^{x}", GREEN), # Exponential scaled
            # (lambda x: np.sin(x), "y = \\sin(x)", BLUE), # Sine scaled
            (lambda x: 0.8*x + 1.5, "y = mx + b", YELLOW) # Linear
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
        linear_graph_static = current_graph # Static graph from the loop
        linear_label_static = current_label # Static label "y=mx+b"

        self.play(
            linear_graph_static.animate.set_stroke(width=6).set_color(YELLOW), # Thicker and ensure color
            Wiggle(linear_label_static) # Briefly wiggle the label
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
        self.remove(linear_graph_static)
        self.add(linear_graph_dynamic)
        # Keep the static label "y=mx+b" for now, positioned correctly
        # Ensure it's on top
        static_eq_label = linear_label_static
        self.add(static_eq_label.set_z_index(1))

        # 5. Explain Slope (m)
        x_start = 1.0
        dx_run = 1.0 # Define run value
        
        # Create slope triangle components - these need to update if m changes during explanation
        slope_triangle = always_redraw(lambda: axes.get_secant_slope_group(
            x=x_start,
            graph=linear_graph_dynamic, # Use dynamic graph
            dx=dx_run, # Use defined run value
            dx_line_color=WHITE,
            dy_line_color=WHITE,
            dx_label=f"run = {dx_run:.1f}", # Show run value in label
            dy_label=f"rise = {m.get_value() * dx_run:.2f}", # Show calculated rise
            secant_line_color=None, # Don't draw the secant line itself
            secant_line_length=0,
        ).set_z_index(0)) # Behind the line

        # Updated m_label showing calculation
        m_label = always_redraw(lambda:
            MathTex(f"m = \\frac{{\\text{{rise}}}}{{\\text{{run}}}} = \\frac{{{m.get_value() * dx_run:.2f}}}{{{dx_run:.1f}}} = {m.get_value():.2f}")
            .scale(0.7)
            .next_to(slope_triangle, UP, buff=0.2)
        )

        self.play(Create(slope_triangle), Write(m_label))
        self.wait(3) # Increased wait time to read the label

        # --- Animate m into equation ---
        # Create the target equation label with the numerical value of m
        # This needs to be dynamic for the next step and final animations
        eq_label_with_m = always_redraw(lambda:
            MathTex(f"y = {m.get_value():.2f}x + b", color=YELLOW)
            .scale(0.8)
            .to_corner(UL).shift(RIGHT*0.5 + DOWN*0.5) # Same position as original
            .set_z_index(1)
        )

        # Animate the transformation from "y=mx+b" to "y = {m_val}x + b"
        self.play(ReplacementTransform(static_eq_label, eq_label_with_m))
        self.wait(1.5)

        # 6. Explain Intercept (b)
        intercept_dot = always_redraw(lambda:
            Dot(axes.c2p(0, b.get_value()), color=PINK, radius=0.1)
            .set_z_index(2) # Make sure dot is visible on top
        )
        # b_label already shows the dynamic value
        b_label = always_redraw(lambda:
             MathTex(f"b = \\text{{y-intercept}} = {b.get_value():.1f}")
            .scale(0.7)
            .next_to(intercept_dot, RIGHT if b.get_value() >= 0 else LEFT, buff=0.2) # Adjusted condition slightly
        )

        self.play(FadeIn(intercept_dot, scale=0.5), Write(b_label))
        self.wait(3) # Increased wait time

        # --- Animate b into equation ---
        # Create the final target equation with numerical values for m and b
        # This needs to be dynamic for the final animations
        final_eq_label = always_redraw(lambda:
            MathTex(f"y = {m.get_value():.2f}x + {b.get_value():.1f}", color=YELLOW)
            .scale(0.8)
            .to_corner(UL).shift(RIGHT*0.5 + DOWN*0.5) # Same position
            .set_z_index(1)
        )

        # Animate the transformation from "y = {m_val}x + b" to "y = {m_val}x + {b_val}"
        # We transform the *currently displayed* label (eq_label_with_m)
        self.play(ReplacementTransform(eq_label_with_m, final_eq_label))
        self.wait(1.5)

        # 7. Animate Parameter Changes
        # Fade out intercept explanation for clarity during animation (but keep slope triangle)
        self.play(FadeOut(intercept_dot), FadeOut(b_label))
        self.wait(0.5)

        # Animate slope 'm' - final_eq_label will update automatically
        m_change_label = Text("Changing slope 'm'", font_size=28).to_corner(DR)
        self.play(Write(m_change_label))
        self.play(m.animate.set_value(1.6), run_time=2) # Increase slope and make slower
        self.wait(1)
        self.play(m.animate.set_value(-1.0), run_time=2) # Decrease slope to negative and make slower
        self.wait(1)
        self.play(m.animate.set_value(m_initial), run_time=1) # Return to original slope and make slower
        self.play(FadeOut(m_change_label))
        self.wait(0.5)

        # Now fade out the slope explanation before the intercept animation
        self.play(FadeOut(slope_triangle), FadeOut(m_label))
        self.wait(0.5)

        # Animate intercept 'b' - final_eq_label will update automatically
        b_change_label = Text("Changing intercept 'b'", font_size=28).to_corner(DR)
        self.play(Write(b_change_label))
        self.play(b.animate.set_value(4.0), run_time=2) # Increase intercept
        self.wait(0.5)
        self.play(b.animate.set_value(-1.0), run_time=3) # Decrease intercept
        self.wait(0.5)
        self.play(b.animate.set_value(b_initial), run_time=2) # Return to original intercept
        self.play(FadeOut(b_change_label)) # Keep final equation on screen
        self.wait(1)

        # Optional: Fade out everything before next clip
        # Now we fade out the dynamic graph and the final label
        self.play(FadeOut(linear_graph_dynamic), FadeOut(final_eq_label), FadeOut(axes), FadeOut(axes_labels))
        self.wait(1)
        '''
        # Add "Insights" title
        insights_title = Text("Insights", color=YELLOW).scale(1.0)
        insights_title.to_edge(UP, buff=0.5)
        self.play(Write(insights_title))
        self.wait(0.5)

        # Create insights split into two lines each for better fitting
        insight1_line1 = Text("1. The slope (m) corresponds to how much the y-variable", 
                            t2c={"slope (m)": YELLOW}).scale(0.7)
        insight1_line2 = Text("   changes for a 1 unit increase in the x-variable.",
                            t2c={"1 unit increase": YELLOW}).scale(0.7)

        insight2_line1 = Text("2. The y-intercept (b) is the value of the y-variable", 
                            t2c={"y-intercept (b)": YELLOW}).scale(0.7)
        insight2_line2 = Text("   when the x-variable is 0.",
                            t2c={"x-variable is 0": YELLOW}).scale(0.7)

        # Group each insight's lines
        insight1 = VGroup(insight1_line1, insight1_line2).arrange(DOWN, aligned_edge=LEFT)
        insight2 = VGroup(insight2_line1, insight2_line2).arrange(DOWN, aligned_edge=LEFT)

        # Arrange insights vertically with proper spacing
        insights_group = VGroup(insight1, insight2).arrange(DOWN, buff=0.8, aligned_edge=LEFT)
        insights_group.next_to(insights_title, DOWN, buff=0.8)

        # Animate insights appearing one by one with pauses (each complete insight at once)
        self.play(FadeIn(insight1))
        self.wait(1.5)

        self.play(FadeIn(insight2))
        self.wait(1.5)

        # Fade out everything
        self.play(FadeOut(insights_title), FadeOut(insights_group))
        self.wait(1)'''

# To render: manim -pqh demo/clip1_linear_review.py Clip1LinearReview
