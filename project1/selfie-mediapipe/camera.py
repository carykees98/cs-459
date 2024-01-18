import cv2
from mediapipe.tasks.python import BaseOptions;
from mediapipe.tasks.python.vision import FaceDetector, FaceDetectorOptions, RunningMode;
from mediapipe import Image, ImageFormat;

def main():
	camera = cv2.VideoCapture(0)

	face_model = FaceDetector.create_from_options(
		FaceDetectorOptions(
			base_options=BaseOptions(model_asset_path="model/blazeface_sr.tflite")
		)
	)
	
	face_centerX = 0.0
	face_centerY = 0.0

	while (True):
		# get frame from camera
		_, frame = camera.read()

		# get face bounding box
		faces = face_model.detect(
			Image(image_format=ImageFormat.SRGB, data=frame)
		)

		# get face center
		for face in faces.detections:
			bounding_box = face.bounding_box
			x = bounding_box.origin_x + bounding_box.width / 2.0
			y = bounding_box.origin_y + bounding_box.height / 2.0
			face_centerX = rollingAvg(face_centerX, x, 10.0)
			face_centerY = rollingAvg(face_centerY, y, 10.0)

		# draw marker on face
		cv2.line(
			frame,
			(round(face_centerX - 20), round(face_centerY)),
			(round(face_centerX + 20), round(face_centerY)),
			(255, 255, 0),
			2
		)
		cv2.line(
			frame,
			(round(face_centerX), round(face_centerY - 20)),
			(round(face_centerX), round(face_centerY + 20)),
			(255, 255, 0),
			2
		)

		# display frame
		cv2.imshow("title", frame)

		# Press Q for death
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

	camera.release()


def rollingAvg(prev, current, n):
	assert n > 0
	return (prev * n + current) / (n + 1)

if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		print("CTRL + C Pressed, Exiting Program")

	cv2.destroyAllWindows()
