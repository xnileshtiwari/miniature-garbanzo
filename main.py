from data import database
from generative_model import get_physics_answers, get_chemistry_answers, get_maths_answers
import streamlit as st
import os


# Hide Streamlit's default menu buttons
hide_menu = """
<style>
#MainMenu {visibility: hidden;}
</style>
"""
st.markdown(hide_menu, unsafe_allow_html=True)


st.set_page_config(
    page_title="69",
    page_icon="🧊",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "Special thanks to Hari Singh for encouraging me to create this app."
    }
)



def load_css():
    css_file = os.path.join(os.path.dirname(__file__), "custom.css")
    try:
        with open(css_file) as f:
            st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)
    except Exception as e:
        print(f"Error loading CSS file: {e}")

# Define subject-specific prompts
PHYSICS_PROMPTS = [
    "⚡ Electric Fields",
    "🔌 Electric Potential",
    "💡 Potential difference",
    "🔋 Capacitance",
]

CHEMISTRY_PROMPTS = [
    "⚛️ Atomic Structure",
    "🧪 Chemical Bonding",
    "🔄 Chemical Reactions",
    "📊 Stoichiometry",
]

MATHS_PROMPTS = [
    "MATRIX MULTIPLICATION",
    "LINEAR EQUATIONS",
    "TRIGONOMETRY",
    "QUADRATIC EQUATIONS",
]

def initialize_session_state():
    """Initialize session state variables"""
    if "current_subject" not in st.session_state:
        st.session_state.current_subject = "Physics"
    if "physics_messages" not in st.session_state:
        st.session_state.physics_messages = []
    if "chemistry_messages" not in st.session_state:
        st.session_state.chemistry_messages = []
    if "maths_messages" not in st.session_state:
        st.session_state.maths_messages = []

def get_current_messages():
    """Get messages for current subject"""
    subject = st.session_state.current_subject
    return {
        "Physics": st.session_state.physics_messages,
        "Chemistry": st.session_state.chemistry_messages,
        "Maths": st.session_state.maths_messages
    }[subject]

def get_current_prompts():
    """Get predefined prompts for current subject"""
    subject = st.session_state.current_subject
    return {
        "Physics": PHYSICS_PROMPTS,
        "Chemistry": CHEMISTRY_PROMPTS,
        "Maths": MATHS_PROMPTS
    }[subject]

def main():
    # Initialize session state
    initialize_session_state()
    
    # Load CSS
    load_css()
    
    # Sidebar with improved subject selection
    with st.sidebar:
        st.markdown('<div class="subject-selection-title">Choose Your Subject</div>', unsafe_allow_html=True)
        st.markdown('<div class="subject-buttons-container">', unsafe_allow_html=True)

        
        # Create three columns for subject buttons

        physics_active = st.session_state.current_subject == "Physics"
        btn_class = "active" if physics_active else ""
        if st.button(
            "🪐 Physics",
            key="physics_btn",
            help="Switch to Physics",
        ):
            st.session_state.current_subject = "Physics"
            st.rerun()
        st.markdown(f"""
            <style>
                div[data-testid="stButton"]:has(button[key="physics_btn"]) button {{
                    border-color: {'var(--primary-color)' if not physics_active else 'transparent'} !important;
                    background: {'var(--surface)' if not physics_active else 'var(--primary-color)'} !important;
                    color: {'var(--primary-color)' if not physics_active else 'white'} !important;
                }}
            </style>
        """, unsafe_allow_html=True)

        chemistry_active = st.session_state.current_subject == "Chemistry"
        btn_class = "active" if physics_active else ""
        if st.button(
            "🧪 Chemistry",
            key="chemistry_btn",
            help="Switch to Chemistry",
        ):
            st.session_state.current_subject = "Chemistry"
            st.rerun()
        st.markdown(f"""
            <style>
                div[data-testid="stButton"]:has(button[key="chemistry_btn"]) button {{
                    border-color: {'var(--primary-color)' if not physics_active else 'transparent'} !important;
                    background: {'var(--surface)' if not physics_active else 'var(--primary-color)'} !important;
                    color: {'var(--primary-color)' if not physics_active else 'white'} !important;
                }}
            </style>
        """, unsafe_allow_html=True)

        maths_active = st.session_state.current_subject == "Maths"
        btn_class = "active" if physics_active else ""
        if st.button(
            "🧮 Maths",
            key="maths_btn",
            help="Switch to Maths",
        ):
            st.session_state.current_subject = "Maths"
            st.rerun()
        st.markdown(f"""
            <style>
                div[data-testid="stButton"]:has(button[key="maths_btn"]) button {{
                    border-color: {'var(--primary-color)' if not physics_active else 'transparent'} !important;
                    background: {'var(--surface)' if not physics_active else 'var(--primary-color)'} !important;
                    color: {'var(--primary-color)' if not physics_active else 'white'} !important;
                }}
            </style>
        """, unsafe_allow_html=True)
        
    
    st.markdown('</div>', unsafe_allow_html=True)


    # Main content area
    st.markdown(
        f'<div class="main-title">{st.session_state.current_subject} Study Assistant</div>',
        unsafe_allow_html=True
    )
    
    # Topic buttons with improved layout
    st.markdown('<div class="topics-grid">', unsafe_allow_html=True)
    cols = st.columns(4)
    for idx, topic in enumerate(get_current_prompts()):
        with cols[idx]:
            if st.button(topic, key=f"topic_{idx}", use_container_width=True):
                st.session_state.temp_input = topic
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Chat interface
    chat_container = st.container()
    with chat_container:
        for message in get_current_messages():
            avatar = "image.png" if message["role"] == "user" else "✨"
            with st.chat_message(message["role"], avatar=avatar):
                st.markdown(message["content"])
    
    # User input handling
    user_input = st.chat_input(
        f"✨ Ask me anything about {st.session_state.current_subject}...",
        key="chat_input"
    )
    
    if user_input or ('temp_input' in st.session_state and st.session_state.temp_input):
        # Handle predefined prompt
        if 'temp_input' in st.session_state and st.session_state.temp_input:
            user_input = st.session_state.temp_input
            st.session_state.temp_input = None
        
        # Add user message
        current_messages = get_current_messages()
        current_messages.append({"role": "user", "content": user_input})
        
        # Show user message
        with st.chat_message("user", avatar="image.png"):
            st.markdown(user_input)
        
        # Process response
        with st.spinner("✨ Generating response..."):
            # Get subject-specific response generator
            subject = st.session_state.current_subject
            if subject == "Physics":
                response_gen = get_physics_answers(user_input)
            elif subject == "Chemistry":
                response_gen = get_chemistry_answers(user_input)
            elif subject == "Maths":
                response_gen = get_maths_answers(user_input)
            
            
            # Stream response
            full_response = ""
            message_placeholder = st.empty()
            
        for chunk in response_gen:
            if isinstance(chunk, list):
                chunk = ' '.join(map(str, chunk))
            chunk_str = str(chunk)
            full_response += chunk_str
            message_placeholder.markdown(
                f'<div class="assistant-message streaming">{full_response}▌</div>',
                unsafe_allow_html=True
            )
        
        # Final response
        message_placeholder.empty()
        with st.chat_message("assistant", avatar="✨"):
            st.markdown(full_response)
            database(user_input, full_response)
        
        current_messages.append({"role": "assistant", "content": full_response})
    
        st.rerun()

if __name__ == "__main__":
    main()
