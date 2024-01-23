import cv2
from mediapipe.tasks.python import BaseOptions;
from mediapipe.tasks.python.vision import ObjectDetector, ObjectDetectorOptions, RunningMode;
from mediapipe import Image, ImageFormat;
from threading import Thread, Lock
from time import sleep

class VisionData:
	def __init__(self):
		self.__detections: list = []
		self.__detections_lock = Lock()
		self.__sentinel = False
	
	def setDetections(self, detections):
		with self.__detections_lock:
			self.__detections = detections
	
	def getDetections(self):
		with self.__detections_lock:
			return self.__detections
	
	def tripSentinel(self) -> None:
		self.__sentinel = True

	def checkSentinel(self) -> bool:
		return self.__sentinel

# Vision thread tasks
def doVisionThread(vision_data: VisionData):
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

		vision_data.setDetections(scene_objects.detections)

		# get detections
		for scene_object in scene_objects.detections:

			for category in scene_object.categories:
				if category.score > 0.4:
					box = scene_object.bounding_box
					# bounding box
					cv2.rectangle(
						frame,
						(box.origin_x, box.origin_y),
						(box.origin_x + box.width, box.origin_y + box.height),
						(0, 255, 0),
						2
					)
					# text shadow
					cv2.putText(
						frame,
						category.category_name,
						(box.origin_x + 2, box.origin_y + 2),
						0,
						1.0,
						(0,0,0),
						2
					)
					# text
					cv2.putText(
						frame,
						category.category_name,
						(box.origin_x, box.origin_y),
						0,
						1.0,
						(0,255,0),
						2
					)

		# display frame
		cv2.imshow("scene", frame)

		# if you take this out it breaks the whole UI
		if cv2.waitKey(1) & 0xFF == ord('q'):
			print("Press CTRL-C to exit")
		
		# exit on sentinel
		if(vision_data.checkSentinel()):
			camera.release()
			cv2.destroyAllWindows()
			return

# Main thread
def main():
	try:
		vision_data: VisionData = VisionData()
		vision_thread: Thread = Thread(target=doVisionThread, args=(vision_data,))
		vision_thread.start()

		for i in range(0, 15):
			sleep(2.0)
			print(vision_data.getDetections())

		vision_data.tripSentinel()
		vision_thread.join()
		print("Done")

	except:
		print("Stopping vision thread...")
		vision_data.tripSentinel()
		vision_thread.join()
		print("Main thread cleaned up.")
		raise

if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		print("CTRL+C Pressed")
