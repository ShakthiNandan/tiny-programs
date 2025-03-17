import win32gui
import win32con
import win32ui
import ctypes
import pyautogui
import time
import threading

# Define BLENDFUNCTION constants for transparency
AC_SRC_OVER = 0x00
AC_SRC_ALPHA = 0x01

# Global list of balls and simulation settings
balls = []
radius = 20       # Ball radius in pixels

# Ball class now includes velocity
class Ball:
    def __init__(self, x, y):
        self.x = x      # current x position
        self.y = y      # current y position
        self.vx = 0.0   # x velocity
        self.vy = 0.0   # y velocity

# Get screen dimensions
screen_width, screen_height = pyautogui.size()

# Custom window procedure to handle key presses:
# - Z key spawns a new ball at the current cursor position.
# - X key removes the oldest ball.
def wndProc(hWnd, msg, wParam, lParam):
    if msg == win32con.WM_KEYDOWN:
        if wParam == ord('Z'):
            x, y = pyautogui.position()
            balls.append(Ball(x, y))
            return 0
        elif wParam == ord('X'):
            if balls:
                balls.pop(0)
            return 0
    return win32gui.DefWindowProc(hWnd, msg, wParam, lParam)

# Create a window class with our custom window procedure.
wndClass = win32gui.WNDCLASS()
hInstance = win32gui.GetModuleHandle(None)
wndClass.lpszClassName = "TransparentWindow"
wndClass.lpfnWndProc = wndProc  # our custom callback
wndClass.hCursor = win32gui.LoadCursor(None, win32con.IDC_ARROW)
wndClass.hbrBackground = win32con.COLOR_WINDOW + 1
atom = win32gui.RegisterClass(wndClass)

# Create a layered, topmost window.
# (We omit WS_EX_TRANSPARENT so it can get focus and receive key events.)
hWnd = win32gui.CreateWindowEx(
    win32con.WS_EX_LAYERED | win32con.WS_EX_TOPMOST,
    wndClass.lpszClassName,
    "Overlay",
    win32con.WS_POPUP,
    0, 0, screen_width, screen_height,
    None, None, hInstance, None
)

# Create a compatible device context (DC) for drawing.
hdc = win32gui.GetDC(hWnd)
mfcDC = win32ui.CreateDCFromHandle(hdc)
bufferDC = mfcDC.CreateCompatibleDC()

# Create a 32-bit bitmap for transparency and select it into the buffer DC.
bitmap = win32ui.CreateBitmap()
bitmap.CreateCompatibleBitmap(mfcDC, screen_width, screen_height)
bufferDC.SelectObject(bitmap)

# --- Physics update functions ---

def update_balls(target_x, target_y, dt):
    # Parameters for physics (tweak these for different behaviors)
    acceleration_factor = 0.5  # How strongly balls are pulled toward the cursor
    damping = 0.98             # Damping to gradually slow velocities
    restitution = 0.9          # Bounce factor on collision (0.0=inelastic, 1.0=elastic)

    # Accelerate each ball toward the target.
    for ball in balls:
        ax = (target_x - ball.x) * acceleration_factor
        ay = (target_y - ball.y) * acceleration_factor
        ball.vx += ax * dt
        ball.vy += ay * dt
        ball.x += ball.vx * dt
        ball.y += ball.vy * dt
        ball.vx *= damping
        ball.vy *= damping

    # Collision detection and resolution (pairwise).
    for i in range(len(balls)):
        for j in range(i+1, len(balls)):
            b1 = balls[i]
            b2 = balls[j]
            dx = b2.x - b1.x
            dy = b2.y - b1.y
            dist = (dx**2 + dy**2)**0.5
            if dist < 2 * radius and dist > 0:
                # Calculate overlap and normalize collision vector.
                overlap = 2 * radius - dist
                nx = dx / dist
                ny = dy / dist

                # Separate the balls by half the overlap each.
                b1.x -= nx * overlap / 2
                b1.y -= ny * overlap / 2
                b2.x += nx * overlap / 2
                b2.y += ny * overlap / 2

                # Relative velocity along the collision normal.
                rvx = b1.vx - b2.vx
                rvy = b1.vy - b2.vy
                vel_along_normal = rvx * nx + rvy * ny

                # Only resolve if balls are moving toward each other.
                if vel_along_normal < 0:
                    impulse = -(1 + restitution) * vel_along_normal / 2  # masses are assumed equal
                    b1.vx += impulse * nx
                    b1.vy += impulse * ny
                    b2.vx -= impulse * nx
                    b2.vy -= impulse * ny

# --- Drawing function ---

def draw_balls():
    # Clear the offscreen buffer (fully transparent).
    bufferDC.FillSolidRect((0, 0, screen_width, screen_height), 0x00000000)
    
    # Draw each ball as a filled circle.
    for ball in balls:
        # Create a brush for the ball. (Using 0x00FF00 for green; note COLORREF is BGR.)
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
    
    # Prepare the BLENDFUNCTION for per‑pixel alpha blending.
    blend = (AC_SRC_OVER, 0, 255, AC_SRC_ALPHA)
    hdc_screen = win32gui.GetDC(0)
    win32gui.UpdateLayeredWindow(
        hWnd,
        hdc_screen,
        (0, 0),  # window position
        (screen_width, screen_height),  # window size
        bufferDC.GetSafeHdc(),
        (0, 0),  # source point in bitmap
        0,       # color key (unused)
        blend,
        win32con.ULW_ALPHA
    )
    win32gui.ReleaseDC(hWnd, hdc_screen)

# --- Main update loop ---

def update_loop():
    dt = 0.01  # time step in seconds (~100 FPS)
    while True:
        # Use the current cursor position as the target.
        target_x, target_y = pyautogui.position()
        update_balls(target_x, target_y, dt)
        draw_balls()
        time.sleep(dt)

# Show the window and bring it to the foreground so it receives key events.
win32gui.ShowWindow(hWnd, win32con.SW_SHOW)
win32gui.SetForegroundWindow(hWnd)
win32gui.SetFocus(hWnd)

# Start the update thread.
threading.Thread(target=update_loop, daemon=True).start()

# Process window messages (this call blocks).
win32gui.PumpMessages()
