# Manim Animations

A collection of mathematical animations created using the Manim library.

## Files

- `convex_ball.py`: Animation showing a convex ball in 3D space with points and vectors
- `clip1_linear_review.py`: Linear algebra review animations
- `manim.cfg`: Configuration file for Manim
- `activate_manim.sh`: Script to activate the Manim environment

## Usage

To render an animation:

```bash
manim -pql convex_ball.py ConvexBallIllustration  # Play in low quality
manim -pqh convex_ball.py ConvexBallIllustration  # Play in high quality
manim -sqh convex_ball.py ConvexBallIllustration  # Save high quality static image
``` 