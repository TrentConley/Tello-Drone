from djitellopy import tello
import keypad_module as km
from time import sleep

km.init()

drone = tello.Tello()
drone.connect()
print(drone.get_battery())

def getImput():
    #drone.takeoff()
    lr,fb,ud,yv = 0,0,0,0
    speed = 80

    if km.getKeys("LEFT"):
        lr = -speed
        print("LEFT KEY PRESSED...")
    elif km.getKeys("RIGHT"):
        lr = speed
        print("RIGHT KEY PRESSED...")

    if km.getKeys("UP"):
        fb = speed
        print("UP KEY PRESSED...")
    elif km.getKeys("DOWN"):
        fb = -speed
        print("DOWN KEY PRESSED...")

    if km.getKeys("w"):
        ud = speed
        print("W KEY PRESSED...")
    elif km.getKeys("s"):
        ud = -speed
        print("S KEY PRESSED...")

    if km.getKeys("a"):
        yv = speed
        print("A KEY PRESSED...")
    elif km.getKeys("d"):
        yv = -speed
        print("D KEY PRESSED...")
    if km.getKeys("q"):
        drone.land()
        print("Q KEY PRESSED...")
    elif km.getKeys("r"):
        drone.takeoff()
        print("R KEY PRESSED...")

    return [lr,fb,ud,yv]


while True:
    val = getImput()
    drone.send_rc_control(val[0], val[1],val[2],val[3])
    sleep(0.05)
