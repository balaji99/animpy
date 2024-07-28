# Animation Engine

This project is a simple 2D animation engine that generates animations and saves them as video files. The engine uses OpenCV for video processing and supports different animation classes defined in the `anim_configs` module.

## Features

- Generates animations based on predefined classes
- Saves animations as video files in the specified resolution
- Supports custom frame rates and video lengths
- Displays the animation in a window during generation

## Requirements

- Python 3.x
- OpenCV

## Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/animation-engine.git
   cd animation-engine
   ```

2. Install the required packages:
   ```
   pip install opencv-python
   ```

## Usage

1. Configure the global variables in the setup section in `anim_engine.py`:

   ```python
   ### BEGIN setup
   # Global variables
   VIDEO_LENGTH = 600  # in seconds
   VIDEO_FRAME_RATE = 100  # Frame rate (fps) of the output video
   VIDEO_FRAME_SIZE = (1920, 1080)  # Output video resolution
   OUTPUT_FOLDER = "generated_animations"  # Output folder
   OUTPUT_VIDEO_FILE_PREFIX = "output"  # Output video file name
   ANIMATION_CLASS_ID = "RADIALIZOR"  # Name of the animation type
   ### END setup
   ```

2. Run the main script:
   ```
   python anim_engine.py
   ```

3. The generated video will be saved in the `OUTPUT_FOLDER` with a filename that includes the current timestamp.


## Using an existing animation type

1. Set `ANIMATION_CLASS_ID` to the desired animation type
2. Change any config items, as required, in the config dictionary defined inside the `animator_configs` dict in the `anim_configs` module.


## Example of using an existing animation type

To generate an animation using the existing `RADIALIZOR` animation and save it as a video file:

1. Ensure the `RADIALIZOR` animation type is defined in the `animator_classes` dictionary in the `anim_configs` module.
2. Ensure the elements in the "RADIALIZOR" config dictionary have appropriate values (See inside the `animator_configs` dictionary in the `anim_configs` module).
3. Set `ANIMATION_CLASS_ID` to `"RADIALIZOR"` in `anim_engine.py`.
4. Run the script:
   ```
   python anim_engine.py
   ```

## Creating your own animation type
1. Create a Python class (say `new_animator`) and store in a Python file (say `new_anim.py`) in the `animators` directory. For examples, look how the existing Python classes there are structured.
1a. Every class must have at least three methods defined - constructor, `setup` and `draw_frame`.
1b. The constructor must accept a dict `anim_config` - this contains various configuration items that can be used by the animator object.
1c. The `setup` function is called just before the animation begins. The animator object can use this opportunity to make preparations to draw frames.
1d. The `draw_frame` function is called when the animation engine wants to render the next frame in series. This function must accept three arguments - `frame_num` and `frame`. `frame_num` represents the sequence number of the frame (the first frame's sequence number is 0). `frame` is the actual 2D array that represents the image frame. This frame is not cleared by the animation engine each time `draw_frame` is called, which means it contains the results of the previous calls to `draw_frame`. In the current call to `draw_frame`, the function can modify the contents of the frame, and that frame will be stored in the output video.
2. Add a reference to the new animator script in `animators\all.py` like so:
from . import new_anim
3. In anim_configs.py, add a line for the new animator in the animator_classes dict, like so
`"NEW_ANIM": animators.new_anim.new_animator,`
3a. In anim_configs.py, add a dict for the new animator in the animator_configs dict, like so
    "NEW_ANIM": {
        "background_color": (0, 180, 240),
    },
3b. Add as many elements in the NEW_ANIM dict, as required. The `new_animator` class can read these config values and process them as needed.
4. Set `ANIMATION_CLASS_ID` to `"NEW_ANIM"` in `anim_engine.py`. 


## License

This project is licensed under the MIT License.

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

## Contact

For any questions or inquiries, please contact [admin@toolkitsite.com](mailto:admin@toolkitsite.com).
