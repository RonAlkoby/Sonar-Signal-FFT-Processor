import tkinter as tk
from tkinter import filedialog
import numpy as np
from scipy.io import wavfile
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

global analysis_mode
analysis_mode = None

def open_file():
    global analysis_mode
    if analysis_mode is None:
        analysis_label.config(text="Please select an analysis mode first.")
        return

    file_path = filedialog.askopenfilename(
        filetypes=[("WAV files", "*.wav"), ("All files", "*.*")]
    )
    if not file_path:
        return
    try:
        create_analysis_frames()
        process_file(file_path)
        reset_button.grid(row=1, column=0, padx=10, pady=5)
    except Exception as e:
        analysis_label.config(text=f"Error: {e}")

def create_analysis_frames():
    global analysis_frame, analysis_label, cursor_label, plot_frame, zoom_frame, time_frequency_frame, fig, canvas, zoom_fig, zoom_canvas, tf_fig, tf_canvas

    analysis_frame = tk.Frame(root, bg="#ADD8E6")
    analysis_frame.pack(pady=10)
    analysis_label = tk.Label(analysis_frame, text="No Analysis Yet", font=("Helvetica", 12), fg="black", bg="#ADD8E6")
    analysis_label.pack()

    cursor_label = tk.Label(root, text="", font=("Helvetica", 12), fg="black", bg="#ADD8E6")
    cursor_label.pack(pady=5)

    plot_frame = tk.Frame(root, bg="#ADD8E6")
    plot_frame.pack(pady=10, fill=tk.BOTH, expand=True)
    fig = plt.Figure(figsize=(6, 4), dpi=100)
    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas_widget = canvas.get_tk_widget()
    canvas_widget.pack(fill=tk.BOTH, expand=True)

    zoom_frame = tk.Frame(root, bg="#ADD8E6")
    zoom_frame.pack(pady=10, fill=tk.BOTH, expand=True)
    zoom_fig = plt.Figure(figsize=(6, 4), dpi=100)
    zoom_canvas = FigureCanvasTkAgg(zoom_fig, master=zoom_frame)
    zoom_canvas_widget = zoom_canvas.get_tk_widget()
    zoom_canvas_widget.pack(fill=tk.BOTH, expand=True)

    time_frequency_frame = tk.Frame(root, bg="#ADD8E6")
    time_frequency_frame.pack(pady=10, fill=tk.BOTH, expand=True)
    tf_fig = plt.Figure(figsize=(6, 4), dpi=100)
    tf_canvas = FigureCanvasTkAgg(tf_fig, master=time_frequency_frame)
    tf_canvas_widget = tf_canvas.get_tk_widget()
    tf_canvas_widget.pack(fill=tk.BOTH, expand=True)

def process_file(file_path):
    global analysis_mode

    samplerate, data = wavfile.read(file_path)
    if len(data.shape) > 1:
        data = data[:, 0]

    n = len(data)
    freq = np.fft.rfftfreq(n, d=1/samplerate)
    fft_data = np.abs(np.fft.rfft(data))

    fft_data_db = 20 * np.log10(fft_data + 1e-10)

    peak_index = np.argmax(fft_data)
    peak_frequency = freq[peak_index]
    peak_amplitude_db = fft_data_db[peak_index]

    analysis_label.config(
        text=(
            f"Peak Frequency: {peak_frequency:.2f} Hz\n"
            f"Peak Amplitude: {peak_amplitude_db:.2f} dB"
        )
    )

    fig.clear()
    ax = fig.add_subplot(111)
    ax.plot(freq, fft_data, color='blue')
    ax.set_title("FFT of Audio File", color='black')
    ax.set_xlabel("Frequency (Hz)", color='black')
    ax.set_ylabel("Amplitude", color='black')
    ax.grid()
    ax.tick_params(colors='black')

    def on_move(event):
        if event.xdata and event.ydata:
            cursor_label.config(
                text=f"Frequency: {event.xdata:.2f} Hz, Amplitude: {event.ydata:.2f}"
            )

    canvas.mpl_connect("motion_notify_event", on_move)
    canvas.draw()

    zoom_fig.clear()
    zoom_ax = zoom_fig.add_subplot(111)
    if analysis_mode == "Active":
        max_amplitude_index = np.argmax(fft_data)
        zoom_start = max(0, max_amplitude_index - 250)
        zoom_end = min(len(freq), max_amplitude_index + 250)
        zoom_ax.plot(freq[zoom_start:zoom_end], fft_data[zoom_start:zoom_end], color='red')
        zoom_ax.set_title("Zoomed FFT - Active", color='black')
    elif analysis_mode == "Passive":
        passive_start = np.searchsorted(freq, 200)
        passive_end = np.searchsorted(freq, 1200)
        zoom_ax.plot(freq[passive_start:passive_end], fft_data[passive_start:passive_end], color='green')
        zoom_ax.set_title("Passive Analysis (200-1200 Hz)", color='black')

    zoom_ax.set_xlabel("Frequency (Hz)", color='black')
    zoom_ax.set_ylabel("Amplitude", color='black')
    zoom_ax.grid()
    zoom_ax.tick_params(colors='black')
    zoom_canvas.draw()

    tf_fig.clear()
    tf_ax = tf_fig.add_subplot(111)
    tf_ax.specgram(data, Fs=samplerate, cmap='viridis')
    tf_ax.set_title("Time-Frequency Analysis", color='black')
    tf_ax.set_xlabel("Time (s)", color='black')
    tf_ax.set_ylabel("Frequency (Hz)", color='black')
    tf_ax.tick_params(colors='black')
    tf_canvas.draw()

def reset_interface():
    global analysis_frame, cursor_label, plot_frame, zoom_frame, time_frequency_frame, analysis_mode
    analysis_mode = None
    analysis_frame.destroy()
    cursor_label.destroy()
    plot_frame.destroy()
    zoom_frame.destroy()
    time_frequency_frame.destroy()
    reset_button.grid_remove()

def set_analysis_mode(mode):
    global analysis_mode
    analysis_mode = mode
    analysis_label.config(text=f"Analysis mode set to {mode}")

root = tk.Tk()
root.title("Sonar Signal FFT Processor")
root.geometry("1000x800")
root.configure(bg="#ADD8E6")

label = tk.Label(root, text="Sonar Signal FFT Processor", font=("Helvetica", 16), fg="black", bg="#ADD8E6")
label.pack(pady=10)

buttons_frame = tk.Frame(root, bg="#ADD8E6")
buttons_frame.pack(pady=20)

active_button = tk.Button(buttons_frame, text="Active Analysis", command=lambda: set_analysis_mode("Active"), font=("Helvetica", 12), bg="#3498DB", fg="white", activebackground="#2980B9", activeforeground="white")
active_button.grid(row=0, column=0, padx=10, pady=5)

passive_button = tk.Button(buttons_frame, text="Passive Analysis", command=lambda: set_analysis_mode("Passive"), font=("Helvetica", 12), bg="#2ECC71", fg="white", activebackground="#27AE60", activeforeground="white")
passive_button.grid(row=0, column=1, padx=10, pady=5)

open_button = tk.Button(buttons_frame, text="Open Audio File", command=open_file, font=("Helvetica", 12), bg="#3498DB", fg="white", activebackground="#2980B9", activeforeground="white")
open_button.grid(row=0, column=2, padx=10, pady=5)

reset_button = tk.Button(buttons_frame, text="Reset", command=reset_interface, font=("Helvetica", 12), bg="#E74C3C", fg="white", activebackground="#C0392B", activeforeground="white")
reset_button.grid(row=1, column=0, padx=10, pady=5, columnspan=4)

exit_button = tk.Button(buttons_frame, text="Exit", command=root.quit, font=("Helvetica", 12), bg="#E74C3C", fg="white", activebackground="#C0392B", activeforeground="white")
exit_button.grid(row=0, column=3, padx=10, pady=5)

root.mainloop()
