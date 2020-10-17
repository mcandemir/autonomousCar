import pyautogui
import win32api
import time


def click_coordinates():
    """
        If the key state changes, get the positions
        """
    for pos in range(2):
        state_prev = win32api.GetKeyState(0x01)
        while True:
            state_current = win32api.GetKeyState(0x01)
            if state_current != state_prev:
                pos = pyautogui.position()
                print("**Positions set: ", pos)
                return pos


def set_pos():
    print('\n*Select first corner of the cam')
    mouse_posX1, mouse_posY1 = click_coordinates()
    time.sleep(0.8)
    print('\n*Select second corner of the cam')
    mouse_posX2, mouse_posY2 = click_coordinates()
    time.sleep(0.8)
    cam_pos = (mouse_posX1, mouse_posY1, mouse_posX2, mouse_posY2)

    return cam_pos
