import cv2
import math
import random
import numpy as np

from . import common


# Start with two circles
# Maintain a list of existing circles
# Every circle's center is chosen at random between width and height.
# Every circle's radius is chosen at random between min(width, height)/10 and min(width, height)/2
# Every circle's "line color" is chosen in sequence
# For every circle, the "direction" is chosen at random.
# For every circle, the angle (in degrees) between radii is set in the "config". This would determine the number of radii that would be rendered.
# Render the radii, leaving a gap of "render_time_gap" seconds between each render. 
# After half of a circle's total radii have been rendered, a new circle is created with probability 0.2
# After all the circle's radii have been rendered, the circle is removed from the list of existing circles. 
# If during render, there are no circles in the list, 3 new circles are created.

class radializor:
    class circ:
        def __init__(self, width, height, angle_gap, line_width, color):
            self.center = np.random.randint(0, width), np.random.randint(0, height)

            lesser_dim = min(width, height)
            self.radius = random.randint(lesser_dim//10, lesser_dim//2)
            # self.radius = 30

            self.init_angle = math.radians(random.randint(0, 360))
            self.angle_gap = math.radians(angle_gap)
            self.line_width = line_width

            self.direction = random.choice([-1, 1])
            self.color = color
            
            self.angle = 0
            self.half_completed_signal = False


        def render_next_radius(self, frame):
            if self.angle < 2 * math.pi:
                adj_angle = self.angle * self.direction + self.init_angle
                      
                circum_point = int(self.center[0] + self.radius * math.cos(adj_angle)), int(self.center[1] + self.radius * math.sin(adj_angle))
                cv2.line(frame, self.center, circum_point, self.color, self.line_width)

                self.angle += self.angle_gap

                if self.half_completed_signal == False and self.angle >= math.pi:
                    self.half_completed_signal = True
                else:
                    self.half_completed_signal = False

            return self.angle
            

    def __init__(self, anim_config):
        self.config = anim_config

        self.width = self.config["frame_size"][0]
        self.height = self.config["frame_size"][1]

        self.angle_gap = self.config["angle_gap"]
        self.frame_gap = int(self.config["render_time_gap"] * self.config["fps"])

        self.line_width = self.config["line_width"]

        self.init_color = common.random_rgb_color()
        self.color = self.init_color.copy()
        self.color_index = 0
        self.color_delta = 1

        self.circles = set()


    def add_circles(self, n = 1):
        for _ in range(n):
            self.circles.add(self.circ(self.width, self.height, self.angle_gap, self.line_width, self.color))

            if random.randint(0, 1000) == 0:
                self.init_color = common.random_rgb_color()
                self.color = self.init_color.copy()
                
            self.color[self.color_index] += self.color_delta
            if self.color[self.color_index] > 255:
                self.color[self.color_index] = 255
                self.color_delta = -1
            elif self.color[self.color_index] < 0:
                self.color[self.color_index] = 0
                self.color_delta = 1
            elif self.color[self.color_index] == self.init_color[self.color_index]:
                self.color_index = (self.color_index + 1) % 3
            

    def setup(self):
        self.add_circles(2)

        frame = np.empty((self.height, self.width, 3), dtype=np.uint8)
        frame[:] = self.config["background_color"]  # Initialize with background color

        return frame
    

    def draw_frame(self, frame_num, frame):  
        if self.frame_gap > 0 and frame_num % self.frame_gap != 0:
            return
        
        remove_circ_list = []
        add_circ_num = 0

        if len(self.circles) == 0:
            self.add_circles(3)

        for circ in self.circles:
            angle = circ.render_next_radius(frame)
            
            create_new_circle = False
            if angle >= 2 * math.pi:
                remove_circ_list.append(circ)
                create_new_circle = True

            if circ.half_completed_signal or create_new_circle:
                if random.random() < 0.2:
                    add_circ_num += 1
                        
        for circ in remove_circ_list:
            self.circles.remove(circ)

        if len(self.circles) < 10:
            self.add_circles(add_circ_num)

        return