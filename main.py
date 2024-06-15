from multiprocessing import Manager, freeze_support
import tkinter as tk
import time

import PresetControl 
import RobotTracking

class CameraController:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Camera Controller")

        self.manager = Manager()
        self.nameSpace = self.manager.Namespace()

        self.presets = open("presets.txt").read().lower().splitlines()
        for i, line in enumerate(self.presets):
            self.presets[i] = line.split(":")[0]

        self.nameSpace.camera1_preset = self.presets[0]
        self.camera1_preset = tk.StringVar()
        self.camera1_preset.set(self.nameSpace.camera1_preset)
        self.camera1_currentPreset = tk.StringVar()
        self.camera1_currentPreset.set(self.nameSpace.camera1_preset)

        self.nameSpace.camera2_preset = self.presets[0]
        self.camera2_preset = tk.StringVar()
        self.camera2_preset.set(self.nameSpace.camera2_preset)
        self.camera2_currentPreset = tk.StringVar()
        self.camera2_currentPreset.set(self.nameSpace.camera2_preset)

        self.presetRows = len(self.presets)

        self.camera1_label = tk.Label(self.window, text="Camera 1 Preset:")
        self.camera1_label.grid(column=0, row=0, padx=10)

        for i, preset in enumerate(self.presets):
            tk.Radiobutton(self.window, text=preset, variable=self.camera1_preset, value=preset, name='camera1' + preset, command=self.change_camera1_preset, justify="left", anchor="w").grid(column=0, row=i+1, padx=10, pady=5, sticky = "w")

        tk.Label(self.window, name='camera1 status').grid(column=0, row=self.presetRows+2, padx=10, pady=5)

        self.camera2_label = tk.Label(self.window, text="Camera 2 Preset:")
        self.camera2_label.grid(column=1, row=0, padx=10)

        for i, preset in enumerate(self.presets):
            tk.Radiobutton(self.window, text=preset, variable=self.camera2_preset, value=preset, name='camera2' + preset, command=self.change_camera2_preset, justify="left", anchor="w").grid(column=1, row=i+1, padx=10, pady=5, sticky = "w")
        
        tk.Label(self.window, name='camera2 status').grid(column=1, row=self.presetRows+2, padx=10, pady=5)

        self.automatic_button = tk.Button(self.window, text="Manual", command=self.automatic_mode)
        self.automatic_button.grid(column=0, row=self.presetRows+3, columnspan=2, pady=10)

        self.change_camera1_preset()
        self.change_camera2_preset()

        self.window.protocol("WM_DELETE_WINDOW", self.stop)
            
    def change_camera1_preset(self):
        self.window.nametowidget('camera1 status').configure(text="Changing preset...")
        self.window.config(cursor="watch")
        self.window.update()
        preset = self.camera1_preset.get()
        print(preset)
        try:
            if preset in self.presets:
                PresetControl.change_preset("192.168.1.10", self.presets.index(preset))
            else:
                raise ValueError("Invalid preset")
        except ValueError as err:
            for arg in err.args:
                print(arg)
            self.window.nametowidget('camera1' + self.camera1_currentPreset.get()).select()
            self.window.nametowidget('camera1 status').configure(text="Error Error Error")
            self.window.config(cursor="")
            return
        
        self.window.nametowidget('camera1 status').configure(text="Preset changed to " + preset + " successfully" )
        self.window.config(cursor="")
        self.camera1_currentPreset.set(preset)

    def change_camera2_preset(self):
        self.window.nametowidget('camera2 status').configure(text="Changing preset...")
        self.window.config(cursor="watch")
        self.window.update()
        preset = self.camera2_preset.get()
        try:
            if preset in self.presets:
                PresetControl.change_preset("192.168.1.9", self.presets.index(preset))
            else:
                raise ValueError("Invalid preset")
        except ValueError as err:
            for arg in err.args:
                print(arg)
            self.window.nametowidget('camera2' + self.camera2_currentPreset.get()).select()
            self.window.nametowidget('camera2 status').configure(text="Error Error Error")
            self.window.config(cursor="")
            return
        
        self.window.nametowidget('camera2 status').configure(text="Preset changed to " + preset + " successfully" )
        self.window.config(cursor="")
        self.camera2_currentPreset.set(preset)

    def automatic_mode(self):
        if self.automatic_button.configure('relief')[-1] == 'sunken':
            self.automatic_button.configure(relief='raised', text='Manual')
            RobotTracking.stop()
            print("Automatic mode stopped")
        else:
            self.automatic_button.configure(relief='sunken', text='Automatic')
            RobotTracking.start(self.nameSpace)
            print("Automatic mode started")
            while self.automatic_button.configure('relief')[-1] == 'sunken':
                if self.camera1_currentPreset.get() != self.nameSpace.camera1_preset:
                    try:
                        self.camera1_preset.set(self.nameSpace.camera1_preset)
                        self.change_camera1_preset()
                    except:
                        pass
                if self.camera2_currentPreset.get() != self.nameSpace.camera2_preset:
                    try:
                        self.camera2_preset.set(self.nameSpace.camera2_preset)
                        self.change_camera2_preset()
                    except:
                        pass
                self.window.update()
                time.sleep(5) # needs to be set to a time appropriate for changing the camera preset

    def run(self):
        self.window.mainloop()

    def stop(self):
        if(self.automatic_button.configure('relief')[-1] == 'sunken'):
            RobotTracking.stop()
        self.manager.shutdown()
        self.window.destroy()

if __name__ == "__main__":
    freeze_support()
    controller = CameraController()
    controller.run()