import cv2
from mediapipe.tasks.python import BaseOptions;
from mediapipe.tasks.python.vision import ObjectDetector, ObjectDetectorOptions, RunningMode;
from mediapipe import Image, ImageFormat;

def main():
	camera = cv2.VideoCapture(0)

	scene_model = ObjectDetector.create_from_options(
		ObjectDetectorOptions(
			base_options=BaseOptions(model_asset_path="model/efficientdet_lite0.tflite")
		)
	)

	while (True):
		# get frame from camera
		_, frame = camera.read()

		# detect objects
		scene_objects = scene_model.detect(
			Image(image_format=ImageFormat.SRGB, data=frame)
		)

		# get detections
		for scene_object in scene_objects.detections:
			for category in scene_object.categories:
				if category.score > 0.5:
					print(category.category_name)
					print("\n")



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
