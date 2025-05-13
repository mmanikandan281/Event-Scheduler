import tkinter as tk
from tkinter import messagebox, filedialog, scrolledtext, ttk
from datetime import datetime
import random

# Helper functions
def parse_time(time_str):
    try:
        return datetime.strptime(time_str, "%H:%M")
    except ValueError:
        return None

def format_time(time_obj):
    return time_obj.strftime("%H:%M")

def has_overlap(new_start, new_end, exclude_index=None):
    for i, event in enumerate(schedule):
        if exclude_index is not None and i == exclude_index:
            continue
        if new_start < event['end'] and new_end > event['start']:
            return True
    return False

def get_random_pastel_color():
    # Generate pastel colors for event tags
    r = random.randint(180, 240)
    g = random.randint(180, 240)
    b = random.randint(180, 240)
    return f'#{r:02x}{g:02x}{b:02x}'

def add_event():
    activity = activity_entry.get().strip()
    start_str = start_entry.get().strip()
    end_str = end_entry.get().strip()
    
    start = parse_time(start_str)
    end = parse_time(end_str)
    
    if not activity or not start or not end:
        messagebox.showerror("Invalid Input", "Please enter all fields in correct format (HH:MM).")
        return
    if end <= start:
        messagebox.showerror("Invalid Time", "End time must be after start time.")
        return
    if has_overlap(start, end):
        messagebox.showerror("Overlap Detected", "This event overlaps with another event.")
        return
    
    # Assign a random pastel color to the event
    color = get_random_pastel_color()
    
    schedule.append({
        'activity': activity, 
        'start': start, 
        'end': end,
        'color': color
    })
    schedule.sort(key=lambda x: x['start'])
    update_timeline()
    update_event_listbox()
    
    activity_entry.delete(0, tk.END)
    start_entry.delete(0, tk.END)
    end_entry.delete(0, tk.END)

def remove_event():
    selected_indices = event_listbox.curselection()
    if not selected_indices:
        messagebox.showwarning("No Selection", "Please select an event to remove.")
        return
    
    index = selected_indices[0]
    removed = schedule.pop(index)
    messagebox.showinfo("Event Removed", f"Removed: {removed['activity']}")
    
    update_timeline()
    update_event_listbox()

def edit_event():
    selected_indices = event_listbox.curselection()
    if not selected_indices:
        messagebox.showwarning("No Selection", "Please select an event to edit.")
        return
    
    index = selected_indices[0]
    event = schedule[index]
    
    # Fill the entry fields with the selected event details
    activity_entry.delete(0, tk.END)
    activity_entry.insert(0, event['activity'])
    
    start_entry.delete(0, tk.END)
    start_entry.insert(0, format_time(event['start']))
    
    end_entry.delete(0, tk.END)
    end_entry.insert(0, format_time(event['end']))
    
    # Remove the event from the schedule
    schedule.pop(index)
    update_timeline()
    update_event_listbox()
    
    # Change the add button to update
    add_button.config(text="Update Event")
    add_button.config(command=lambda: update_event(event))

def update_event(old_event):
    # Add the event with the updated details
    add_event()
    
    # Reset the add button
    add_button.config(text="Add Event")
    add_button.config(command=add_event)

def update_timeline():
    timeline_canvas.delete("all")
    
    # Draw timeline background
    canvas_width = timeline_canvas.winfo_width()
    if canvas_width < 10:  # Not properly initialized yet
        canvas_width = 480
    
    hour_width = canvas_width / 12  # 12 hours (8:00 - 20:00)
    start_hour = 8  # 8:00 AM
    
    # Draw time markers
    for i in range(13):  # 8:00 to 20:00
        hour = start_hour + i
        x = i * hour_width
        
        # Draw vertical line for each hour
        timeline_canvas.create_line(x, 0, x, 150, fill="#e0e0e0")
        
        # Draw hour label
        hour_str = f"{hour:02d}:00"
        timeline_canvas.create_text(x + 2, 10, text=hour_str, anchor="nw", font=("Arial", 8))
    
    # Draw events on timeline
    y_offset = 30
    row_height = 25
    current_row = 0
    
    for event in schedule:
        start_minutes = event['start'].hour * 60 + event['start'].minute
        end_minutes = event['end'].hour * 60 + event['end'].minute
        
        start_x = ((start_minutes / 60) - start_hour) * hour_width
        end_x = ((end_minutes / 60) - start_hour) * hour_width
        
        # Find available row
        can_fit = False
        for row in range(5):  # Max 5 rows
            can_fit = True
            y = y_offset + row * row_height
            current_row = row
            break
            
        # Draw event rectangle
        rect_y = y_offset + current_row * row_height
        event_rect = timeline_canvas.create_rectangle(
            start_x, rect_y, end_x, rect_y + row_height - 2,
            fill=event['color'], outline="#999999"
        )
        
        # Draw event text
        time_text = f"{format_time(event['start'])}-{format_time(event['end'])}"
        timeline_canvas.create_text(
            start_x + 3, rect_y + 3,
            text=f"{event['activity']} ({time_text})",
            anchor="nw",
            font=("Arial", 8)
        )
        
        current_row += 1

def update_event_listbox():
    event_listbox.delete(0, tk.END)
    for event in schedule:
        time_range = f"{format_time(event['start'])} - {format_time(event['end'])}"
        event_listbox.insert(tk.END, f"{time_range} : {event['activity']}")

def save_to_file():
    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt")]
    )
    if file_path:
        with open(file_path, 'w') as f:
            f.write("📅 Event Timeline\n")
            f.write("-" * 50 + "\n")
            for event in schedule:
                line = f"{format_time(event['start'])} - {format_time(event['end'])} : {event['activity']}\n"
                f.write(line)
            f.write("-" * 50 + "\n")
        messagebox.showinfo("Saved", f"Timeline saved to '{file_path}'")

# Main window setup
root = tk.Tk()
root.title("🎓 Event Scheduler")
root.geometry("600x650")
root.configure(bg="#f5f5f5")

# Apply a theme
style = ttk.Style()
style.theme_use('clam')  # 'clam', 'alt', 'default', 'classic'

# Configure common styles
style.configure('TFrame', background='#f5f5f5')
style.configure('TLabel', background='#f5f5f5', font=('Arial', 10))
style.configure('TButton', font=('Arial', 10, 'bold'))
style.configure('Header.TLabel', font=('Arial', 14, 'bold'))

schedule = []

# Main container
main_frame = ttk.Frame(root, padding=15)
main_frame.pack(fill=tk.BOTH, expand=True)

# Title
title_frame = ttk.Frame(main_frame)
title_frame.pack(fill=tk.X, pady=(0, 15))
title_label = ttk.Label(title_frame, text=" Event Scheduler", style='Header.TLabel')
title_label.pack()

# Input Frame with modern styling
input_frame = ttk.LabelFrame(main_frame, text="Add New Event", padding=10)
input_frame.pack(fill=tk.X, pady=10)

# Grid for input fields
ttk.Label(input_frame, text="Activity Name:").grid(row=0, column=0, sticky=tk.W, pady=5)
activity_entry = ttk.Entry(input_frame, width=30)
activity_entry.grid(row=0, column=1, padx=5, pady=5, sticky=tk.W)

ttk.Label(input_frame, text="Start Time (HH:MM):").grid(row=1, column=0, sticky=tk.W, pady=5)
start_entry = ttk.Entry(input_frame, width=15)
start_entry.grid(row=1, column=1, padx=5, pady=5, sticky=tk.W)

ttk.Label(input_frame, text="End Time (HH:MM):").grid(row=2, column=0, sticky=tk.W, pady=5)
end_entry = ttk.Entry(input_frame, width=15)
end_entry.grid(row=2, column=1, padx=5, pady=5, sticky=tk.W)

# Buttons frame
buttons_frame = ttk.Frame(input_frame)
buttons_frame.grid(row=3, column=0, columnspan=2, sticky=tk.EW, pady=10)

# Create styled buttons
add_button = tk.Button(
    buttons_frame, text="Add Event", command=add_event, 
    bg="#4CAF50", fg="white", font=("Arial", 10, "bold"),
    padx=10, pady=5, borderwidth=0
)
add_button.pack(side=tk.LEFT, padx=5)

# Visual timeline
timeline_frame = ttk.LabelFrame(main_frame, text="Event Timeline", padding=10)
timeline_frame.pack(fill=tk.BOTH, expand=True, pady=10)

timeline_canvas = tk.Canvas(timeline_frame, bg="white", height=150)
timeline_canvas.pack(fill=tk.X, expand=True)

# Event list
event_list_frame = ttk.LabelFrame(main_frame, text="Event List", padding=10)
event_list_frame.pack(fill=tk.BOTH, expand=True, pady=10)

event_listbox = tk.Listbox(event_list_frame, height=8, bg="white", borderwidth=0, 
                           font=("Arial", 10), selectbackground="#a6d4fa")
event_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Scrollbar for event list
scrollbar = ttk.Scrollbar(event_list_frame, orient=tk.VERTICAL, command=event_listbox.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
event_listbox.config(yscrollcommand=scrollbar.set)

# Event management buttons
event_mgmt_frame = ttk.Frame(main_frame)
event_mgmt_frame.pack(fill=tk.X, pady=10)

edit_button = tk.Button(
    event_mgmt_frame, text="✏️ Edit Event", command=edit_event,
    bg="#FF9800", fg="white", font=("Arial", 10, "bold"),
    padx=10, pady=5, borderwidth=0
)
edit_button.pack(side=tk.LEFT, padx=5)

remove_button = tk.Button(
    event_mgmt_frame, text="🗑️ Remove Event", command=remove_event,
    bg="#F44336", fg="white", font=("Arial", 10, "bold"),
    padx=10, pady=5, borderwidth=0
)
remove_button.pack(side=tk.LEFT, padx=5)

# Save Button
save_button = tk.Button(
    main_frame, text="💾 Save to File", command=save_to_file,
    bg="#2196F3", fg="white", font=("Arial", 10, "bold"),
    padx=10, pady=5, width=20, borderwidth=0
)
save_button.pack(pady=10)

# Status bar
status_bar = ttk.Label(root, text="Ready", relief=tk.SUNKEN, anchor=tk.W)
status_bar.pack(side=tk.BOTTOM, fill=tk.X)

# Window resize handler
def on_window_resize(event):
    update_timeline()

root.bind("<Configure>", on_window_resize)

# Run the app
root.mainloop()