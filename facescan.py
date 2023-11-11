import cv2
import time

def capture_image_with_preview(camera_index=0, image_path="D:\VIT\Fall_Semester_2023-24\HCI\HCIProject\captured\captured_image.jpg"):
    # Open the camera
    cap = cv2.VideoCapture(camera_index)

    # Check if the camera is opened successfully
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    # Display a preview screen for 3 seconds
    preview_duration = 3  # in seconds
    start_time = time.time()

    while time.time() - start_time < preview_duration:
        # Capture a single frame
        ret, frame = cap.read()

        # Check if the frame was successfully captured
        if not ret:
            print("Error: Could not read frame.")
            cap.release()
            return

        # Display the frame in a window named "Preview"
        cv2.imshow('Preview', frame)

        # Wait for a short duration to simulate a preview
        cv2.waitKey(30)

    # Destroy the preview window
    cv2.destroyWindow('Preview')

    # Capture a single frame after the preview
    ret, frame = cap.read()

    # Check if the frame was successfully captured
    if not ret:
        print("Error: Could not read frame.")
        cap.release()
        return

    # Save the captured frame as an image file
    cv2.imwrite(image_path, frame)

    # Release the camera
    cap.release()

    print(f"Image captured and saved as {image_path}")

# Call the function to capture an image with a preview (you can specify the camera index if needed)
capture_image_with_preview()
