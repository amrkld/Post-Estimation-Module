# Pose Detection Module

## Overview

This module uses MediaPipe and OpenCV to perform real-time pose detection on video sources. It captures video from a webcam or a file, processes each frame to detect and draw human pose landmarks, and optionally saves the processed video to a file.

## Features

- Real-time pose detection using MediaPipe.
- Visualizes pose landmarks and connections on video frames.
- Calculates and displays frames per second (FPS).
- Optionally saves the processed video to a file.
- Handles video capture from both webcam and video files.

## Requirements

Ensure you have the following Python packages installed:

- `opencv-python==4.7.0.72`
- `mediapipe==0.10.0`

You can install these dependencies using the provided `requirements.txt` file:

```sh
pip install -r requirements.txt
```

## Usage

### Running the Module

To run the module, use the following command:

```sh
python your_script_name.py
```

Replace `your_script_name.py` with the name of the Python file containing the code.

### Parameters

The `main` function accepts the following parameters:

- `video_source` (str or int): The path to the video file or the index of the webcam (default is `0` for the default webcam).
- `save` (bool): Flag indicating whether to save the processed video to a file (default is `False`).
- `output_path` (str): The path to save the processed video if `save` is set to `True`. If not specified, defaults to `"saved_output/output_video.mp4"`.

### Example

To process a video file and save the output, modify the `__main__` section of the script as follows:

```python
if __name__ == "__main__":
    file_path = "path/to/your/video.mp4"  # Path to your input video file
    output_path = "path/to/save/output_video.mp4"  # Path to save the processed video

    main(video_source=file_path, save=True, output_path=output_path)
```

## Functions

### `initialize_pose_detector()`

Initializes the MediaPipe pose detector and drawing utilities.

**Returns:**
- `pose`: MediaPipe pose object.
- `mp_draw`: MediaPipe drawing utilities object.

### `process_frame(img, pose, mp_draw)`

Processes a single frame to detect and draw pose landmarks.

**Arguments:**
- `img` (ndarray): The input image.
- `pose` (MediaPipe Pose object): The MediaPipe pose object.
- `mp_draw` (MediaPipe Drawing Utilities object): The MediaPipe drawing utilities.

**Returns:**
- `img` (ndarray): The image with pose landmarks drawn.

### `calculate_fps(p_time)`

Calculates the frames per second (FPS).

**Arguments:**
- `p_time` (float): The previous time frame.

**Returns:**
- `fps` (float): Calculated frames per second.
- `c_time` (float): Current time frame.

### `save_video(video_writer, img)`

Writes the current frame to the video file.

**Arguments:**
- `video_writer` (cv2.VideoWriter): OpenCV VideoWriter object.
- `img` (ndarray): The current frame to be written.

### `main(video_source=0, save=False, output_path=None)`

Main function to perform pose detection on video source.

**Arguments:**
- `video_source` (str or int): The video file path or webcam index.
- `save` (bool): Flag to save the processed video.
- `output_path` (str): The output file path for the saved video.

## Troubleshooting

- Ensure your Python environment has the required packages installed.
- Check the video source path and index.
- If saving the video, verify that the output directory exists or can be created.
