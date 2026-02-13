# ⚕️ HealthMate AI - Virtual Health Assistant
**Organization:** DevelopersHub Corporation | **AI/ML Internship Task 4**

HealthMate AI is a specialized medical chatbot designed to provide instant, science-based health information. This project focuses on **Prompt Engineering** and the deployment of open-source Large Language Models (LLMs) to create a safe, empathetic, and professional medical assistant.

---

## 🎯 Project Objective
The goal of this task was to develop a functional AI Health Assistant that:
* Answers general medical queries using the **TinyLlama-1.1B-Chat** model.
* Demonstrates advanced **Prompt Engineering** to control AI behavior and tone.
* Prioritizes user safety by integrating medical disclaimers and emergency protocols.
* Operates locally without relying on expensive external APIs.

---

## 📸 Project Screenshots

### 🖥️ Main User Interface
![Main UI](screenshots/chat_interface.jfif)
*A modern, intuitive Streamlit interface designed for seamless user interaction.*

### 💬 AI Response & Logic
![AI Response](screenshots/AI_response.jfif)
*Empathetic, structured, and informative health guidance with embedded safety disclaimers.*

---

## 🛠️ Methodology & Tools
* **Model:** `TinyLlama-1.1B-Chat` (Open-source model via Hugging Face).
* **Interface:** `Streamlit` (Web-based Python framework).
* **Deployment:** Local inference using `transformers`, `torch`, and `accelerate` libraries.
* **Environment:** Developed and tested using Google Colab and Local VS Code environment.

---

## 🛡️ Safety & Prompt Engineering
The AI's personality is "programmed" through a robust System Prompt, ensuring it:
1.  **Professionalism:** Acts as a knowledgeable and supportive medical assistant.
2.  **Accuracy:** Provides information based on scientific medical data.
3.  **Mandatory Disclaimer:** Always reminds users: *"I am an AI, not a doctor."*
4.  **Emergency Awareness:** Identifies urgent symptoms and directs users to seek immediate professional medical help.

---

## 🚀 How to Run Locally

1. **Clone the Repository:**
   ```bash
   git clone [https://github.com/hifzanazir00781/DevHub_Internship_Task4_Healthmate-ai.git](https://github.com/hifzanazir00781/DevHub_Internship_Task4_Healthmate-ai.git)
   cd DevHub_Internship_Task4_Healthmate-ai
