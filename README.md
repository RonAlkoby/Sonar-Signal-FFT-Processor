
# Sonar Signal FFT Processor

## Overview
The **Sonar Signal FFT Processor** is a Python-based GUI application for analyzing sonar audio signals. It allows users to process `.wav` files and extract key information such as peak frequency, amplitude, and time-frequency analysis. The application supports two modes of analysis: *Active* and *Passive*.

## Features
- **Load and Process `.wav` Files**: Upload any `.wav` file for analysis.
- **FFT Analysis**: Perform a Fast Fourier Transform to identify peak frequencies and amplitudes.
- **Mode Selection**:
  - *Active Mode*: Focuses on a 500 Hz bandwidth around the peak frequency.
  - *Passive Mode*: Displays the 200-1200 Hz frequency range.
- **Time-Frequency Analysis**: Visualize the signal as a spectrogram.
- **Interactive Cursor**: Move the mouse over the FFT graph to display frequency and amplitude values.
- **Reset Functionality**: Clear all analysis data and reload the interface for a new file.

## Prerequisites
Make sure you have the following installed:
- Python 3.8 or higher
- Required Python libraries:
  - `numpy`
  - `scipy`
  - `matplotlib`
  - `tkinter`

To install the required libraries, run:
```bash
pip install numpy scipy matplotlib
```

## How to Run
1. Clone or download the repository.
2. Open a terminal in the project directory.
3. Run the application using:
   ```bash
   python sonar_fft_processor.py
   ```

## Usage Instructions
1. **Select Analysis Mode**:
   - Choose either *Active Analysis* or *Passive Analysis* from the main interface.
2. **Load a File**:
   - Click the `Open Audio File` button to upload a `.wav` file.
3. **View Results**:
   - The application will display:
     - FFT graph with peak frequency and amplitude.
     - Zoomed analysis based on the selected mode.
     - A spectrogram for time-frequency analysis.
4. **Interactive Cursor**:
   - Hover over the FFT graph to view the frequency and amplitude at any point.
5. **Reset**:
   - Click the `Reset` button to clear the interface and prepare for a new analysis.
6. **Exit**:
   - Click the `Exit` button to close the application.

## Project Structure
- `sonar_fft_processor.py`: Main application script.
- `README.md`: Documentation for the project.

## Future Improvements
- Support for additional audio formats (e.g., `.mp3`).
- Enhanced analysis options, such as harmonic detection.
- Improved UI responsiveness and design.

## License
This project is open-source and available under the MIT License.

![PIC2](https://github.com/user-attachments/assets/865820a8-96f1-4e3b-84cc-51c75716f3bf)
![PIC1](https://github.com/user-attachments/assets/9b985f41-3473-4f3c-b161-f36b9cf0cf7e)



