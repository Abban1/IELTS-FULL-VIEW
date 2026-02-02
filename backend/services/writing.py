# utils.py
import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

# Initialize Groq client
client = Groq(
    api_key=os.getenv("GROQ_API_KEY")
)

def generate_ielts_task(task_type: str, level: str = "Academic") -> str:
    """
    Generate IELTS Writing Task prompt using Groq/OPEN-AI  (text-only)
    """
    if task_type == "task1":
        prompt = (
            f"""Generate an IELTS Writing Task 1 {level} question.Write only question.The sample question is:The plans below show a harbour in 2000 and how it looks today.
            Summarise the information by selecting and reporting the main features, and
            make comparisons where relevant."""
            f"Describe the diagram/graph/table/chart in text only. "
            f"Make it realistic and exam-style."
        )
    elif task_type == "task2":
        prompt = (
            f"""Generate an IELTS Writing Task 2 {level} essay question.Write only question.The sample question is:The working week should be shorter and workers should have
                longer weekend.
                Do you agree or disagree?"""
            f"Use refernce question as a context and be creative"
            f"Use real IELTS-style topics and clear instructions."
        )
    else:
        return "Invalid task type. Choose 'task1' or 'task2'."

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",  # supported Groq model
            messages=[
                {"role": "system", "content": "You are an IELTS writing test generator."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=300
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"Error generating task: {str(e)}"
