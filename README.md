# Hand Gesture Controlled Scrolling

This project allows you to control the scrolling of windows or web pages on your computer using hand gestures. By using a webcam, the system detects hand movements, including the number of fingers raised and the direction of movement. It translates these gestures into scrolling actions for smooth and interactive control. The system allows users to scroll up or down based on finger gestures, and it halts scrolling when no fingers or a closed fist is detected.

## Features:
- **Hand Gesture Recognition**: Detects open hand, closed fist, and the number of fingers raised.
- **Scroll Control**: Users can scroll up or down based on their finger movements.
- **Stop Scroll**: When no fingers are detected or a closed fist is shown, the scrolling stops.
- **Smooth Detection**: Provides smooth scrolling control with minimal delay, providing a natural user experience.

## Technologies Used:
- **Python**: The main programming language used to implement the system.
- **OpenCV**: OpenCV is used for computer vision tasks, particularly for capturing the webcam feed and detecting hand gestures.
- **Numpy**: Used for performing efficient mathematical operations.

## Installation:
## Installation:

### 1. Download the project:
   - Download the project files as a ZIP archive from the GitHub repository.
   - Extract the files to a folder on your computer.

### 2. Install Python and Dependencies:
   Ensure that Python is installed on your system. You can download Python from the [official website](https://www.python.org/downloads/).

### 3. Install Required Libraries:
   Once Python is installed, open a terminal (or Command Prompt) and install the required libraries using `pip`:

   ```bash
   pip install opencv-python numpy 
