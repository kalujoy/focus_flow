# ICT 323 Introduction to Python Programming

## GROUP 4

# FocusFlow - Productivity Suite

A desktop productivity application built with PyQt6 that combines task management, Pomodoro timer, and analytics in one unified interface. FocusFlow helps users stay organized, manage their time effectively using the Pomodoro technique, and track their productivity through visual analytics.

## Table of Contents

1. [About the Project](#about-the-project)
2. [Features](#features)
3. [Tech Stack](#tech-stack)
4. [Installation](#installation)
5. [Usage](#usage)
6. [Project Structure](#project-structure)
7. [Screenshots](#screenshots)
8. [Key Functionalities](#key-functionalities)
9. [Data Storage](#data-storage)
10. [Contributing](#contributing)
11. [License](#license)

## About the Project

FocusFlow is a comprehensive desktop application designed to enhance productivity by integrating three essential productivity tools into a single application. The application uses a modern dark-themed user interface that is easy on the eyes and provides a seamless user experience.

This project was developed as a group assignment for ICT 323 Introduction to Python Programming course. The application demonstrates the use of Python GUI programming with PyQt6, data visualization with Matplotlib, and data handling with Pandas.

The main motivation behind FocusFlow is to provide a unified solution for students, professionals, and anyone looking to improve their productivity. By combining task management, time tracking, and analytics, users can get a complete picture of their productivity patterns and make informed decisions about how they spend their time.

## Features

FocusFlow comes packed with a variety of features designed to help you stay organized and productive:

### Task Management

- **Create Tasks**: Add new tasks with a title, category, priority level, due date, and notes
- **Edit Tasks**: Modify existing tasks to update details as needed
- **Delete Tasks**: Remove tasks that are no longer needed
- **Mark as Complete**: Track progress by marking tasks as done
- **Categories**: Organize tasks by category (Educational, Financial, Cooking, Personal, Work, Health, Shopping, Other)
- **Priority Levels**: Set task priority as Low, Medium, or High
- **Due Dates**: Track when tasks are due
- **Notes**: Add additional details and context to tasks
- **Category Icons**: Visual icons for each category for easy identification

### Pomodoro Timer

- **Customizable Duration**: Set any duration from 1 minute to 8 hours
- **Task Linking**: Link the timer to specific tasks for productivity tracking
- **Visual Progress**: Progress bar showing remaining time
- **Start/Pause/Reset**: Full control over the timer
- **Completion Alerts**: Notifications when the timer completes

### Analytics Dashboard

- **Pie Chart**: View completed tasks by category
- **Bar Chart**: View completed tasks by priority level
- **Line Chart**: Track daily productivity over the last 30 days
- **Refresh Charts**: Update analytics with current data
- **Export Reports**: Download your productivity data as CSV files

## Tech Stack

The application is built using the following technologies:

- **Python 3.x**: The programming language used for the entire application
- **PyQt6**: A set of Python bindings for Qt6, used for creating the graphical user interface
- **Matplotlib**: A comprehensive library for creating static, animated, and interactive visualizations in Python, used for the analytics charts
- **Pandas**: A fast, flexible, and expressive data structure designed to make working with "relational" or "labeled" data both easy and intuitive, used for data handling and CSV export
- **QSS (Qt Style Sheets)**: Used for styling the application with a modern dark theme

## Installation

To run FocusFlow on your local machine, follow these steps:

1. **Ensure Python is installed**: Make sure you have Python 3.x installed on your system. You can download it from python.org if you don't have it installed.

2. **Clone or download the project**: Get a copy of the FocusFlow project files.

3. **Install dependencies**: Open your terminal or command prompt and run the following command to install all required dependencies:

```
bash
pip install -r requirements.txt
```

This will install all the necessary packages including PyQt6, matplotlib, and pandas.

4. **Run the application**: After installing the dependencies, you can start the application by running:

```
bash
python main.py
```

## Usage

Once the application is running, you'll see the main window with three tabs:

### Tasks Tab

1. Enter a task description in the text field
2. Select a category from the dropdown
3. Set the priority level (Low, Medium, or High)
4. Choose a due date (optional)
5. Add any notes (optional)
6. Click "Add Task" to create the task

Once created, you can:

- Click "Edit" to modify the task
- Click "Delete" to remove the task
- Click "Mark Done" to complete the task
- Click "Start Timer" to start a Pomodoro session for that task

### Pomodoro Tab

1. Click "Set Custom Time" to choose your focus duration
2. Click "Start" to begin the timer
3. The progress bar will show remaining time
4. Click "Pause" to pause the timer
5. Click "Reset" to reset the timer to the beginning

When the timer completes, you'll receive a notification.

### Analytics Tab

1. View your productivity charts (pie, bar, and line charts)
2. Click "Refresh Charts" to update the data
3. Click "Download Full Report (CSV)" to export your data

## Project Structure

The project is organized as follows:

```
FocusFlow/
├── main.py                 # Application entry point
├── styles.qss              # Main stylesheet
├── styles copy.qss         # Backup stylesheet
├── requirements.txt        # Python dependencies
├── README.md               # This file
├── src/
│   ├── __init__.py         # Package initialization
│   ├── main_window.py     # Main application window
│   ├── task_manager.py     # Task management logic
│   ├── pomodoro_widget.py # Pomodoro timer widget
│   └── analytics_widget.py # Analytics charts
├── assets/
│   ├── icons/              # Category icons
│   │   ├── cooking.png
│   │   ├── educational.png
│   │   ├── financial.png
│   │   ├── health.png
│   │   ├── personal.png
│   │   ├── shopping.png
│   │   └── work.png
│   └── styles/
│       └── dark_style.css # Dark theme styles
├── data/
│   ├── task.json          # Task data (JSON format)
│   └── tasks.json         # Additional task storage
├── docs/
│   └── user_manual.pdf    # User manual
└── report.pdf             # Project report
```

## Screenshots

The app features a modern, dark-themed UI with three main tabs:

### Tasks Tab

- Input form for adding new tasks with category, priority, due date, and notes
- Visual task cards with priority indicators and category icons
- Action buttons for editing, deleting, marking complete, and starting timers
- Clean and organized layout with scrollable task list

### Pomodoro Tab

- Large, easy-to-read timer display
- Progress bar showing remaining time
- Custom time setting dialog
- Start, Pause, and Reset controls

### Analytics Tab

- Pie chart showing completed tasks by category
- Bar chart showing completed tasks by priority
- Line chart showing daily productivity over 30 days
- Refresh and Export buttons

## Key Functionalities

### Task Management System

The task management system allows users to create comprehensive task entries with multiple attributes:

- **Text**: The main description of the task
- **Category**: One of 8 predefined categories with corresponding icons
- **Priority**: Three levels (Low, Medium, High) with color coding
- **Due Date**: Optional due date for task deadline tracking
- **Notes**: Additional context or details about the task
- **Status**: Boolean flag indicating whether the task is complete

Tasks are stored in a JSON file for persistence between sessions.

### Pomodoro Timer

The Pomodoro timer implementation includes:

- Configurable duration (hours and minutes)
- Task linking for productivity tracking
- Real-time countdown display
- Progress bar visualization
- Start, pause, and reset functionality
- Signal emission when timer completes

### Analytics System

The analytics system provides visual insights into productivity:

- **Category Analysis**: Pie chart showing distribution of completed tasks across categories
- **Priority Analysis**: Bar chart showing completion count by priority level
- **Time Series Analysis**: Line chart showing daily task completion over 30 days
- **Data Export**: CSV export functionality for external analysis

## Data Storage

FocusFlow uses JSON format for data storage:

- Tasks are saved in `data/tasks.json`
- The file is automatically created when the first task is added
- Data is loaded when the application starts
- Changes are saved immediately after any modification

CSV reports can be exported from the Analytics tab for external analysis and backup purposes.

## Contributing

This project was created as a group assignment for educational purposes. However, if you'd like to contribute to the project:

1. Fork the repository
2. Create a new branch for your feature
3. Make your changes and commit them
4. Push to the branch
5. Create a Pull Request

## License

This project is for educational purposes as part of the ICT 323 course.

---

Developed by GROUP 4 - ICT 323 Introduction to Python Programming
#   f o c u s _ f l o w  
 