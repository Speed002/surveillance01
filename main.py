from tkinter import *
import cv2
from PIL import Image, ImageTk
import time
import face_recognition
# sounds
# ----------------- AppGui class ----------------------------------------
class App:
    def __init__(self, video_source=0):
        self.AppName = "Surveillance"
        self.window = Tk()
        self.window.title(self.AppName)
        # self.window.resizable(0,0)
        self.window['bg'] = 'black'
        self.video_source = video_source

        self.vid = MyVideoCapture(self.video_source)
        self.label = Label(self.window, text=self.AppName, font=15, bg='blue', fg="white").pack(side=TOP, fill=BOTH)

        # Create a canvas that can fit the above video source inside the window
        self.canvas = Canvas(self.window, width = self.vid.width, height = self.vid.height, bg="red")
        self.canvas.pack()

        # Button to take snap shot
        self.btn_snapshot = Button(self.window, text="Snapshot", width=30, bg="goldenrod2", activebackground="red", command=self.snapshot)
        self.btn_snapshot.pack(anchor=CENTER, expand=TRUE)
        self.update()
        # run the current open window after building the blocks
        self.window.mainloop()

    def snapshot(self):
        # get a frame from the video source, and take its picture
        check, frame = self.vid.getFrame()
        if check:
            # image name saved should be inform of the time it was taken
            image = "IMG-"+time.strftime("%H-%M-%S-%d-%m") + ".jpg"
            cv2.imwrite(image, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            # ---------------------show message on window that image is saved------------------
            msg = Label(self.window, text="image saved "+image, bg="black", fg="green").place(x=430, y=510)

    def update(self):
        # Get a frame from the video_source
        isTrue, frame = self.vid.getFrame()

        if isTrue:
            # locate faces
            frame = self.locate_face(frame)
            self.photo = ImageTk.PhotoImage(image = Image.fromarray(frame))
            self.canvas.create_image(0, 0, image = self.photo, anchor = NW)
        self.window.after(15, self.update)

    def locate_face(self, frame):
        # Find all face locations and encodings in the current frame processing
        face_location = face_recognition.face_locations(frame)
        face_encoding = face_recognition.face_encodings(frame, face_location)

        for (top, right, bottom, left), face_encoding in zip(face_location, face_encoding):
            name = "person"
            cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
            # Draw a label with a name below the face while implementing the parent frame
            cv2.rectangle(frame, (left, bottom - 20), (right, bottom), (0, 0, 255), cv2.FILLED)
            font = cv2.FONT_HERSHEY_SIMPLEX
            cv2.putText(frame, name, (left + 6, bottom - 5), font, 0.5, (255, 255, 255), 1)
        return frame

# ----------------- class capturing the video in frames ---------------------------
class MyVideoCapture:
    def __init__(self, video_source=0):
        # open the video source with cv2
        self.vid = cv2.VideoCapture(video_source)
        if not self.vid.isOpened(): # if it doesnt open, pull an error for the user
            raise ValueError("Unable to open camera \n Select another video source:", video_source)
        # but if it opens, take the measurements of the camera feed or the video feed
        self.width = self.vid.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT)

    def getFrame(self):
        if self.vid.isOpened():
            isTrue, frame = self.vid.read()
            if isTrue:
                # to say if indeed there is a frame picked, begin processing it by converting it to gray
                return (isTrue, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (isTrue, None)
        else:
            return

    def __del__(self):
        if self.vid.isOpened():
            self.vid.release()

if __name__ == "__main__":
    App()