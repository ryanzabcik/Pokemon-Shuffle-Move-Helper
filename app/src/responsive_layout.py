import tkinter as tk
import customtkinter


class ResponsiveFlowFrame(customtkinter.CTkFrame):
    """A CTkFrame that arranges child items left-to-right and wraps them onto new rows when width shrinks."""

    def __init__(self, master, row_spacing=2, **kwargs):
        kwargs.setdefault("fg_color", "transparent")
        kwargs.setdefault("height", 10)
        super().__init__(master, **kwargs)
        self._items = []  # list of (widget, padx, pady)
        self._row_spacing = row_spacing
        self._reflow_job = None
        self._last_avail_width = -1
        self._last_height_px = -1
        self._on_height_change = None

        self.bind("<Configure>", self._schedule_reflow, add="+")
        self.bind("<Map>", self._schedule_reflow, add="+")

    def add_item(self, widget, padx=2, pady=2):
        self._items.append((widget, padx, pady))
        if isinstance(widget, ResponsiveFlowFrame):
            widget._on_height_change = self._schedule_reflow
        elif hasattr(widget, "_flow_child") and isinstance(widget._flow_child, ResponsiveFlowFrame):
            widget._flow_child._on_height_change = self._schedule_reflow

    def natural_width(self):
        total = 0
        for widget, padx, _ in self._items:
            w = self._item_natural_width(widget)
            total += w + 2 * padx
        return max(total, 1)

    @staticmethod
    def _item_natural_width(widget):
        if isinstance(widget, ResponsiveFlowFrame):
            return widget.natural_width()
        if hasattr(widget, "_flow_child") and isinstance(widget._flow_child, ResponsiveFlowFrame):
            return max(widget._flow_child.natural_width(), widget.winfo_reqwidth())
        return max(widget.winfo_reqwidth(), 1)

    def _schedule_reflow(self, event=None):
        if self._reflow_job is not None:
            try:
                self.after_cancel(self._reflow_job)
            except Exception:
                pass
        self._reflow_job = self.after_idle(self.reflow)

    def reflow(self):
        self._reflow_job = None
        if not self.winfo_exists():
            return
        avail_width = self.winfo_width()
        if avail_width <= 1:
            return

        x = 0
        y = 0
        row_height = 0

        for widget, padx, pady in self._items:
            if not widget.winfo_exists():
                continue

            item_nat_w = self._item_natural_width(widget)
            is_flow_container = isinstance(widget, ResponsiveFlowFrame) or (
                hasattr(widget, "_flow_child") and isinstance(widget._flow_child, ResponsiveFlowFrame)
            )
            max_inner_w = max(1, avail_width - 2 * padx)
            placed_w = min(item_nat_w, max_inner_w) if is_flow_container else item_nat_w
            slot_w = placed_w + 2 * padx

            if x > 0 and x + slot_w > avail_width:
                x = 0
                y += row_height + self._row_spacing
                row_height = 0

            if is_flow_container:
                w_scaling = widget._get_widget_scaling() if hasattr(widget, "_get_widget_scaling") else 1.0
                widget.configure(width=max(1, int(round(placed_w / w_scaling))))
                widget.place(x=x + padx, y=y + pady)
                if hasattr(widget, "_flow_child") and isinstance(widget._flow_child, ResponsiveFlowFrame):
                    widget._flow_child.update_idletasks()
                    widget._flow_child.reflow()
                elif isinstance(widget, ResponsiveFlowFrame):
                    widget.update_idletasks()
                    widget.reflow()
            else:
                widget.place(x=x + padx, y=y + pady)

            widget.update_idletasks()
            item_h = widget.winfo_reqheight()
            slot_h = item_h + 2 * pady

            x += slot_w
            if slot_h > row_height:
                row_height = slot_h

        total_height_px = max(1, y + row_height)
        self._last_avail_width = avail_width

        if total_height_px != self._last_height_px:
            self._last_height_px = total_height_px
            scaling = self._get_widget_scaling() if hasattr(self, "_get_widget_scaling") else 1.0
            self.configure(height=max(1, int(round(total_height_px / scaling))))
            if self._on_height_change is not None:
                self._on_height_change()
