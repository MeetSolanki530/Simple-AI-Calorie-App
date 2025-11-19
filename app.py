import streamlit as st
import os
import base64
from openai import OpenAI
from dotenv import load_dotenv
from PIL import Image

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")
openai_base_url = os.getenv("OPENAI_BASE_URL")
openai_model = os.getenv("OPENAI_BASE_MODEL")

client = OpenAI(api_key=openai_api_key, base_url=openai_base_url)


def encode_image_to_base64(image):
    return base64.b64encode(image.read()).decode("utf-8")


def analyze_food_image(encoded_image):
    system_prompt = """
You are a nutrition expert that analyzes food images.

Provide JSON ONLY with exact fields:

{
  "Food Name": "",
  "serving_description": "",
  "calories": 0.0,
  "fat_grams": 0.0,
  "protein_grams": 0.0,
  "confidence_level": ""
}

Do NOT add extra text.
"""

    messages = [
        {"role": "system", "content": system_prompt},
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "Analyze this food image."},
                {
                    "type": "image_url",
                    "image_url": {"url": f"data:image/jpeg;base64,{encoded_image}"}
                }
            ]
        },
    ]

    response = client.chat.completions.create(
        model=openai_model,
        messages=messages
    )

    return response.choices[0].message.content


# -------------------------------
# Streamlit UI
# -------------------------------

st.title("🥗 AI Calorie & Nutrition Analyzer")
st.write("Upload a food image and let AI estimate calories & nutrients.")

uploaded_image = st.file_uploader("Upload Food Image", type=["jpg", "jpeg", "png"])

if uploaded_image:
    st.image(uploaded_image, caption="Uploaded Image", use_column_width=True)

    if st.button("Analyze"):
        with st.spinner("Analyzing… thodo wait kar..."):
            encoded = encode_image_to_base64(uploaded_image)
            result = analyze_food_image(encoded)

        st.success("Analysis Complete!")
        st.code(result, language="json")
