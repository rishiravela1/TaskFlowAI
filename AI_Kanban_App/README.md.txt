AI-Powered Kanban Tasks Tracker
This project is a web-based Kanban board application with a Python Flask backend and an AI-powered feature to suggest sub-tasks using the Gemini API.

Features
Kanban Board: A classic three-column board (To Do, In Progress, Done).

Drag & Drop: Easily move tasks between columns.

AI Sub-task Suggestions: For any task, click the "sparkle" icon (✨) to get AI-generated suggestions for smaller, actionable sub-tasks.

Confetti!: Celebrate completing a task with a confetti animation.

Persistent Storage: Tasks are managed by a Python backend (Note: this version uses a simple in-memory dictionary, so tasks will reset if the server restarts).

How to Run the Application
This application requires two parts running simultaneously in two separate terminal windows: the Python backend and a simple server for the HTML frontend.

Step 1: Run the Backend Server (Terminal 1)
Prerequisites:

Make sure you have Python 3.6+ installed.

You'll need to install the required Python libraries. Open your first terminal and run:

pip3 install Flask Flask-Cors requests

(Note: You may need to use pip3 on macOS and Linux).

(Optional) Add your Gemini API Key:

Open the app.py file.

Find the line API_KEY = "".

If you have a Google AI Studio API key, paste it between the quotes. If you are running this in a supported playground, you can leave it as an empty string.

Run the Server:

In your first terminal, navigate to the directory where you saved your files.

Run the following command:

python3 app.py

Note: On macOS and many Linux systems, you must use python3. On some Windows systems, the command may still be python.

You should see output indicating the server is running on http://127.0.0.1:5001. Leave this terminal running.

Step 2: Run the Frontend Server (Terminal 2)
Open a second terminal window.

On Mac, you can press Command + T in your existing terminal or Command + N to open a new one.

Navigate to the Same Directory:

In this new terminal, go to the exact same project folder where your kanban_tracker.html file is located.

Start the Frontend Server:

Run the following simple command:

python3 -m http.server

This will start a basic web server. You will see a message like Serving HTTP on 0.0.0.0 port 8000 (http://0.0.0.0:8000/). Leave this second terminal running too.

Step 3: Use the App
Open Your Web Browser:

Go to this address: http://localhost:8000/kanban_tracker.html

Do not open the HTML file directly from your folder anymore.

Start Using the App!

The Kanban board will load and should now be fully functional. You will be able to add, move, and get AI suggestions for your tasks.