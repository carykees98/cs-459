import cv2

def main():
	camera = cv2.VideoCapture(0)

	face_model = cv2.CascadeClassifier(cv2.data.haarcascades + 
			"haarcascade_frontalface_default.xml")

	while (True):
		# get frame from camera
		_, frame = camera.read()

		# get face bounding box
		faces = face_model.detectMultiScale(
			cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY),
			scaleFactor=1.25, # how much to scale the image for the model
			minNeighbors=4, # how many matching regions we need for a positive match
			minSize=(20, 20), # minimum size (px) to detect a face
			maxSize=(600, 600) # maximum size (px) to detect a face
		)

		for (face_x, face_y, face_w, face_h) in faces:
			# draw face bounding box
			cv2.rectangle(
				frame, # image to modify
				(face_x, face_y), # first corner
				(face_x + face_w, face_y + face_h), # second corner
				(255, 255, 0), # color
				0 # line type
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