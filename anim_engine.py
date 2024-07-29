import os
import cv2
import datetime
import anim_configs


### BEGIN setup
# Global variables
VIDEO_LENGTH = 5  # in seconds
VIDEO_FRAME_RATE = 30  # Frame rate (fps) of the output video
VIDEO_FRAME_SIZE = (1920, 1080)  # Output video resolution
OUTPUT_FOLDER = "generated_animations"  # Output folder
OUTPUT_VIDEO_FILE_PREFIX = "output"  # Output video file name
ANIMATION_CLASS_ID = "CIRC_RADIALIZOR"  # Name of the animation type
### END setup


def animate(cv2_frame_sink, anim_class_id, fps, frame_dimensions, animation_duration):
    if anim_class_id in anim_configs.animator_classes:
        total_num_frames = int(fps * animation_duration)

        anim_config = anim_configs.animator_configs[anim_class_id]
        anim_config["fps"] = fps
        anim_config["frame_size"] = frame_dimensions
        anim_config["animation_duration"] = animation_duration
        
        # Create an object
        anim_obj = anim_configs.animator_classes[anim_class_id](anim_config)

        frame = anim_obj.setup()

        for frame_num in range(total_num_frames):
            anim_obj.draw_frame(frame_num, frame)

            # Write the frame
            cv2_frame_sink.write(frame)

            # Display the frame
            opencv_window_name = "Animation"
            cv2.imshow(opencv_window_name, frame)

            # Check for keypress (with a short delay)
            key = cv2.waitKey(1) & 0xFF
            if key == 27 or key == ord('q'):  # ESC or 'q' key to exit
                break
            
            # Check if the window is closed
            if cv2.getWindowProperty(opencv_window_name, cv2.WND_PROP_VISIBLE) < 1:
                break
    else:
        print(f"Error: Animation class '{anim_class_id}' not found.")
    

def main():
    global VIDEO_FRAME_SIZE, VIDEO_FRAME_RATE, VIDEO_LENGTH, ANIMATION_CLASS_ID
    global OUTPUT_FOLDER, OUTPUT_VIDEO_FILE_PREFIX

    # Get the current timestamp in YYYYMMDD_HHMMSS format
    current_timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    # Setup for video recording
    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    # Append the timestamp to the output video filename
    output_video_filename = os.path.join(OUTPUT_FOLDER, f"{OUTPUT_VIDEO_FILE_PREFIX}_{current_timestamp}.mp4")

    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    frame_sink = cv2.VideoWriter(output_video_filename, fourcc, VIDEO_FRAME_RATE, VIDEO_FRAME_SIZE)

    animate(frame_sink, ANIMATION_CLASS_ID, VIDEO_FRAME_RATE, VIDEO_FRAME_SIZE, VIDEO_LENGTH)

    # Release everything if job is finished
    frame_sink.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
