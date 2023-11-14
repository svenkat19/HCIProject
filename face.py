from deepface import DeepFace
import cv2

result = DeepFace.verify(img1_path = "D:\\VIT\\Fall_Semester_2023-24\\HCI\\HCIProject\\userimages\\admin.jpg", img2_path = "D:\\VIT\\Fall_Semester_2023-24\\HCI\\HCIProject\\userimages\\svenkat.png")
print(result)