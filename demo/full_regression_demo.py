from manim import *

# Import all the individual clip classes
from clip1_linear_review import Clip1LinearReview
from clip2_OLS import Clip2OLSIntuition
from clip4_real_life_example import Clip4RealLifeExample
from clip5_conclusion import Clip5Conclusion

# Create a new class that inherits from Scene and runs all clips in sequence
class FullRegressionDemo(Scene):
    def construct(self):


        # Play each clip consecutively without transitions
        clips = [
            Clip1LinearReview,
            Clip2OLSIntuition,
            Clip4RealLifeExample, 
            Clip5Conclusion
        ]
        
        for SceneClass in clips:
            # Create temporary instance and use its construct method 
            # by binding the construct method to our current scene instance
            temp_scene = SceneClass()
            temp_scene.construct = SceneClass.construct.__get__(self, self.__class__)
            temp_scene.construct()

# To render: manim -pqm demo/full_regression_demo.py FullRegressionDemo

# To render with audio: manim -pqh demo/full_regression_demo.py FullRegressionDemo --audio_dir audio

# To render with audio and video: manim -pqh demo/full_regression_demo.py FullRegressionDemo --audio_dir audio --renderer=opengl

