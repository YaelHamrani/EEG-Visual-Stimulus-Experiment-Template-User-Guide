# EEG-Visual-Stimulus-Experiment-Template-User-Guide
This project provides a ready-to-use template for an EEG experiment involving visual stimuli. In each trial, the participant is presented with two doors and is asked to choose one. Feedback is then provided in the form of points. The experiment is fully customizable and supports integration with real-time EEG data via OpenViBE.


________________________________________
## Requirements
Software Installation
1.	OpenViBE 3.6.0 

  	OpenViBE is an open-source software platform for designing and running Brain-Computer Interface (BCI) experiments. It enables real-time access to a wide range of EEG acquisition devices.

  	Download from: https://openvibe.inria.fr/

  	Supported EEG hardware: https://openvibe.inria.fr/supported-hardware/

2.	Python 3.10.11

  	The experiment script is developed and tested using Python 3.10.11. Other Python 3.10+ versions may also be compatible.
________________________________________
## Project Structure and Customization

This project allows for flexible design and visual customization. It includes:

•	Visual Stimuli (Images Folder) -
Two doors are displayed during each trial. You can replace the images located in the Images folder with any other images you'd like to use.

•	Design File (Design Folder -Trial Logic & Timing) -
The experiment logic (image order, timing, feedback, etc.) is controlled via a .csv design file stored in the Design folder. You can easily create or edit this file to fit your specific experiment layout.

   Design File's Columns include:

   o	name – The filename of the image to display (e.g., door1.png). This image must exist in the Images folder defined in the code.

   o	duration – The duration (in seconds) the image should be displayed if wait_for_key is set to False. This value is ignored when wait_for_key is True.

   o	wait_for_key – A boolean value (True / False) that determines how long the image stays on screen:

     •	If True, the image will remain visible until the participant presses the spacebar.

     •	If False, the image will remain on screen for the number of seconds specified in the duration column.

________________________________________
## OpenViBE Interface

Before using OpenViBE, ensure that your EEG device is connected to your PC as you would for any standard recording session. However, instead of launching the device’s proprietary software, you can now use OpenViBE to read and stream the EEG data.

OpenViBE consists of two main applications that work together to configure and run EEG-based experiments:

### 1. OpenViBE Acquisition Server (64-bit)

   This application is responsible for connecting to the EEG device and controlling its configuration.
   
   Here you can:

   •	Select the device type (e.g., BrainAmp, Emotiv, etc.)

   •	Choose which channels to record

   •	Set the sampling rate

   •	Start and stop the EEG signal acquisition
 
  Tip: You should launch the Acquisition Server first, before running the experiment in Designer.
![image](https://github.com/user-attachments/assets/2ee50ad7-3735-490e-9f04-b8c36c77fa95)




Fig 1: OpenViBE Acquisition Server: Choosing Driver from supported devices, Driver Properties: number of channels and sampling rate.  Than press connect and play to transmit signal from device.
________________________________________
### 2. OpenViBE Designer (64-bit)
    
    This is the main application where you:

    •	Load and run OpenViBE scenarios (graphical workflows) - attached is the test.xml file

    •	Stream EEG data in real-time
    
    •	Process signals, apply filters, and send event markers (stimulations)
    
    •	Interact with external Python scripts or GUIs (like the door experiment)
 
    The Designer is where you run the actual logic of your experiment and manage communication with other components using tools like Lab Streaming Layer (LSL).
![image](https://github.com/user-attachments/assets/4335012a-053d-4c82-a589-ffab7c130771)



Fig 2: Designer's Experiment Scenario 

1.	Acquisition Client Box (in OpenViBE Designer)-

The Acquisition Client Box is a core component used within OpenViBE Designer scenarios. It acts as a bridge between the Acquisition Server and the experiment logic running in Designer.

•	It receives the EEG signal from the connected Acquisition Server (which is reading from your EEG device).

•	It streams the data into the scenario, allowing you to process the EEG in real time.

•	You can apply filters, extract features, or route the signal to external scripts (e.g., via Lab Streaming Layer or Python processing).

2.	Channel Rename Box (in OpenViBE Designer)

The Channel Rename box is used to assign meaningful, human-readable names to the EEG channels being streamed into your scenario.

•	By default, EEG devices often label channels numerically (e.g., Ch1, Ch2, Ch3, ...).

•	The Channel Rename box allows you to replace those default labels with standard EEG names (e.g., Fz, Cz, Pz, Oz, etc.).

•	This is especially helpful when:

    o	Applying spatial filters or montages

    o	Visualizing data using known electrode positions
    
    o	Performing offline analysis with consistent channel labels
 
 You can manually input the desired channel names in the box configuration, matching the number of channels in your signal.

________________________________________
### Running the Experiment

For easy setup and run please check out this video manual https://youtu.be/gEdyHdbDCOE

Also a bit of information of the design of the task presented in this git:

The Doors Task is a simple reward-processing paradigm where participants choose between two doors, leading to positive (reward) or negative (loss) outcomes.

Although the choice is random, this task reliably elicits neural responses associated with reward anticipation and outcome evaluation.

The ventral striatum (VS) — a core region of the brain's reward circuitry — shows increased activation during both:

•	Anticipation of possible rewards

•	Receipt of rewarding outcomes.

You can read more about the task:

•	Proudfit, G.H. (2015), The reward positivity: From basic research on reward to a biomarker for depression. Psychophysiol, 52: 449-459. https://doi.org/10.1111/psyp.12370

•	Jocham G, Klein TA, Ullsperger M. Dopamine-mediated reinforcement learning signals in the striatum and ventromedial prefrontal cortex underlie value-based choices. J Neurosci. 2011 Feb 2;31(5):1606-13. doi: 
10.1523/JNEUROSCI.3904-10.2011. PMID: 21289169; PMCID: PMC6623749.

•	Bowyer C, Brush CJ, Threadgill H, Harmon-Jones E, Treadway M, Patrick CJ, Hajcak G. The effort-doors task: Examining the temporal dynamics of effort-based reward processing using ERPs. Neuroimage. 2021 Mar;228:117656. doi: 10.1016/j.neuroimage.2020.117656. Epub 2021 Jan 4. PMID: 33359338.


![image](https://github.com/user-attachments/assets/3f88326b-1125-400f-be05-e8fcb3c17f1f)


Fig 3: Task Design 


