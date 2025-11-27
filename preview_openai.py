import os
import json
from pypdf import PdfReader
from openai import OpenAI
from dotenv import load_dotenv

# -------------------------------------------------------
# Load API key
# -------------------------------------------------------
load_dotenv()
client = OpenAI()

# -------------------------------------------------------
# Function to extract all text from a PDF
# -------------------------------------------------------
def extract_pdf_text(path):
    reader = PdfReader(path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text


# -------------------------------------------------------
# LLM system & user prompts
# -------------------------------------------------------
SYSTEM_PROMPT = """
You are AiTA, the Ai Teaching Assistant.
Your task is to generate a concise lecture preview from lecture slides for students to review before lecture.

Return a JSON object strictly following this format:

{
  "main_topics": [],
  "what_you_will_learn": [],
  "key_definitions": [],
  "prereq_refreshers": [],
  "questions_to_keep_in_mind": [],
  "warmup_check_questions": []
}

Guidelines:
- Base everything ONLY on the provided slide text.
- Be concise and student-friendly.
- Tailor to students finishing undergraduate or in masters degree.
- Identify prerequisites, key definitions, and high-level goals.
- Warm-up questions should test basic prereqs, not lecture-specific details.
"""

USER_PROMPT_TEMPLATE = """
Below is the extracted text from the lecture slides.
Generate the lecture preview according to the JSON schema.

--- BEGIN SLIDE TEXT ---
{slide_text}
--- END SLIDE TEXT ---
"""


# -------------------------------------------------------
# Call OpenAI to generate preview
# -------------------------------------------------------
def generate_preview(text):
    prompt = USER_PROMPT_TEMPLATE.format(slide_text=text)

    response = client.chat.completions.create(
        model="gpt-4.1",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": prompt}
        ],
        temperature=0.2,
    )
    
    return response.choices[0].message.content


# -------------------------------------------------------
# Main
# -------------------------------------------------------
def main():
    lecture_path = "lectures/talk.pdf"

    print(f"Reading PDF: {lecture_path}")
    slide_text = extract_pdf_text(lecture_path)
    
    # Write extracted text to a .txt file
    text_output_path = "lectures/talk_extracted.txt"
    with open(text_output_path, "w") as txt_file:
        txt_file.write(slide_text)
    print(f"Extracted text saved to {text_output_path}")

    print("Calling AI for lecture preview...")
    preview_json_str = generate_preview(slide_text)

    # Save as JSON file
    output_path = "lecture1_preview.json"
    with open(output_path, "w") as f:
        f.write(preview_json_str)

    print(f"\nDone! Preview saved to {output_path}\n")
    print(preview_json_str)


if __name__ == "__main__":
    main()