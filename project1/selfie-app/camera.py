import cv2

def main():
	camera = cv2.VideoCapture(0)

	face_model = cv2.CascadeClassifier(cv2.data.haarcascades + 
			"haarcascade_frontalface_default.xml")
	
	face_centerX = 0.0
	face_centerY = 0.0

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

		if(len(faces) > 0):
			face_minX = faces[0][0]
			face_minY = faces[0][1]
			face_maxX = face_minX + faces[0][2]
			face_maxY = face_minY + faces[0][3]

			face_centerX = rollingAvg(face_centerX, (face_minX + face_maxX) / 2.0, 10)
			face_centerY = rollingAvg(face_centerY, (face_minY + face_maxY) / 2.0, 10)

			cv2.rectangle(
				frame, # image to modify
				(face_minX, face_minY), # first corner
				(face_maxX, face_maxY), # second corner
				(0, 255, 255), # color
				2 # line width
			)

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