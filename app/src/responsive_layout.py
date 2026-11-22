import tkinter as tk
import customtkinter


class ResponsiveFlowFrame(customtkinter.CTkFrame):
    """A CTkFrame that arranges child group frames left-to-right and wraps them onto new rows when width shrinks."""

    def __init__(self, master, row_spacing=4, **kwargs):
        kwargs.setdefault("fg_color", "transparent")
        kwargs.setdefault("height", 10)
        super().__init__(master, **kwargs)
        self._items = []  # list of (widget, padx, pady)
        self._row_spacing = row_spacing
        self._reflow_job = None
        self._verify_job = None
        self._last_avail_width = -1
        self._last_height_px = -1
        self._last_sizes = {}

        self.bind("<Configure>", self._schedule_reflow, add="+")
        self.bind("<Map>", self._schedule_reflow, add="+")

    def add_item(self, widget, padx=4, pady=2):
        self._items.append((widget, padx, pady))
        tk.Widget.bind(widget, "<Configure>", lambda e, w=widget: self._on_child_configure(w), add="+")

    def _on_child_configure(self, widget):
        if not widget.winfo_exists():
            return
        cur = (widget.winfo_reqwidth(), widget.winfo_reqheight())
        if cur != self._last_sizes.get(widget):
            self._schedule_reflow()

    def _schedule_reflow(self, event=None):
        if self._reflow_job is not None:
            try:
                self.after_cancel(self._reflow_job)
            except Exception:
                pass
        self._reflow_job = self.after_idle(self.reflow)

    def reflow(self, _pass=0):
        self._reflow_job = None
        if not self.winfo_exists():
            return
        avail_width = self.winfo_width()
        if avail_width <= 1:
            return

        self.update_idletasks()

        x = 0
        y = 0
        row_height = 0

        for widget, padx, pady in self._items:
            if not widget.winfo_exists():
                continue

            item_w = max(widget.winfo_reqwidth(), 1)
            item_h = max(widget.winfo_reqheight(), 1)
            self._last_sizes[widget] = (widget.winfo_reqwidth(), widget.winfo_reqheight())
            slot_w = item_w + 2 * padx
            slot_h = item_h + 2 * pady

            if x > 0 and x + slot_w > avail_width:
                x = 0
                y += row_height + self._row_spacing
                row_height = 0

            scaling = self._get_widget_scaling() if hasattr(self, "_get_widget_scaling") else 1.0
            w_scaling = widget._get_widget_scaling() if hasattr(widget, "_get_widget_scaling") else scaling
            widget.place(x=(x + padx) / w_scaling, y=(y + pady) / w_scaling)
            x += slot_w
            if slot_h > row_height:
                row_height = slot_h

        total_height_px = max(1, y + row_height)
        self._last_avail_width = avail_width

        if total_height_px != self._last_height_px:
            self._last_height_px = total_height_px
            scaling = self._get_widget_scaling() if hasattr(self, "_get_widget_scaling") else 1.0
            self.configure(height=max(1, int(round(total_height_px / scaling))))

        if _pass < 2:
            self.update_idletasks()
            for widget, _, _ in self._items:
                if widget.winfo_exists() and (widget.winfo_reqwidth(), widget.winfo_reqheight()) != self._last_sizes.get(widget):
                    self.reflow(_pass=_pass + 1)
                    return

        if self._verify_job is not None:
            try:
                self.after_cancel(self._verify_job)
            except Exception:
                pass
        self._verify_job = self.after(50, self._verify_sizes)

    def _verify_sizes(self):
        self._verify_job = None
        if not self.winfo_exists():
            return
        for widget, _, _ in self._items:
            if widget.winfo_exists() and (widget.winfo_reqwidth(), widget.winfo_reqheight()) != self._last_sizes.get(widget):
                self.reflow()
                return
