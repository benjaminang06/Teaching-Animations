from manim import *

class Clip5Conclusion(Scene):
    def construct(self):
        # Title
        title = Text("Linear Regression: Key Takeaways").scale(1.0)
        title.to_edge(UP, buff=0.5)
        
        self.play(Write(title))
        self.wait(1)
        
        # Points to appear one by one
        point1 = Text("1. Linear regression models the relationship between variables.",
                    t2c={"Linear regression": YELLOW}).scale(0.7)
        
        point2 = Text("2. Best fit line minimizes the sum of squared errors (SSR).",
                    t2c={"minimizes": YELLOW, "sum of squared errors": YELLOW}).scale(0.7)
        
        point3 = Text("3. OLS provides closed form solutions for slope and intercept.",
                    t2c={"closed form solutions": YELLOW}).scale(0.7)
        
        # Arrange points vertically with some space in between
        points_group = VGroup(point1, point2, point3).arrange(DOWN, buff=0.8, aligned_edge=LEFT)
        points_group.next_to(title, DOWN, buff=0.8)
        
        # Animate points appearing one by one with pauses
        self.play(FadeIn(point1))
        self.wait(2.5)
        
        self.play(FadeIn(point2))
        self.wait(2.5)
        
        self.play(FadeIn(point3))
        self.wait(3)
        
        # Optional: add a formula reminder at the bottom
        formulas = VGroup(
            MathTex(r"\hat{m} = \frac{\sum (x_i - \bar{x})(y_i - \bar{y})}{\sum (x_i - \bar{x})^2}").scale(0.6),
            MathTex(r"\hat{b} = \bar{y} - \hat{m} \bar{x}").scale(0.6)
        ).arrange(DOWN, buff=0.3)
        
        formulas_box = SurroundingRectangle(formulas, buff=0.2, color=BLUE, corner_radius=0.2)
        formulas_group = VGroup(formulas, formulas_box)
        formulas_group.to_edge(DOWN, buff=0.5)
        
        self.play(
            FadeIn(formulas_group)
        )
        self.wait(3)
        
        # Final thank you message
        thank_you = Text("Thank you!", color=BLUE).scale(1.2)
        
        self.play(
            FadeOut(points_group),
            FadeOut(formulas_group),
            FadeOut(title),
            run_time=1.5
        )
        
        self.play(Write(thank_you))
        self.wait(2)
        
        self.play(FadeOut(thank_you))
        self.wait(1) 