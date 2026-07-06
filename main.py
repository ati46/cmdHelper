import tkinter as tk
from tkinter import ttk
from pynput import keyboard
import time
import os
import json
import platform
import subprocess
import re
import pypinyin

from data_generator import ensure_data_files

# --- Pinyin Translation Helper ---
def to_pinyin(text):
    if not text:
        return "", ""
    try:
        # Full pinyin (without tone marks)
        full_list = pypinyin.pinyin(text, style=pypinyin.Style.NORMAL)
        full = "".join([item[0] for item in full_list]).lower()
        
        # Initials (first letter of each character)
        initials_list = pypinyin.pinyin(text, style=pypinyin.Style.FIRST_LETTER)
        initials = "".join([item[0] for item in initials_list]).lower()
        
        return full, initials
    except Exception as e:
        print(f"Error converting to pinyin: {e}")
        return "", ""

# --- Config & Data Loading ---
def get_data_dir():
    app_name = "cmd_helper"
    if platform.system() == "Windows":
        base_dir = os.environ.get("APPDATA", os.path.expanduser("~"))
        return os.path.join(base_dir, app_name, "data")
    else:
        base_dir = os.environ.get("XDG_CONFIG_HOME", os.path.expanduser("~/.config"))
        return os.path.join(base_dir, app_name, "data")

def load_data(data_dir):
    all_data = []
    if not os.path.exists(data_dir):
        return all_data
    
    for filename in os.listdir(data_dir):
        if filename.endswith(".json"):
            tool_name = filename[:-5].capitalize()
            filepath = os.path.join(data_dir, filename)
            try:
                with open(filepath, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    for item in data:
                        item['tool'] = tool_name
                        
                        # Pre-calculate pinyin for action and keywords to make search instant
                        action_full, action_initials = to_pinyin(item.get('action', ''))
                        item['pinyin_action_full'] = action_full
                        item['pinyin_action_initials'] = action_initials
                        
                        kw_fulls = []
                        kw_initials = []
                        for kw in item.get('keywords', []):
                            kf, ki = to_pinyin(kw)
                            kw_fulls.append(kf)
                            kw_initials.append(ki)
                        item['pinyin_keywords_full'] = kw_fulls
                        item['pinyin_keywords_initials'] = kw_initials
                        
                        all_data.append(item)
            except Exception as e:
                print(f"Error loading {filepath}: {e}")
    return all_data

# --- Multi-Monitor Support Helpers (X11 / xrandr) ---
def get_monitors():
    monitors = []
    try:
        # Run xrandr to get monitor geometries (Linux/X11)
        output = subprocess.check_output(["xrandr"], universal_newlines=True)
        pattern = re.compile(r'\b(\d+)x(\d+)\+(\d+)\+(\d+)\b')
        for line in output.splitlines():
            if " connected " in line:
                match = pattern.search(line)
                if match:
                    w, h, x, y = map(int, match.groups())
                    monitors.append({"width": w, "height": h, "x": x, "y": y})
    except Exception as e:
        print(f"Error querying xrandr: {e}")
    return monitors

def get_active_monitor(monitors, pointer_x, pointer_y):
    for m in monitors:
        if (m["x"] <= pointer_x < m["x"] + m["width"] and
            m["y"] <= pointer_y < m["y"] + m["height"]):
            return m
    if monitors:
        return monitors[0]
    return None

# --- UI Application ---
class CmdHelperApp:
    def __init__(self):
        self.data_dir = get_data_dir()
        ensure_data_files(self.data_dir)
        self.all_data = load_data(self.data_dir)
        
        self.root = tk.Tk()
        self.root.title("快捷命令助手 (Double Right Alt)")
        self.root.geometry("850x500")
        self.root.attributes("-topmost", True)
        
        # On Linux/X11, set window type to dialog so tiling WMs (like i3wm) float it by default
        try:
            self.root.attributes("-type", "dialog")
        except tk.TclError:
            pass
        
        # Disable minimize/maximize on some platforms to make it look like a popup
        self.root.resizable(True, True)
        
        # Hide by default
        self.root.withdraw()
        
        self.setup_ui()
        self.root.protocol("WM_DELETE_WINDOW", self.hide_window)
        self.root.bind("<Escape>", lambda e: self.hide_window())
        self.root.bind("<FocusOut>", self.on_focus_out)

    def setup_ui(self):
        style = ttk.Style()
        # Use a better looking theme if available
        if 'clam' in style.theme_names():
            style.theme_use('clam')
            
        style.configure("Treeview.Heading", font=("Arial", 11, "bold"))
        style.configure("Treeview", font=("Arial", 11), rowheight=28)
        
        main_frame = ttk.Frame(self.root, padding="15")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Make the background main_frame draggable
        self.make_draggable(main_frame)
        
        # Header text
        header_label = ttk.Label(main_frame, text="🔍 输入关键词搜索 | 💡 双击或回车复制命令 | ⬇️ 方向键向下选择", font=("Arial", 10, "italic"), foreground="gray")
        header_label.pack(anchor=tk.W, pady=(0, 5))
        
        # Make the header text label draggable
        self.make_draggable(header_label)
        
        # Search Entry
        self.search_var = tk.StringVar()
        self.search_var.trace("w", self.on_search)
        self.entry = ttk.Entry(main_frame, textvariable=self.search_var, font=("Arial", 14))
        self.entry.pack(fill=tk.X, pady=(0, 15))
        self.entry.bind("<Return>", self.on_entry_return)
        self.entry.bind("<Down>", self.focus_treeview)
        
        # Results Treeview
        columns = ("Tool", "Action", "Command")
        self.tree = ttk.Treeview(main_frame, columns=columns, show="headings", selectmode="browse")
        self.tree.heading("Tool", text="工具")
        self.tree.heading("Action", text="操作说明")
        self.tree.heading("Command", text="命令 / 快捷键")
        
        self.tree.column("Tool", width=80, anchor=tk.CENTER)
        self.tree.column("Action", width=250, anchor=tk.W)
        self.tree.column("Command", width=300, anchor=tk.W)
        
        self.tree.bind("<Double-1>", self.on_item_select)
        self.tree.bind("<Return>", self.on_item_select)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(main_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscroll=scrollbar.set)
        
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.update_list()

    def on_search(self, *args):
        query = self.search_var.get().lower()
        self.update_list(query)
        
    def update_list(self, query=""):
        for item in self.tree.get_children():
            self.tree.delete(item)
            
        terms = query.split()
        for item in self.all_data:
            match_all = True
            for term in terms:
                term = term.lower()
                # 1. Check original text
                original_text = f"{item['tool']} {item['action']} {' '.join(item.get('keywords', []))} {item['command']}".lower()
                if term in original_text:
                    continue
                
                # 2. Check pinyin action (full & initials)
                if term in item.get('pinyin_action_full', '') or term in item.get('pinyin_action_initials', ''):
                    continue
                
                # 3. Check pinyin keywords (full & initials)
                kw_match = False
                for kf, ki in zip(item.get('pinyin_keywords_full', []), item.get('pinyin_keywords_initials', [])):
                    if term in kf or term in ki:
                        kw_match = True
                        break
                if kw_match:
                    continue
                
                # Term did not match anywhere
                match_all = False
                break
                
            if match_all:
                self.tree.insert("", tk.END, values=(item['tool'], item['action'], item['command']))

    def on_entry_return(self, event):
        children = self.tree.get_children()
        if children:
            first_item = children[0]
            item_values = self.tree.item(first_item, "values")
            if item_values:
                self.copy_to_clipboard(item_values[2])
        self.hide_window()

    def focus_treeview(self, event):
        children = self.tree.get_children()
        if children:
            self.tree.focus(children[0])
            self.tree.selection_set(children[0])
            self.tree.focus_force()

    def on_item_select(self, event):
        selected_item = self.tree.selection()
        if selected_item:
            item_values = self.tree.item(selected_item[0], "values")
            if item_values:
                self.copy_to_clipboard(item_values[2])
        self.hide_window()

    def copy_to_clipboard(self, text):
        # Remove trailing comments or alternative commands like " (..." or " 或 ..."
        import re
        clean_text = re.split(r' \(| （| 或 ', text)[0].strip()
        
        self.root.clipboard_clear()
        self.root.clipboard_append(clean_text)
        self.root.update()

    def on_focus_out(self, event):
        # Use a small delay to let focus stabilize and avoid closing on transient focus changes
        self.root.after(100, self.check_focus)

    def check_focus(self):
        if not self.root.winfo_viewable():
            return
        if self.root.focus_get() is None:
            self.hide_window()

    def show_window(self):
        # 1. Pre-calculate size and position (for standard WMs to avoid flicker)
        self.root.update_idletasks()
        width = self.root.winfo_width()
        height = self.root.winfo_height()
        
        # If the window has not been mapped yet or is too small, use default dimensions
        if width < 300 or height < 200:
            width = 850
            height = 500
            
        # Get active monitor containing the mouse cursor
        monitors = get_monitors()
        pointer_x = self.root.winfo_pointerx()
        pointer_y = self.root.winfo_pointery()
        active_monitor = get_active_monitor(monitors, pointer_x, pointer_y)
        
        if active_monitor:
            x = active_monitor["x"] + (active_monitor["width"] // 2) - (width // 2)
            y = active_monitor["y"] + (active_monitor["height"] // 2) - (height // 2)
        else:
            # Fallback to virtual screen centering
            x = (self.root.winfo_screenwidth() // 2) - (width // 2)
            y = (self.root.winfo_screenheight() // 2) - (height // 2)
            
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
        self.all_data = load_data(self.data_dir) # reload data in case user modified it
        
        # 2. Map and show the window
        self.root.deiconify()
        self.root.lift()
        
        # 3. Force geometry application after mapping (for tiling WMs like i3wm)
        self.root.update_idletasks()
        self.root.geometry(f'{width}x{height}+{x}+{y}')
        
        # 4. Focus
        self.root.focus_force()
        self.entry.focus()
        self.search_var.set("") # clear previous search

    # --- Client-side Window Dragging (for borderless / titlebar-less WMs) ---
    def make_draggable(self, widget):
        widget.bind("<Button-1>", self.start_drag)
        widget.bind("<B1-Motion>", self.drag)

    def start_drag(self, event):
        self.drag_x = event.x
        self.drag_y = event.y

    def drag(self, event):
        deltax = event.x - self.drag_x
        deltay = event.y - self.drag_y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f"+{x}+{y}")
        
    def hide_window(self):
        self.root.withdraw()

# --- Hotkey Listener ---
last_ctrl_time = 0
app_instance = None

def on_press(key):
    global last_ctrl_time, app_instance
    try:
        if key == keyboard.Key.alt_r:
            current_time = time.time()
            if current_time - last_ctrl_time < 0.5:
                # Double pressed
                if app_instance:
                    app_instance.root.after(0, app_instance.show_window)
                last_ctrl_time = 0 # reset
            else:
                last_ctrl_time = current_time
    except AttributeError:
        pass

def run_app():
    global app_instance
    app_instance = CmdHelperApp()
    
    # Start hotkey listener
    listener = keyboard.Listener(on_press=on_press)
    listener.start()
    
    # Start tkinter mainloop
    print(f"Cmd Helper is running in the background.")
    print(f"Data directory: {app_instance.data_dir}")
    print(f"Double press 'Right Alt' to open the search popup.")
    app_instance.root.mainloop()

if __name__ == "__main__":
    run_app()
