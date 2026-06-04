import dearpygui.dearpygui as dpg

dpg.create_context()

with dpg.window(label="Viewport"):
    dpg.add_text("Test")

dpg.create_viewport(title="Project Kobon", width=600, height=600)

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()

dpg.destroy_context()