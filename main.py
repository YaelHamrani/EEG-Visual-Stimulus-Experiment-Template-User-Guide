import numpy as np
import pandas as pd
import pygame
import os
import time
import tkinter as tk
from tkinter import filedialog
from datetime import datetime

# === GUI Input Form ===
def get_user_inputs():
    root = tk.Tk()
    root.title("Experiment Setup")
    inputs = {}

    tk.Label(root, text="Subject ID:").grid(row=0, column=0)
    tk.Label(root, text="Cycle No.:").grid(row=1, column=0)
    
    e_sub_id = tk.Entry(root)
    e_cycle = tk.Entry(root)
    
    e_sub_id.grid(row=0, column=1)
    e_cycle.grid(row=1, column=1)
    

    def browse_file():
        file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
        inputs["design_file"] = file_path
        lbl_file.config(text=os.path.basename(file_path))

    tk.Button(root, text="Select Design CSV", command=browse_file).grid(row=3, column=0)
    lbl_file = tk.Label(root, text="No file selected")
    lbl_file.grid(row=3, column=1)

    def submit():
        inputs["sub_id"] = e_sub_id.get()
        inputs["cycle_no"] = e_cycle.get()
        root.destroy()

    tk.Button(root, text="Start", command=submit).grid(row=4, column=0, columnspan=2)
    root.mainloop()
    return inputs


user_inputs = get_user_inputs()
SUB_ID = user_inputs["sub_id"]
CYCLE_NO = user_inputs["cycle_no"]
CSV_DESIGN_FILE = user_inputs["design_file"]
IMAGE_FOLDER = r'C:\Users\fmri\Desktop\Doors Experiment\Images' #change to your path
output_path = r'C:\Users\fmri\Desktop\Doors Experiment\Data'    #change to your path
OUTPUT_LOG_FILE = output_path + f'\{SUB_ID}_C{CYCLE_NO}.csv'
OUTPUT_INFO_FILE = output_path + f'\{SUB_ID}_C{CYCLE_NO}_info.txt'


# === OpenViBE Box Class ===
class MyOVBox(OVBox):
    def __init__(self):
        OVBox.__init__(self)
        self.running = True
        self.design = pd.read_csv(CSV_DESIGN_FILE)
        self.image_index = 0
        self.image_start_time = None
        self.waiting_for_space = False
        self.current_row = None
        self.sampling_rate = None

    def initialize(self):
        pygame.init()

        # Get display info
        infoObject = pygame.display.Info()
        screen_width = infoObject.current_w
        screen_height = infoObject.current_h

        # Use borderless window instead of fullscreen
        self.screen = pygame.display.set_mode((screen_width, screen_height), pygame.NOFRAME)

        pygame.display.set_caption("OpenViBE Image Display")
        pygame.mouse.set_visible(False)
        self.clock = pygame.time.Clock()

    def uninitialize(self):
        pygame.quit()
        with open(OUTPUT_INFO_FILE, 'w') as f:
            f.write(f"Subject ID: {SUB_ID}\n")
            f.write(f"Cycle No: {CYCLE_NO}\n")
            f.write(f"Sampling Rate: {self.sampling_rate}\n")
            f.write("Design:\n")
            f.write(self.design.to_csv(index=False))
        # self.output[1].append(OVStimulationEnd())

    def show_next_image(self):
        if self.image_index >= len(self.design):
            self.running = False
            return

        row = self.design.iloc[self.image_index]
        self.current_row = row
        image_path = os.path.join(IMAGE_FOLDER, row['name'])
        duration = float(row['duration'])
        wait_for_key = row.get('wait_for_key', False) in [True, 'True', 'true', 1]

        if not os.path.exists(image_path):
            print(f"Missing image: {image_path}")
            self.image_index += 1
            return

        img = pygame.image.load(image_path)
        img = pygame.transform.scale(img, self.screen.get_size())
        self.screen.blit(img, (0, 0))
        pygame.display.flip()

        stim_id = int(33024 + abs(hash(row['name'])) % 1000)
        stim_time = self.getCurrentTime()
        stim = OVStimulation(stim_id, stim_time, 0.1)
        stim_set = OVStimulationSet(stim_time, stim_time + 0.1)
        stim_set.append(stim)
        self.output[1].append(stim_set)

        self.image_start_time = stim_time
        self.waiting_for_space = wait_for_key

    def send_key_stimulation(self, key_number):
        stim_time = self.getCurrentTime()
        stim_id = 33030 + key_number  # Example: 33031 for key "1", 33032 for key "2"
        stim = OVStimulation(stim_id, stim_time, 0.1)
        stim_set = OVStimulationSet(stim_time, stim_time + 0.1)
        stim_set.append(stim)
        self.output[1].append(stim_set)
        print(f"Sent stimulation for key: {key_number}")

    def process(self):
        for chunkIdx in range(len(self.input[0])):
            chunk = self.input[0].pop()
            if isinstance(chunk, OVSignalHeader):
                self.sampling_rate = chunk.samplingRate
                self.output[0].append(chunk)
            elif isinstance(chunk, OVSignalBuffer):
                self.output[0].append(chunk)
            elif isinstance(chunk, OVSignalEnd):
                self.output[0].append(chunk)

        now = self.getCurrentTime()

        # Show first image if needed
        if self.image_index == 0 and self.image_start_time is None:
            self.show_next_image()
    
        # Always check keyboard events globally
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.image_index += 1
                    self.send_key_stimulation(0)  # Custom stim for space
                    self.show_next_image()
                elif event.key == pygame.K_q:
                    self.running = False
                elif event.key == pygame.K_1:
                    self.send_key_stimulation(1)
                elif event.key == pygame.K_2:
                    self.send_key_stimulation(2)

        # Check for time-based image change (only if not waiting for space)
        if not self.waiting_for_space and self.image_start_time is not None:
            duration = float(self.current_row['duration'])
            if now - self.image_start_time >= duration:
                self.image_index += 1
                self.show_next_image()


box = MyOVBox()
