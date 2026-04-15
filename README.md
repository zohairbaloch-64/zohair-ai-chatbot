# 🤖 Zohair AI Chatbot

Zohair AI Chatbot is a modern, AI-powered conversational web application built using Streamlit and Groq's LLM API. It provides a clean UI, user authentication, chat history management, and real-time AI responses.

---

## 🚀 Features

- 🔐 User Authentication (Login & Signup)
- 💬 Multiple Chat Sessions
- 🧠 AI-powered Responses (Groq API - LLaMA 3)
- 📝 Automatic Chat Title Generation
- 🔍 Chat Search Functionality
- 📊 Basic Analytics Dashboard
- ⚡ Streaming Typing Effect
- 📱 Responsive UI

---

## 🛠️ Tech Stack

- **Frontend:** Streamlit
- **Backend:** Python
- **Database:** SQLite
- **Authentication:** bcrypt + hashlib
- **AI Model:** Groq (LLaMA 3.3 70B)

---

## 📂 Project Structure


├── app.py
├── chatbot.db
├── requirements.txt
├── README.md
└── .env


---

## 🔐 Security

- Passwords are hashed using SHA-256 + bcrypt
- API keys are stored securely using environment variables / Streamlit secrets
- Sensitive files are excluded using `.gitignore`

---

## ⚙️ Installation

```bash
git clone https://github.com/your-username/zohair-ai-chatbot.git
cd zohair-ai-chatbot
pip install -r requirements.txt
streamlit run app.py
🌍 Deployment

This app can be deployed using:

Streamlit Cloud (recommended)
Render
AWS / VPS
📊 Future Improvements
NLP-based chat title generation
Advanced analytics dashboard
Rate limiting & security enhancements
Dark/Light theme toggle
Export chat history

👨‍💻 Author

Zohair Baloch

⭐ Support

If you like this project, give it a ⭐ on GitHub!