import dearpygui.dearpygui as dpg
from pathlib import Path

ICON_PATH = Path(__file__).resolve().parents[1] / "Kobon.ico"

dpg.create_context()

with dpg.window(label="Viewport"):
    dpg.add_text("Test")

dpg.create_viewport(title="Project Kobon", width=600, height=600, small_icon=str(ICON_PATH), large_icon=str(ICON_PATH))

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()

dpg.destroy_context()