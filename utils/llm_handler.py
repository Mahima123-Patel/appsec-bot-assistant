from transformers import pipeline

# Use lightweight model
qa_model = pipeline("text2text-generation", model="google/flan-t5-base")

def get_remediation_response(vuln_type, comment_text):
    prompt = f"How can I fix a {vuln_type} vulnerability?"
    try:
        result = qa_model(prompt, max_length=100)[0]['generated_text']
        return result.strip()
    except Exception as e:
        return f"Error using Hugging Face model: {e}"




# from transformers import pipeline

# # Light, fast model (loads quickly and works great)
# qa_model = pipeline("text2text-generation", model="google/flan-t5-base")

# def get_remediation_response(vuln_type, comment_text):
#     prompt = f"Remediation advice for {vuln_type}. Developer said: {comment_text}"
#     try:
#         result = qa_model(prompt, max_length=100)[0]['generated_text']
#         return result
#     except Exception as e:
#         return f"Error using Hugging Face model: {e}"



# import openai
# import os
# from dotenv import load_dotenv

# load_dotenv()
# openai.api_key = os.getenv("OPENAI_API_KEY")

# def get_remediation_response(vuln_type, comment_text):
#     prompt = f"Provide remediation advice for a {vuln_type} vulnerability. Developer said: {comment_text}"
#     try:
#         response = openai.ChatCompletion.create(
#             model="gpt-3.5-turbo",
#             messages=[{"role": "user", "content": prompt}],
#             max_tokens=150,
#             temperature=0.3
#         )
#         return response['choices'][0]['message']['content'].strip()
#     except Exception as e:
#         return f"Error calling OpenAI: {e}"
