import win32gui
import win32con
import win32ui
import ctypes
import pyautogui
import time
import threading

# Define BLENDFUNCTION constants
AC_SRC_OVER = 0x00
AC_SRC_ALPHA = 0x01

# Global list of balls and settings
balls = []
easing = 0.001     # Easing factor (0: no movement, 1: instant)
radius = 20      # Radius of each ball

# A simple ball class to store its current position
class Ball:
    def __init__(self, x, y):
        self.x = x
        self.y = y

# Get screen dimensions
screen_width, screen_height = pyautogui.size()

# Custom window procedure to handle key presses
def wndProc(hWnd, msg, wParam, lParam):
    if msg == win32con.WM_KEYDOWN:
        # Z key (spawn new ball)
        if wParam == ord('Z'):
            x, y = pyautogui.position()
            balls.append(Ball(x, y))
            return 0
        # X key (remove oldest ball)
        elif wParam == ord('X'):
            if balls:
                balls.pop(0)
            return 0
    return win32gui.DefWindowProc(hWnd, msg, wParam, lParam)

# Create a window class with our custom window procedure
wndClass = win32gui.WNDCLASS()
hInstance = win32gui.GetModuleHandle(None)
wndClass.lpszClassName = "TransparentWindow"
wndClass.lpfnWndProc = wndProc  # our custom callback
wndClass.hCursor = win32gui.LoadCursor(None, win32con.IDC_ARROW)
wndClass.hbrBackground = win32con.COLOR_WINDOW
atom = win32gui.RegisterClass(wndClass)

# Create a layered, topmost window (clickable to get keyboard focus)
hWnd = win32gui.CreateWindowEx(
    win32con.WS_EX_LAYERED | win32con.WS_EX_TOPMOST,
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

# Create a 32-bit bitmap for transparency and select it into the buffer DC
bitmap = win32ui.CreateBitmap()
bitmap.CreateCompatibleBitmap(mfcDC, screen_width, screen_height)
bufferDC.SelectObject(bitmap)

def draw_balls():
    # Clear the buffer with full transparency (ARGB = 0x00RRGGBB)
    bufferDC.FillSolidRect((0, 0, screen_width, screen_height), 0x00000000)
    
    # Get current cursor position (target for balls to chase)
    target_x, target_y = pyautogui.position()
    
    # If no ball exists, spawn one automatically at the target position.
    if not balls:
        balls.append(Ball(target_x, target_y))
    
    # Update each ball's position and draw it
    for ball in balls:
        # Easing: move ball toward the cursor gradually
        ball.x += (target_x - ball.x) * easing
        ball.y += (target_y - ball.y) * easing

        # Create a brush for the ball.
        # Using 0x00FF00 for green (COLORREF: BGR ordering; 0x00FF00 is green)
        brush = win32gui.CreateBrushIndirect({
            "Style": win32con.BS_SOLID,
            "Color": 0x00FF00,
            "Hatch": 0
        })
        win32gui.SelectObject(bufferDC.GetSafeHdc(), brush)
        win32gui.Ellipse(
            bufferDC.GetSafeHdc(),
            int(ball.x) - radius,
            int(ball.y) - radius,
            int(ball.x) + radius,
            int(ball.y) + radius
        )
        win32gui.DeleteObject(brush)
    
    # Prepare the BLENDFUNCTION tuple for per-pixel alpha blending:
    # (BlendOp, BlendFlags, SourceConstantAlpha, AlphaFormat)
    blend = (AC_SRC_OVER, 0, 255, AC_SRC_ALPHA)
    
    # Update the layered window with the offscreen buffer content
    hdc_screen = win32gui.GetDC(0)
    win32gui.UpdateLayeredWindow(
        hWnd,
        hdc_screen,
        (0, 0),                         # Window position on screen
        (screen_width, screen_height),  # Window size
        bufferDC.GetSafeHdc(),          # Source DC (our bitmap)
        (0, 0),                         # Source point in the bitmap
        0,                              # Color key (unused)
        blend,                          # BLENDFUNCTION for alpha blending
        win32con.ULW_ALPHA
    )
    win32gui.ReleaseDC(hWnd, hdc_screen)

def update():
    while True:
        draw_balls()
        time.sleep(0.01)  # roughly 100 FPS for smooth animation

# Show the window and bring it to the foreground so it can receive key events
win32gui.ShowWindow(hWnd, win32con.SW_SHOW)
win32gui.SetForegroundWindow(hWnd)

# Start the update thread for smooth animation
threading.Thread(target=update, daemon=True).start()

# Process window messages (this call blocks)
win32gui.PumpMessages()
