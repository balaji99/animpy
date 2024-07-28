import numpy as np

class blank:
    def __init__(self, anim_config):
        self.config = anim_config


    def setup(self):
        width = self.config["frame_size"][0]
        height = self.config["frame_size"][1]
        
        frame = np.empty((height, width, 3), dtype=np.uint8)
        frame[:] = self.config["background_color"]  # Initialize with background color

        return frame
    

    def draw_frame(self, frame_num, frame):
        return
