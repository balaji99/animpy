import numpy as np
import cv2
import math
import random

from . import common


class single_bezier_pf:
    def __init__(self, anim_config):
        self.config = anim_config
        self.width = self.config["frame_size"][0]
        self.height = self.config["frame_size"][1]
        self.bg_color = self.config["background_color"]
        self.num_points = self.config["num_points"]
        self.keep_previous_frames = self.config["keep_previous_frames"]
        self.random_line_color = self.config["random_line_color"]
        self.fixed_line_colors = self.config["fixed_line_colors"]
        self.line_width = self.config["line_width"]


    def setup(self):
        frame = np.empty((self.height, self.width, 3), dtype=np.uint8)
        frame[:] = self.bg_color  # Initialize with background color
        return frame
    

    # Function to create a Bezier curve path
    def bezier_curve(self, control_points, num_points=100):
        t = np.linspace(0, 1, num_points)
        curve = np.zeros((num_points, 2))
        n = len(control_points) - 1
        for i in range(num_points):
            for j in range(len(control_points)):
                curve[i] += (math.comb(n, j) * (t[i]**j) * ((1 - t[i])**(n-j)) * control_points[j])
        return curve
    

    # Function to draw the Bezier curve
    def draw_bezier_curve(self, frame, curve, line_color):
        for i in range(1, len(curve)):
            cv2.line(frame, tuple(curve[i-1].astype(int)), tuple(curve[i].astype(int)), line_color, self.line_width)
    

    def draw_frame(self, frame_num, frame):
        if not self.keep_previous_frames:
            # Clear the frame with the background color
            frame[:] = self.bg_color
        
        # Generate random control points
        control_points = common.random_points(self.width, self.height, 4)

        # Create a Bezier curve path
        curve = self.bezier_curve(control_points, self.num_points)

        # Set the line color
        if self.random_line_color:
            self.line_color = common.random_rgb_color()
        else:
            self.line_color = random.choice(self.fixed_line_colors)

        # Draw the Bezier curve
        self.draw_bezier_curve(frame, curve, self.line_color)

