import streamlit as st
import json
import time
import requests
from streamlit_lottie import st_lottie

# Page configuration
st.set_page_config(
    page_title="Medical Quiz Game",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for futuristic theme
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Montserrat:wght@400;600;700&display=swap');
    
    :root {
        --primary: #6EC3F4;
        --secondary: #A2E3C4;
        --accent: #FF7E5F;
        --dark: #2D3748;
        --light: #F8FAFC;
    }
    
    body {
        font-family: 'Montserrat', sans-serif;
        background-color: #F0F8FF;
        background-image: radial-gradient(circle at 10% 20%, rgba(174, 234, 255, 0.3) 0%, rgba(255, 255, 255, 0) 90%);
    }
    
    .stApp {
        background: linear-gradient(135deg, #F0F8FF 0%, #E6F7FF 100%);
    }
    
    .title {
        color: var(--dark);
        text-align: center;
        font-weight: 700;
        font-size: 2.5rem;
        margin-bottom: 0.5rem;
        text-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    
    .subtitle {
        color: var(--dark);
        text-align: center;
        font-weight: 400;
        margin-bottom: 2rem;
    }
    
    .question-card {
        background: white;
        border-radius: 16px;
        padding: 2rem;
        box-shadow: 0 8px 32px rgba(31, 135, 229, 0.1);
        border: 1px solid rgba(110, 195, 244, 0.3);
        margin-bottom: 2rem;
        position: relative;
        overflow: hidden;
    }
    
    .question-card::before {
        content: "";
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, var(--primary), var(--secondary));
    }
    
    .question-text {
        font-size: 1.2rem;
        font-weight: 600;
        color: var(--dark);
        margin-bottom: 1.5rem;
    }
    
    .stButton>button {
        border-radius: 12px !important;
        padding: 0.75rem 1.5rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        border: none !important;
        width: 100%;
        margin-bottom: 0.75rem;
        text-align: left;
        position: relative;
        overflow: hidden;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px) !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1) !important;
    }
    
    .option-btn-0 {
        background: linear-gradient(135deg, var(--primary) 0%, #4AB8F8 100%) !important;
        color: white !important;
    }
    
    .option-btn-1 {
        background: linear-gradient(135deg, var(--secondary) 0%, #7ED9A8 100%) !important;
        color: white !important;
    }
    
    .option-btn-2 {
        background: linear-gradient(135deg, #FF9A8B 0%, var(--accent) 100%) !important;
        color: white !important;
    }
    
    .option-btn-3 {
        background: linear-gradient(135deg, #A78BFA 0%, #8B5CF6 100%) !important;
        color: white !important;
    }
    
    .score-card {
        background: white;
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 4px 16px rgba(0,0,0,0.05);
        margin-bottom: 1.5rem;
    }
    
    .score-title {
        font-size: 1rem;
        font-weight: 600;
        color: var(--dark);
        margin-bottom: 0.5rem;
    }
    
    .score-value {
        font-size: 2rem;
        font-weight: 700;
        color: var(--primary);
        margin-bottom: 0;
    }
    
    .leaderboard {
        background: white;
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 4px 16px rgba(0,0,0,0.05);
    }
    
    .leaderboard-title {
        font-size: 1rem;
        font-weight: 600;
        color: var(--dark);
        margin-bottom: 1rem;
        text-align: center;
    }
    
    .leaderboard-item {
        display: flex;
        align-items: center;
        padding: 0.5rem 0;
        border-bottom: 1px solid rgba(0,0,0,0.05);
    }
    
    .leaderboard-pos {
        font-weight: 700;
        margin-right: 1rem;
        width: 24px;
        height: 24px;
        display: flex;
        align-items: center;
        justify-content: center;
        border-radius: 50%;
    }
    
    .pos-1 {
        background: gold;
        color: white;
    }
    
    .pos-2 {
        background: silver;
        color: white;
    }
    
    .pos-3 {
        background: #cd7f32;
        color: white;
    }
    
    .timer {
        width: 60px;
        height: 60px;
        border-radius: 50%;
        background: white;
        display: flex;
        align-items: center;
        justify-content: center;
        box-shadow: 0 4px 16px rgba(0,0,0,0.1);
        margin: 0 auto 1.5rem;
        font-weight: 700;
        font-size: 1.5rem;
        color: var(--primary);
        border: 3px solid var(--primary);
    }
    
    .correct-answer {
        animation: pulse 0.5s ease;
        box-shadow: 0 0 0 4px rgba(110, 195, 244, 0.5) !important;
    }
    
    @keyframes pulse {
        0% { transform: scale(1); }
        50% { transform: scale(1.05); }
        100% { transform: scale(1); }
    }
    
    .progress-container {
        width: 100%;
        height: 8px;
        background: rgba(110, 195, 244, 0.2);
        border-radius: 4px;
        margin-bottom: 1.5rem;
    }
    
    .progress-bar {
        height: 100%;
        border-radius: 4px;
        background: linear-gradient(90deg, var(--primary), var(--secondary));
        transition: width 0.3s ease;
    }
    
    .stage-indicator {
        display: inline-block;
        padding: 0.25rem 0.75rem;
        border-radius: 12px;
        background: var(--secondary);
        color: var(--dark);
        font-weight: 600;
        font-size: 0.8rem;
        margin-bottom: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Function to load Lottie animation from URL
def load_lottie_url(url: str):
    try:
        r = requests.get(url)
        if r.status_code != 200:
            return None
        return r.json()
    except:
        return None

# Function to load questions from JSON file
def load_questions(stage):
    try:
        with open(f"questions/stage{stage}.json", "r") as f:
            return json.load(f)["questions"]
    except:
        return []

# Initialize session state
if 'player_name' not in st.session_state:
    st.session_state.player_name = None
if 'current_stage' not in st.session_state:
    st.session_state.current_stage = 1
if 'score' not in st.session_state:
    st.session_state.score = 0
if 'question_number' not in st.session_state:
    st.session_state.question_number = 0
if 'start_time' not in st.session_state:
    st.session_state.start_time = None
if 'time_left' not in st.session_state:
    st.session_state.time_left = 30
if 'last_answer' not in st.session_state:
    st.session_state.last_answer = None

# Lottie animations
lottie_welcome = load_lottie_url("https://assets2.lottiefiles.com/packages/lf20_touohxv0.json")  # Doctor welcome
lottie_correct = load_lottie_url("https://assets2.lottiefiles.com/packages/lf20_jbrw3hcz.json")   # Correct answer
lottie_wrong = load_lottie_url("https://assets1.lottiefiles.com/packages/lf20_x1gjdldd.json")     # Wrong answer
lottie_transition = load_lottie_url("https://assets10.lottiefiles.com/packages/lf20_x62chJ.json") # Stage transition
lottie_win = load_lottie_url("https://assets2.lottiefiles.com/packages/lf20_jimqos21.json")       # Win animation
lottie_medical = load_lottie_url("https://assets5.lottiefiles.com/packages/lf20_0yfsb3a1.json")   # Medical equipment

# Mock leaderboard data
leaderboard_data = [
    {"name": "Dr. Smith", "score": 950},
    {"name": "Prof. Johnson", "score": 870},
    {"name": "Nurse Lee", "score": 820},
    {"name": "MedStudent", "score": 790},
    {"name": "Resident", "score": 750}
]

# Main interface
st.markdown('<div class="title">🏥 Medical Quiz Challenge</div>', unsafe_allow_html=True)

if st.session_state.player_name is None:
    # Login page
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.markdown('<div class="subtitle">Test Your Medical Knowledge with Futuristic Quiz Experience</div>', unsafe_allow_html=True)
        
        with st.form("login_form"):
            player_name = st.text_input("Enter your name:")
            submit_button = st.form_submit_button("Start Challenge")
            
            if submit_button and player_name:
                st.session_state.player_name = player_name
                st.session_state.start_time = time.time()
                st.session_state.time_left = 30
                st.rerun()
    
    with col2:
        if lottie_welcome:
            st_lottie(lottie_welcome, height=350, key="welcome")

else:
    # Game interface for logged-in player
    col1, col2 = st.columns([3, 1])
    
    with col1:
        questions = load_questions(st.session_state.current_stage)
        
        if st.session_state.question_number >= len(questions):
            # Stage completed
            st.success("Congratulations! You've completed this stage!")
            
            if st.session_state.current_stage == 1:
                st.markdown("Preparing for Stage 2 - Advanced Medical Knowledge!")
                if st.button("Continue to Stage 2", key="continue_btn"):
                    if lottie_transition:
                        st_lottie(lottie_transition, height=200, key="transition")
                    time.sleep(2)
                    st.session_state.current_stage = 2
                    st.session_state.question_number = 0
                    st.session_state.time_left = 30
                    st.rerun()
            else:
                # Game completed
                st.markdown("### 🎉 Congratulations! You've completed the Medical Quiz Challenge!")
                st.markdown(f"Final Score: **{st.session_state.score}** points")
                
                # Add player to leaderboard if in top 5
                if st.session_state.score > leaderboard_data[-1]["score"]:
                    leaderboard_data.append({"name": st.session_state.player_name, "score": st.session_state.score})
                    leaderboard_data.sort(key=lambda x: x["score"], reverse=True)
                    leaderboard_data = leaderboard_data[:5]
                    st.balloons()
                
                if lottie_win:
                    st_lottie(lottie_win, height=250, key="win")
                
                if st.button("Play Again", key="restart_btn"):
                    st.session_state.clear()
                    st.rerun()
        else:
            # Display current question
            current_question = questions[st.session_state.question_number]
            
            # Progress bar
            progress = (st.session_state.question_number + 1) / len(questions)
            st.markdown(f'<div class="stage-indicator">Stage {st.session_state.current_stage}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="progress-container"><div class="progress-bar" style="width: {progress*100}%"></div></div>', unsafe_allow_html=True)
            
            # Question card
            st.markdown(f'<div class="question-card"><div class="question-text">{current_question["question"]}</div></div>', unsafe_allow_html=True)
            
            # Display options as styled buttons
            for i, option in enumerate(current_question["options"]):
                button_class = f"option-btn-{i % 4}"
                if st.button(option, key=f"option_{i}", help="Select your answer"):
                    selected_index = i
                    st.session_state.last_answer = time.time()
                    
                    # Check answer
                    if selected_index == current_question["correct_answer"]:
                        st.session_state.score += current_question["points"]
                        st.markdown(f'<div class="stButton"><button class="{button_class} correct-answer">✓ Correct! +{current_question["points"]} points</button></div>', unsafe_allow_html=True)
                        if lottie_correct:
                            st_lottie(lottie_correct, height=150, key="correct")
                    else:
                        st.markdown(f'<div class="stButton"><button class="{button_class}">✗ Wrong</button></div>', unsafe_allow_html=True)
                        if lottie_wrong:
                            st_lottie(lottie_wrong, height=150, key="wrong")
                        correct_answer = current_question["options"][current_question["correct_answer"]]
                        st.markdown(f"**Correct answer:** {correct_answer}")
                    
                    time.sleep(1.5)
                    st.session_state.question_number += 1
                    st.session_state.time_left = 30
                    st.rerun()
    
    with col2:
        # Timer
        st.markdown('<div class="timer" id="timer">30</div>', unsafe_allow_html=True)
        
        # Score card
        st.markdown('<div class="score-card"><div class="score-title">YOUR SCORE</div><div class="score-value">{}</div></div>'.format(st.session_state.score), unsafe_allow_html=True)
        
        # Leaderboard
        st.markdown('<div class="leaderboard"><div class="leaderboard-title">🏆 LEADERBOARD</div>', unsafe_allow_html=True)
        
        for i, player in enumerate(leaderboard_data[:3]):
            pos_class = f"pos-{i+1}" if i < 3 else ""
            st.markdown(f"""
            <div class="leaderboard-item">
                <div class="leaderboard-pos {pos_class}">{i+1}</div>
                <div style="flex-grow: 1">{player['name']}</div>
                <div style="font-weight: 600">{player['score']}</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)  # Close leaderboard div
        
        # Medical animation
        if lottie_medical:
            st_lottie(lottie_medical, height=150, key="medical")

# JavaScript for timer
timer_script = """
<script>
    let timeLeft = 30;
    const timerElement = document.getElementById('timer');
    
    function updateTimer() {
        timeLeft--;
        timerElement.textContent = timeLeft;
        
        if (timeLeft <= 10) {
            timerElement.style.color = '#FF7E5F';
            timerElement.style.borderColor = '#FF7E5F';
        }
        
        if (timeLeft <= 0) {
            // Time's up - automatically move to next question
            window.location.href = window.location.href;
        }
    }
    
    // Update timer every second
    setInterval(updateTimer, 1000);
</script>
"""
st.components.v1.html(timer_script, height=0)