# Raspberry Pi Currency Authentication

## Project Overview

This project is a real-time embedded system for detecting counterfeit Indian banknotes using a Raspberry Pi 4 and UV-based fluorescent security-fiber analysis.

The system uses UV illumination to detect fluorescent security features present in genuine Indian currency notes. Image processing and computer vision techniques are used to analyze the captured image and authenticate the currency.

## Features

- Real-time Indian currency authentication
- UV-based fluorescent security-fiber detection
- Camera-based image acquisition
- Image processing using OpenCV
- ORB feature detection
- HSV-based image segmentation
- Template matching
- LCD display for authentication results
- Supports ₹100, ₹200 and ₹500 banknotes

## Hardware Requirements

- Raspberry Pi 4
- Pi Camera
- UV illumination source
- 16x2 I2C LCD display
- Jumper wires
- Power supply
- Currency notes for testing

## Software Requirements

- Python 3
- OpenCV
- NumPy
- Picamera2
- RPLCD
- SMBus2

## Project Structure

```text
Raspberry-Pi-Currency-Authentication/
│
├── src/
│   └── currency_authentication.py
│
├── Requirements.txt
│
└── README.md

Installation

Clone the repository:
git clone https://github.com/Nanditha-429/Raspberry-Pi-Currency-Authentication.git
Navigate to the project directory:
cd Raspberry-Pi-Currency-Authentication
Install the required Python libraries:
pip install -r Requirements.txt

How It Works:
The currency note is placed in front of the camera.
UV illumination is applied to the currency note.
The Pi Camera captures the image.
OpenCV processes the captured image.
Fluorescent security features are analyzed.
Image processing techniques are used for authentication.
The system determines whether the currency is genuine or potentially counterfeit.
The authentication result is displayed on the LCD.

Technologies Used:
Raspberry Pi 4
Python
OpenCV
Computer Vision
Picamera2
NumPy
RPLCD
I2C LCD
UV Fluorescence Analysis
Applications

This system can be used as a low-cost embedded solution for assisting with the authentication of Indian banknotes and demonstrating computer-vision-based counterfeit detection.

AUTHOR:

Nanditha Reddy

GitHub: https://github.com/Nanditha-429
