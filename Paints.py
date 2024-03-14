import tkinter as tk
from tkinter import ttk, colorchooser, messagebox
from tkinter import filedialog
from PIL import Image, ImageDraw
from PIL import ImageTk
from PIL import Image, ImageTk
import pygame
import random
import os

class StartupScreen:
    def __init__(self, parent):
        self.parent = parent
        self.startup = tk.Toplevel(parent)
        self.startup.title("Tkinter Drawing App")

        self.startup_width = 700
        self.startup_height = 500

        screen_width = self.parent.winfo_screenwidth()
        screen_height = self.parent.winfo_screenheight()

        x_position = (screen_width - self.startup_width) // 2
        y_position = (screen_height - self.startup_height) // 2

        self.startup.geometry(f"{self.startup_width}x{self.startup_height}+{x_position}+{y_position}")

        script_dir = os.path.dirname(os.path.abspath(__file__))

        image_path = os.path.join(script_dir, "paint.png")

        try:
            self.image = tk.PhotoImage(file=image_path)
        except tk.TclError:
            print(f"Error loading image from {image_path}")
            self.image = None

        if self.image:
            label_image = tk.Label(self.startup, image=self.image)
            label_image.place(relx=0.5, rely=0.5, anchor=tk.CENTER) 
            label_text = tk.Label(self.startup, text="Drawing App", font=("Arial", 24, "bold"))
            label_text.pack(pady=20)

        self.bg_color = "#add8e6"  

        self.transition_to_light_red()

    def close_startup(self):
        self.startup.destroy()
        self.parent.deiconify() 

    def transition_to_light_red(self):
        target_color = "#ffcccb"  
        transition_duration = 1000  
        steps = 100 

        self.transition_step(target_color, steps, transition_duration, 0)

    def transition_step(self, target_color, steps, duration, current_step):
        if current_step <= steps:
            r = int((1 - current_step / steps) * int(self.bg_color[1:3], 16) + (current_step / steps) * int(target_color[1:3], 16))
            g = int((1 - current_step / steps) * int(self.bg_color[3:5], 16) + (current_step / steps) * int(target_color[3:5], 16))
            b = int((1 - current_step / steps) * int(self.bg_color[5:], 16) + (current_step / steps) * int(target_color[5:], 16))

            intermediate_color = "#{:02x}{:02x}{:02x}".format(r, g, b)

            self.startup.configure(bg=intermediate_color)

            self.startup.after(int(duration / steps), self.transition_step, target_color, steps, duration, current_step + 1)
        else:
            self.startup.configure(bg=target_color)
            self.startup.after(2000, self.close_startup)  

class StatTool:
    def __init__(self, root):
        self.root = root
        self.status_var = tk.StringVar()
        self.status_var.set("Current Tool: Pencil | Current Color: Black")
        self.status_font = ("Arial", 14, "bold")
        self.status_bar = ttk.Label(root, textvariable=self.status_var, anchor=tk.W, font=self.status_font)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def update_status(self, tool, color):
        self.status_var.set(f"Current Tool: {tool} | Current Color: {color}")

class PTkinterDrawingApp:
    def __init__(self, root):
        pygame.mixer.init()
        
        self.root = root
        self.root.title("Tkinter Drawing App")
        self.root.withdraw() 
 
        self.startup = StartupScreen(root)

        self.status_bar = StatTool(root)

        self.style = ttk.Style()
        self.style.configure("TButton", padding=10, font=("Helvetica", 6), background="light gray", foreground="black")
        self.style.configure("TButtonDark", background="dark gray", foreground="white")

        self.canvas = tk.Canvas(root, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        self.canvas.config(cursor="pencil")

        self.pen_color = "Black"
        self.drawing = False
        self.points = []

        self.strokes = []  
        self.undone_strokes = []  
        self.undone_canvas_states = []  
        self.bg_color = "white"  

        self.is_coloring_book_option_selected = False

        self.red_canvas = tk.Canvas(root, bg="red", width=15, height=15, highlightthickness=0, bd=0)
        self.red_canvas.bind("<Button-1>", lambda event: self.set_color("red"))
        self.red_canvas.pack(side=tk.LEFT, padx=6, pady=6)

        self.blue_canvas = tk.Canvas(root, bg="blue", width=15, height=15, highlightthickness=0, bd=0)
        self.blue_canvas.bind("<Button-1>", lambda event: self.set_color("blue"))
        self.blue_canvas.pack(side=tk.LEFT, padx=6, pady=6)

        self.yellow_canvas = tk.Canvas(root, bg="yellow", width=15, height=15, highlightthickness=0, bd=0)
        self.yellow_canvas.bind("<Button-1>", lambda event: self.set_color("yellow"))
        self.yellow_canvas.pack(side=tk.LEFT, padx=6, pady=6)

        self.green_canvas = tk.Canvas(root, bg="green", width=15, height=15, highlightthickness=0, bd=0)
        self.green_canvas.bind("<Button-1>", lambda event: self.set_color("green"))
        self.green_canvas.pack(side=tk.LEFT, padx=6, pady=6)

        self.pink_canvas = tk.Canvas(root, bg="pink", width=15, height=15, highlightthickness=0, bd=0)
        self.pink_canvas.bind("<Button-1>", lambda event: self.set_color("pink"))
        self.pink_canvas.pack(side=tk.LEFT, padx=6, pady=6)

        self.purple_canvas = tk.Canvas(root, bg="purple", width=15, height=15, highlightthickness=0, bd=0)
        self.purple_canvas.bind("<Button-1>", lambda event: self.set_color("purple"))
        self.purple_canvas.pack(side=tk.LEFT, padx=6, pady=6)

        self.brown_canvas = tk.Canvas(root, bg="brown", width=15, height=15, highlightthickness=0, bd=0)
        self.brown_canvas.bind("<Button-1>", lambda event: self.set_color("brown"))
        self.brown_canvas.pack(side=tk.LEFT, padx=6, pady=6)

        self.grey_canvas = tk.Canvas(root, bg="grey", width=15, height=15, highlightthickness=0, bd=0)
        self.grey_canvas.bind("<Button-1>", lambda event: self.set_color("grey"))
        self.grey_canvas.pack(side=tk.LEFT, padx=6, pady=6)

        self.black_canvas = tk.Canvas(root, bg="black", width=15, height=15, highlightthickness=0, bd=0)
        self.black_canvas.bind("<Button-1>", lambda event: self.set_color("black"))
        self.black_canvas.pack(side=tk.LEFT, padx=6, pady=6)

        self.brush_size = 2

        self.brush_size_label = ttk.Label(root, text="Brush Size: 2", font=("Arial", 12, "bold"))
        self.brush_size_label.pack(side=tk.LEFT, padx=6, pady=6)

        self.brush_size_scale = ttk.Scale(root, from_=1, to=10, orient=tk.HORIZONTAL, length=100, command=self.updating_brush_size)
        self.brush_size_scale.set(self.brush_size)
        self.brush_size_scale.pack(side=tk.LEFT, padx=6, pady=6)

        self.color_button = ttk.Button(root, text="Pick Color", command=self.pick_color, style="TButton")
        self.color_button.pack(side=tk.LEFT, pady=6)

        self.random_color_button = ttk.Button(root, text="Random Color", command=self.generate_random_color, style="TButton")
        self.random_color_button.pack(side=tk.LEFT, pady=6)

        self.bucket_button = ttk.Button(root, text="Bucket Fill", command=self.bucket_fill, style="TButton")
        self.bucket_button.pack(side=tk.LEFT, pady=6)

        self.eraser_button = ttk.Button(root, text="Eraser", command=self.toggle_eraser, style="TButton")
        self.eraser_button.pack(side=tk.LEFT, pady=6)

        self.erase_button = ttk.Button(root, text="Clear Canvas", command=self.ask_erase, style="TButton")
        self.erase_button.pack(side=tk.LEFT, pady=6)

        self.coloring_book_button = ttk.Button(root, text="Coloring Book", command=self.show_coloring_book, style="TButton")
        self.coloring_book_button.pack(side=tk.LEFT, pady=6)

        self.dark_mode_button = ttk.Button(root, text="Toggle Dark Mode", command=self.toggle_dark_mode, style="TButton")
        self.dark_mode_button.pack(side=tk.LEFT, pady=6)

        self.save_button = ttk.Button(root, text="Save", command=self.save_as_jpeg, style="TButton")
        self.save_button.pack(side=tk.RIGHT, padx=6, pady=6)

        self.redo_button = ttk.Button(root, text="Redo", command=self.redo, style="TButton")
        self.redo_button.pack(side=tk.RIGHT, padx=6, pady=6)

        self.undo_button = ttk.Button(root, text="Undo", command=self.undo, style="TButton")
        self.undo_button.pack(side=tk.RIGHT, padx=6, pady=6)

        script_dir = os.path.dirname(os.path.abspath(__file__))

        self.eraser_sound_path = os.path.join(script_dir, "erasing.wav")
        self.eraser_sound = pygame.mixer.Sound(self.eraser_sound_path)

        splat_sound_path = os.path.join(script_dir, "splat.wav")
        self.splat_sound = pygame.mixer.Sound(splat_sound_path)

        wipe_sound_path = os.path.join(script_dir, "wipeglass.wav")
        self.wipe_sound = pygame.mixer.Sound(wipe_sound_path)

        coloring_book_sound_path = os.path.join(script_dir, "coloringbook.wav")
        self.coloring_book_sound = pygame.mixer.Sound(coloring_book_sound_path)

        self.coloring_book_image_path = os.path.join(script_dir, "innocentperson.png")
        try:
            self.coloring_book_image = Image.open(self.coloring_book_image_path)
            self.coloring_book_image = ImageTk.PhotoImage(self.coloring_book_image)
        except Exception as e:
            print(f"Error loading coloring book image: {e}")
            self.coloring_book_image = None

        self.canvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.canvas.bind("<Button-1>", self.beginning_draw)
        self.canvas.bind("<B1-Motion>", self.draw)
        self.canvas.bind("<ButtonRelease-1>", self.stop_draw)

        root.bind("<Control-z>", lambda event: self.undo())
        root.bind("<Control-s>", lambda event: self.save_as_jpeg())
        root.bind("<Control-y>", lambda event: self.redo())
        root.bind("<Control-e>", lambda event: self.toggle_eraser())
        root.bind("<Control-c>", lambda event: self.ask_erase())
        root.bind("<Control-r>", lambda event: self.generate_random_color())
        root.bind("<Control-b>", lambda event: self.bucket_fill())
        root.bind("<Control-p>", lambda event: self.pick_color())
        root.bind("<Control-d>", lambda event: self.toggle_dark_mode())
        root.bind("<Control-a>", lambda event: self.show_coloring_book())

        self.dark_mode = False  
        self.is_eraser = False  

        self.canvas_saved = True
        root.protocol("WM_DELETE_WINDOW", self.on_closing)

    def beginning_draw(self, event):
        self.drawing = True
        self.points = []
        color = self.pen_color if not self.is_eraser else self.bg_color
        style = "line" if not self.is_eraser else "oval"  
        self.points.append((event.x, event.y, color, style, self.brush_size))
        self.status_bar.update_status("Pencil" if not self.is_eraser else "Eraser", self.pen_color)
        
    def updating_brush_size(self, size):
        try:
            self.brush_size = round(float(size))
            self.brush_size_label.config(text=f"Brush Size: {self.brush_size}")
        except ValueError:
            pass  

    def draw(self, event):
     if self.drawing:
        x, y = event.x, event.y
        color = self.pen_color if not self.is_eraser else self.bg_color
        style = "line" if not self.is_eraser else "line"  

        if style == "line" and self.points:
            x0, y0, _, _, _ = self.points[-1]
            self.canvas.create_line(x0, y0, x, y, fill=color, width=self.brush_size * 2, capstyle=tk.ROUND, smooth=tk.TRUE)

        self.points.append((x, y, color, style, self.brush_size))

    def stop_draw(self, event):
        if self.drawing:
            self.drawing = False
            self.strokes.append(list(self.points))
            self.undone_strokes = []
            self.update_canvas_state()

    def update_canvas_state(self):
     self.undone_canvas_states.append({"bg_color": self.bg_color, "strokes": list(self.strokes)})
     self.canvas_saved = False

    def undo(self):
        if self.strokes:
            last_stroke = self.strokes.pop()
            self.undone_strokes.append(last_stroke)
            self.redraw()

    def redo(self):
        if self.undone_strokes:
            undone_stroke = self.undone_strokes.pop()
            self.strokes.append(undone_stroke)
            self.redraw()

    def ask_erase(self):
        response = messagebox.askyesno("WARNING", "This will clear your canvas. Are you sure you want to continue?", icon=messagebox.WARNING)
        if response:
            self.erase()

    def erase(self):
        self.undone_canvas_states.append({"bg_color": self.bg_color})
        self.canvas.delete("all")
        self.strokes = []
        self.undone_strokes = []
        self.bg_color = "white"
        self.redraw()
        self.play_sound(self.wipe_sound)

    def redraw(self):
        self.canvas.delete("all")

        self.canvas.create_rectangle(0, 0, self.canvas.winfo_width(), self.canvas.winfo_height(), fill=self.bg_color, outline="")

        for stroke in self.strokes:
            for i in range(len(stroke) - 1):
                x1, y1, color, style, brush_size = stroke[i]
                x2, y2, _, _, _ = stroke[i + 1]

                if style == "line":
                    self.canvas.create_line(x1, y1, x2, y2, fill=color, width=brush_size * 2, capstyle=tk.ROUND, smooth=tk.TRUE)
                elif style == "oval":
                    self.canvas.create_oval(
                        x1 - brush_size, y1 - brush_size,
                        x1 + brush_size, y1 + brush_size,
                        fill=color, outline=color
                    )

    def pick_color(self):
        color = colorchooser.askcolor(parent=self.root, title="Pick a Color", color=self.pen_color)[1]
        if color:
            self.pen_color = color
            self.status_bar.update_status("Pencil" if not self.is_eraser else "Eraser", self.pen_color)

    def set_color(self, color):
     color = color.capitalize()
     self.pen_color = color
     self.status_bar.update_status("Pencil" if not self.is_eraser else "Eraser", self.pen_color)

    def generate_random_color(self):
        random_color = "#{:06x}".format(random.randint(0, 0xFFFFFF))
        self.set_color(random_color)
        self.status_bar.update_status("Random Color", random_color)

    def bucket_fill(self):
        self.undone_canvas_states.append({"bg_color": self.bg_color})
        color = colorchooser.askcolor(parent=self.root, title="Pick a Color", color=self.bg_color)[1]
        if color:
            self.bg_color = color
            self.redraw()
            self.status_bar.update_status("Bucket Fill", self.bg_color)
            self.play_sound(self.splat_sound) 

    def toggle_dark_mode(self):
        self.dark_mode = not self.dark_mode

        if self.dark_mode:
            self.root.configure(bg="black")
            button_style = "TButtonDark"
        else:
            self.root.configure(bg="white")
            button_style = "TButton"

        self.style.configure(button_style, background="dark gray", foreground="white" if self.dark_mode else "black")
        self.redraw()
        self.status_bar.update_status("Toggle Dark Mode", "")

    def toggle_eraser(self):
     self.is_eraser = not self.is_eraser

     if self.is_eraser:
        self.canvas.config(cursor="circle")  
        self.eraser_button.configure(style="TButton")
        self.play_sound(self.eraser_sound)
     else:
        self.canvas.config(cursor="pencil")
        self.eraser_button.configure(style="TButton")

    def play_sound(self, sound):
        pygame.mixer.Sound.play(sound)

    def save_as_jpeg(self):
     file_path = filedialog.asksaveasfilename(defaultextension=".jpeg", filetypes=[("JPEG files", "*.jpeg")])
     if file_path:
        self.root.update()

        image = Image.new("RGB", (self.canvas.winfo_width(), self.canvas.winfo_height()), color=self.bg_color)
        draw = ImageDraw.Draw(image)

        for stroke in self.strokes:
            for i in range(len(stroke) - 1):
                x1, y1, color, _, brush_size = stroke[i]
                x2, y2, _, _, _ = stroke[i + 1]
                draw.line([(x1, y1), (x2, y2)], fill=color, width=brush_size * 2)

        if self.coloring_book_image and self.is_coloring_book_option_selected:
            coloring_book_image_pil = Image.open(self.coloring_book_image_path)
            coloring_book_image_pil = coloring_book_image_pil.convert("RGBA")

            x_position = (self.canvas.winfo_width() - coloring_book_image_pil.width) // 2
            y_position = (self.canvas.winfo_height() - coloring_book_image_pil.height) // 2

            image.paste(coloring_book_image_pil, (x_position, y_position), coloring_book_image_pil)

        image.save(file_path, "JPEG")

        save_sound_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "saving.wav")
        save_sound = pygame.mixer.Sound(save_sound_path)
        self.play_sound(save_sound)

        self.undone_canvas_states = [] 
        messagebox.showinfo("Saved", f"Canvas saved as {file_path}")
        self.status_bar.update_status("Save", "")
        self.canvas_saved = True

    def is_canvas_saved(self):
        return self.canvas_saved

    def on_closing(self):
        if (self.strokes or self.undone_strokes) and not self.is_canvas_saved():
            response = messagebox.askyesnocancel("Unsaved Changes", "Do you want to save your changes before closing?", icon=messagebox.WARNING)
            if response is not None:
                if response:
                    self.save_as_jpeg()
                self.root.destroy()
        else:
            self.root.destroy()

    def show_coloring_book(self):
        if self.coloring_book_image:
            self.is_coloring_book_option_selected = True  

            self.canvas.delete("drawing")

            canvas_width = self.canvas.winfo_width()
            canvas_height = self.canvas.winfo_height()

            image_width = self.coloring_book_image.width()
            image_height = self.coloring_book_image.height()

            x_position = (canvas_width - image_width) // 2
            y_position = (canvas_height - image_height) // 2

            self.canvas.create_image(x_position, y_position, anchor=tk.NW, image=self.coloring_book_image, tags="drawing")
            self.status_bar.update_status("Coloring Book", "")
            self.is_eraser = False

            self.play_sound(self.coloring_book_sound)

if __name__ == "__main__":
    root = tk.Tk()
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    app = PTkinterDrawingApp(root)
    app_width = 800
    app_height = 600
    x_position_app = (screen_width - app_width) // 2
    y_position_app = (screen_height - app_height) // 2
    root.geometry(f"{app_width}x{app_height}+{x_position_app}+{y_position_app}")
    root.mainloop()
