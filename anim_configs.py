import animators.all as animators

# Dictionary of animator classes
animator_classes = {
    "BLANK": animators.blank.blank,
    "SINGLE_BEZIER_PF": animators.single_bezier_pf.single_bezier_pf,
    "RADIALIZOR": animators.radializor.radializor,
}

# Animation config dictionary
animator_configs = {
    "BLANK": {
        "background_color": (0, 180, 240),
    },

    "BLINK": {
        "background_colors": [(0, 180, 240), (0, 180, 240),],
    },

    # Single Bezier curve is rendered in one frame
    "SINGLE_BEZIER_PF": {
        "num_points": 100,
        "random_line_color": True,
        "fixed_line_colors": (0, 0, 255),
        "background_color": (255, 255, 255),
        "line_width": 60,
        "control_points": 6,
        "keep_previous_frames": True,
        "erase_canvas": 10,
    },

    # Single Bezier curve is rendered in one frame
    "RADIALIZOR": {
        "angle_gap": 6, # degrees
        "render_time_gap": 0.01,
        "background_color": (255, 255, 255),
        "line_width": 10,
    },
}
