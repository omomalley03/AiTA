import os
import json
from pypdf import PdfReader
from anthropic import Anthropic
from dotenv import load_dotenv

# -------------------------------------------------------
# Load API key
# -------------------------------------------------------
load_dotenv()
client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

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
Your task is to transform university lecture slides into:

1. Structured JSON for internal app processing
2. A helpful, human-readable lecture preview with clear sections, equations, explanations, and conceptual scaffolding — similar to high-quality teaching notes.


Your response must be valid JSON following this exact schema:

{
  "main_topics": [],
  "what_you_will_learn": [],
  "key_definitions": [],
  "prereq_refreshers": [],
  "questions_to_keep_in_mind": [],
  "warmup_check_questions": [],
  "human_readable_summary": ""
}

Requirements for human_readable_summary:
- Write in a friendly, structured, pedagogical tone.
- Use section dividers (⸻), headings, and bullet points.
- Include inline mathematical equations (if appropriate) using LaTeX-like syntax (e.g., P(x) = e^{-E(x)}/Z).
- Provide intuitive explanations, not only definitions.
- Break the lecture into logical parts (e.g., Part 1, Part 2, Part 3).
- Include:
  • Big-picture motivation
  • Key equations and derivations
  • Algorithm descriptions (numbered steps if appropriate)
  • Conceptual interpretations (“why this matters”)
  • Small worked examples, if present in slides
- Produce something that reads like a professor’s high-quality lecture overview.

Only use information grounded in the provided lecture slides.
"""

USER_PROMPT_TEMPLATE = """
Below is the extracted text from the lecture slides.
Generate the lecture preview according to the JSON schema.

--- BEGIN SLIDE TEXT ---
{slide_text}
--- END SLIDE TEXT ---
"""


# -------------------------------------------------------
# Call Anthropic to generate preview
# -------------------------------------------------------
def generate_preview(text):
    prompt = USER_PROMPT_TEMPLATE.format(slide_text=text)

    response = client.messages.create(
        model="claude-opus-4-5-20251101",
        system=SYSTEM_PROMPT,
        messages=[{"role": "user", "content": prompt}],
        max_tokens=4096,
        temperature=0.2,
    )

    # Anthropic returns content as a list of text blocks
    return response.content[0].text
def clean_json_output(s: str) -> str:
    """
    Remove leading ```json or ``` and any trailing ``` from LLM output.
    """
    s = s.strip()
    if s.startswith("```json"):
        s = s[len("```json"):].strip()
    elif s.startswith("```"):
        s = s[len("```"):].strip()
    if s.endswith("```"):
        s = s[:-3].strip()
    return s

def save_summary_markdown(json_path: str, output_path: str):
    """
    Load lecture.json, extract the human_readable_summary field,
    and save it as a markdown (.md) file with the same file name as the json but with .md.
    """
    if not os.path.exists(json_path):
        print(f"JSON file not found: {json_path}")
        return

    try:
        with open(json_path, "r") as jf:
            data = json.load(jf)

        summary = data.get("human_readable_summary", "")
        if not summary:
            print("No 'human_readable_summary' field found in JSON.")
            return

        with open(output_path, "w") as md_file:
            md_file.write(summary)

        print(f"Markdown summary saved to {output_path}")

    except Exception as e:
        print("Failed to read JSON or write markdown:", e)



# -------------------------------------------------------
# Main
# -------------------------------------------------------
def main():
    lecture_name = "discrete.pdf"
    lecture_path = "lectures/"+lecture_name

    print(f"Reading PDF: {lecture_path}")
    slide_text = extract_pdf_text(lecture_path)

    # Write extracted text to a .txt file
    text_output_path = lecture_path.replace(".pdf",".txt")
    with open(text_output_path, "w") as txt_file:
        txt_file.write(slide_text)
    print(f"Extracted text saved to {text_output_path}")

    print("Calling AI for lecture preview...")
    preview_json_str = generate_preview(slide_text)
    preview_json_str = clean_json_output(preview_json_str)
    # Save as JSON file
    output_path = "previews/preview_"+lecture_name.replace(".pdf",".json")
    with open(output_path, "w") as f:
        f.write(preview_json_str)

    print(f"\nDone! Preview saved to {output_path}\n")
    print(preview_json_str)

    save_summary_markdown(output_path, output_path.replace(".json",".md"))




if __name__ == "__main__":
    main()