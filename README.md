Event Scheduler
A user-friendly desktop application built with Python and Tkinter for scheduling and visualizing events on a graphical timeline.
Overview
Event Scheduler allows users to manage daily events with a clean interface, featuring a visual timeline for easy planning. Users can add, edit, and remove events, check for time conflicts, and save schedules to a text file. The application uses pastel colors for event visualization and supports a time range from 8:00 AM to 8:00 PM.
Features

Event Management: Add, edit, or remove events with activity names and start/end times (HH:MM format).
Visual Timeline: Displays events on a 12-hour timeline (8:00 AM to 8:00 PM) with pastel-colored event blocks.
Overlap Detection: Prevents scheduling conflicts by checking for overlapping events.
Save to File: Export your schedule to a text file for easy sharing or backup.
Modern UI: Styled with a clean, modern look using Tkinter's 'clam' theme and custom button designs.
Responsive Design: Timeline adjusts dynamically to window resizing.

Requirements

Python 3.6 or higher
Tkinter (included with standard Python installations)
No additional external libraries required

Installation

Clone the repository:git clone https://github.com/your-username/event-scheduler.git


Navigate to the project directory:cd event-scheduler


(Optional) Verify dependencies:pip install -r requirements.txt

Note: Tkinter is typically included with Python, so no additional dependencies are usually needed.

Usage

Run the application:python src/event_scheduler.py


Add an Event:
Enter the activity name, start time, and end time in the "Add New Event" section (use HH:MM format, e.g., 09:30).
Click "Add Event" to include it in the schedule.


Edit an Event:
Select an event from the "Event List."
Click "✏️ Edit Event" to populate the input fields with the event details.
Modify the details and click "Update Event."


Remove an Event:
Select an event from the "Event List."
Click "🗑️ Remove Event" to delete it.


Save Schedule:
Click "💾 Save to File" to export the schedule as a text file.


View the timeline in the "Event Timeline" section, which updates automatically.

Example
Add an event:

Activity: "Team Meeting"
Start Time: 10:00
End Time: 11:30

The event appears on the timeline as a pastel-colored block and in the event list as "10:00 - 11:30 : Team Meeting."
Directory Structure
event-scheduler/
├── src/
│   └── event_scheduler.py  # Main application code
├── README.md              # Project documentation
└── requirements.txt       # Python dependencies (empty, as Tkinter is built-in)

Contributing
Contributions are welcome! Please follow these steps:

Fork the repository.
Create a new branch (git checkout -b feature/your-feature).
Make your changes and commit (git commit -m "Add your feature").
Push to the branch (git push origin feature/your-feature).
Open a Pull Request.

License
This project is licensed under the MIT License. See the LICENSE file for details.
Acknowledgments

Built with Python and Tkinter.
Inspired by the need for simple, visual event planning tools.


Replace your-username in the clone URL with your actual GitHub username.
