import cv2
import mediapipe as mp
import time
import os

def initialize_pose_detector():
    """Initializes the MediaPipe pose detector."""
    mp_pose = mp.solutions.pose
    pose = mp_pose.Pose()
    mp_draw = mp.solutions.drawing_utils
    return pose, mp_draw

def process_frame(img, pose, mp_draw):
    """Processes a single frame for pose detection and drawing landmarks.

    Args:
        img (ndarray): The input image.
        pose (mp.solutions.pose.Pose): The MediaPipe pose object.
        mp_draw (mp.solutions.drawing_utils): The MediaPipe drawing utilities.

    Returns:
        img (ndarray): The image with pose landmarks drawn.
    """
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    results = pose.process(img_rgb)

    if results.pose_landmarks:
        mp_draw.draw_landmarks(img, results.pose_landmarks, mp.solutions.pose.POSE_CONNECTIONS)
        
        # Customize circles around landmarks
        for id, lm in enumerate(results.pose_landmarks.landmark):
            h, w, c = img.shape
            cx, cy = int(lm.x * w), int(lm.y * h)
            cv2.circle(img, (cx, cy), 5, (255, 0, 0), cv2.FILLED)

    return img

def calculate_fps(p_time):
    """Calculates the frames per second (FPS).

    Args:
        p_time (float): The previous time frame.

    Returns:
        fps (float): Calculated frames per second.
        c_time (float): Current time frame.
    """
    c_time = time.time()
    fps = 1 / (c_time - p_time)
    return fps, c_time

def save_video(video_writer, img):
    """Writes the current frame to the video file.

    Args:
        video_writer (cv2.VideoWriter): OpenCV VideoWriter object.
        img (ndarray): The current frame to be written.
    """
    video_writer.write(img)

def main(video_source=0, save=False, output_path="saved_output/output_video.mp4"):
    """Main function to perform pose detection on video source.

    Args:
        video_source (str or int): The video file path or webcam index.
        save (bool): Flag to save the processed video.
        output_path (str): The output file path for the saved video.
    """
    cap = cv2.VideoCapture(video_source)

    if not cap.isOpened():
        print(f"Error: Unable to open video source {video_source}")
        return

    # Initialize pose detector and variables
    pose, mp_draw = initialize_pose_detector()
    p_time = 0

    # Set up video writer if saving is enabled
    if save:
        # Create the directory if it doesn't exist
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # Codec for .mp4 format
        fps = int(cap.get(cv2.CAP_PROP_FPS))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        video_writer = cv2.VideoWriter(output_path, fourcc, fps, (width, height))
        print(f"Saving output to {output_path}")

    while True:
        success, img = cap.read()
        if not success:
            print("Failed to capture image")
            break

        img = process_frame(img, pose, mp_draw)
        fps, p_time = calculate_fps(p_time)

        cv2.putText(img, f"{int(fps)}", (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 225, 0), 3)
        cv2.imshow("Pose Detection", img)

        # Save the frame to video if enabled
        if save:
            save_video(video_writer, img)

        # Check for user input to break the loop
        if cv2.waitKey(1) & 0xFF == 27:  # 27 is the ASCII code for the Esc key
            break

        # Alternatively, check if the window is closed
        if cv2.getWindowProperty('Pose Detection', cv2.WND_PROP_VISIBLE) < 1:
            break

    cap.release()
    if save:
        video_writer.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    # Default video source is a webcam (index 0), but can be replaced with a video file path
    main("videos/video_01.mp4", save=False)
