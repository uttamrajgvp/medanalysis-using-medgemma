import os
import requests
import json
import base64
from PIL import Image as PILImage
import streamlit as st
from io import BytesIO
import time

# Ollama configuration
OLLAMA_BASE_URL = "http://localhost:11434/api/generate"
MEDGEMMA_MODEL = "amsaravi/medgemma-4b-it:q6"  # Replace with your specific MedGemma model name

# Medical Analysis Query
medical_analysis_prompt = """
You are a highly skilled medical imaging expert with extensive knowledge in radiology and diagnostic imaging. I will provide you with a text description of a medical image. Please analyze this description and structure your response as follows:

### 1. Image Type & Region
- Identify imaging modality (X-ray/MRI/CT/Ultrasound/etc.) based on the description.
- Specify anatomical region and positioning.
- Evaluate image quality and technical adequacy.

### 2. Key Findings
- Highlight primary observations systematically.
- Identify potential abnormalities with detailed descriptions.
- Include measurements and densities where relevant.

### 3. Diagnostic Assessment
- Provide primary diagnosis with confidence level.
- List differential diagnoses ranked by likelihood.
- Support each diagnosis with observed evidence.
- Highlight critical/urgent findings.

### 4. Patient-Friendly Explanation
- Simplify findings in clear, non-technical language.
- Avoid medical jargon or provide easy definitions.
- Include relatable visual analogies.

### 5. Clinical Recommendations
- Suggest appropriate follow-up studies if needed.
- Recommend consultation with specialists when relevant.
- Provide general treatment considerations.

**Important Notes:**
- This analysis is for educational/research purposes only
- Always consult qualified healthcare professionals for medical decisions
- AI analysis should supplement, not replace, professional medical judgment

Ensure a structured and medically accurate response using clear markdown formatting.
"""

def check_ollama_connection():
    """Check if Ollama is running and accessible"""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=10)
        if response.status_code == 200:
            models = response.json().get("models", [])
            model_names = [model["name"] for model in models]
            return True, model_names
        else:
            return False, []
    except:
        return False, []

def check_model_loaded(model_name):
    """Check if the specified model is loaded in Ollama"""
    is_connected, available_models = check_ollama_connection()
    if not is_connected:
        return False
    
    return any(model_name in model for model in available_models)

def analyze_medical_image(image_path, max_retries=2):
    """Processes and analyzes a medical image using MedGemma via Ollama."""
    retry_count = 0
    last_error = None

    while retry_count <= max_retries:
        try:
            # Load and prepare the image
            image = PILImage.open(image_path)

            # Convert to RGB if not already
            if image.mode != 'RGB':
                image = image.convert('RGB')

            # Resize for optimal clarity (optional, or skip if image is clear)
            width, height = image.size
            aspect_ratio = width / height
            new_width = 800
            new_height = int(new_width / aspect_ratio)
            resized_image = image.resize((new_width, new_height), PILImage.Resampling.LANCZOS)

            # Encode the image as base64
            buffered = BytesIO()
            resized_image.save(buffered, format="JPEG")
            image_b64 = base64.b64encode(buffered.getvalue()).decode('utf-8')

            # Build messages for MedGemma chat-style input
            messages = [
                {
                    "role": "system",
                    "content": [
                        {"type": "text", "text": "You are a highly skilled medical imaging expert."}
                    ]
                },
                {
                    "role": "user",
                    "content": [
                        {"type": "text", "text": f"{medical_analysis_prompt}"},
                        {"type": "image", "image": image_b64}
                    ]
                }
            ]

            payload = {
                "model": MEDGEMMA_MODEL,
                "prompt": messages,
                "stream": False
            }

            response = requests.post(
                OLLAMA_BASE_URL,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=180
            )

            if response.status_code == 200:
                result = response.json()
                response_content = result["response"]

                # Try to extract only structured medical report (starting from ### 1.)
                report_start = response_content.find("### 1.")
                if report_start != -1:
                    cleaned_report = response_content[report_start:]
                else:
                    cleaned_report = response_content

                return cleaned_report
            else:
                last_error = f"❌ Error: HTTP {response.status_code} - {response.text}"

        except requests.exceptions.ConnectionError:
            last_error = "❌ Connection Error: Cannot connect to Ollama. Please ensure it is running at http://localhost:11434"
        except requests.exceptions.Timeout:
            last_error = "❌ Timeout Error: Request to MedGemma took too long."
        except Exception as e:
            last_error = f"⚠️ Unexpected Error: {str(e)}"
        finally:
            retry_count += 1
            time.sleep(2)  # wait before retry

    return f"{last_error} (after {max_retries} retries)"

def analyze_medical_text(text_input, max_retries=2):
    """Analyze medical text/reports using Ollama with retry mechanism"""
    retry_count = 0
    last_error = None
    
    while retry_count <= max_retries:
        try:
            text_analysis_prompt = f"""
You are a medical expert analyzing a medical report or text. Please provide:

### 1. Document Analysis
- Type of medical document
- Key medical findings mentioned
- Relevant medical history

### 2. Clinical Interpretation
- Significant findings and their implications
- Potential diagnoses suggested by the text
- Areas requiring attention

### 3. Patient-Friendly Summary
- Explain findings in simple terms
- Highlight important points for patient understanding

### 4. Recommendations
- Suggested follow-up actions
- Questions to discuss with healthcare provider

**Medical Text to Analyze:**
{text_input}

**Important:** This analysis is for educational purposes only. Always consult healthcare professionals for medical decisions.
"""
            
            payload = {
                "model": MEDGEMMA_MODEL,
                "prompt": text_analysis_prompt,
                "stream": False
            }
            
            response = requests.post(
                OLLAMA_BASE_URL,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=180  # Increased timeout for text analysis
            )
            
            if response.status_code == 200:
                result = response.json()
                return result["response"]
            else:
                last_error = f"❌ Error analyzing text: HTTP {response.status_code} - {response.text}"
                
        except Exception as e:
            last_error = f"❌ Text analysis error: {str(e)}"
        
        retry_count += 1
        if retry_count <= max_retries:
            time.sleep(2)  # Wait before retrying
    
    return f"{last_error} (after {max_retries} retries)"

# Streamlit UI setup
st.set_page_config(
    page_title="MedAnalysis AI - Ollama", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# Header
st.title("🩺 MedAnalysis AI - Local Ollama Edition 🔬")
st.markdown(
    """
    Welcome to **MedAnalysis AI**! This tool uses your local Ollama instance with MedGemma model to analyze:
    - 📸 **Medical Images** (X-rays, MRIs, CT scans, Ultrasounds, etc.)
    - 📄 **Medical Text Reports**
    
    *Powered by local AI for enhanced privacy and control.*
    """
)

# Check Ollama connection
st.sidebar.header("🔗 Ollama Connection")
is_connected, available_models = check_ollama_connection()
model_loaded = check_model_loaded(MEDGEMMA_MODEL)

if is_connected:
    st.sidebar.success("✅ Ollama is connected!")
    st.sidebar.write("**Available Models:**")
    for model in available_models:
        if model == MEDGEMMA_MODEL:
            st.sidebar.write(f"🩺 {model} ✓")
        elif "medgemma" in model.lower() or "medical" in model.lower():
            st.sidebar.write(f"🩺 {model}")
        else:
            st.sidebar.write(f"• {model}")
    
    if not model_loaded:
        st.sidebar.warning(f"⚠️ Required model '{MEDGEMMA_MODEL}' is not loaded.")
        st.sidebar.markdown(f"Run this command to load the model: `ollama pull {MEDGEMMA_MODEL}`")
else:
    st.sidebar.error("❌ Cannot connect to Ollama")
    st.sidebar.write("Please ensure Ollama is running on localhost:11434")
    st.sidebar.code("ollama serve", language="bash")

# Analysis type selection
st.sidebar.header("📋 Analysis Type")
analysis_type = st.sidebar.radio(
    "Choose analysis type:",
    ("Medical Image Analysis", "Medical Text Analysis")
)

if analysis_type == "Medical Image Analysis":
    st.header("📸 Medical Image Analysis")
    
    # Upload image section
    st.sidebar.header("Upload Medical Image:")
    uploaded_file = st.sidebar.file_uploader(
        "Choose a medical image file", 
        type=["jpg", "jpeg", "png", "bmp", "gif", "tiff", "dcm"]
    )
    
    if uploaded_file is not None:
        # Display the uploaded image
        col1, col2 = st.columns([1, 1])
        
        with col1:
            st.subheader("📋 Uploaded Image")
            st.image(uploaded_file, caption="Medical Image for Analysis", use_container_width=True)
        
        with col2:
            st.subheader("📊 Image Information")
            file_details = {
                "Filename": uploaded_file.name,
                "File Type": uploaded_file.type,
                "File Size": f"{uploaded_file.size / 1024:.1f} KB"
            }
            for key, value in file_details.items():
                st.write(f"**{key}:** {value}")
        
        # Analysis button
        if st.sidebar.button("🔍 Analyze Medical Image", type="primary"):
            if not is_connected:
                st.error("❌ Cannot analyze: Ollama is not connected. Please start Ollama and refresh the page.")
            elif not model_loaded:
                st.error(f"❌ Required model '{MEDGEMMA_MODEL}' is not loaded. Please run `ollama pull {MEDGEMMA_MODEL}` first.")
            else:
                with st.spinner("🔍 Analyzing medical image... This may take 1-5 minutes depending on your hardware."):
                    # Save the uploaded image to a temporary file
                    image_path = f"temp_uploaded_image.{uploaded_file.type.split('/')[1]}"
                    with open(image_path, "wb") as f:
                        f.write(uploaded_file.getbuffer())
                    
                    # Run analysis on the uploaded image
                    report = analyze_medical_image(image_path)
                    
                    # Display the report
                    if "❌" in report or "⚠️" in report:
                        st.error(report)
                        st.info("If you're experiencing timeout errors, try restarting Ollama or increasing the timeout value in the code.")
                    else:
                        st.subheader("📋 Medical Analysis Report")
                        st.markdown(report)
                    
                    # Clean up the saved image file
                    if os.path.exists(image_path):
                        os.remove(image_path)
    else:
        st.info("⬆️ Please upload a medical image using the sidebar to begin analysis.")

else:  # Medical Text Analysis
    st.header("📄 Medical Text Analysis")
    
    st.markdown("Enter medical text, reports, or clinical notes for AI analysis:")
    
    text_input = st.text_area(
        "Medical Text/Report:",
        height=200,
        placeholder="Enter medical report, clinical notes, or medical text here..."
    )
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        analyze_text_btn = st.button("🔍 Analyze Medical Text", type="primary")
    
    if analyze_text_btn:
        if not text_input.strip():
            st.warning("⚠️ Please enter some medical text to analyze.")
        elif not is_connected:
            st.error("❌ Cannot analyze: Ollama is not connected. Please start Ollama and refresh the page.")
        elif not model_loaded:
            st.error(f"❌ Required model '{MEDGEMMA_MODEL}' is not loaded. Please run `ollama pull {MEDGEMMA_MODEL}` first.")
        else:
            with st.spinner("🔍 Analyzing medical text... This may take 1-3 minutes depending on your hardware."):
                report = analyze_medical_text(text_input)
                
                if "❌" in report or "⚠️" in report:
                    st.error(report)
                    st.info("If you're experiencing timeout errors, try restarting Ollama or increasing the timeout value in the code.")
                else:
                    st.subheader("📋 Medical Text Analysis Report")
                    st.markdown(report)

# Footer
st.markdown("---")
st.markdown(
    """
    <div style='text-align: center; color: #666; font-size: 0.9em;'>
        <p><strong>⚠️ Medical Disclaimer:</strong> This tool is for educational and research purposes only. 
        Always consult qualified healthcare professionals for medical diagnosis and treatment decisions.</p>
        <p>Powered by MedGemma Model • Made by CoolDude</p>
    </div>
    """, 
    unsafe_allow_html=True
)