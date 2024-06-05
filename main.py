import tkinter as tk

import PresetControl 

class CameraController:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Camera Controller")

        self.presets = ["Preset 1", "Preset 2", "Preset 3", "Automatic"] # read these from text file

        self.camera1_preset = tk.StringVar()
        self.camera1_preset.set(self.presets[0])

        self.camera2_preset = tk.StringVar()
        self.camera2_preset.set(self.presets[0])

        self.camera1_label = tk.Label(self.window, text="Camera 1 Preset:")
        self.camera1_label.pack()

        self.camera1_dropdown = tk.OptionMenu(self.window, self.camera1_preset, *self.presets, command=self.change_camera1_preset)
        self.camera1_dropdown.pack()

        self.camera2_label = tk.Label(self.window, text="Camera 2 Preset:")
        self.camera2_label.pack()

        self.camera2_dropdown = tk.OptionMenu(self.window, self.camera2_preset, *self.presets, command=self.change_camera2_preset)
        self.camera2_dropdown.pack()

    def change_camera1_preset(self, preset):
        print(f"Camera 1 preset changing to {preset}")
        # Implement the logic to change the preset of camera 1
        try:
            PresetControl.change_preset("192.168.1.10", self.presets.index(preset))
        except ValueError as err:
            # should not update GUI
            for arg in err.args:
                print(arg)

    def change_camera2_preset(self, preset):
        print(f"Camera 2 preset changed to {preset}")
        # Implement the logic to change the preset of camera 2
        PresetControl.change_preset("192.168.1.9", self.presets.index(preset))


    def run(self):
        self.window.mainloop()

if __name__ == "__main__":
    controller = CameraController()
    controller.run()