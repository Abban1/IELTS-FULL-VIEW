import os
from dotenv import load_dotenv
from groq import Groq

# Load environment variables
load_dotenv()

# Initialize Groq client mn0-jokil,
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# Constants
MODEL = "llama-3.3-70b-versatile"
SYSTEM_ROLE = (
    "You are an expert IELTS General Training Reading test generator. "
    "Generate full GT Reading tests strictly following IELTS guidelines. "
    "Use neutral, factual, practical language only. "
    "Passages must be realistic from Official public information / procedural guide / instruction leaflet,staff handbooks, training guides, or company notices not academic essays. "
    "Ensure word counts per section are correct and question types match IELTS GT standards. "
    "Avoid first-person storytelling. Do NOT provide answers, only generate passages and questions. "
  
"-Do not give headings to passages"




)

def _generate(prompt: str) -> str:
    """
    Helper function to call Groq API and return generated text.
    """
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": SYSTEM_ROLE},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,  
            max_tokens=6000
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error: {str(e)}"

# =========================
# SECTION 1 – EASY (2 Passages)
# =========================
def generate_section_1(level="General Training", difficulty="Easy") -> str:
    prompt = f"""
Generate SECTION 1 of an IELTS GENERAL TRAINING Reading Test.

LEVEL: {level}
SECTION DIFFICULTY: {difficulty}
SECTION 1 – Everyday / Workplace Documents

Passage 1 (Questions 1–7): 300–450 words 4-5 paragraphs
-Each paragraph must be unique with repect to eachother.
- Source: Official public information / procedural guide / instruction leaflet,workplace documents such as staff handbooks, training guides, company notices
- Style: neutral, concise, factual; no narrative, no first-person storytelling
- Content: practical and realistic workplace scenarios
- Questions (1–7): Question should start with: (True/False/Not Given)


Passage 2 (Questions 8–14): 500–650 words
- Source: staff handbooks, training guides, or company notices rather than academic essays.
- Structure: exactly 7 paragraphs.
- Style: Passage must not contain words directly in starting which are in headings and must be paraphrased wordings.
- Questions (8–14): 7 headings as question, each ≤3 words.Heading must be paraphrased and not directly copy pasted from passage.
  "Number questions clearly and follow IELTS formatting."
    "Do NOT provide answers"
- Difficulty: slightly higher than Passage 1

"""
    return _generate(prompt)

# =========================
# SECTION 2 – MEDIUM (Workplace / training context)
# =========================
def generate_section_2(level="General Training", difficulty="Medium") -> str:
    prompt = f"""
Generate SECTION 2 of an IELTS GENERAL TRAINING Reading Test.

LEVEL: {level}
SECTION DIFFICULTY: {difficulty}
SECTION 2 – Workplace / Training Context

Passage 1 (Questions 15–20): 450–500 words
-Each paragraph must be unique with repect to eachother.
- staff handbooks, training guides, or company notices rather than academic essays.
-Not in an academic style
- Questions: True/False/Not Given, requiring inference and careful reading
- Do NOT provide answers

Passage 2 (Questions 21–27): 450–500 words
-Each paragraph must be unique with repect to eachother.
- Similar source and style
- Questions: Multiple Choice Questions (MCQs), each with 4 options
- Paragraphs: 5–7 concise paragraphs

"""
    return _generate(prompt)

# =========================
# SECTION 3 – HARD (General interest / social issues)
# =========================
def generate_section_3(level="General Training", difficulty="Hard") -> str:
    prompt = f"""
Generate SECTION 3 of an IELTS GENERAL TRAINING Reading Test.

LEVEL: {level}
SECTION DIFFICULTY: {difficulty}
SECTION 3 – General Interest / Social Issues

Passage (Questions 28–40): 700–800 words
- Topic: workplace documents such as staff handbooks, training guides, company notices
- Paragraphs: 6–7, neutral, factual, clear tone
-Each paragraph must be unique with repect to eachother.
- Questions (28–40): mix of sentence completion, multiple-choice questions (MCQs), summary completion
- Difficulty: higher than Sections 1 and 2, requiring inference, scanning for details, and understanding implied meaning
"""
    return _generate(prompt)

# =========================
# Full Test Generator
# =========================
def generate_full_ielts_gt_reading():
    section_1 = generate_section_1()
    section_2 = generate_section_2()
    section_3 = generate_section_3()
    return f"{section_1}\n\n{section_2}\n\n{section_3}"

# =========================
# Example usage
# =========================
if __name__ == "__main__":
    test_content = generate_full_ielts_gt_reading()
    # Save to a text file
    with open("IELTS_GT_Reading_Test.txt", "w", encoding="utf-8") as f:
        f.write(test_content)
    print("IELTS General Training Reading Test generated and saved as 'IELTS_GT_Reading_Test.txt'.")
