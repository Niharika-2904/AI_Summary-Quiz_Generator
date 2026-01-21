from openai import OpenAI
from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

client = OpenAI(
    api_key=os.getenv("GROQ_API_KEY"),
    base_url="https://api.groq.com/openai/v1"
)

def _call_api(text_chunk, prompt):
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": text_chunk}
        ]
    )
    return response.choices[0].message.content.strip()

def split_text(text, max_words=700):
    """
    Splits text into chunks of up to max_words words.
    """
    words = text.split()
    for i in range(0, len(words), max_words):
        yield ' '.join(words[i:i + max_words])

def get_summary(text):
    """
    Generate a clear, concise summary of the given text.
    If the text is too long, splits it into chunks and summarizes each.
    """
    prompt = "Summarize the following PDF text clearly and concisely:"
    max_words = 700

    if len(text.split()) <= max_words:
        return _call_api(text, prompt)

    summaries = []
    for chunk in split_text(text, max_words):
        summaries.append(_call_api(chunk, prompt))

    # Combine the chunk summaries into a final concise one
    final_summary = _call_api('\n\n'.join(summaries), 
                              "Summarize the following partial summaries into one concise summary:")
    return final_summary


def generate_quiz(text):
    """
    Generate a 5-question multiple choice quiz with answers from the given text.
    Uses the summary as the quiz source to avoid token overflow.
    Returns a JSON string with clear correct answers.
    """
    # Step 1 — Generate concise summary first
    summary = get_summary(text)

    # Step 2 — Build quiz prompt
    prompt = (
        "From the following text, create a 5-question multiple choice quiz. "
        "For each question, provide exactly 4 options labelled (A), (B), (C), (D), and specify the correct answer as one of A/B/C/D. "
        "Return the quiz in **valid JSON** format with this structure:\n\n"
        "{\n"
        "  \"quiz\": [\n"
        "    {\n"
        "      \"question\": \"Question text here\",\n"
        "      \"options\": [\"A. option1\", \"B. option2\", \"C. option3\", \"D. option4\"],\n"
        "      \"answer\": \"A\"\n"
        "    },\n"
        "    ...\n"
        "  ]\n"
        "}\n\n"
        "Do not include any explanations or text outside the JSON object."
    )

    # Step 3 — Call API with summary
    quiz_json = _call_api(summary, prompt)
    return quiz_json
