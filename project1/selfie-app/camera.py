import cv2

def main():
	camera = cv2.VideoCapture(0)

	while (True):
		# get frame from camera
		_, frame = camera.read()

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