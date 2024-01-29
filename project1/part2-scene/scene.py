"""
	scene.py
	Project 1, Part 2: Static Scene Application
	CS459 Human Computer Interaction
	Cary Keesler, Juno Meifert, Andrew Tringali
"""
import cv2
from mediapipe.tasks.python import BaseOptions
from mediapipe.tasks.python.vision import ObjectDetector, ObjectDetectorOptions, RunningMode
from mediapipe import Image, ImageFormat
import pyttsx3
import speech_recognition as sr
import winsound
from threading import Thread, Lock
from dataclasses import dataclass
from datetime import datetime
from time import sleep

#
# ========== Class definitions ==========
#

# Represents an object that has been detected in the scene
@dataclass
class SceneObject:
	name: str
	x: float
	y: float
	area: int
	quadrant: str

# Data to be synchronized between the control thread and the vision thread
class VisionData:
	def __init__(self):
		self.__detections: list[SceneObject] = []
		self.__detections_lock = Lock()
		self.__sentinel = False
		self.__available = False
		self.__save_image_flag = False
	
	# Publish detected objects for control thread
	def setDetections(self, detections):
		with self.__detections_lock:
			self.__detections = detections
	
	# Get detected objects
	def getDetections(self):
		with self.__detections_lock:
			return self.__detections
	
	# Trip sentinel to shut down vision thread
	def tripSentinel(self) -> None:
		self.__sentinel = True

	# Check sentinel (for use by vision thread)
	def checkSentinel(self) -> bool:
		return self.__sentinel
	
	# Signal that vision data is available
	def signalAvailable(self) -> None:
		self.__available = True

	# Check if vision data is available
	def isAvailable(self) -> bool:
		return self.__available
	
	# Request an image capture
	def requestSaveImage(self) -> None:
		self.__save_image_flag = True
	
	# Reset the image capture request flag
	def resetSaveImage(self) -> None:
		self.__save_image_flag = False

	# Check the image capture request flag
	def checkSaveImage(self) -> bool:
		return self.__save_image_flag
	
# Provides functionality for classifying the quadrant that an object is in
class FrameQuadrants:
	def __init__(self, width, height, tolerance = 60):
		self.__width = width
		self.__height = height
		self.__centerX = width / 2
		self.__centerY = height / 2
		self.__tolerance = tolerance

	# Gets the width of the frame
	def getWidth(self) -> int:
		return self.__width
	
	# Gets the height of the frame
	def getHeight(self) -> int:
		return self.__height

	# Gets the quadrant that an object is in
	def classify(self, x, y) -> str:
		# left half
		if(x < self.__centerX - self.__tolerance):
			if(y < self.__centerY - self.__tolerance):
				return "top_left"
			elif(y > self.__centerY + self.__tolerance):
				return "bottom_left"
			
			return "middle_left"
		# right half
		elif(x > self.__centerX + self.__tolerance):
			if(y < self.__centerY - self.__tolerance):
				return "top_right"
			elif(y > self.__centerY + self.__tolerance):
				return "bottom_right"
			
			return "middle_right"
		
		# middle vertical but not horizontal
		if(y < self.__centerY - self.__tolerance):
			return "top_middle"
		elif(y > self.__centerY + self.__tolerance):
			return "bottom_middle"
		
		return "middle_middle"
	
	# Gets the direction of movement required to position the object
	# Opposite movement of the face program
	def getMovement(current: str, target: str):
		current_y = current.split("_", 2)[0]
		current_x = current.split("_", 2)[1]
		target_y = target.split("_", 2)[0]
		target_x = target.split("_", 2)[1]

		# move horizontally first
		if(current_x != target_x):
			match current_x:
				case "left":
					return "Left"
				case "right":
					return "Right"
				case _:
					if(target_x == "left"):
						return "Right"
					return "Left"
		else: # move vertically once centered horizontally
			match current_y:
				case "bottom":
					return "Down"
				case "top":
					return "Up"
				case _:
					if(target_y == "top"):
						return "Down"
					return "Up"

# Text to speech wrapper
class TextToSpeech:
	def __init__(self):
		self.__tts = pyttsx3.init()

	# Speak a phrase
	def say(self, text: str) -> None:
		print("[TTS] Speaking phrase \"" + text + "\".")
		self.__tts.say(text)
		self.__tts.runAndWait()

# Speech to text wrapper
class SpeechToText:
	def __init__(self):
		self.__speech = sr.Recognizer()
	
	# Listen and transcribe a phrase
	def listen(self) -> str:
		print("[STT] Listening...")
		with sr.Microphone() as input:
			self.__speech.adjust_for_ambient_noise(input, duration=0.3)
			winsound.PlaySound("bump.wav", winsound.SND_FILENAME)
			recorded_audio = self.__speech.listen(input)
			phrase = self.__speech.recognize_whisper(
				recorded_audio, language="english"
			).lower()
			print("[STT] Transcribed phrase \"" + phrase + "\"")
			return SpeechToText.sanitize(phrase)
	
	# Remove punctuation and leading/trailing whitespace from a transcription
	def sanitize(phrase: str) -> str:
		return phrase.replace(".", "").replace("!", "").replace("?", "").strip()
	
# Contains useful functions for sorting objects in the control thread
class ObjectHelper:
	# Gets the most apparent instance of an object in the scene
	def getMostApparent(scene_objects: list[SceneObject], name: str) -> SceneObject:
		max_area: int = 0
		candidate_obj: SceneObject = SceneObject("", 0.0, 0.0, 0, "")
		for o in scene_objects:
			if(o.name == name and o.area >= max_area):
				candidate_obj = o
		return candidate_obj

#
# ========== End class definitions ==========
#

#
# Called by vision thread when it is started
# Shared vision data instance should be passed to it
#
def doVisionThread(vision_data: VisionData):
	print("[Vision] Starting vision thread...")

	# Set up camera input and frame parameters
	camera = cv2.VideoCapture(0)
	_, frame = camera.read()
	frame_quads: FrameQuadrants = FrameQuadrants(frame.shape[1], frame.shape[0])

	# Set up object detection
	scene_model = ObjectDetector.create_from_options(
		ObjectDetectorOptions(
			base_options=BaseOptions(model_asset_path="model/efficientdet_lite0.tflite")
		)
	)

	print("[Vision] Running object detection.")
	while (True):
		# Get a single frame from the camera
		_, frame = camera.read()

		# Detect objects in the frame
		scene_detections = scene_model.detect(
			Image(image_format=ImageFormat.SRGB, data=frame)
		)

		# Save image on request
		if(vision_data.checkSaveImage()):
			print("[Vision] Saving image...")
			winsound.PlaySound("shutter.wav", winsound.SND_FILENAME)
			cv2.imwrite(datetime.now().strftime("%Y%m%d%H%M%S.jpg"), frame)
			vision_data.resetSaveImage()

		# Screen detections and populate scene object list
		scene_objects: list[SceneObject] = []
		for detection in scene_detections.detections:
			for category in detection.categories:
				if category.score > 0.35:
					box = detection.bounding_box
					scene_objects.append(
						SceneObject(
							category.category_name,
							box.origin_x + box.width / 2,
							box.origin_y + box.height / 2,
							(box.width * box.height),
							frame_quads.classify(box.origin_x + box.width / 2, box.origin_y + box.height / 2)
						)
					)
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
		
		# Update shared detection information for control thread
		vision_data.setDetections(scene_objects)
		vision_data.signalAvailable()

		# Display frame for debug
		cv2.imshow("scene", frame)

		# If you take this out it breaks the whole UI
		if cv2.waitKey(1) & 0xFF == ord('q'):
			print("Press CTRL-C to exit")
		
		# Exit on sentinel
		if(vision_data.checkSentinel()):
			camera.release()
			cv2.destroyAllWindows()
			return

#
# Control (main) thread tasks.
# Handles startup and shutdown of the vision thread, as well as user 
# interaction.
#
def main():
	try:
		print("[Control] Starting scene application.")
		tts: TextToSpeech = TextToSpeech()
		stt: SpeechToText = SpeechToText()
		vision_data: VisionData = VisionData()
		vision_thread: Thread = Thread(target=doVisionThread, args=(vision_data,))
		vision_thread.start()

		# Wait on vision thread
		tts.say("Just a second while the camera starts up")
		while(not vision_data.isAvailable()):
			sleep(1.0)

		# Get objects in scene
		tts.say("Looking at the scene")
		scene_names: list[str] = []
		for o in vision_data.getDetections():
			if(scene_names.count(o.name) == 0):
				scene_names.append(o.name)

		# Have user pick an object
		tts.say("I see: " + " ".join(scene_names) + ", What would you like to take a picture of?")
		target_object: str = ""
		while(True):
			user_choice: str = stt.listen()
			if(scene_names.count(user_choice) > 0):
				target_object = user_choice
				break
			else:
				tts.say("Sorry, we couldn't recognize what you said")
		tts.say(target_object)

		# Have user pick a position
		tts.say("Where would you like the " + target_object + " to be? You can say things like, top left, bottom right, center")
		target_quadrant: str = ""
		while(True):
			user_choice: str = stt.listen()
			match user_choice:
				case "top left":
					tts.say("Top left")
					target_quadrant = "top_left"
					break
				case "top right":
					tts.say("Top right")
					target_quadrant = "top_right"
					break
				case "bottom left":
					tts.say("Bottom left")
					target_quadrant = "bottom_right"
					break
				case "bottom right":
					tts.say("Bottom right")
					target_quadrant = "bottom_right"
					break
				case "center":
					tts.say("Center")
					target_quadrant = "middle_middle"
					break
				case _:
					tts.say("Sorry, we couldn't recognize what you said")
		tts.say("We'll guide your camera to the right spot now, Please move it slowly")

		# Guide object to proper position
		while(True):
			scene_objects: list[SceneObject] = vision_data.getDetections()
			tracked_object: SceneObject = ObjectHelper.getMostApparent(scene_objects, target_object)
			if(tracked_object.quadrant == target_quadrant):
				break
			if(tracked_object.name != "" and tracked_object.quadrant != ""):
				tts.say(FrameQuadrants.getMovement(tracked_object.quadrant, target_quadrant))
			sleep(0.1)

		# Take a picture
		tts.say("Perfect, Taking a picture now")
		vision_data.requestSaveImage()
		while(vision_data.checkSaveImage()):
			sleep(0.1)
		tts.say("Done saving the picture")

		# Clean up
		print("[Shutdown] Stopping vision thread...")
		vision_data.tripSentinel()
		vision_thread.join()
		print("[Shutdown] Done.")

	except:
		print("[Shutdown] Stopping vision thread...")
		vision_data.tripSentinel()
		vision_thread.join()
		print("[Shutdown] Main thread cleaned up.")
		raise

if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		print("CTRL+C Pressed")
