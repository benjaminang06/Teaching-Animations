from manim import *
import numpy as np

class Clip4RealLifeExample(Scene):
    def construct(self):
        # 1. Scenario Title
        scenario_title = Text("Example: Study Days vs. Exam Grade").scale(0.9)
        scenario_title.to_edge(UP)
        self.play(Write(scenario_title))
        self.wait(1)

        # 2. Data Table
        # Define the data
        data = [
            ["2", "60"],
            ["5", "85"],
            ["1", "60"],
            ["7", "88"],
            ["3", "75"],
            ["4", "72"],
            ["6", "80"]
        ]
        # Define headers separately for col_labels
        headers = ["Days (X)", "Grade (Y)"]

        # Extract numerical data for later use
        data_points_num = np.array([[float(x), float(y)] for x, y in data])
        x_values = data_points_num[:, 0]
        y_values = data_points_num[:, 1]

        # Create the table
        data_table = Table(
            data,
            col_labels=[Text(h) for h in headers],
            include_outer_lines=True,
            h_buff=0.7,
            v_buff=0.4,
            line_config={"stroke_width": 2, "color": WHITE}
        ).scale(0.55)

        # Position the table below the title and center it
        data_table.next_to(scenario_title, DOWN, buff=0.5)

        # Animate the table appearing
        self.play(Create(data_table), run_time=2)
        self.wait(2)

        # 3. Initial Graph on Right Side (will be removed for calculations)
        axes = Axes(
            x_range=[0, 8, 1],
            y_range=[50, 100, 10],
            x_length=5.5,
            y_length=4,
            axis_config={"include_numbers": True, "include_tip": False},
            x_axis_config={"numbers_to_include": np.arange(1, 8, 1)},
            y_axis_config={"numbers_to_include": np.arange(50, 101, 10)},
        )

        axes_labels = axes.get_axis_labels(
            x_label=Tex("Days Studying (X)").scale(0.7),
            y_label=Tex("Exam Grade (Y)").scale(0.7)
        )
        
        # Group axes and labels
        axes_group = VGroup(axes, axes_labels)
        axes_group.to_edge(RIGHT, buff=0.5)
        axes_group.shift(DOWN*0.3)

        # Shrink table and move it to left side - centered vertically
        self.play(
            data_table.animate.scale(0.7).to_edge(LEFT, buff=0.5).shift(DOWN*0.3),
            Create(axes),
            Write(axes_labels),
            run_time=2
        )
        self.wait(1)

        # 4. Initial Scatter Plot
        dots = VGroup()
        for x_val, y_val in data_points_num:
            dot = Dot(point=axes.c2p(x_val, y_val), color=YELLOW)
            dots.add(dot)

        # Animate dots appearing
        self.play(AnimationGroup(*[GrowFromCenter(dot) for dot in dots], lag_ratio=0.2), run_time=2)
        self.wait(2)

        # 5. OLS Introduction
        ols_text = Text("Ordinary Least Squares (OLS)").scale(0.6)
        ols_text.next_to(scenario_title, DOWN, buff=0.2).align_to(scenario_title, RIGHT)
        
        self.play(Write(ols_text), run_time=1)
        self.wait(1)

        # 6. TRANSITION: Remove graph, keep table for calculations
        # Move table further to the left
        self.play(
            FadeOut(axes_group),
            FadeOut(dots),
            FadeOut(ols_text),
            data_table.animate.scale(1.25).to_edge(LEFT, buff=0.3).center().shift(LEFT*3.5),
            run_time=1.5
        )
        
        # Add the closed form formulas below the table
        closed_form_title = Text("OLS Formulas:").scale(0.6)
        closed_form_m = MathTex(r"\hat{m} = \frac{\sum (x_i - \bar{x})(y_i - \bar{y})}{\sum (x_i - \bar{x})^2}").scale(0.55)
        closed_form_b = MathTex(r"\hat{b} = \bar{y} - \hat{m} \cdot \bar{x}").scale(0.55)

        closed_form_group = VGroup(closed_form_title, closed_form_m, closed_form_b).arrange(DOWN, buff=0.2, aligned_edge=LEFT)
        closed_form_group.next_to(data_table, DOWN, buff=0.5).align_to(data_table, LEFT).shift(RIGHT*0.5)

        self.play(Write(closed_form_group), run_time=1.5)
        self.wait(1)

        # 7. Setup Calculation Area - moved more to the LEFT
        calc_title = Text("Step-by-step OLS Calculation:").scale(0.7)
        calc_title.to_corner(UR, buff=0.8).shift(DOWN*1.25 + LEFT*1.5)  # Added LEFT shift to move it more left

        # Calculate means
        x_mean = np.mean(x_values)
        y_mean = np.mean(y_values)
        
        # Then adjust all the subsequent calculation steps to follow from this new position
        step1_text = Text("Step 1: Calculate means").scale(0.55)
        step1_text.next_to(calc_title, DOWN, buff=0.3).align_to(calc_title, LEFT)
       
        # Simplified means calculation - just 2 lines
        step1_calc_x = MathTex(
            r"\bar{x} = \frac{1}{7}(2 + 5 + 1 + 7 + 3 + 4 + 6) = 4.00"
        ).scale(0.5)
        
        

        step1_calc_y = MathTex(
            r"\bar{y} = \frac{1}{7}(60 + 85 + 60 + 88 + 75 + 72 + 80) = 74.29"
        ).scale(0.5)
        
        
        step1_calcs = VGroup(step1_calc_x, step1_calc_y).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        step1_calcs.next_to(step1_text, DOWN, buff=0.2).align_to(step1_text, LEFT)
        
        self.play(Write(calc_title), run_time=1)
        self.play(Write(step1_text), run_time=1.5)
        self.wait(0.5)

        # Position each calculation line independently
        step1_calc_x.next_to(step1_text, DOWN, buff=0.2).align_to(step1_text, LEFT)
        step1_calc_y.next_to(step1_calc_x, DOWN, buff=0.2).align_to(step1_calc_x, LEFT)

        # Now show each calculation line one at a time
        self.play(Write(step1_calc_x), run_time=1.5)
        self.wait(1)  # Pause to understand x̄
        self.play(Write(step1_calc_y), run_time=1.5)
        self.wait(1.5)  # Pause to understand ȳ

        # Group them now for later reference/movement
        step1_calcs = VGroup(step1_calc_x, step1_calc_y)

        # Step 2 with smaller text
        step2_text = Text("Step 2: Calculate numerator and denominator").scale(0.55)
        step2_text_pos = step2_text.copy().next_to(step1_calcs, DOWN, buff=0.4).align_to(step1_text, LEFT)
        self.play(Write(step2_text_pos), run_time=1)
        self.wait(0.5)  # Pause after title

        # Calculate values
        x_minus_mean = x_values - x_mean
        y_minus_mean = y_values - y_mean
        products = x_minus_mean * y_minus_mean
        x_minus_mean_squared = x_minus_mean ** 2

        numerator = sum(products)
        denominator = sum(x_minus_mean_squared)

        # Split the numerator calculation into parts
        step2_calc_num_formula = MathTex(
            r"\text{Numerator} = \sum (x_i - \bar{x})(y_i - \bar{y})"
        ).scale(0.48)
        step2_calc_num_formula.next_to(step2_text_pos, DOWN, buff=0.2).align_to(step2_text_pos, LEFT)

        step2_calc_num_values = MathTex(
            r"= (2 - 4)(60 - 74.29) + (5 - 4)(85 - 74.29) + \ldots = " + f"{numerator:.2f}"
        ).scale(0.48)
        step2_calc_num_values.next_to(step2_calc_num_formula, DOWN, buff=0.1).align_to(step2_calc_num_formula, LEFT)

        # Split the denominator calculation into parts
        step2_calc_den_formula = MathTex(
            r"\text{Denominator} = \sum (x_i - \bar{x})^2"
        ).scale(0.48)
        step2_calc_den_formula.next_to(step2_calc_num_values, DOWN, buff=0.2).align_to(step2_calc_num_formula, LEFT)

        step2_calc_den_values = MathTex(
            r"= (2 - 4)^2 + (5 - 4)^2 + \ldots = " + f"{denominator:.2f}"
        ).scale(0.48)
        step2_calc_den_values.next_to(step2_calc_den_formula, DOWN, buff=0.1).align_to(step2_calc_den_formula, LEFT)

        # Play each line one at a time
        self.play(Write(step2_calc_num_formula), run_time=1.5)
        self.wait(0.5)
        self.play(Write(step2_calc_num_values), run_time=1.5)
        self.wait(1)  # Longer pause to understand numerator

        self.play(Write(step2_calc_den_formula), run_time=1.5)
        self.wait(0.5)
        self.play(Write(step2_calc_den_values), run_time=1.5)
        self.wait(1.5)  # Longer pause to understand denominator

        # Group for transitions
        step2_calcs_pos = VGroup(step2_calc_num_formula, step2_calc_num_values, step2_calc_den_formula, step2_calc_den_values)

        # Now REMOVE Step 1 and move Step 2 up to Step 1's position
        step2_text.next_to(calc_title, DOWN, buff=0.3).align_to(calc_title, LEFT)

        # Need to recreate these in their proper positions for the transition
        step2_calc_num = VGroup(
            MathTex(r"\text{Numerator} = \sum (x_i - \bar{x})(y_i - \bar{y})").scale(0.48),
            MathTex(r"= (2 - 4)(60 - 74.29) + (5 - 4)(85 - 74.29) + \ldots = " + f"{numerator:.2f}").scale(0.48)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)

        step2_calc_den = VGroup(
            MathTex(r"\text{Denominator} = \sum (x_i - \bar{x})^2").scale(0.48),
            MathTex(r"= (2 - 4)^2 + (5 - 4)^2 + \ldots = " + f"{denominator:.2f}").scale(0.48)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)

        step2_calcs = VGroup(step2_calc_num, step2_calc_den).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        step2_calcs.next_to(step2_text, DOWN, buff=0.2).align_to(step2_text, LEFT)

        self.play(
            FadeOut(step1_text), 
            FadeOut(step1_calcs),
            ReplacementTransform(step2_text_pos, step2_text),
            ReplacementTransform(step2_calcs_pos, step2_calcs),
            run_time=1.5
        )
        self.wait(1)

        # Step 3: Calculate slope and intercept - line by line
        m_value = numerator / denominator
        b_value = y_mean - m_value * x_mean

        step3_text = Text("Step 3: Calculate slope and intercept").scale(0.55)
        step3_text_pos = step3_text.copy().next_to(step2_calcs, DOWN, buff=0.4).align_to(step2_text, LEFT)
        self.play(Write(step3_text_pos), run_time=1)
        self.wait(0.5)  # Pause after title

        # Slope calculation line by line
        step3_calc_m_formula = MathTex(
            r"\hat{m} = \frac{\text{Numerator}}{\text{Denominator}}"
        ).scale(0.5)
        step3_calc_m_formula.next_to(step3_text_pos, DOWN, buff=0.2).align_to(step3_text_pos, LEFT)

        step3_calc_m_values = MathTex(
            r"= \frac{" + f"{numerator:.2f}" + "}{" + f"{denominator:.2f}" + "} = " + f"{m_value:.2f}"
        ).scale(0.5)
        step3_calc_m_values.next_to(step3_calc_m_formula, DOWN, buff=0.1).align_to(step3_calc_m_formula, LEFT)

        # Intercept calculation line by line
        step3_calc_b_formula = MathTex(
            r"\hat{b} = \bar{y} - \hat{m} \cdot \bar{x}"
        ).scale(0.5)
        step3_calc_b_formula.next_to(step3_calc_m_values, DOWN, buff=0.2).align_to(step3_calc_m_formula, LEFT)

        step3_calc_b_values = MathTex(
            r"= " + f"{y_mean:.2f} - {m_value:.2f} \cdot {x_mean:.2f} = " + f"{b_value:.2f}"
        ).scale(0.5)
        step3_calc_b_values.next_to(step3_calc_b_formula, DOWN, buff=0.1).align_to(step3_calc_b_formula, LEFT)

        # Play each line one at a time
        self.play(Write(step3_calc_m_formula), run_time=1.5)
        self.wait(0.5)
        self.play(Write(step3_calc_m_values), run_time=1.5)
        self.wait(1.0)  # Pause for slope

        self.play(Write(step3_calc_b_formula), run_time=1.5)
        self.wait(0.5)
        self.play(Write(step3_calc_b_values), run_time=1.5)
        self.wait(1.5)  # Longer pause for intercept

        # Group for transitions
        step3_calcs_pos = VGroup(step3_calc_m_formula, step3_calc_m_values, step3_calc_b_formula, step3_calc_b_values)

        # Now REMOVE Step 2 and move Step 3 up to Step 2's position
        step3_text.next_to(calc_title, DOWN, buff=0.3).align_to(calc_title, LEFT)

        # Need to recreate these in their proper positions for the transition
        step3_calc_m = VGroup(
            MathTex(r"\hat{m} = \frac{\text{Numerator}}{\text{Denominator}}").scale(0.5),
            MathTex(r"= \frac{" + f"{numerator:.2f}" + "}{" + f"{denominator:.2f}" + "} = " + f"{m_value:.2f}").scale(0.5)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)

        step3_calc_b = VGroup(
            MathTex(r"\hat{b} = \bar{y} - \hat{m} \cdot \bar{x}").scale(0.5),
            MathTex(r"= " + f"{y_mean:.2f} - {m_value:.2f} \cdot {x_mean:.2f} = " + f"{b_value:.2f}").scale(0.5)
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.1)

        step3_calcs = VGroup(step3_calc_m, step3_calc_b).arrange(DOWN, aligned_edge=LEFT, buff=0.2)
        step3_calcs.next_to(step3_text, DOWN, buff=0.2).align_to(step3_text, LEFT)

        self.play(
            FadeOut(step2_text), 
            FadeOut(step2_calcs),
            ReplacementTransform(step3_text_pos, step3_text),
            ReplacementTransform(step3_calcs_pos, step3_calcs),
            run_time=1.5
        )
        self.wait(1)

        # Step 4: Final equation
        step4_text = Text("Step 4: Write the regression equation").scale(0.55)
        step4_text_pos = step4_text.copy().next_to(step3_calcs, DOWN, buff=0.4).align_to(step3_text, LEFT)
        self.play(Write(step4_text_pos), run_time=1)
        self.wait(0.5)  # Pause after title

        # Show equation step by step
        step4_equation_formula = MathTex(r"\hat{y} = \hat{m}x + \hat{b}").scale(0.6)
        step4_equation_formula.next_to(step4_text_pos, DOWN, buff=0.2)

        step4_equation_values = MathTex(r"= " + f"{m_value:.2f}x + {b_value:.2f}").scale(0.6)
        step4_equation_values.next_to(step4_equation_formula, DOWN, buff=0.1).align_to(step4_equation_formula, LEFT)

        # Play each line
        self.play(Write(step4_equation_formula), run_time=1.5)
        self.wait(0.5)
        self.play(Write(step4_equation_values), run_time=1.5)
        self.wait(1.5)  # Longer pause for final equation

        # Group for transitions
        step4_equation_pos = VGroup(step4_equation_formula, step4_equation_values)

        # Now REMOVE Step 3 and move Step 4 up to Step 3's position
        step4_text.next_to(calc_title, DOWN, buff=0.3).align_to(calc_title, LEFT)

        # Create the combined equation for the transition
        step4_equation = MathTex(r"\hat{y} = \hat{m}x + \hat{b} = " + f"{m_value:.2f}x + {b_value:.2f}").scale(0.6)
        step4_equation.next_to(step4_text, DOWN, buff=0.2)

        self.play(
            FadeOut(step3_text), 
            FadeOut(step3_calcs),
            ReplacementTransform(step4_text_pos, step4_text),
            ReplacementTransform(step4_equation_pos, step4_equation),
            run_time=1.5
        )
        self.wait(2)
        
        # 8. TRANSITION: Remove table, add graph on left
        # Prepare the graph for the left side - MAKE SMALLER AND MORE LEFT
        left_axes = Axes(
            x_range=[0, 8, 1],
            y_range=[50, 100, 10],
            x_length=4.5,  # Even smaller
            y_length=4,
            axis_config={"include_numbers": True, "include_tip": False},
            x_axis_config={"numbers_to_include": np.arange(1, 8, 1)},
            y_axis_config={"numbers_to_include": np.arange(50, 101, 10)},
        )

        left_axes_labels = left_axes.get_axis_labels(
            x_label=Tex("Days Studying (X)").scale(0.6),
            y_label=Tex("Exam Grade (Y)").scale(0.6)
        )
        
        left_axes_group = VGroup(left_axes, left_axes_labels)
        left_axes_group.to_edge(LEFT, buff=0.5)  # Moved back from edge
        left_axes_group.center().shift(DOWN*0.3 + LEFT*3.0)  # Changed from LEFT*4.0 to LEFT*3.0
        
        # Create dots for the left graph
        left_dots = VGroup()
        for x_val, y_val in data_points_num:
            dot = Dot(point=left_axes.c2p(x_val, y_val), color=YELLOW)
            left_dots.add(dot)
        
        # Place the final equation near the x-axis label with color
        final_equation = MathTex(r"\hat{y} = " + f"{m_value:.2f}x + {b_value:.2f}").scale(0.6).set_color(GREEN)
        # Position slightly above and to the left of the x-axis label
        final_equation.next_to(left_axes_labels[0], UP + LEFT, buff=0.3)  

        self.play(
            FadeOut(data_table),
            FadeOut(closed_form_group),
            FadeOut(VGroup(calc_title, step4_text, step4_equation)),
            FadeIn(left_axes_group),
            FadeIn(left_dots),
            Write(final_equation),  # Now just the equation, no title
            run_time=2
        )
        self.wait(1)

        # 9. Draw Regression Line on Left Graph
        regression_line = left_axes.plot(lambda x: m_value * x + b_value, color=GREEN)
        line_label = Text("Best-Fit Line (OLS)", color=GREEN).scale(0.5)
        line_label.next_to(regression_line.point_from_proportion(0.8), UP, buff=0.2)
        
        self.play(
            Create(regression_line),
            Write(line_label),
            run_time=2
        )
        self.wait(1.5)
        
        # 10. Interpretation Section on Right Side - POSITION MORE TO LEFT
        interpret_title = Text("Interpreting the Results:").scale(0.6)
        interpret_title.to_corner(UR, buff=0.5).shift(LEFT*1.0 + DOWN*1.0)  # Changed from LEFT*0.5 to LEFT*1.0
        
        # Interpretation of slope and intercept - MAKE SHORTER
        slope_meaning = MathTex(r"\hat{m} = " + f"{m_value:.2f}" + r"\text{: Each day } \rightarrow " + f"{m_value:.2f}" + r" \text{ points}").scale(0.45)
        intercept_meaning = MathTex(r"\hat{b} = " + f"{b_value:.2f}" + r"\text{: 0 days } \rightarrow " + f"{b_value:.2f}" + r" \text{ points}").scale(0.45)
        r_squared = 0.85  # Example value - calculate actual R² if needed
        r_squared_meaning = MathTex(r"R^2 = " + f"{r_squared:.2f}" + r"\text{: Model explains } " + f"{int(r_squared*100)}\%" + r" \text{ variance}").scale(0.45)

        # Position each element individually
        slope_meaning.next_to(interpret_title, DOWN, buff=0.2).align_to(interpret_title, LEFT)
        intercept_meaning.next_to(slope_meaning, DOWN, buff=0.2).align_to(slope_meaning, LEFT)
        r_squared_meaning.next_to(intercept_meaning, DOWN, buff=0.2).align_to(intercept_meaning, LEFT)

        # Group for later reference
        interpret_group = VGroup(slope_meaning, intercept_meaning, r_squared_meaning)

        self.play(Write(interpret_title), run_time=1)
        self.wait(0.5)

        # Show each interpretation one at a time
        self.play(Write(slope_meaning), run_time=1.5)
        self.wait(1.5)  # Pause to understand slope interpretation

        self.play(Write(intercept_meaning), run_time=1.5)
        self.wait(1.5)  # Pause to understand intercept interpretation

        self.play(Write(r_squared_meaning), run_time=1.5)
        self.wait(2)  # Longer pause to understand R² interpretation

        # 11. REPLACE with Prediction Example on Right Side - KEEP equation visible
        prediction_x = 4.5  # Example: 4.5 days of studying
        prediction_y = m_value * prediction_x + b_value
        
        predict_title = Text("Making a Prediction:").scale(0.6)
        predict_title.to_corner(UR, buff=0.5).shift(LEFT*1.0 + DOWN*1.0)  # Changed from LEFT*0.5 to LEFT*2.0
        
        # Position each element individually
        predict_question = MathTex(r"\text{If a student studies for } " + f"{prediction_x}" + r" \text{ days:}").scale(0.45)
        predict_question.next_to(predict_title, DOWN, buff=0.2).align_to(predict_title, LEFT)

        predict_equation_line1 = MathTex(r"\hat{y} = " + f"{m_value:.2f} \cdot {prediction_x} + {b_value:.2f}").scale(0.45)
        predict_equation_line1.next_to(predict_question, DOWN, buff=0.2).align_to(predict_question, LEFT)

        predict_equation_line2 = MathTex(r"= " + f"{m_value * prediction_x:.2f} + {b_value:.2f}").scale(0.45)
        predict_equation_line2.next_to(predict_equation_line1, DOWN, buff=0.1).align_to(predict_equation_line1, LEFT)

        predict_equation_line3 = MathTex(r"= " + f"{prediction_y:.1f}").scale(0.45)
        predict_equation_line3.next_to(predict_equation_line2, DOWN, buff=0.1).align_to(predict_equation_line2, LEFT)

        predict_conclusion = Text(f"Expected Grade: {prediction_y:.1f}", color=RED).scale(0.5)
        predict_conclusion.next_to(predict_equation_line3, DOWN, buff=0.2).align_to(predict_question, LEFT)

        # Group for later reference
        predict_group = VGroup(predict_question, predict_equation_line1, predict_equation_line2, predict_equation_line3, predict_conclusion)

        self.play(
            FadeOut(interpret_title),
            FadeOut(interpret_group),
            Write(predict_title),
            run_time=1
        )
        self.wait(1)

        # Show each prediction element one at a time
        self.play(Write(predict_question), run_time=1.5)
        self.wait(1)  # Pause after question

        self.play(Write(predict_equation_line1), run_time=1.5)
        self.wait(0.5)  # Brief pause

        self.play(Write(predict_equation_line2), run_time=1.5)
        self.wait(0.5)  # Brief pause

        self.play(Write(predict_equation_line3), run_time=1.5)
        self.wait(1)  # Longer pause for final calculation

        self.play(Write(predict_conclusion), run_time=1.5)
        self.wait(2)  # Longer pause for the conclusion

        # Visualize the prediction on the graph
        prediction_dot = Dot(point=left_axes.c2p(prediction_x, prediction_y), color=RED)
        prediction_line_h = DashedLine(
            left_axes.c2p(0, prediction_y),
            left_axes.c2p(prediction_x, prediction_y),
            color=RED_A
        )
        prediction_line_v = DashedLine(
            left_axes.c2p(prediction_x, 50),
            left_axes.c2p(prediction_x, prediction_y),
            color=RED_A
        )
        
        self.play(
            GrowFromCenter(prediction_dot),
            Create(prediction_line_h),
            Create(prediction_line_v),
            run_time=1.5
        )
        
        # Add labels for the prediction point
        x_label = MathTex(f"x = {prediction_x}").scale(0.4).next_to(prediction_line_v, DOWN, buff=0.1)
        y_label = MathTex(f"y = {prediction_y:.1f}").scale(0.4).next_to(prediction_line_h, LEFT, buff=0.1)
        
        self.play(Write(x_label), Write(y_label), run_time=1)
        # self.wait(1)
        
        # 12. Conclusion
        conclusion_text = Text("In summary, OLS regression helps us quantify relationships and make predictions.", color=YELLOW).scale(0.6)
        conclusion_text.to_edge(DOWN, buff=0.5)
        
        # self.play(Write(conclusion_text), run_time=1.5)
        # self.wait(2)
        
        # Final fade out - update to include just final_equation instead of final_equation_group
        self.play(
            FadeOut(VGroup(
                scenario_title, left_axes_group, left_dots, regression_line, line_label,
                predict_title, predict_group, prediction_dot, prediction_line_h, prediction_line_v,
                x_label, y_label, final_equation  # Changed from final_equation_group
            )),
            run_time=2
        )
        self.wait(1)

# To render: manim -pqh demo/clip4_real_life_example.py Clip4RealLifeExample