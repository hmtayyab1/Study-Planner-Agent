import os
from flask import Flask, render_template, request
from groq import Groq
from dotenv import load_dotenv
load_dotenv()

# ----------------------------
# Initialize Flask and Groq
# ----------------------------
app = Flask(__name__)
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ----------------------------
# AI Schedule Generator
# ----------------------------
def generate_ai_schedule(subjects, priorities, total_time):
    prompt = f"""
You are an expert study planner. 
Create a detailed daily study schedule for a total of {total_time} minutes.
Subjects: {', '.join(subjects)}
Priorities: {', '.join(priorities)}

Requirements:
- Distribute time based on priority (high=longer, low=shorter)
- Include short breaks where needed
- Give motivational tips for each subject
- Provide start and end times, starting at 09:00
- Format: "HH:MM - HH:MM: Subject (XX mins) | Tip: ..."
"""
    try:
        response = client.chat.completions.create(
            model="openai/gpt-oss-20b",
            messages=[
                {"role": "system", "content": "You are a helpful study assistant."},
                {"role": "user", "content": prompt}
            ]
        )
        schedule_text = response.choices[0].message.content.strip()
        return schedule_text
    except Exception as e:
        return f"Error generating schedule: {e}"

# ----------------------------
# Flask Routes
# ----------------------------
@app.route("/", methods=["GET", "POST"])
def index():
    schedule = ""
    if request.method == "POST":
        total_time = int(request.form["total_time"])
        subjects = request.form["subjects"].split(",")
        priorities = request.form["priorities"].split(",")
        schedule = generate_ai_schedule(subjects, priorities, total_time)
    return render_template("index.html", schedule=schedule)

# ----------------------------
# Run App
# ----------------------------
if __name__ == "__main__":
    app.run(debug=True)
