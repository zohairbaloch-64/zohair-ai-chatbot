import streamlit as st
from groq import Groq
import os
from dotenv import load_dotenv
from datetime import datetime
import sqlite3
import uuid
import hashlib
import bcrypt

# ================= CONFIG =================
st.set_page_config(page_title="Zohair AI Chatbot", layout="wide")
load_dotenv()
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

# ================= DATABASE =================
conn = sqlite3.connect("chatbot.db", check_same_thread=False)
c = conn.cursor()

c.execute("CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT UNIQUE, password TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS chats (id TEXT PRIMARY KEY, user_id INTEGER, title TEXT)")
c.execute("CREATE TABLE IF NOT EXISTS messages (id TEXT PRIMARY KEY, chat_id TEXT, role TEXT, content TEXT, time TEXT)")
conn.commit()

# ================= SECURITY =================
def hash_password(password):
    return bcrypt.hashpw(hashlib.sha256(password.encode()).hexdigest().encode(), bcrypt.gensalt()).decode()

def verify_password(password, hashed):
    return bcrypt.checkpw(hashlib.sha256(password.encode()).hexdigest().encode(), hashed.encode())

# ================= SESSION =================
if "user" not in st.session_state:
    st.session_state.user = None
if "page" not in st.session_state:
    st.session_state.page = "login"
if "chat_id" not in st.session_state:
    st.session_state.chat_id = None
if "edit_chat" not in st.session_state:
    st.session_state.edit_chat = None
if "show_sidebar" not in st.session_state:
    st.session_state.show_sidebar = True

# ================= CSS (FIXED VISIBILITY) =================
st.markdown("""
<style>
header {visibility:hidden;}

body {
    background:#0f172a;
    color:#f8fafc;
    font-family: Inter, sans-serif;
}

/* CHAT BUBBLES */
.chat-user {
    background:#2563eb;
    color:#ffffff;
    padding:14px 16px;
    border-radius:14px;
    margin:10px 0;
    max-width:65%;
    margin-left:auto;
    font-size:15px;
    line-height:1.6;
    box-shadow:0 4px 20px rgba(0,0,0,0.4);
}

.chat-ai {
    background:#334155;  /* brighter for contrast */
    color:#f1f5f9;
    padding:14px 16px;
    border-radius:14px;
    margin:10px 0;
    max-width:65%;
    font-size:15px;
    line-height:1.6;
    box-shadow:0 4px 20px rgba(0,0,0,0.4);
}

/* MARKDOWN FIX */
.chat-ai p {
    margin:0;
}

/* CODE BLOCKS */
.chat-ai code {
    background:#020617;
    color:#38bdf8;
    padding:4px 6px;
    border-radius:6px;
}

.chat-ai pre {
    background:#020617;
    padding:10px;
    border-radius:10px;
    overflow-x:auto;
}

/* INPUT */
.stTextInput input {
    background:#1e293b !important;
    color:white !important;
}

/* SIDEBAR */
section[data-testid="stSidebar"] {
    background:#020617;
    border-right:1px solid #1e293b;
}

/* BUTTON */
.stButton>button {
    background:transparent;
    color:#cbd5f5;
}
.stButton>button:hover {
    background:#1e293b;
    color:white;
}

/* CHAT INPUT */
[data-testid="stChatInput"] {
    background:#0f172a;
}

/* MOBILE */
@media (max-width: 768px) {
    .chat-user, .chat-ai {
        max-width:90%;
    }
}
</style>
""", unsafe_allow_html=True)

# ================= LOGIN =================
if st.session_state.page == "login":
    col1,col2,col3 = st.columns([1,2,1])
    with col2:
        st.markdown("## 🔐 Zohair AI Chatbot")

        username = st.text_input("Username", key="login_user")
        password = st.text_input("Password", type="password", key="login_pass")

        if st.button("Login", key="login_btn"):
            c.execute("SELECT * FROM users WHERE username=?", (username,))
            user = c.fetchone()
            if user and verify_password(password, user[2]):
                st.session_state.user = user
                st.session_state.page = "chat"
                st.rerun()
            else:
                st.error("Invalid credentials")

        if st.button("Signup", key="goto_signup"):
            st.session_state.page = "signup"
            st.rerun()

# ================= SIGNUP =================
elif st.session_state.page == "signup":
    col1,col2,col3 = st.columns([1,2,1])
    with col2:
        st.markdown("## Signup")

        username = st.text_input("Username", key="signup_user")
        password = st.text_input("Password", type="password", key="signup_pass")

        if st.button("Create", key="create_btn"):
            try:
                c.execute("INSERT INTO users VALUES (NULL,?,?)", (username, hash_password(password)))
                conn.commit()
                st.success("Account created")
            except:
                st.error("User exists")

        if st.button("Back", key="back_login"):
            st.session_state.page = "login"
            st.rerun()

# ================= CHAT =================
elif st.session_state.page == "chat":

    user_id = st.session_state.user[0]

    col1,col2,col3 = st.columns([1,6,1])

    with col1:
        if st.button("☰", key="menu_btn"):
            st.session_state.show_sidebar = not st.session_state.show_sidebar

    with col2:
        st.markdown("### 🤖 Zohair AI")

    # SIDEBAR
    if st.session_state.show_sidebar:

        st.sidebar.title("💬 Chats")

        if st.sidebar.button("🚪 Logout", key="logout_btn"):
            st.session_state.user = None
            st.session_state.page = "login"
            st.rerun()

        search = st.sidebar.text_input("🔍 Search", key="search_box")

        if st.sidebar.button("➕ New Chat", key="new_chat"):
            chat_id = str(uuid.uuid4())
            c.execute("INSERT INTO chats VALUES (?,?,?)",(chat_id,user_id,"New Chat"))
            conn.commit()
            st.session_state.chat_id = chat_id

        c.execute("SELECT id,title FROM chats WHERE user_id=?", (user_id,))
        chats = c.fetchall()

        if search:
            chats = [chat for chat in chats if search.lower() in chat[1].lower()]

        for chat in chats:
            col1,col2,col3 = st.sidebar.columns([5,1,1])

            if col1.button(chat[1], key=f"chat_{chat[0]}"):
                st.session_state.chat_id = chat[0]

            if col2.button("✏️", key=f"edit_{chat[0]}"):
                st.session_state.edit_chat = chat[0]

            if col3.button("🗑️", key=f"delete_{chat[0]}"):
                c.execute("DELETE FROM chats WHERE id=?", (chat[0],))
                c.execute("DELETE FROM messages WHERE chat_id=?", (chat[0],))
                conn.commit()
                st.rerun()

        if st.session_state.edit_chat:
            new = st.sidebar.text_input("Rename chat", key="rename_input")
            if st.sidebar.button("Save", key="rename_save"):
                c.execute("UPDATE chats SET title=? WHERE id=?", (new, st.session_state.edit_chat))
                conn.commit()
                st.session_state.edit_chat = None
                st.rerun()

    # CHAT
    if not st.session_state.chat_id:
        st.info("Select a chat")
        st.stop()

    chat_id = st.session_state.chat_id

    c.execute("SELECT role,content FROM messages WHERE chat_id=?", (chat_id,))
    messages = c.fetchall()

    for role, content in messages:
        if role=="user":
            st.markdown(f"<div class='chat-user'>{content}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='chat-ai'>{content}</div>", unsafe_allow_html=True)

    prompt = st.chat_input("Message Zohair AI...")

    if prompt:
        c.execute("INSERT INTO messages VALUES (?,?,?,?,?)",
                  (str(uuid.uuid4()),chat_id,"user",prompt,str(datetime.now())))
        conn.commit()

        st.markdown(f"<div class='chat-user'>{prompt}</div>", unsafe_allow_html=True)

        placeholder = st.empty()
        placeholder.markdown("<div class='chat-ai'>Typing...</div>", unsafe_allow_html=True)

        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[{"role":r,"content":c} for r,c in messages]+[{"role":"user","content":prompt}]
        )

        reply = response.choices[0].message.content

        full = ""
        for char in reply:
            full += char
            placeholder.markdown(f"<div class='chat-ai'>{full}▌</div>", unsafe_allow_html=True)

        placeholder.markdown(f"<div class='chat-ai'>{full}</div>", unsafe_allow_html=True)

        if len(messages) < 2:
            c.execute("UPDATE chats SET title=? WHERE id=?", (prompt[:30], chat_id))
            conn.commit()

        c.execute("INSERT INTO messages VALUES (?,?,?,?,?)",
                  (str(uuid.uuid4()),chat_id,"assistant",reply,str(datetime.now())))
        conn.commit()

    # ANALYTICS
    st.sidebar.markdown("---")
    st.sidebar.title("📊 Analytics")

    c.execute("SELECT COUNT(*) FROM chats WHERE user_id=?", (user_id,))
    st.sidebar.metric("Chats", c.fetchone()[0])

    c.execute("SELECT COUNT(*) FROM messages WHERE role='user'")
    st.sidebar.metric("Messages", c.fetchone()[0])