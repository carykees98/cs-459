import pyttsx3

def main():
    tts = pyttsx3.init()
    tts.setProperty("rate", 125)
    tts.say("John Madden")
    tts.runAndWait()

if __name__ == "__main__":
	try:
		main()
	except KeyboardInterrupt:
		print("CTRL + C Pressed, Exiting Program")