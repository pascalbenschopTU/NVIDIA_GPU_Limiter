import subprocess
import tkinter as tk

def get_gpu_power():
    result = subprocess.run(['nvidia-smi', '-i', '0', '--format=csv,noheader,nounits', '--query-gpu=power.draw'], stdout=subprocess.PIPE)
    power = float(result.stdout.decode('utf-8').strip())
    return power

def get_gpu_temperature():
    result = subprocess.run(['nvidia-smi', '-i', '0', '--format=csv,noheader,nounits', '--query-gpu=temperature.gpu'], stdout=subprocess.PIPE)
    temperature = float(result.stdout.decode('utf-8').strip())
    return temperature

def limit_gpu_power(power_limit):
    subprocess.run(['nvidia-smi', '-i', '0', '-pl', str(power_limit)])

def update_power_limit():
    global current_limit
    try:
        current_limit = int(entry.get())
    except ValueError:
        # Handle non-integer input or empty string
        status_label.config(text="Invalid input for power limit", fg="red")
        return
    
    # Set value in entry to empty
    entry.delete(0, tk.END)
    
    limit_gpu_power(current_limit)
    status_label.config(text="Power limit set to {}W".format(current_limit))

def check_power():
    power = get_gpu_power()
    power_label.config(text="Power draw: {:.2f} W".format(power))
    polling_interval = slider.get()

    global current_limit
    
    if 100 < current_limit < 450 and power > current_limit + 10:
        status_label.config(text="Power limit reached, reducing to {}W".format(current_limit), fg="red")
        limit_gpu_power(current_limit)
    else:
        status_label.config(text="", fg="black")

    max_power_label.config(text="Max Power Limit: {}W".format(current_limit))
    
    temperature = get_gpu_temperature()
    temperature_label.config(text="GPU Temperature: {} °C".format(temperature))
    
    root.after(polling_interval, check_power)  # Schedule next update

current_limit = 450

root = tk.Tk()
root.title("GPU Power Limiter")
root.geometry("400x400")
root.configure(bg="white")

# Main frame
frame = tk.Frame(root, bg="white")
frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)

# Labels
max_power_label = tk.Label(frame, text="Max Power Limit: 320W", font=("Arial", 14), bg="white", fg="black")
max_power_label.pack(pady=10, anchor=tk.W)

power_label = tk.Label(frame, text="Current Power: ", font=("Arial", 14), bg="white", fg="black")
power_label.pack(pady=5, anchor=tk.W)

temperature_label = tk.Label(frame, text="Temperature: ", font=("Arial", 14), bg="white", fg="black")
temperature_label.pack(pady=5, anchor=tk.W)

# Input frame
input_frame = tk.Frame(frame, bg="lightgray")
input_frame.pack(pady=(20, 0), anchor=tk.W, fill=tk.BOTH, expand=True)

# Entry label and entry
entry_label = tk.Label(input_frame, text="Set Max Power (W):", font=("Arial", 12), bg="lightgray", fg="black")
entry_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

entry = tk.Entry(input_frame, font=("Arial", 12))
entry.grid(row=1, column=0, padx=10, pady=5, sticky="w")

# Update button
update_button = tk.Button(input_frame, text="Update", command=update_power_limit, font=("Arial", 12), bg="black", fg="white")
update_button.grid(row=1, column=1, padx=10, pady=5, sticky="w")

# Slider label and slider
slider_label = tk.Label(input_frame, text="Update polling interval (ms):", font=("Arial", 12), bg="lightgray", fg="black")
slider_label.grid(row=2, column=0, padx=10, pady=5, sticky="w")

slider = tk.Scale(input_frame, from_=500, to=5000, resolution=500, orient=tk.HORIZONTAL, length=200)
slider.set(2000)
slider.grid(row=3, column=0, padx=10, pady=5, sticky="w")

# Status label
status_label = tk.Label(input_frame, text="", font=("Arial", 12), bg="lightgray", fg="green")
status_label.grid(row=4, column=0, padx=10, pady=5, sticky="w")

check_power()  # Start the power checking loop
root.mainloop()

