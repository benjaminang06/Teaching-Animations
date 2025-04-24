from manim import *
import numpy as np

# Helper function to create residuals for a given line/dots
def create_residuals(axes_obj, dots_collection, m_val, b_val, line_color=GRAY, stroke_width=2):
    residuals_group = VGroup()
    for dot in dots_collection:
        x_val = axes_obj.p2c(dot.get_center())[0]
        y_actual = axes_obj.p2c(dot.get_center())[1]
        y_predicted = m_val * x_val + b_val
        start_point = axes_obj.c2p(x_val, y_predicted)
        end_point = dot.get_center()
        res_line = DashedLine(start_point, end_point, color=line_color, stroke_width=stroke_width)
        residuals_group.add(res_line)
    return residuals_group

# Dynamic squares function moved to the top level for reuse
def create_dynamic_squares(axes_obj, dot_collection, m_val, b_val):
    sq_group = VGroup()
    for dot in dot_collection:
        x_c = axes_obj.p2c(dot.get_center())[0]
        y_c = axes_obj.p2c(dot.get_center())[1]
        y_pred = m_val * x_c + b_val
        side = max(0.01, abs(y_c - y_pred))
        sq = Square(side_length=side, color=BLUE, fill_opacity=0.5)
        sq.move_to(axes_obj.c2p(x_c, (y_c + y_pred) / 2))
        sq_group.add(sq)
    return sq_group

class Clip2OLSIntuition(Scene):
    def construct(self):
        # 1. Title
        title = Text("Fitting a Line: How to Choose?").scale(1.1)
        self.play(Write(title))
        self.wait(1.5)
        self.play(FadeOut(title))
        self.wait(0.5)

        # 2. Setup Generic Scatter Plot
        np.random.seed(0)
        x_coords = np.array([1, 1.5, 2.5, 3, 4, 4.5, 5.5, 6])
        y_coords = 0.7 * x_coords + 1.5 + np.random.normal(0, 0.8, size=x_coords.size)

        axes = Axes(
            x_range=[0, 7, 1], y_range=[0, 7, 1], x_length=7, y_length=5.5,
            axis_config={"include_tip": False, "stroke_opacity": 0.5},
        ).shift(DOWN*1.0)
        axes_labels = axes.get_axis_labels(x_label="X", y_label="Y")
        dots = VGroup(*[Dot(axes.c2p(x, y), color=YELLOW) for x, y in zip(x_coords, y_coords)])
        plot_elements = VGroup(axes, axes_labels, dots)

        self.play(Create(plot_elements))
        self.wait(1)

        # NEW: Line exploration animation before the "intuitive fit" section
        search_text = Text("We choose parameters to fit this data...").scale(0.6).to_edge(UP)
        self.play(Write(search_text))
        self.wait(0.5)

        # Create initial line with random parameters that look clearly off
        initial_m, initial_b = 0.9, 0.8  # Starting values
        search_line = axes.plot(lambda x: initial_m * x + initial_b, color=YELLOW_D)

        # Show the parameters directly under the search text instead of equation
        param_text = MathTex(
            r"m = " + f"{initial_m:.1f}",
            r",\quad b = " + f"{initial_b:.1f}"
        ).scale(0.7)
        param_text.next_to(search_text, DOWN, buff=0.3)

        self.play(Create(search_line), Write(param_text))
        self.wait(0.5)

        # Create several transitions exploring different parameter values
        # These will progressively move toward our "poor fit" (m_a=0.2, b_a=3.5)
        transitions = [
            (0.9, 0.8),  # Initial
            (1.2, 1.5),  # Steeper with higher intercept
            (0.5, 2.0),  # Less steep
            (0.8, 3.0),  # Higher intercept
            (0.4, 3.8),  # Getting closer to poor fit
            (0.2, 3.5),  # Final value - matching our "poor fit" line
        ]

        for i in range(1, len(transitions)):
            prev_m, prev_b = transitions[i-1]
            next_m, next_b = transitions[i]
            next_line = axes.plot(lambda x: next_m * x + next_b, color=YELLOW_D)
            next_param_text = MathTex(
                r"m = " + f"{next_m:.1f}",
                r",\quad b = " + f"{next_b:.1f}"
            ).scale(0.7)
            next_param_text.next_to(search_text, DOWN, buff=0.3)
            
            self.play(
                ReplacementTransform(search_line, next_line),
                ReplacementTransform(param_text, next_param_text),
                run_time=0.8
            )
            search_line = next_line
            param_text = next_param_text
            self.wait(0.3)

        # First, define the poor fit line (but don't show it yet)
        m_a, b_a = 0.2, 3.5  # Clearly bad parameters
        line_a = axes.plot(lambda x: m_a * x + b_a, color=RED)

        # Now we can transform the search line into line_a
        self.play(
            FadeOut(search_text),
            FadeOut(param_text),
            ReplacementTransform(search_line, line_a)  # Now this will work because line_a exists
        )
        self.wait(1)  # Add a pause here to let the poor fit line be visible for a moment

        # Continue with the existing code
        intro_text = Text("Visually, it is easy to determine if a line is a good fit for a set of points.").scale(0.6).to_edge(UP)
        self.play(Write(intro_text))
        self.wait(1.5)

        beta1_ols, beta0_ols = np.polyfit(x_coords, y_coords, 1)

        # ADD LABELS to the poor fit line (it's already on screen)
        label_a = MathTex(f"y = {m_a:.1f}x + {b_a:.1f}", color=RED).scale(0.7).next_to(line_a, UP, buff=0.1)
        fit_label_a = Text("Good Fit?", color=RED).scale(0.6).next_to(label_a, RIGHT)

        # Show residuals for line A 
        residuals_a = create_residuals(axes, dots, m_a, b_a)
        self.play(Write(label_a), Write(fit_label_a), Create(residuals_a), run_time=1.5)
        self.wait(1)  # Add a pause to appreciate the residuals

        # NEW: Add mathematical definition for residuals when first shown
        residual_def_text = Text("These vertical lines are 'residuals'").scale(0.6).to_edge(UP, buff=1.0)
        residual_formula = MathTex(r"e_i = y_i - (mx_i + b) = \text{actual} - \text{predicted}").scale(0.7)
        residual_formula.next_to(residual_def_text, DOWN, buff=0.2)
        self.play(FadeOut(intro_text), Write(residual_def_text), Write(residual_formula))
        self.wait(1.5)

        # Add back the circumscribe animation for the poor fit
        self.play(Circumscribe(dots, color=RED, fade_out=True, run_time=1.5))
        self.wait(1.5)  # Add another pause after the circumscription

        # We can keep the residuals visible a bit longer before fading them
        self.wait(1)
        self.play(FadeOut(residuals_a), FadeOut(residual_def_text), FadeOut(residual_formula), FadeOut(fit_label_a), FadeOut(label_a), FadeOut(line_a))
        
        self.wait(0.5)  # Add a small pause before transitioning to the good fit
        '''
        # Good Fit Line (Example B - using OLS params directly or close to them)
        line_b = axes.plot(lambda x: beta1_ols * x + beta0_ols, color=GREEN)
        label_b = MathTex(f"y = {beta1_ols:.1f}x + {beta0_ols:.1f}", color=GREEN).scale(0.7).next_to(line_b, DOWN, buff=0.1)
        fit_label_b = Text("Good Fit?", color=GREEN).scale(0.6).next_to(label_b, RIGHT)

        # Show residuals for line B
        residuals_b = create_residuals(axes, dots, beta1_ols, beta0_ols)
        self.play(
            ReplacementTransform(line_a, line_b),
            ReplacementTransform(label_a, label_b),
            ReplacementTransform(fit_label_a, fit_label_b),
            Create(residuals_b)
        )
        
        # NEW: Remind viewers about residuals for good fit
        residual_good_text = Text("Smaller residuals").scale(0.6).to_edge(UP, buff=1.0)
        self.play(Write(residual_good_text))
        self.wait(1)
        
        self.play(Circumscribe(dots, color=GREEN, fade_out=True, run_time=1.5))
        self.wait(2.5)

        # Fade out examples and intro text
        self.play(FadeOut(residual_good_text), FadeOut(line_b), FadeOut(label_b), FadeOut(fit_label_b), FadeOut(residuals_b))
        self.wait(0.5)
        '''
        # 4. Bridge to Mathematical Definition
        math_intro_text = Text("How do we mathematically define and find the 'best' line?").scale(0.6).to_edge(UP)
        self.play(Write(math_intro_text))
        self.wait(2)

        # 5. Introduce OLS and SSR Directly - Using Dynamic Elements from the Start
        self.play(FadeOut(math_intro_text))
        ols_intro_text = Text("One common method: Ordinary Least Squares (OLS)").scale(0.6).to_edge(UP)
        self.play(Write(ols_intro_text))

        # Create trackers for parameters (start with NON-optimal values)
        initial_poor_m = 0.2  # Start with a poor slope
        initial_poor_b = beta0_ols + 2.0  # Start with a poor intercept 
        m_tracker = ValueTracker(initial_poor_m)  # Start with poor values
        b_tracker = ValueTracker(initial_poor_b)

        # Start with the line in red to indicate poor fit
        line_color_tracker = ValueTracker(1)  # Start with 1 = red
        ols_line_dynamic = always_redraw(lambda:
            axes.plot(
                lambda x: m_tracker.get_value() * x + b_tracker.get_value(), 
                color=interpolate_color(GREEN, RED, line_color_tracker.get_value())
            )
        )

        # Create line first with RED color (poor fit)
        self.play(Create(ols_line_dynamic))
        self.wait(0.5)

        # Show Residuals for the dynamic line (let's still use residuals for clear visualization)
        residuals_ols = create_residuals(axes, dots, initial_poor_m, initial_poor_b)
        res_label = Text("Recall: residuals are the vertical distances").scale(0.6).next_to(ols_intro_text, DOWN)
        res_formula = MathTex(r"e_i = y_i - (mx_i + b)").scale(0.6).next_to(res_label, DOWN)
        
        self.play(Write(res_label), Write(res_formula))
        self.play(Create(residuals_ols))
        self.wait(2)

        # Show Squaring and SSR - Using Dynamic Squares from the Start
        self.play(FadeOut(res_label), FadeOut(res_formula))
        ssr_text = Text("OLS minimizes the Sum of the Squared Residuals (SSR)").scale(0.6).next_to(ols_intro_text, DOWN)
        ssr_formula = MathTex(
            r"SSR &= \sum e_i^2\\", 
            r"&= \sum (y_i - (mx_i + b))^2"
        ).scale(0.6).next_to(ssr_text, DOWN)
        self.play(Write(ssr_text), Write(ssr_formula))

        # Create dynamic squares immediately
        squares_dynamic = always_redraw(lambda:
            create_dynamic_squares(axes, dots, m_tracker.get_value(), b_tracker.get_value())
        )
        
        # Animate squares appearing through transformation from residuals
        anims = []
        temp_squares = create_dynamic_squares(axes, dots, initial_poor_m, initial_poor_b)  # Create static version matching current line
        transformed_squares = VGroup()  # Group to track the transformed objects
        for i, res_line in enumerate(residuals_ols):
            if i < len(temp_squares):
                copied_line = res_line.copy()
                anims.append(Transform(copied_line, temp_squares[i]))
                transformed_squares.add(copied_line)  # Add to tracking group
        
        self.play(AnimationGroup(*anims, lag_ratio=0.1))
        self.add(squares_dynamic)  # Add the always_redraw version
        self.play(FadeOut(residuals_ols), FadeOut(transformed_squares))  # Fade out both original residuals AND transformed squares
        self.wait(3)
        
        # Fade out the explanation text
        self.play(FadeOut(ols_intro_text), FadeOut(ssr_text), FadeOut(ssr_formula))

        # 6. OLS Goal and Minimization Animation - One seamless formula
        # Create a function to calculate actual SSR value for current parameters
        def calculate_ssr(m_val, b_val):
            ssr = sum([(y - (m_val * x + b_val))**2 for x, y in zip(x_coords, y_coords)])
            return ssr

        # Create tracker to control symbolic vs numeric display
        display_mode = ValueTracker(0)  # 0=symbolic, 1=numeric

        # Create a single formula that changes only the variable parts
        ssr_formula = always_redraw(lambda:
            MathTex(
                r"\text{Minimize: } SSR = \sum_{i=1}^{n} (y_i - (",
                # This part changes from "m" to the actual value
                r"m" if display_mode.get_value() < 0.5 else f"{m_tracker.get_value():.2f}",
                r"x_i + ",
                # This part changes from "b" to the actual value
                r"b" if display_mode.get_value() < 0.5 else f"{b_tracker.get_value():.2f}",
                r"))^2",
                # The SSR value only appears after switching to numeric mode
                "" if display_mode.get_value() < 0.5 else r" = " + f"{calculate_ssr(m_tracker.get_value(), b_tracker.get_value()):.2f}"
            ).scale(0.7).to_corner(UP)
        )

        # Show the formula (initially with symbolic m, b)
        self.play(Write(ssr_formula))
        self.wait(0.5)  # First pause

        # Switch to numeric values (showing the current poor fit values)
        self.play(display_mode.animate.set_value(1), run_time=0.7)
        self.wait(0.5)  # Second pause

        # Now let's explore some other poor fits before finding the optimal
        poor_b_2 = beta0_ols - 2.0  # Try a different poor fit (too low)
        self.play(b_tracker.animate.set_value(poor_b_2), run_time=2.0)
        self.wait(0.5)

        # Try different slope
        poor_m_2 = 1.2  # Try a steeper slope (still poor fit)
        self.play(m_tracker.animate.set_value(poor_m_2), run_time=2.0)
        self.wait(0.5)

        # NOW animate to the optimal values - first fix the slope
        self.play(m_tracker.animate.set_value(beta1_ols), run_time=2.0)
        self.wait(0.3)

        # Then fix the intercept
        self.play(b_tracker.animate.set_value(beta0_ols), run_time=2.0)
        self.wait(0.3)

        # Now change the color to green to indicate optimal fit
        self.play(line_color_tracker.animate.set_value(0), run_time=0.7)
        
        # Final OLS line label
        ols_label = Text("OLS Best-Fit Line").scale(0.6).next_to(ols_line_dynamic, RIGHT, buff=0.1).set_color(GREEN)
        self.play(Write(ols_label))
        self.wait(2)

        # When transitioning to the calculus section, update the group name
        plot_elements_final = VGroup(axes, axes_labels, dots, ols_line_dynamic, squares_dynamic, ols_label)
        explanation_group = VGroup(ssr_formula)  # Now just this one formula

        # 7. Mention Calculus & Formulas
        # Group ALL plot elements for fading, including squares_dynamic and ols_label
        plot_elements_final = VGroup(axes, axes_labels, dots, ols_line_dynamic, squares_dynamic, ols_label)
        
        # NEW: Add mathematical notation for minimization step
        # First show the calculus approach
        min_process = MathTex(
            r"\text{To minimize SSR, we use calculus:}\\",
            r"\frac{\partial \text{SSR}}{\partial m} = 0 \quad \text{and} \quad \frac{\partial \text{SSR}}{\partial b} = 0"
        ).scale(0.6).to_corner(DOWN)
        
        self.play(Write(min_process))
        self.wait(2)
        
        # Fade out BOTH the plot elements, explanation group, and minimization
        self.play(
            FadeOut(plot_elements_final),
            FadeOut(explanation_group),
            FadeOut(min_process)
        )
        self.wait(0.5)
        
        calc_text = Text("Solving the equations gives us:", t2c={"equations": YELLOW}).scale(0.6)
        m_hat_formula = MathTex(r"\hat{m} = \frac{\sum (x_i - \bar{x})(y_i - \bar{y})}{\sum (x_i - \bar{x})^2}").scale(0.6)
        b_hat_formula = MathTex(r"\hat{b} = \bar{y} - \hat{m} \bar{x}").scale(0.6)
        formula_explanation_grp = VGroup(calc_text, m_hat_formula, b_hat_formula).arrange(DOWN, buff=0.4).center()
        preview_text = Text("We use these to compute the line for real data.").scale(0.6).next_to(formula_explanation_grp, DOWN, buff=0.5)
        
        self.play(Write(formula_explanation_grp))
        self.wait(3)
        self.play(Write(preview_text))
        self.wait(2.5)
        self.play(FadeOut(formula_explanation_grp), FadeOut(preview_text))
        self.wait(0.5)

# To render: manim -pql demo/clip2_OLS.py Clip2OLSIntuition   