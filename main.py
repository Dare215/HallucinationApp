import streamlit as st
from openai import OpenAI
import base64

# ✅ Initialize OpenAI client
client = OpenAI(api_key="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")

# 🎯 Streamlit App UI
st.set_page_config(page_title="Hallucination Correction Assistant", layout="wide")
st.title("🧠 Hallucination Correction Assistant")
st.markdown("This app uses a fine-tuned GPT model to correct hallucinated statements. Enter your input below:")

# 📝 Text input
user_input = st.text_area("Enter a potentially hallucinated response:", height=200)

# 🔍 Button logic
if st.button("Check & Correct") and user_input.strip():
    try:
        # 🧠 Call the fine-tuned model
        response = client.chat.completions.create(
            model="ft:gpt-3.5-turbo-0125:dares-apis:hallucination-logical-v1:BvwmRqwc",
            messages=[
                {"role": "system", "content": "You are a hallucination correction assistant."},
                {"role": "user", "content": user_input}
            ]
        )

        # ✅ Extract and display correction
        corrected = response.choices[0].message.content.strip()

        # 🤖 Confidence estimation (mocked as 95% for demo)
        confidence_score = 0.95
        emoji = "✅" if confidence_score > 0.85 else "⚠️" if confidence_score > 0.5 else "❌"

        # 📊 Side-by-side layout
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("🔍 Original")
            st.code(user_input, language="markdown")

        with col2:
            st.subheader("✅ Corrected")
            st.success(corrected)

        # 📈 Show confidence
        st.subheader("🤖 Confidence Level")
        st.progress(confidence_score)
        st.markdown(f"{emoji} Estimated Confidence: **{int(confidence_score * 100)}%**")

        # 📥 Download corrected output
        def get_text_download_link(text, filename):
            b64 = base64.b64encode(text.encode()).decode()
            return f'<a href="data:file/txt;base64,{b64}" download="{filename}">📥 Download Corrected Output</a>'

        st.markdown(get_text_download_link(corrected, "corrected_output.txt"), unsafe_allow_html=True)

    except Exception as e:
        st.error(f"🚨 An error occurred: {e}")
