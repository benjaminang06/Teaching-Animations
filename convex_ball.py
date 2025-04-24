from manim import *
import numpy as np

class ConvexBallIllustration(ThreeDScene):
    def construct(self):
        # Set up 3D axes for context
        axes = ThreeDAxes(
            x_range=[-3, 3, 1],
            y_range=[-3, 3, 1],
            z_range=[-3, 3, 1],
            x_length=6,
            y_length=6,
            z_length=6,
        )
        axes_labels = axes.get_axis_labels()

        # Set a fixed camera orientation for the static image
        self.set_camera_orientation(phi=75 * DEGREES, theta=30 * DEGREES, distance=10)

        # Define the ball (Sphere) - Unit ball
        center = ORIGIN
        radius = 1.0 # Changed to unit radius
        ball = Sphere(
            center=center,
            radius=radius,
            resolution=(24, 24),
            u_range=[0.001, PI - 0.001],
            v_range=[0, TAU]
            )
        ball.set_opacity(0.2)
        ball.set_color(BLUE) # Keep blue for now, can change later
        ball.set_stroke(WHITE, width=1, opacity=0.5)

        # Ball label - Closed Unit Ball
        # ball_label_text = "B(\mathbf{0}, r)" # Example for open ball centered at origin
        ball_label_text = "\\overline{B}(\mathbf{0}, 1)" # Closed unit ball
        ball_label = MathTex(ball_label_text).scale(0.8)
        ball_label.to_corner(UR)
        self.add_fixed_in_frame_mobjects(ball_label)

        # Center point and label
        center_dot = Dot3D(center, color=RED, radius=0.08)
        center_label = MathTex("\mathbf{0}").scale(0.8).next_to(center_dot, OUT * 0.5 + RIGHT * 0.5)

        # Pick two points inside the unit ball
        point_x_coords = np.array([0.3, 0.5, 0.4]) # New vector x inside unit ball
        point_y_coords = np.array([-0.6, -0.2, 0.3]) # New vector y inside unit ball

        point_x = Dot3D(point_x_coords, color=YELLOW, radius=0.08)
        point_y = Dot3D(point_y_coords, color=GREEN, radius=0.08)
        label_x = MathTex("\mathbf{x}").scale(0.8).next_to(point_x, OUT * 0.5)
        label_y = MathTex("\mathbf{y}").scale(0.8).next_to(point_y, OUT * 0.5)

        # Vectors from origin to x and y
        vector_x = Arrow3D(
            start=ORIGIN, end=point_x_coords, color=YELLOW, thickness=0.01, base_radius=0.03, height=0.15
        )
        vector_y = Arrow3D(
            start=ORIGIN, end=point_y_coords, color=GREEN, thickness=0.01, base_radius=0.03, height=0.15
        )

        # Line segment between x and y
        line_segment = Line3D(
            point_x_coords,
            point_y_coords,
            color=WHITE,
            thickness=0.015
            )

        # Line segment equation label (e.g., in bottom-left corner)
        line_label_text = "t\mathbf{x} + (1-t)\mathbf{y}, \\ \\ t \in [0, 1]"
        line_label = MathTex(line_label_text).scale(0.7)
        line_label.to_corner(DOWN + LEFT)
        self.add_fixed_in_frame_mobjects(line_label)

        # Add all elements to the scene directly (no animations)
        self.add(
            axes, axes_labels, ball, center_dot, 
            point_x, point_y, vector_x, vector_y, line_segment
        )
        self.add_fixed_orientation_mobjects(center_label, label_x, label_y)

# To render this scene as a single static image, save the code as convex_ball.py and run:
# manim -s convex_ball.py ConvexBallIllustration
# Use -sqh for high quality single image 