import cv2
from mediapipe.tasks.python import BaseOptions;
from mediapipe.tasks.python.vision import FaceDetector, FaceDetectorOptions;
from mediapipe import Image, ImageFormat;
from threading import Thread, Lock
from time import sleep

# Data to be shared between the main thread and the vision thread
class VisionData:
	def __init__(self):
		self.__quadrant = "none"
		self.__quadrant_lock = Lock()
		self.__display_text = ""
		self.__display_text_lock = Lock()
		self.__sentinel = False
		
	
	def setQuadrant(self, quadrant: str) -> None:
		with self.__quadrant_lock:
			self.__quadrant = quadrant
	
	def getQuadrant(self) -> str:
		with self.__quadrant_lock:
			return self.__quadrant
		
	def setDisplayText(self, text: str) -> None:
		with self.__display_text_lock:
			self.__display_text = text
		
	def getDisplayText(self) -> str:
		with self.__display_text_lock:
			return self.__display_text
	
	def tripSentinel(self) -> None:
		self.__sentinel = True

	def checkSentinel(self) -> bool:
		return self.__sentinel

# Provides functionality for classifying the quadrant that a face is in
class FrameQuadrants:
	def __init__(self, width, height, tolerance = 50):
		self.__width = width
		self.__height = height
		self.__centerX = width / 2
		self.__centerY = height / 2
		self.__tolerance = tolerance

	def getWidth(self) -> int:
		return self.__width
	
	def getHeight(self) -> int:
		return self.__height

	def classify(self, x, y) -> str:
		# left half
		if(x < self.__centerX - self.__tolerance):
			if(y < self.__centerY - self.__tolerance):
				return "topleft"
			elif(y > self.__centerY + self.__tolerance):
				return "bottomleft"
			return "middleleft"
		# right half
		elif(x > self.__centerX + self.__tolerance):
			if(y < self.__centerY - self.__tolerance):
				return "topright"
			elif(y > self.__centerY + self.__tolerance):
				return "bottomright"
			return "middleright"
		
		# close to center
		if(y < self.__centerY - self.__tolerance):
			return "topcenter"
		elif(y > self.__centerY + self.__tolerance):
			return "bottomcenter"
		return "center"

# Vision thread tasks
def doVisionThread(vision_data: VisionData):
	# Set up camera input and frame parameters
	camera = cv2.VideoCapture(0)
	_, frame = camera.read()
	frame_quads = FrameQuadrants(frame.shape[1], frame.shape[0])

	# Set up face detection
	face_model = FaceDetector.create_from_options(
		FaceDetectorOptions(
			base_options=BaseOptions(model_asset_path="model/blazeface_sr.tflite")
		)
	)
	
	while (True):
		# Get a single frame from the camera
		_, frame = camera.read()

		# get face bounding box
		faces = face_model.detect(
			Image(image_format=ImageFormat.SRGB, data=frame)
		)

		# get face center
		if(len(faces.detections) > 0):
				box = faces.detections[0].bounding_box
				x = box.origin_x + box.width / 2.0
				y = box.origin_y + box.height / 2.0

				# Draw marker on face
				cv2.line(
					frame,
					(round(x - 20), round(y)),
					(round(x + 20), round(y)),
					(255, 255, 0),
					2
				)
				cv2.line(
					frame,
					(round(x), round(y - 20)),
					(round(x), round(y + 20)),
					(255, 255, 0),
					2
				)

				# Display text from control thread
				display_text = vision_data.getDisplayText()
				# text shadow
				cv2.putText(
					frame,
					display_text,
					(50, 50),
					0,
					1.0,
					(0,0,0),
					2
				)
				# text
				cv2.putText(
					frame,
					display_text,
					(50, 50),
					0,
					1.0,
					(0,255,0),
					2
				)
				vision_data.setQuadrant(frame_quads.classify(x, y))
		else:
			vision_data.setQuadrant("none")

		# display frame
		cv2.imshow("selfie", frame)

		if cv2.waitKey(1) & 0xFF == ord('q'):
			print("CTRL-C to exit")

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

		for i in range(0, 300):
			sleep(0.1)
			vision_data.setDisplayText(vision_data.getQuadrant())
			print(vision_data.getQuadrant())

		vision_data.tripSentinel()
		vision_thread.join()
		print("Done")

	except KeyboardInterrupt:
		print("Stopping vision thread...")
		vision_data.tripSentinel()
		vision_thread.join()
		print("Main thread cleaned up.")
		pass

if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		print("CTRL+C")
