# utils.py
import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

# Initialize Groq client
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_ielts_speaking(level: str = "Academic", context_question: str = None) -> str:
    """
    Generate IELTS Speaking Test prompt using Groq.
    Only returns exam questions, no discussion or commentary.
    context_question: optional reference topic to guide Part 2 and Part 3
    """
    context_text = f"Use the following reference context for the test: {context_question}" if context_question else ""

    prompt = (
        f"""
        You are an IELTS Speaking Test generator for {level} level.
        Generate a **full IELTS Speaking Test** (Parts 1, 2, 3) and **output ONLY the test questions**.
        {context_text}

        Follow these strict instructions:

        1. **Do NOT include explanations, answers, or commentary.**
        2. **Part 1: Introduction & Interview**
           - Only 4-5 questions about familiar topics (home, work, study, hobbies).
           - Must select only (one topic)
           - Format:
             Topic: [topic]
             Question 1: [question]
             Question 2: [question]
             ...
        3. **Part 2: Long Turn**
           - One topic with guidance for speaking 1-2 minutes.
           - Use the context question to guide the topic.
           - Format:
             Topic: [topic]
             You should say:
             - [bullet point 1]
             - [bullet point 2]
             - [bullet point 3]
             - [bullet point 4]
        4. **Part 3: Discussion**
           - 3-4 questions based on general ideas or opinion based topics.
           - Use the context question to make questions relevant.
           - Only questions.
           - Format:
             Question 1: [question]
             Question 2: [question]
             Question 3: [question]

        Output must be realistic, concise, and in IELTS exam style.
        """
    )

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are an IELTS test generator."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=500
        )
        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"Error generating task: {str(e)}"
