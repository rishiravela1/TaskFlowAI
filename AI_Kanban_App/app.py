from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import json
import os
import uuid

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:8000"}})

# In-memory database
tasks = {
    "todo": [{"id": "task-1", "text": "Plan company offsite", "subtasks": []}],
    "inprogress": [{"id": "task-2", "text": "Develop new feature", "subtasks": [
        {"id": "sub-1", "text": "Design the UI", "completed": True},
        {"id": "sub-2", "text": "Code the logic", "completed": False}
    ]}],
    "done": [{"id": "task-3", "text": "Fix login bug", "subtasks": []}]
}

# --- Gemini API Configuration ---
API_KEY = "AIzaSyByxLuS5uIFZqWgvYll2wZEh2xdL5poRF8" # Your Google AI Studio API Key
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key={API_KEY}"

# --- Helper function to find a task by ID ---
def find_task(task_id):
    for column in tasks.values():
        for task in column:
            if task['id'] == task_id:
                return task
    return None

# --- API Endpoints for Tasks ---

@app.route('/tasks', methods=['GET'])
def get_tasks():
    return jsonify(tasks)

@app.route('/tasks', methods=['POST'])
def add_task():
    data = request.json
    if not data or 'text' not in data or not data['text'].strip():
        return jsonify({"error": "Task text is required"}), 400
    
    new_task = {
        'id': f"task-{uuid.uuid4()}",
        'text': data['text'].strip(),
        'subtasks': []  # Initialize with an empty subtasks array
    }
    tasks['todo'].append(new_task)
    return jsonify(new_task), 201

@app.route('/tasks/update', methods=['POST'])
def update_tasks():
    global tasks
    tasks = request.json
    return jsonify({"message": "Tasks updated successfully"}), 200

@app.route('/tasks/<task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks
    for column in tasks:
        tasks[column] = [task for task in tasks[column] if task['id'] != task_id]
    return jsonify({"message": f"Task {task_id} deleted"}), 200

# --- NEW: API Endpoints for Sub-tasks ---

@app.route('/tasks/<task_id>/subtask', methods=['POST'])
def add_subtask(task_id):
    parent_task = find_task(task_id)
    if not parent_task:
        return jsonify({"error": "Parent task not found"}), 404
    
    data = request.json
    if not data or 'text' not in data:
        return jsonify({"error": "Sub-task text is required"}), 400

    new_subtask = {
        'id': f"sub-{uuid.uuid4()}",
        'text': data['text'],
        'completed': False
    }
    
    if 'subtasks' not in parent_task:
        parent_task['subtasks'] = []
    parent_task['subtasks'].append(new_subtask)
    
    return jsonify(new_subtask), 201

@app.route('/tasks/<task_id>/subtask/<subtask_id>', methods=['PUT'])
def update_subtask(task_id, subtask_id):
    parent_task = find_task(task_id)
    if not parent_task or 'subtasks' not in parent_task:
        return jsonify({"error": "Parent task or subtasks not found"}), 404

    subtask_to_update = next((st for st in parent_task['subtasks'] if st['id'] == subtask_id), None)
    if not subtask_to_update:
        return jsonify({"error": "Sub-task not found"}), 404
        
    data = request.json
    if 'completed' in data:
        subtask_to_update['completed'] = data['completed']
    
    return jsonify(subtask_to_update)

# --- AI Endpoint ---

@app.route('/suggest-subtasks', methods=['POST'])
def suggest_subtasks():
    if not API_KEY:
        return jsonify({"error": "AI feature is disabled. No API key found on the server."}), 400

    data = request.json
    if not data or 'task_text' not in data:
        return jsonify({"error": "task_text is required"}), 400

    task_text = data['task_text']

    system_prompt = (
        "You are an expert project manager. Your role is to break down a "
        "complex task into 3-5 smaller, actionable sub-tasks. "
        "Return the sub-tasks as a JSON object with a single key 'subtasks' "
        "which contains an array of strings."
    )
    
    user_prompt = f"Here is the parent task: '{task_text}'"

    payload = {
        "systemInstruction": {"parts": [{"text": system_prompt}]},
        "contents": [{"parts": [{"text": user_prompt}]}],
        "generationConfig": {
            "responseMimeType": "application/json",
            "responseSchema": {
                "type": "OBJECT",
                "properties": { "subtasks": { "type": "ARRAY", "items": {"type": "STRING"} } }
            }
        }
    }

    try:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash-preview-05-20:generateContent?key={API_KEY}"
        response = requests.post(url, json=payload, headers={'Content-Type': 'application/json'})
        response.raise_for_status() 
        
        result = response.json()
        json_text = result.get('candidates', [{}])[0].get('content', {}).get('parts', [{}])[0].get('text', '{}')
        subtasks_data = json.loads(json_text)
        
        return jsonify(subtasks_data)

    except requests.exceptions.RequestException as e:
        if isinstance(e, requests.exceptions.HTTPError) and e.response.status_code == 403:
             return jsonify({"error": "AI API request failed: Forbidden. Check your API key."}), 500
        return jsonify({"error": f"API request failed: {e}"}), 500
    except (KeyError, IndexError, json.JSONDecodeError) as e:
        return jsonify({"error": f"Failed to parse AI response: {e}", "raw_response": "Response from AI was not in the expected format."}), 500

if __name__ == '__main__':
    app.run(debug=True, port=5001)


