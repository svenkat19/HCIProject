import cv2
import time
from deepface import DeepFace

def capture_and_compare(camera_index=0, image_path="D:\\VIT\\Fall_Semester_2023-24\\HCI\\HCIProject\\captured\\captured_image.jpg"):
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

    # Perform face recognition using DeepFace
    try:
        result = DeepFace.verify("D:\\VIT\\Fall_Semester_2023-24\\HCI\\HCIProject\\userimages\\admin.jpg", image_path)

        # Display the face verification result
        if result["verified"]:
            print("Face verification result: True")
        else:
            print("Face verification result: False")

    except Exception as e:
        print("Error during face verification:", str(e))

# Call the function to capture an image with a preview and perform face recognition
capture_and_compare()
