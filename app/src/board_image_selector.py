from PIL import Image
import tkinter as tk
from src import match_icons
from pathlib import Path
import os
from src import constants, custom_utils
import customtkinter
import cv2
from src import log_utils
import src.file_utils

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from main import ImageSelectorApp

log = log_utils.get_logger()


class BoardIconSelector(customtkinter.CTkToplevel):
     
    def __init__(self, master = None, root: "ImageSelectorApp" = None, folder = ""): #type: ignore
         
        super().__init__(master = master)
        self.title(f"Select a Icon to be Saved as a new {folder} type")
        self.root = root
        self.folder = folder
        self.selected_image = None
        self.zoom = 1.0
        self.fit_zoom = 1.0
        self.min_zoom = 0.2
        self.max_zoom = 3.0
        self.cell_pad = 6
        self.num_columns = 6
        self.original_images = []
        self.cell_labels = []
        self.image_widgets = [] #type: ignore
        self.create_widgets()
        self.after(100, self.focus)

    def _get_scaling(self):
        if hasattr(self, "board_frame") and hasattr(self.board_frame, "_get_widget_scaling"):
            return self.board_frame._get_widget_scaling()
        if hasattr(self, "_get_window_scaling"):
            return self._get_window_scaling()
        return 1.0

    def _canvas_bg_color(self):
        mode = customtkinter.get_appearance_mode()
        fg = customtkinter.ThemeManager.theme["CTkFrame"]["fg_color"]
        return fg[1] if mode == "Dark" else fg[0]

    def _compute_fit_zoom(self, avail_w_px=None, avail_h_px=None):
        if not self.original_images:
            return 1.0
        scaling = self._get_scaling()
        cell_w = max(img.width for img in self.original_images)
        cell_h = max(img.height for img in self.original_images)
        num_rows = (len(self.original_images) + self.num_columns - 1) // self.num_columns

        if avail_w_px is None or avail_h_px is None:
            screen_w = self.winfo_screenwidth()
            screen_h = self.winfo_screenheight() - custom_utils.get_taskbar_size()
            avail_w_px = screen_w * 0.88 - 30
            avail_h_px = screen_h * 0.85 - 90

        pad_px = 2 * self.cell_pad * scaling
        fit_w = (avail_w_px / self.num_columns - pad_px) / max(1.0, cell_w * scaling)
        fit_h = (avail_h_px / max(1, num_rows) - pad_px) / max(1.0, cell_h * scaling)
        return max(self.min_zoom, min(1.0, fit_w, fit_h))

    def create_widgets(self):
        toolbar = customtkinter.CTkFrame(self, fg_color="transparent")
        toolbar.grid(row=0, column=0, columnspan=2, sticky="ew", padx=8, pady=(6, 2))

        customtkinter.CTkLabel(toolbar, text="Zoom:").pack(side=tk.LEFT, padx=(0, 6))
        customtkinter.CTkButton(toolbar, text="-", width=32, command=self.zoom_out).pack(side=tk.LEFT, padx=2)
        self.zoom_label = customtkinter.CTkLabel(toolbar, text="100%", width=48)
        self.zoom_label.pack(side=tk.LEFT, padx=4)
        customtkinter.CTkButton(toolbar, text="+", width=32, command=self.zoom_in).pack(side=tk.LEFT, padx=2)
        customtkinter.CTkButton(toolbar, text="Fit", width=50, command=self.zoom_to_fit).pack(side=tk.LEFT, padx=(8, 2))
        customtkinter.CTkButton(toolbar, text="100%", width=55, command=lambda: self.set_zoom(1.0)).pack(side=tk.LEFT, padx=2)

        self.canvas = tk.Canvas(self, highlightthickness=0, bg=self._canvas_bg_color())
        v_scroll = customtkinter.CTkScrollbar(self, orientation="vertical", command=self.canvas.yview)
        h_scroll = customtkinter.CTkScrollbar(self, orientation="horizontal", command=self.canvas.xview)
        self.canvas.configure(yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)

        self.board_frame = customtkinter.CTkFrame(self.canvas, fg_color="transparent")
        self.board_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )
        self.canvas.create_window((0, 0), window=self.board_frame, anchor="nw")

        self.canvas.grid(row=1, column=0, sticky="nsew")
        v_scroll.grid(row=1, column=1, sticky="ns")
        h_scroll.grid(row=2, column=0, sticky="ew")

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        icons_list = match_icons.make_cell_list()
        for cv_img in icons_list:
            pil_img = Image.fromarray(cv2.cvtColor(cv_img, cv2.COLOR_RGB2BGR))
            self.original_images.append(pil_img)

        self.fit_zoom = self._compute_fit_zoom()
        self.zoom = self.fit_zoom
        self.zoom_label.configure(text=f"{int(round(self.zoom * 100))}%")

        row_index = 0
        col_index = 0
        for pil_img in self.original_images:
            scaled_size = (
                max(1, int(round(pil_img.width * self.zoom))),
                max(1, int(round(pil_img.height * self.zoom))),
            )
            tk_image = customtkinter.CTkImage(pil_img, size=scaled_size)
            self.image_widgets.append(tk_image)

            label = customtkinter.CTkLabel(self.board_frame, image=tk_image, text="", cursor="hand2")
            label.image = tk_image
            label.bind("<Button-1>", lambda event, custom_image=pil_img: self.on_image_click(custom_image))
            label.grid(row=row_index, column=col_index, padx=self.cell_pad, pady=self.cell_pad)
            self.cell_labels.append(label)

            col_index += 1
            if col_index >= self.num_columns:
                col_index = 0
                row_index += 1

        self.bind("<MouseWheel>", self._on_mousewheel)
        self.bind("<Shift-MouseWheel>", self._on_shift_mousewheel)
        self.bind("<Control-plus>", lambda e: self.zoom_in())
        self.bind("<Control-equal>", lambda e: self.zoom_in())
        self.bind("<Control-minus>", lambda e: self.zoom_out())

        self._configure_initial_geometry()

    def _configure_initial_geometry(self):
        self.update_idletasks()
        scaling = self._get_scaling()
        screen_w = self.winfo_screenwidth()
        screen_h = self.winfo_screenheight() - custom_utils.get_taskbar_size()

        req_w = self.board_frame.winfo_reqwidth() + 30
        req_h = self.board_frame.winfo_reqheight() + 70
        win_w = min(req_w, int(screen_w * 0.92))
        win_h = min(req_h, int(screen_h * 0.90))
        x = max(0, (screen_w - win_w) // 2)
        y = max(0, (screen_h - win_h) // 2)
        self.geometry(f"{int(win_w / scaling)}x{int(win_h / scaling)}+{x}+{y}")

    def _on_mousewheel(self, event):
        if event.state & 0x4:  # Control key held
            if event.delta > 0:
                self.zoom_in()
            elif event.delta < 0:
                self.zoom_out()
        else:
            self.canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def _on_shift_mousewheel(self, event):
        self.canvas.xview_scroll(int(-1 * (event.delta / 120)), "units")

    def zoom_in(self):
        self.set_zoom(self.zoom * 1.15)

    def zoom_out(self):
        self.set_zoom(self.zoom / 1.15)

    def zoom_to_fit(self):
        canvas_w = self.canvas.winfo_width()
        canvas_h = self.canvas.winfo_height()
        if canvas_w > 50 and canvas_h > 50:
            self.fit_zoom = self._compute_fit_zoom(canvas_w - 8, canvas_h - 8)
        else:
            self.fit_zoom = self._compute_fit_zoom()
        self.set_zoom(self.fit_zoom)

    def set_zoom(self, new_zoom):
        self.zoom = max(self.min_zoom, min(self.max_zoom, new_zoom))
        self.zoom_label.configure(text=f"{int(round(self.zoom * 100))}%")
        new_widgets = []
        for pil_img, label in zip(self.original_images, self.cell_labels):
            scaled_size = (
                max(1, int(round(pil_img.width * self.zoom))),
                max(1, int(round(pil_img.height * self.zoom))),
            )
            tk_image = customtkinter.CTkImage(pil_img, size=scaled_size)
            label.configure(image=tk_image)
            label.image = tk_image
            new_widgets.append(tk_image)
        self.image_widgets = new_widgets
        self.board_frame.update_idletasks()
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))
    
    def on_image_click(self, image):
        self.selected_image = image
        self.destroy()
        PokemonIconSelector(root=self.root, folder=self.folder)

class PokemonIconSelector(tk.Toplevel):
     
    def __init__(self, master = None, root = None, action = None, folder = None):
         
        super().__init__(master = master)
        self.title("Select The Pokemon That the New Icon will be Saved")
        self.root = root
        self.action = action
        self.folder=folder
        self.selected_image = None
        self.create_widgets()

    def create_widgets(self):
        num_columns = 6
        row_index = 0
        col_index = 0

        self.state('zoomed')

        # Create a Canvas and a Scrollbar
        canvas = tk.Canvas(self)
        scrollbar = customtkinter.CTkScrollbar(self, command=canvas.yview)
        
        # Create a frame inside the canvas that will contain the images
        scrollable_frame = tk.Frame(canvas)

        # Bind the scrollbar to the canvas
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        # Add the scrollable frame inside the canvas
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")

        # Configure the canvas to use the scrollbar
        canvas.configure(yscrollcommand=scrollbar.set)

        # Add the scrollbar and canvas to the grid
        canvas.grid(row=0, column=0, sticky="nsew")
        scrollbar.grid(row=0, column=1, sticky="ns")

        # Ensure that the canvas expands to fill the available space
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Add the images to the scrollable frame
        widgets_list = self.root.get_selected_images_widgets_list()
        for widgets in widgets_list:
            if self.folder == "barrier":
                image_cv2 = custom_utils.open_cv2_image(custom_utils.verify_or_update_png_path(Path(constants.IMAGES_PATH, widgets[0].cget("text"))).as_posix())
                image_cv2 = custom_utils.add_transparent_image(image_cv2)
                image = Image.fromarray(cv2.cvtColor(image_cv2, cv2.COLOR_RGB2BGR))
            else:
                image = Image.open(custom_utils.verify_or_update_png_path(Path(constants.IMAGES_PATH, widgets[0].cget("text"))))
            tk_image = customtkinter.CTkImage(image, size=image.size)

            label = customtkinter.CTkLabel(scrollable_frame, image=tk_image, text="", cursor="hand2")
            label.image = tk_image  # Keep a reference to avoid garbage collection
            label.bind("<Button-1>", lambda event, image_name=widgets[0].cget("text"): self.on_image_click(image_name))
            label.grid(row=row_index, column=col_index, padx=10, pady=10)

            col_index += 1
            if col_index >= num_columns:
                col_index = 0
                row_index += 1
    
    def on_image_click(self, image_name):
        self.selected_image_name = image_name
        if self.action == "Remove_Barrier":
            ExtraIconSelector(root=self.root, selected_image = image_name, action=self.action)
        elif self.action == "Remove_Extra":
            ExtraIconSelector(root=self.root, selected_image = image_name, action=self.action)
        else:
            save_new_icon(self.root.board_image_selector.selected_image, image_name, self.root.board_image_selector.folder)
            self.root.clear_icons_cache()
        self.root.reveal_or_hide_barrier_img()
        self.destroy()


class ExtraIconSelector(tk.Toplevel):
     
    def __init__(self, master = None, root = None, selected_image = None, action = None):
         
        super().__init__(master = master)
        self.title("Select The Extra Icon that you want to remove")
        self.root = root
        self.action = action
        self.selected_image = selected_image
        self.create_widgets()
        
    def create_widgets(self):
        num_columns = 6
        row_index = 0
        col_index = 0

        if self.action == "Remove_Extra":
            images_path = src.file_utils.find_matching_files(constants.IMAGES_EXTRA_PATH, Path(self.selected_image).stem, ".png")
        else:
            images_path = src.file_utils.find_matching_files(constants.IMAGES_BARRIER_PATH, Path(self.selected_image).stem, ".png")

        for image_path in images_path:
            image_path = Path(image_path)
            image = Image.open(Path(image_path))
            tk_image = customtkinter.CTkImage(image, size=image.size)

            label = customtkinter.CTkLabel(self, image=tk_image, text="", cursor="hand2")
            label.image = tk_image  # Keep a reference to avoid garbage collection
            label.bind("<Button-1>", lambda event, image_path=image_path: self.on_image_click(image_path))
            label.grid(row=row_index, column=col_index, padx=10, pady=10)

            col_index += 1
            if col_index >= num_columns:
                col_index = 0
                row_index += 1

    def on_image_click(self, image_path):
        self.image_path = image_path
        remove_icon(image_path)
        self.root.reveal_or_hide_barrier_img()
        self.root.clear_icons_cache()
        self.destroy()

def remove_icon(image_path):
    if os.path.exists(image_path):
        os.remove(image_path)
        log.info(f"Eliminado o Arquivo: {image_path}")

def save_new_icon(image, image_name, folder):
    if folder == "barrier":
        os.makedirs(constants.IMAGES_BARRIER_PATH, exist_ok=True)
        image_path = custom_utils.verify_or_update_png_path(Path(constants.IMAGES_BARRIER_PATH, image_name))
        image_path = custom_utils.get_next_filename(image_path)
    else:
        os.makedirs(constants.IMAGES_EXTRA_PATH, exist_ok=True)
        image_path = custom_utils.verify_or_update_png_path(Path(constants.IMAGES_EXTRA_PATH, image_name))
        image_path = custom_utils.get_next_filename(image_path)
    image = image.resize(constants.downscale_res)
    image_path = custom_utils.verify_or_update_png_path(image_path)
    image.save(image_path)
