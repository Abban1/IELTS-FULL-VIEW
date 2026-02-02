import os
from dotenv import load_dotenv
from groq import Groq


load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def generate_ielts_listening_test(level: str = "Academic") -> str:
    """
    Generate a full IELTS Listening test in plain text using Groq.
    """
    prompt = f"""
You are an IELTS Listening test generator.
Be creative and do not copy paste content
Reference test 

SECTION 1 - Questions 1-10

Questions 1-5
Complete the table below. Write ONE WORD AND/OR A NUMBER for each answer.

Apartments | Facilities | Other Information | Cost
-------------------------------------------------
Rose Garden Apartments | studio flat | Example entertainment programme: Greek … | €219
Blue Bay Apartments | large salt-water swimming pool | just 1 ___ metres from beach, near shops | €275
Sunny Retreat Apartments | terrace | watersports | €490
The Grand | – | Greek paintings, overlooking ___, near supermarket and disco | €___
City Centre Apartments | – | – | €420

Questions 6-10
Complete the table below. Write ONE WORD AND/OR A NUMBER for each answer.

GREEK ISLAND HOLIDAYS — Insurance Benefits

Insurance Benefits | Maximum Amount
-------------------------------------------------
Cancellation | €800. Additional benefit allows a ___ % refund for travel to resort
Hospital | €500. Additional benefit allows a ___ % refund for departure
Personal belongings | Up to €3000; €500 for one ___
Assistant Manager | Name: Ben ___, Direct phone line: 081260543216


SECTION 2 - Questions 11-20

Questions 11-13
Choose the correct letter, A, B, or C.

Winridge Forest Railway Park

11. Simon's idea for a theme park came from
A. his childhood hobby
B. his interest in landscape design
C. his visit to another park

12. When they started, the family decided to open the park only when
A. the weather was expected to be good
B. the children were not at school
C. there were fewer farming commitments

13. Since opening, the park has had
A. 50,000 visitors
B. 100,000 visitors
C. 150,000 visitors


Questions 14-18
Match people to their main area of work. Choose FIVE answers from A-H.

Area of work (A-H)
A. advertising
B. animal care
C. building
D. educational links
E. engine maintenance
F. food and drink
G. sales
H. staffing

People
14. Simon | ___
15. Liz | ___
16. Sarah | ___
17. Duncan | ___
18. Judith | ___


Questions 19-20
Complete the table. Write ONE WORD AND/OR A NUMBER for each answer.

Feature | Size | Biggest Challenge | Target Age Group
-----------------------------------------------------
Railway | 1.2 km | Making tunnels | ___
Go-Kart arena | ___ m | Removing mounds on track | ___


SECTION 3 - Questions 21-30

Complete the notes below. Write NO MORE THAN TWO WORDS AND/OR A NUMBER for each answer.

Study Skills Tutorial — Caroline Benning

Dissertation topic: 21 ___
Strengths: 22 ___, computer modelling
Weaknesses: lack of background information, poor 23 ___ skills
Possible strategy: peer group discussion
Benefits: increases 24 ___
Problems: dissertations tend to contain the same 25 ___
Use the 26 ___ service: provides structured programme
Limited: 27 ___
Consult study skills books: good source of 28 ___, can be too 29 ___
Recommendations: use a card index, read all notes
Next tutorial date: 30 January


SECTION 4 - Questions 31-40

Questions 31-32
Choose the correct letter, A, B, or C.

31. The owners of the underground house
A. had no experience of living in a rural area
B. were interested in environmental issues
C. wanted a professional project manager

32. What does the speaker say about the site of the house?
A. The land was quite cheap
B. Stone was being extracted nearby
C. It was in a completely unspoilt area


Questions 33-40
Complete the notes below. Write ONE WORD AND/OR A NUMBER for each answer.

The Underground House

Design
Built in the earth, two floors
South-facing side: constructed of two layers of 33 ___
Photovoltaic tiles: attached for solar energy
Insulation: layer of foam used to improve 34 ___

Special features
- Internal mirrors and 35 ___ for extra light
- House may produce more 36 ___ than needed in future
- Recycled wood used for 37 ___ of the house
- Domestic waste system is 38 ___, organic

Environmental issues
- Use of large quantities of 39 ___ in construction was harmful
- House will pay environmental debt within 40 ___


Generate a new IELTS Listening test for {level} level.
Dont go for scientific topics
Ask tougher and unobvious questions
Wording of questions must be in a aparaphrase manner
Dont ask obvious and clear answers
**Must complete  total 40 questions
Generate in exact format as given but in plainntext

"""

    try:
        response = client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=[
                {"role": "system", "content": "You are an expert IELTS Listening test generator."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
            max_tokens=5000
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"Error generating listening test: {str(e)}"
