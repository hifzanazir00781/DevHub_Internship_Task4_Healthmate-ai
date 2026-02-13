import streamlit as st
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
import time
from datetime import datetime
import random

# --- UI Configuration ---
st.set_page_config(
    page_title="HealthMate AI - Your Virtual Health Assistant", 
    page_icon="⚕️", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Custom CSS ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    .stApp {
        font-family: 'Poppins', sans-serif;
        background: linear-gradient(145deg, #f0f4f8 0%, #d9e2ec 100%);
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(165deg, #0f172a 0%, #1e293b 100%);
        border-right: 3px solid #3b82f6;
    }
    
    .sidebar-header {
        background: linear-gradient(135deg, #2563eb 0%, #7c3aed 100%);
        padding: 2rem 1.5rem;
        border-radius: 0 0 30px 30px;
        margin-bottom: 1.5rem;
        text-align: center;
        box-shadow: 0 10px 25px rgba(0,0,0,0.3);
        border-bottom: 3px solid #fbbf24;
    }
    
    .sidebar-header h2 { color: white; font-size: 1.8rem; font-weight: 700; margin-bottom: 0.5rem; }
    .sidebar-header p { color: #fef9c3; font-size: 1rem; background: rgba(0,0,0,0.2); padding: 0.3rem 1rem; border-radius: 50px; display: inline-block; }
    
    .status-container {
        background: #1e293b;
        padding: 1.2rem;
        border-radius: 15px;
        margin: 1rem 0;
        border-left: 5px solid #10b981;
    }
    
    .online-dot {
        display: inline-block; width: 12px; height: 12px;
        background: #10b981; border-radius: 50%; margin-right: 8px;
        animation: blink 2s infinite; box-shadow: 0 0 10px #10b981;
    }
    
    @keyframes blink { 0%, 100% { opacity: 1; } 50% { opacity: 0.5; } }
    
    .message-bubble { padding: 1rem 1.5rem; border-radius: 20px; margin-bottom: 1rem; max-width: 80%; font-size: 0.95rem; line-height: 1.5; }
    .user-bubble { background: linear-gradient(135deg, #2563eb, #1e4b8f); color: white; margin-left: auto; border-bottom-right-radius: 5px; }
    .assistant-bubble { background: white; color: #1e293b; margin-right: auto; border-bottom-left-radius: 5px; border-left: 5px solid #2563eb; box-shadow: 0 5px 15px rgba(0,0,0,0.1); }
    
    .main-header {
        background: linear-gradient(135deg, #1e4b8f 0%, #2563eb 100%);
        padding: 2rem; border-radius: 30px; margin-bottom: 2rem; text-align: center;
    }
    .main-header h1 { color: white; margin: 0; }
    .main-header p { color: #fef9c3; }

    .stButton button { width: 100%; border-radius: 10px; }
    </style>
""", unsafe_allow_html=True)

# --- Sidebar ---
with st.sidebar:
    st.markdown('<div class="sidebar-header"><h2>⚕️ HealthMate AI</h2><p>Created by Hifza Nazir</p></div>', unsafe_allow_html=True)
    st.markdown('<div class="status-container"><span class="online-dot"></span><span style="color:white;">AI Assistant Online</span><p style="color:#94a3b8; font-size:0.8rem;">✓ Ready to help 24/7</p></div>', unsafe_allow_html=True)
    
    st.markdown('<p style="color:#fbbf24; font-weight:600; margin-top:10px;">📋 Quick Actions</p>', unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    with col1:
        if st.button("🏥 Hospitals"): st.sidebar.info("Finding hospitals...")
    with col2:
        if st.button("📞 Emergency"): st.sidebar.warning("Call: 1122")

    st.markdown('<div style="background:#312e81; padding:1rem; border-radius:15px; margin-top:20px;">'
                '<h4 style="color:#fef9c3; margin:0;">⚠️ Disclaimer</h4>'
                '<p style="color:#e2e8f0; font-size:0.8rem;">General info only. Consult a doctor for medical advice.</p></div>', unsafe_allow_html=True)

# --- Model Loading ---
@st.cache_resource
def load_model():
    model_path = r"D:\tinyllama_model"
    tokenizer = AutoTokenizer.from_pretrained(model_path)
    model = AutoModelForCausalLM.from_pretrained(
        model_path,
        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
        device_map="auto"
    )
    return pipeline("text-generation", model=model, tokenizer=tokenizer), tokenizer

try:
    pipe, tokenizer = load_model()
except Exception as e:
    st.error(f"Error loading model: {e}")

# --- Chat Logic ---
def health_chatbot(user_query):
    emergency_keywords = ["chest pain", "heart attack", "stroke", "not breathing", "severe bleeding"]
    is_emergency = any(k in user_query.lower() for k in emergency_keywords)

    full_prompt = (
        f"<|system|>\nYou are HealthMate AI, a medical assistant. Provide clear info and a disclaimer.<|end|>\n"
        f"<|user|>\n{user_query}<|end|>\n"
        f"<|assistant|>\n"
    )

    with st.spinner("🤔 Thinking..."):
        outputs = pipe(
            full_prompt, 
            max_new_tokens=250, 
            do_sample=True, 
            temperature=0.7,
            top_p=0.9,
            repetition_penalty=1.2,
            pad_token_id=tokenizer.eos_token_id,
            eos_token_id=tokenizer.eos_token_id
        )
        
    response = outputs[0]["generated_text"].split("<|assistant|>\n")[-1].strip()
    
    if is_emergency:
        emergency_html = '<div style="background:red; color:white; padding:10px; border-radius:10px; font-weight:bold;">🚨 EMERGENCY: CALL 1122 NOW!</div><br>'
        response = emergency_html + response

    return response

# --- Chat Interface ---
st.markdown('<div class="main-header"><h1>🏥 HealthMate AI Assistant</h1><p>Your Intelligent Virtual Health Companion</p></div>', unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "👋 Hello! I'm HealthMate AI. How can I help?", "time": datetime.now().strftime("%I:%M %p")}]

for msg in st.session_state.messages:
    div_class = "user-bubble" if msg["role"] == "user" else "assistant-bubble"
    align = "flex-end" if msg["role"] == "user" else "flex-start"
    st.markdown(f'<div style="display: flex; justify-content: {align};"><div class="message-bubble {div_class}">{msg["content"]}<br><small style="opacity:0.6;">{msg["time"]}</small></div></div>', unsafe_allow_html=True)

# Quick Questions
cols = st.columns(4)
questions = ["Fever Symptoms", "Cold vs Flu", "Healthy Diet", "Sleep Tips"]
for i, q in enumerate(questions):
    if cols[i].button(q):
        st.session_state.pending_prompt = q

# Input
user_input = st.chat_input("Ask about your health...")
if user_input or "pending_prompt" in st.session_state:
    prompt = user_input if user_input else st.session_state.pop("pending_prompt")
    st.session_state.messages.append({"role": "user", "content": prompt, "time": datetime.now().strftime("%I:%M %p")})
    res = health_chatbot(prompt)
    st.session_state.messages.append({"role": "assistant", "content": res, "time": datetime.now().strftime("%I:%M %p")})
    st.rerun()

if st.button("🔄 Clear Conversation"):
    st.session_state.messages = []
    st.rerun()