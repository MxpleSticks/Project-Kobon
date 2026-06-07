import dearpygui.dearpygui as dpg
from pathlib import Path

ICON_PATH = Path(__file__).resolve().parents[1] / "Kobon.ico"

dpg.create_context()

with dpg.window(label="Instructions (usage guide)", modal=True, show=True, tag="popup", width=600, height=400, pos=[100, 100], no_resize=True, no_move=True):
    

    with dpg.child_window(height=-40, border=False):
        dpg.add_text(
            "Welcome to Project Kobon's output viewer! \n \n"
            
            "Import the file your Discord Webhook outputed into the imports field (left side) to \n"
            "to view it."
        )
    
    dpg.add_separator()
    
    dpg.add_button(
        label="Close", 
        width=-1, 
        callback=lambda: dpg.configure_item("popup", show=False)
    )


with dpg.window(label="Viewport", no_close=True, tag="Primary Window"):
    dpg.add_text("Test")

dpg.create_viewport(title="Project Kobon", width=800, height=600, small_icon=str(ICON_PATH), large_icon=str(ICON_PATH))

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Primary Window", True)
dpg.start_dearpygui()
dpg.destroy_context()