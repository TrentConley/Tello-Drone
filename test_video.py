import cv2
from djitellopy import tello
import threading


def process_tello_video(drone):
    while True:
        frame = drone.get_frame_read().frame
        cv2.imshow("Frame", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cv2.destroyAllWindows()


import matplotlib.pyplot as plt


def process_tello_video_plt(drone):
    plt.ion()  # Turn on interactive mode
    fig, ax = plt.subplots()  # Create a figure and a set of subplots

    while True:
        frame = drone.get_frame_read().frame
        ax.imshow(frame)  # Convert BGR to RGB
        plt.pause(0.01)  # Pause for interval seconds.

        # If the figure window is closed, break the loop
        if not plt.fignum_exists(fig.number):
            break

    plt.ioff()  # Turn off interactive mode


from PIL import Image
import numpy as np


def process_tello_video_pil(drone):
    while True:
        frame = drone.get_frame_read().frame
        img = Image.fromarray(frame)  # Convert the frame to an image
        img.show()  # Display the image


from PIL import Image, ImageTk
import tkinter as tk


def process_tello_video_tk(drone):
    window = tk.Tk()  # Create a window
    label = tk.Label(window)  # Create a label in the window
    label.pack()  # Adjusts the size of the window to the size of the image

    def update_image():
        frame = drone.get_frame_read().frame
        img = Image.fromarray(frame)  # Convert the frame to an image
        photo = ImageTk.PhotoImage(img)  # Convert the image to a PhotoImage
        label.config(image=photo)  # Set the image of the label to the PhotoImage
        label.image = photo  # Keep a reference to the image
        window.after(10, update_image)  # Update the image every 10 ms

    update_image()  # Start updating the image
    window.mainloop()  # Start the main loop of tcl


def main():
    drone = tello.Tello()
    drone.connect()
    drone.streamon()

    # # Create a new thread
    # video_thread = threading.Thread(target=process_tello_video, args=(drone,))

    # # Start the new thread
    # video_thread.start()
    process_tello_video(drone)


print("running main")
main()
