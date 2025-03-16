# Surveillance Video Analysis and Summarizing

## Overview

This project focuses on analyzing surveillance videos to extract meaningful information and summarize key events. By processing video feeds, the system identifies significant activities, aiding in efficient monitoring and review.

## Features

- **Backend Processing**: Analyzes video frames to detect and summarize notable events.
- **Graphical User Interface (GUI)**: Built with PyQt6 to provide a user-friendly interface for uploading videos and viewing summaries.

## Installation

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/muhammedfayiz122/Surveillance-video-analysis-and-Summarizing.git
   ```

2. **Navigate to the Project Directory**:

   ```bash
   cd Surveillance-video-analysis-and-Summarizing
   ```

3. **Install Dependencies**:

   Ensure you have Python installed. Install the required packages using:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. **Backend Processing**:

   Run the `backnd.py` script to analyze the video:

   ```bash
   python backnd.py input_video.mp4
   ```

2. **Graphical User Interface**:

   Launch the `front.py` script to start the PyQt6-based GUI:

   ```bash
   python front.py
   ```

   Use the interface to upload videos and view summarized results.

## Directory Structure

```
Surveillance-video-analysis-and-Summarizing/
├── backnd.py                # Backend processing script for video analysis
├── front.py                 # PyQt6-based GUI script
├── requirements.txt         # List of required Python packages
└── README.md                # Project documentation
```

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any enhancements or bug fixes.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

## Acknowledgements

Special thanks to the open-source community for providing tools and libraries that made this project possible.
