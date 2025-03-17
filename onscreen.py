import win32gui
import win32con
import win32ui
import ctypes
import pyautogui
import time
import threading

# Define BLENDFUNCTION constants:
AC_SRC_OVER = 0x00
AC_SRC_ALPHA = 0x01

# Get screen dimensions
screen_width, screen_height = pyautogui.size()

# Create window class
wndClass = win32gui.WNDCLASS()
hInstance = win32gui.GetModuleHandle(None)
wndClass.lpszClassName = "TransparentWindow"
wndClass.lpfnWndProc = win32gui.DefWindowProc
wndClass.hCursor = win32gui.LoadCursor(None, win32con.IDC_ARROW)
wndClass.hbrBackground = win32con.COLOR_WINDOW
atom = win32gui.RegisterClass(wndClass)

# Create window with transparent properties
hWnd = win32gui.CreateWindowEx(
    win32con.WS_EX_LAYERED | win32con.WS_EX_TRANSPARENT | win32con.WS_EX_TOPMOST,
    wndClass.lpszClassName,
    "Overlay",
    win32con.WS_POPUP,
    0, 0, screen_width, screen_height,
    None, None, hInstance, None
)

# Create a compatible device context (DC) for drawing
hdc = win32gui.GetDC(hWnd)
mfcDC = win32ui.CreateDCFromHandle(hdc)
bufferDC = mfcDC.CreateCompatibleDC()

# Create a 32-bit bitmap for transparency
bitmap = win32ui.CreateBitmap()
bitmap.CreateCompatibleBitmap(mfcDC, screen_width, screen_height)
bufferDC.SelectObject(bitmap)

# Global ball position and a flag to initialize it
ball_x, ball_y = 0, 0
first_run = True

def draw_ball():
    global ball_x, ball_y, first_run

    # Clear the buffer with full transparency (0x00000000)
    bufferDC.FillSolidRect((0, 0, screen_width, screen_height), 0x00000000)

    # Get current cursor position (target position)
    target_x, target_y = pyautogui.position()

    # On the first run, place the ball at the cursor immediately.
    if first_run:
        ball_x, ball_y = target_x, target_y
        first_run = False
    else:
        # Update the ball's position with easing for smooth movement.
        easing = 0.1  # Adjust between 0 (no movement) and 1 (instant)
        ball_x += (target_x - ball_x) * easing
        ball_y += (target_y - ball_y) * easing

    # Create a brush to draw the ball (using a dictionary with correct keys)
    brush = win32gui.CreateBrushIndirect({
        "Style": win32con.BS_SOLID,
        "Color": 0x0000FF,  # COLORREF value. Note: 0x0000FF will display as red because of Windows' BGR ordering.
        "Hatch": 0
    })

    # Select the brush into the DC and draw an ellipse (ball)
    win32gui.SelectObject(bufferDC.GetSafeHdc(), brush)
    radius = 20  # radius of the ball
    win32gui.Ellipse(bufferDC.GetSafeHdc(), int(ball_x) - radius, int(ball_y) - radius, int(ball_x) + radius, int(ball_y) + radius)

    # Prepare the BLENDFUNCTION tuple:
    # (BlendOp, BlendFlags, SourceConstantAlpha, AlphaFormat)
    blend = (AC_SRC_OVER, 0, 255, AC_SRC_ALPHA)

    # Update the layered window with the buffer content
    hdc_screen = win32gui.GetDC(0)
    win32gui.UpdateLayeredWindow(
        hWnd,
        hdc_screen,
        (0, 0),                       # Window position
        (screen_width, screen_height),# Window size
        bufferDC.GetSafeHdc(),        # Source DC with our bitmap
        (0, 0),                       # Source point
        0,                            # Color key (unused)
        blend,                        # BLENDFUNCTION structure
        win32con.ULW_ALPHA
    )
    win32gui.ReleaseDC(hWnd, hdc_screen)

    # Clean up the brush to avoid memory leaks
    win32gui.DeleteObject(brush)

def update():
    while True:
        draw_ball()
        time.sleep(0.01)  # roughly 100 FPS for smooth updates

# Show the transparent window
win32gui.ShowWindow(hWnd, win32con.SW_SHOW)

# Start the update thread to animate the ball
threading.Thread(target=update, daemon=True).start()

# Process window messages
win32gui.PumpMessages()
