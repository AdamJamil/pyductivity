import tkinter as tk
import PyHook3
import pythoncom
import threading
import win32gui
import screeninfo
from datetime import datetime
import tkinter.font


class Reminder:
    def __init__(self):
        self.name = "description"
        now = datetime.now()
        self.min = now.minute
        self.hour = now.hour
        self.day = now.day
        self.month = now.month
        self.year = now.year
        self.remind = 5


key = "F14"
add_reminder_key = "R"

prod_key = False
prod_key_used = False
win_open = False
reminder_screen = False
cursor = (0, 0, 0)
cursor_animation_thread = None

curr_reminder = Reminder()

root = tk.Tk()
canvas = None
width, height = 0, 0
root.attributes('-alpha', 0.35)
color = "#000010"
root.configure(bg=color)
root.overrideredirect(True)

font = tk.font.Font(family="Segoe UI", size=72)
small_font = tk.font.Font(family="Segoe UI", size=21)


def _create_circle(self, x, y, r, **kwargs):
    return self.create_oval(x-r, y-r, x+r, y+r, **kwargs)


def _create_round_rectangle(self, x, y, w, h, r=25, **kwargs):
    return self.create_circle(x + r, y + r, r, outline="", **kwargs) \
           and self.create_circle(x + w - r - 1, y + r, r, outline="", **kwargs) \
           and self.create_circle(x + r, y + h - r - 1, r, outline="", **kwargs) \
           and self.create_circle(x + w - r - 1, y + h - r - 1, r, outline="", **kwargs) \
           and self.create_rectangle(x, y+r, x + w, y + h - r, outline="", **kwargs) \
           and self.create_rectangle(x+r, y, x + w - r, y + h, outline="", **kwargs)


tk.Canvas.create_circle = _create_circle
tk.Canvas.create_round_rectangle = _create_round_rectangle


def set_geom():
    global width, height
    rect = win32gui.GetWindowRect(win32gui.GetForegroundWindow())
    cent = (rect[0] + rect[2]) // 2, (rect[1] + rect[3]) // 2
    for monitor in screeninfo.get_monitors():
        if monitor.x <= cent[0] <= monitor.x + monitor.width and monitor.y <= cent[1] <= monitor.y + monitor.height:
            width, height = monitor.width, monitor.height
            root.geometry(str(monitor.width) + "x" + str(monitor.height) + "+" + str(monitor.x) + "+" + str(monitor.y))
            return


def animate_cursor():
    while True:
        break


def init_add_reminder_ui():
    global canvas, width, height, font
    canvas = tk.Canvas(root, bg=color, width=width, height=height, highlightthickness=0)
    canvas.pack()
    reminder_string = "add a reminder"
    t_width_px = font.measure(reminder_string)
    t_height_px = (72*4) // 3
    t_x = (width // 2) - (t_width_px / 2)
    t_y = (height * (1 / 5)) - (t_height_px / 2)

    t_width_px += 40
    t_height_px += 40
    t_x -= 20
    t_y -= 20

    canvas.create_round_rectangle(t_x - 10, t_y - 10, t_width_px + 20, 400, r=10, fill="#2226DD")

    canvas.create_round_rectangle(t_x, t_y, t_width_px, t_height_px, r=10, fill="#2284DD")
    canvas.create_text((width // 2, height * (1 / 5)), text=reminder_string, font=font, fill="#2226DD")

    text_rows = [["description"], ["00:00", "AM", "01", "Jan", "0000"], ["Remind me", "5 min", "before"]]
    writable = [[True], [True, True, True, True, True], [False, True, False]]






def destroy_add_reminder_ui():
    global canvas
    canvas.destroy()


def load_add_reminder_screen():
    global prod_key, win_open, prod_key_used, reminder_screen

    prod_key_used = True
    set_geom()
    init_add_reminder_ui()
    root.deiconify()
    win_open = True
    reminder_screen = True


def key_down(event):
    global prod_key, win_open, prod_key_used, reminder_screen

    if event.Key == key:
        prod_key = True
        prod_key_used = False
        return True

    if event.Key == add_reminder_key and prod_key:
        load_add_reminder_screen()
        return False

    return True


def key_up(event):
    global prod_key, win_open, prod_key_used, reminder_screen

    if event.Key == key:
        if not prod_key_used:
            if win_open:
                reminder_screen = False
                root.withdraw()
                if canvas is not None:
                    destroy_add_reminder_ui()
            else:
                set_geom()
                root.deiconify()
            win_open = not win_open
        prod_key = False
        return True

    return True


hm = PyHook3.HookManager()
hm.KeyDown = key_down
hm.KeyUp = key_up
hm.HookKeyboard()
thread = threading.Thread(target=pythoncom.PumpMessages)
thread.start()
root.withdraw()
root.mainloop()
