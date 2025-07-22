# 🩺 MedAnalysis AI - Local Ollama Edition

A powerful, privacy-focused medical imaging and text analysis tool powered by local AI. This application uses Ollama with the MedGemma model to provide comprehensive analysis of medical images and clinical text reports.

![License](https://img.shields.io/badge/license-Apache%202.0-blue.svg)
![Python](https://img.shields.io/badge/python-3.8+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-latest-red.svg)

## ✨ Features

### 📸 Medical Image Analysis
- **Multi-format Support**: X-rays, MRIs, CT scans, Ultrasounds, and more
- **Comprehensive Reports**: Detailed analysis including image type, key findings, diagnostic assessment, and patient-friendly explanations
- **File Format Support**: JPG, PNG, TIFF, DICOM, and other common medical imaging formats
- **Intelligent Processing**: Automatic image optimization and preprocessing

### 📄 Medical Text Analysis
- **Clinical Report Processing**: Analyze medical reports, clinical notes, and documentation
- **Structured Output**: Organized analysis with clinical interpretation and recommendations
- **Patient-Friendly Summaries**: Complex medical information simplified for patient understanding

### 🔒 Privacy & Security
- **100% Local Processing**: All analysis runs locally on your machine
- **No Data Upload**: Your medical data never leaves your computer
- **HIPAA-Friendly**: Suitable for healthcare environments requiring data privacy

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- [Ollama](https://ollama.com/) installed and running
- MedGemma model pulled in Ollama

### Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/uttamrajgvp/medanalysis-ai.git
   cd medanalysis-ai
   ```

2. **Install Python dependencies:**
   ```bash
   pip install streamlit requests pillow
   ```

3. **Install and setup Ollama:**
   ```bash
   # Install Ollama (visit https://ollama.ai for platform-specific instructions)
   
   # Start Ollama service
   ollama serve
   
   # Pull the MedGemma model
   ollama pull amsaravi/medgemma-4b-it:q6
   ```

4. **Run the application:**
   ```bash
   streamlit run medanalysis_ollama.py
   ```

5. **Open your browser and navigate to:**
   ```
   http://localhost:8501
   ```

## 📋 Usage Guide

### Medical Image Analysis

1. **Upload Image**: Use the sidebar to upload your medical image
2. **Review Image**: Preview the uploaded image and file details
3. **Analyze**: Click "Analyze Medical Image" to start the AI analysis
4. **Review Results**: Get comprehensive analysis including:
   - Image type and technical assessment
   - Key medical findings
   - Diagnostic assessment with confidence levels
   - Patient-friendly explanations
   - Clinical recommendations

### Medical Text Analysis

1. **Enter Text**: Paste your medical report or clinical notes
2. **Analyze**: Click "Analyze Medical Text"
3. **Review Results**: Get structured analysis including:
   - Document type identification
   - Clinical interpretation
   - Patient-friendly summary
   - Follow-up recommendations

## 🛠️ Configuration

### Model Configuration
The application uses the MedGemma model by default. You can modify the model in the configuration:

```python
MEDGEMMA_MODEL = "amsaravi/medgemma-4b-it:q6"
```

### Ollama Configuration
The application connects to Ollama at `http://localhost:11434` by default. Modify if your Ollama instance runs elsewhere:

```python
OLLAMA_BASE_URL = "http://localhost:11434/api/generate"
```

## 📁 Project Structure

```
medanalysis-ai/
├── medanalysis_ollama.py    # Main Streamlit application
├── LICENSE                  # Apache 2.0 License
├── README.md               # Project documentation
└── requirements.txt        # Python dependencies (create if needed)
```

## 🔧 System Requirements

### Minimum Requirements
- **RAM**: 8GB (16GB recommended for optimal performance)
- **Storage**: 5GB free space for model storage
- **CPU**: Multi-core processor (GPU acceleration optional but recommended)

### Recommended Setup
- **RAM**: 16GB or higher
- **GPU**: NVIDIA GPU with CUDA support for faster processing
- **Storage**: SSD for better model loading performance

## 🚨 Important Medical Disclaimer

**⚠️ FOR EDUCATIONAL AND RESEARCH PURPOSES ONLY**

This tool is designed for educational and research purposes. It should **NEVER** be used as a substitute for professional medical advice, diagnosis, or treatment. Key points:

- Always consult qualified healthcare professionals for medical decisions
- AI analysis should supplement, not replace, professional medical judgment
- This tool is not FDA-approved for clinical diagnosis
- Results should be validated by medical professionals
- Not suitable for emergency medical situations

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request. For major changes, please open an issue first to discuss what you would like to change.

## 📝 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## 🐛 Troubleshooting

### Common Issues

**Ollama Connection Error:**
```bash
# Ensure Ollama is running
ollama serve

# Check if the service is accessible
curl http://localhost:11434/api/tags
```

**Model Not Found:**
```bash
# Pull the required model
ollama pull amsaravi/medgemma-4b-it:q6

# List available models
ollama list
```

**Performance Issues:**
- Ensure adequate RAM (16GB recommended)
- Close unnecessary applications
- Consider using GPU acceleration if available

**Timeout Errors:**
- Increase timeout values in the code
- Ensure your system meets minimum requirements
- Try with smaller image files

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/yourusername/medanalysis-ai/issues) section
2. Create a new issue with detailed information about your problem
3. Include system specifications and error messages

## 🙏 Acknowledgments

- **MedGemma Team**: For developing the medical-focused language model
- **Ollama Team**: For providing the excellent local AI platform
- **Streamlit Team**: For the user-friendly web framework
- **Healthcare Community**: For feedback and validation

## 🔮 Roadmap

- [ ] Support for DICOM file processing
- [ ] Batch processing capabilities
- [ ] Integration with more medical AI models
- [ ] Enhanced visualization features
- [ ] Multi-language support
- [ ] API endpoints for integration

---

<div align="center">
  <p><strong>Made with ❤️ for the Medical Community</strong></p>
  <p><em>Empowering healthcare through accessible AI technology</em></p>
</div>
