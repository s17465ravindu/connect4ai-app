import streamlit as st
from connect4_logic import *
import time

st.set_page_config(page_title="Connect 4 AI", layout="wide")

# ---------------- SESSION STATE ----------------
if "board" not in st.session_state:
    st.session_state.board = create_board()

if "game_over" not in st.session_state:
    st.session_state.game_over = False

if "turn" not in st.session_state:
    st.session_state.turn = "player"

if "player_score" not in st.session_state:
    st.session_state.player_score = 0

if "ai_score" not in st.session_state:
    st.session_state.ai_score = 0

if "draw_score" not in st.session_state:
    st.session_state.draw_score = 0

if "difficulty" not in st.session_state:
    st.session_state.difficulty = None

if "winner" not in st.session_state:
    st.session_state.winner = None


# ---------------- STYLE ----------------
st.markdown("""
<style>

.stApp {
    background: radial-gradient(circle at top left, #0f3d2e, #021c16);
    color: white;
}

.title {
    text-align: center;
    font-size: 42px;
    font-weight: 700;
}

.subtitle {
    text-align: center;
    color: #6ee7b7;
    margin-bottom: 25px;
}

.status-bar {
    display: flex;
    justify-content: space-between;
    align-items: center;

    background: rgba(16,185,129,0.08);

    border: 1px solid rgba(16,185,129,0.3);

    padding: 16px 22px;

    border-radius: 18px;

    width: 80%;
    margin: auto;

    margin-bottom: 20px;
}

.turn-box {
    text-align: center;
    font-size: 22px;
    font-weight: 600;
    margin-bottom: 25px;
}

.board-container {
    width: 610px;
    margin: auto;
}

.board {
    display: grid;
    grid-template-columns: repeat(7, 70px);

    gap: 12px;

    background: rgba(16,185,129,0.08);

    padding: 22px;

    border-radius: 24px;

    box-shadow: 0 0 40px rgba(16,185,129,0.25);
}

.cell {
    width: 70px;
    height: 70px;
    border-radius: 50%;
    background: rgba(255,255,255,0.08);
}

.player {
    background: #22c55e;
    box-shadow: 0 0 18px #22c55e;
}

.ai {
    background: #facc15;
    box-shadow: 0 0 18px #facc15;
}

div[data-testid="horizontal-block"] {
    justify-content: center !important;
}

.stButton > button {

    width: 90px !important;
    height: 48px;

    border-radius: 999px;

    border: 1px solid rgba(16,185,129,0.5);

    background: rgba(16,185,129,0.08);

    color: white;

    transition: 0.2s;

    margin-top: 18px;
}

.stButton > button:hover {
    transform: scale(1.05);
    background: rgba(16,185,129,0.2);
}

.popup {

    width: 420px;

    margin: auto;

    margin-top: 30px;

    padding: 30px;

    border-radius: 22px;

    text-align: center;

    font-size: 28px;

    font-weight: bold;

    background: rgba(0,0,0,0.55);

    border: 2px solid rgba(255,255,255,0.15);

    box-shadow: 0 0 30px rgba(255,255,255,0.12);

    animation: glow 1.2s infinite alternate;
}

@keyframes glow {
    from {
        transform: scale(1);
    }

    to {
        transform: scale(1.02);
    }
}

</style>
""", unsafe_allow_html=True)


# ---------------- DIFFICULTY SELECTION ----------------
if st.session_state.difficulty is None:

    st.markdown("""
    <style>

    .difficulty-wrapper {

        width: 500px;

        margin: auto;

        margin-top: 160px;
    }

    /* SELECT BOX */

    div[data-baseweb="select"] > div {

        background: rgba(255,255,255,0.06) !important;

        border-radius: 18px !important;

        border: 1px solid rgba(255,255,255,0.08) !important;

        min-height: 60px !important;

        color: white !important;

        backdrop-filter: blur(10px);
    }

    /* BUTTON */

    .stButton > button {

        width: 100% !important;

        height: 60px;

        border-radius: 18px;

        font-size: 18px;

        font-weight: 600;

        margin-top: 25px;

        background: linear-gradient(
            135deg,
            rgba(16,185,129,0.95),
            rgba(5,150,105,0.95)
        ) !important;

        border: none !important;

        color: white !important;

        transition: 0.25s;
    }

    .stButton > button:hover {

        transform: scale(1.02);

        box-shadow: 0 0 25px rgba(16,185,129,0.35);
    }

    </style>
    """, unsafe_allow_html=True)

    left, center, right = st.columns([1,1.2,1])

    with center:

        st.markdown(
            "<h1 style='text-align:center; margin-bottom:35px;'>🎮 Connect 4 AI</h1>",
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <div style='
                text-align:center;
                font-size:18px;
                color:#d1d5db;
                margin-bottom:14px;
                font-weight:500;
            '>
                Select Difficulty Level
            </div>
            """,
            unsafe_allow_html=True
        )

        difficulty = st.selectbox(
            "",
            ["Easy", "Medium", "Hard"],
            index=1,
            label_visibility="collapsed"
        )

        if st.button("Start Game", use_container_width=True):

            st.session_state.difficulty = difficulty
            st.rerun()

    st.stop()


# ---------------- HEADER ----------------
st.markdown('<div class="title">Connect 4 AI</div>', unsafe_allow_html=True)

st.markdown(
    '<div class="subtitle">Strategic Intelligence Dashboard</div>',
    unsafe_allow_html=True
)

status_text = (
    "🧠 AI Thinking..."
    if st.session_state.turn == "ai"
    else "🎯 Your Turn"
)

st.markdown(f"""
<div class="status-bar">

<div>
🎮 Difficulty:
<b>{st.session_state.difficulty}</b>
</div>

<div>
🏆 Player: {st.session_state.player_score}
&nbsp;&nbsp; | &nbsp;&nbsp;
🤖 AI: {st.session_state.ai_score}
&nbsp;&nbsp; | &nbsp;&nbsp;
🤝 Draws: {st.session_state.draw_score}
</div>

<div>
{status_text}
</div>

</div>
""", unsafe_allow_html=True)


# ---------------- DRAW BOARD ----------------
def draw_board(board):

    html = '<div class="board-container"><div class="board">'

    for row in reversed(board):

        for cell in row:

            if cell == PLAYER:
                html += '<div class="cell player"></div>'

            elif cell == AI:
                html += '<div class="cell ai"></div>'

            else:
                html += '<div class="cell"></div>'

    html += '</div></div>'

    st.markdown(html, unsafe_allow_html=True)


draw_board(st.session_state.board)


# ---------------- PLAYER MOVE ----------------
if st.session_state.turn == "player" and not st.session_state.game_over:

    left, center, right = st.columns([1,2,1])

    with center:

        cols = st.columns(COLUMN_COUNT)

        for col in range(COLUMN_COUNT):

            if cols[col].button(str(col + 1), key=f"col_{col}"):

                if is_valid(st.session_state.board, col):

                    row = get_next_open_row(
                        st.session_state.board,
                        col
                    )

                    drop_piece(
                        st.session_state.board,
                        row,
                        col,
                        PLAYER
                    )

                    # WIN
                    if winning_move(st.session_state.board, PLAYER):

                        st.session_state.game_over = True
                        st.session_state.winner = "PLAYER"

                        st.session_state.player_score += 1

                    # DRAW
                    elif is_draw(st.session_state.board):

                        st.session_state.game_over = True
                        st.session_state.winner = "DRAW"

                        st.session_state.draw_score += 1

                    else:
                        st.session_state.turn = "ai"

                    st.rerun()


# ---------------- AI MOVE ----------------
elif st.session_state.turn == "ai" and not st.session_state.game_over:

    time.sleep(0.6)

    ai_col = get_ai_move(
        st.session_state.board,
        st.session_state.difficulty
    )

    if ai_col is not None and is_valid(st.session_state.board, ai_col):

        row = get_next_open_row(
            st.session_state.board,
            ai_col
        )

        drop_piece(
            st.session_state.board,
            row,
            ai_col,
            AI
        )

        # AI WIN
        if winning_move(st.session_state.board, AI):

            st.session_state.game_over = True
            st.session_state.winner = "AI"

            st.session_state.ai_score += 1

        # DRAW
        elif is_draw(st.session_state.board):

            st.session_state.game_over = True
            st.session_state.winner = "DRAW"

            st.session_state.draw_score += 1

    st.session_state.turn = "player"

    st.rerun()


# ---------------- RESULT POPUP ----------------
if st.session_state.game_over:

    if st.session_state.winner == "PLAYER":

        st.markdown("""
        <div class="popup">
        🏆 YOU WIN!
        </div>
        """, unsafe_allow_html=True)

    elif st.session_state.winner == "AI":

        st.markdown("""
        <div class="popup">
        🤖 AI WINS!
        </div>
        """, unsafe_allow_html=True)

    else:

        st.markdown("""
        <div class="popup">
        🤝 DRAW MATCH
        </div>
        """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns([1,1,1])

    with c2:

        if st.button("Next Round"):

            st.session_state.board = create_board()

            st.session_state.game_over = False

            st.session_state.turn = "player"

            st.session_state.winner = None

            st.rerun()


# ---------------- RESET ----------------
st.markdown("<br>", unsafe_allow_html=True)

r1, r2, r3 = st.columns([1,1,1])

with r2:

    if st.button("Reset Game"):

        st.session_state.board = create_board()

        st.session_state.game_over = False

        st.session_state.turn = "player"

        st.session_state.player_score = 0

        st.session_state.ai_score = 0

        st.session_state.draw_score = 0

        st.session_state.winner = None

        # Ask difficulty again
        st.session_state.difficulty = None

        st.rerun()