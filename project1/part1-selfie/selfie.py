"""
	selfie.py
	Project 1, Part 1: Selfie Application
	CS459 Human Computer Interaction
	Cary Keesler, Juno Meifert, Andrew Tringali
"""
import cv2
from mediapipe.tasks.python import BaseOptions
from mediapipe.tasks.python.vision import FaceDetector, FaceDetectorOptions
from mediapipe import Image, ImageFormat
import pyttsx3
import speech_recognition as sr
from threading import Thread, Lock
from datetime import datetime
from time import sleep

#
# ========== Class definitions ==========
#

# Data to be synchronized between the control thread and the vision thread
class VisionData:
	def __init__(self):
		self.__quadrant = "none"
		self.__quadrant_lock = Lock()
		self.__display_text = ""
		self.__display_text_lock = Lock()
		self.__sentinel = False
		self.__available = False
		self.__save_image_flag = False
	
	# Publish quadrant detected face is in
	def setQuadrant(self, quadrant: str) -> None:
		with self.__quadrant_lock:
			self.__quadrant = quadrant
	
	# Get the quadrant that a detected face is in
	def getQuadrant(self) -> str:
		with self.__quadrant_lock:
			return self.__quadrant
	
	# Sets the debug display text on the frame
	def setDisplayText(self, text: str) -> None:
		with self.__display_text_lock:
			self.__display_text = text
	
	# Gets the debug display text for the frame
	def getDisplayText(self) -> str:
		with self.__display_text_lock:
			return self.__display_text
	
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

# Provides functionality for classifying the quadrant that a face is in
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
	
	# Gets the direction of movement required to position the user in a quadrant
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
					return "Up"
				case "top":
					return "Down"
				case _:
					if(target_y == "top"):
						return "Up"
					return "Down"
	
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
			recorded_audio = self.__speech.listen(input)
			phrase = self.__speech.recognize_whisper(
				recorded_audio, language="english"
			).lower()
			print("[STT] Transcribed phrase \"" + phrase + "\"")
			return SpeechToText.__sanitize(phrase)
	
	# Remove punctuation and leading/trailing whitespace from a transcription
	def __sanitize(phrase: str) -> str:
		return phrase.replace(".", "").replace("!", "").replace("?", "").strip()

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
	frame_quads = FrameQuadrants(frame.shape[1], frame.shape[0])

	# Set up face detection
	face_model = FaceDetector.create_from_options(
		FaceDetectorOptions(
			base_options=BaseOptions(model_asset_path="model/blazeface_sr.tflite")
		)
	)

	print("[Vision] Running face detection.")
	while (True):
		# Get a single frame from the camera
		_, frame = camera.read()

		# get face bounding box
		faces = face_model.detect(
			Image(image_format=ImageFormat.SRGB, data=frame)
		)

		# Save image on request
		if(vision_data.checkSaveImage()):
			print("[Vision] Saving image...")
			cv2.imwrite(datetime.now().strftime("%Y%m%d%H%M%S.jpg"), frame)
			vision_data.resetSaveImage()

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

		vision_data.signalAvailable()

		# Display frame for debug
		cv2.imshow("selfie", frame)

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
		# Set up user interaction wrappers and vision thread
		print("[Control] Starting selfie application.")
		tts: TextToSpeech = TextToSpeech()
		stt: SpeechToText = SpeechToText()
		vision_data: VisionData = VisionData()
		vision_thread: Thread = Thread(
			target=doVisionThread, args=(vision_data,)
		)
		vision_thread.start()

		# Wait on vision thread
		tts.say("Just a second while the camera starts up")
		while(not vision_data.isAvailable()):
			sleep(1.0)

		# Guide user to frame
		if(vision_data.getQuadrant() == "none"):
			tts.say("Your face isn't in frame")
			tts.say("Your face isn't in frame. Try moving your head slowly " + 
		   			"left and right, then up and down")
			while(vision_data.getQuadrant() == "none"):
				sleep(0.1)
		
		# Prompt user for face location
		tts.say("You're in frame! Where would you like your face to be? " + 
		  		"You can say things like, top left, bottom right, or center")
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
					tts.say("Sorry, we didn't quite get that, please try again")
		tts.say("We'll guide you to the right spot now, " + 
		  		"Please move your head slowly")

		# Guide user to desired quadrant
		while(vision_data.getQuadrant() != target_quadrant):
			current_quadrant: str = vision_data.getQuadrant()
			vision_data.setDisplayText(
				FrameQuadrants.getMovement(current_quadrant, target_quadrant)
			)
			tts.say(
				FrameQuadrants.getMovement(current_quadrant, target_quadrant)
			)
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
		# Shut down vision thread on exception
		print("[Shutdown] Stopping vision thread...")
		vision_data.tripSentinel()
		vision_thread.join()
		print("[Shutdown] Main thread cleaned up.")
		raise

if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		print("CTRL+C")
