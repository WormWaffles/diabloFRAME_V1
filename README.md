# DiabloFRAME_V1

The Photo and Video Slideshow Program is a Python application designed to create dynamic slideshows by displaying images and videos in a customizable sequence. It includes features such as Ken Burns effect for images and transitions between media. This program can be used for various purposes, including digital signage or home entertainment.

## Table of Contents
- [Introduction](#DiabloFRAME_V1)
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)

## Features
- Display images and videos in a specified folder.
- Customize image transitions and display duration.
- Apply Ken Burns effect to images.
- Seamless transitions between images and videos.
- Support for various image and video formats.

## Prerequisites
Before running the Photo and Video Slideshow Program, make sure you have the following installed:
- Python (version 3.6 or higher)
- OpenCV (cv2)
- NumPy
- glob (usually included with Python)

## Installation
1. Clone or download the repository to your local machine.

   ```shell
   git clone https://github.com/WormWaffles/DiabloFRAME_V1
   ```
2. Navigate to the project directory.
  ```shell
  cd diabloFRAME_V1
  ```

## Usage
1. Customize the program settings in the script, including:
- Image hold time (delay)
- Path to the main folder (path)
- Whether home videos play on the hour (home_vid)
2. Run the program using Python.
  ```shell
  python main.py
  ```
3. The program will display a slideshow of images and videos based on your settings. Use 'q' to quit the program.
