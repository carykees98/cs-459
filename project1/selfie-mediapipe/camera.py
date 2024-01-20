import cv2
from mediapipe.tasks.python import BaseOptions;
from mediapipe.tasks.python.vision import FaceDetector, FaceDetectorOptions;
from mediapipe import Image, ImageFormat;


# Stores and smoothly updates the location of a detected face
class Face:
	def __init__(self, smoothness = 5):
		self.__centerX = 0.0
		self.__centerY = 0.0
		self.__smoothness = smoothness
	
	def updateLocation(self, x, y):
		self.__centerX = self.__rollingAvg(self.__centerX, x, self.__smoothness)
		self.__centerY = self.__rollingAvg(self.__centerY, y, self.__smoothness)

	def getLocation(self):
		return (self.__centerX, self.__centerY)
	
	def getX(self):
		return self.__centerX
	
	def getY(self):
		return self.__centerY

	def __rollingAvg(self, prev, current, n):
		assert n > 0
		return (prev * n + current) / (n + 1)


class FrameQuadrants:
	def __init__(self, width, height, tolerance = 50):
		self.__width = width
		self.__height = height
		self.__centerX = width / 2
		self.__centerY = height / 2
		self.__tolerance = tolerance

	def getWidth(self):
		return self.__width
	
	def getHeight(self):
		return self.__height

	def classify(self, x, y):
		# centered
		if(
			x > self.__centerX - self.__tolerance and
			x < self.__centerX + self.__tolerance and
			y > self.__centerY - self.__tolerance and
			y < self.__centerY + self.__tolerance
		):
			#return "center"
			print()
		
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
		

def main():
	camera = cv2.VideoCapture(0)
	_, frame = camera.read()

	face_model = FaceDetector.create_from_options(
		FaceDetectorOptions(
			base_options=BaseOptions(model_asset_path="model/blazeface_sr.tflite")
		)
	)

	face = Face()
	frame_quads = FrameQuadrants(frame.shape[1], frame.shape[0])
	print(frame.shape)

	while (True):
		# get frame from camera
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
				face.updateLocation(x, y)

				cv2.rectangle(
					frame, # image to modify
					(box.origin_x, box.origin_y), # first corner
					(box.origin_x + box.width, box.origin_y + box.height), # second corner
					(0, 255, 255), # color
					2 # line width
				)
				# show quadrant
				# text shadow
				cv2.putText(
					frame,
					frame_quads.classify(face.getX(), face.getY()),
					(50, 50),
					0,
					1.0,
					(0,0,0),
					2
				)
				# text
				cv2.putText(
					frame,
					frame_quads.classify(face.getX(), face.getY()),
					(50, 50),
					0,
					1.0,
					(0,255,0),
					2
				)


		# draw marker on face
		cv2.line(
			frame,
			(round(face.getX() - 20), round(face.getY())),
			(round(face.getX() + 20), round(face.getY())),
			(255, 255, 0),
			2
		)
		cv2.line(
			frame,
			(round(face.getX()), round(face.getY() - 20)),
			(round(face.getX()), round(face.getY() + 20)),
			(255, 255, 0),
			2
		)

		# display frame
		cv2.imshow("title", frame)

		# Press Q for death
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break

	camera.release()




if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		print("CTRL + C Pressed, Exiting Program")

	cv2.destroyAllWindows()
