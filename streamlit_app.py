import streamlit as st
import asyncio
import os
from dotenv import load_dotenv
from groq import AsyncGroq
from tools import initialize_player_name, validate_player_move, determine_round_winner, update_game_state_after_round, AVAILABLE_GAME_MOVES
import random

# Load environment variables
load_dotenv()

# Initialize Streamlit page config
st.set_page_config(
    page_title="Rock Paper Scissors Plus",
    page_icon="🪨",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        text-align: center;
        color: #1f77b4;
        font-size: 3rem;
        margin-bottom: 1rem;
    }
    .game-status {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 10px;
        border-left: 5px solid #1f77b4;
        margin: 1rem 0;
    }
    .move-button {
        font-size: 2rem;
        padding: 0.5rem 1rem;
        margin: 0.2rem;
    }
    .chat-message {
        
        padding: 1rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        border-left: 4px solid #1f77b4;
    }
    .score-display {
        text-align: center;
        font-size: 1.5rem;
        font-weight: bold;
        margin: 1rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
def initialize_streamlit_session_state():
    if 'current_game_state' not in st.session_state:
        st.session_state.current_game_state = {
            "player_name": None,
            "round": 1,
            "user_score": 0,
            "bot_score": 0,
            "user_used_bomb": False,
            "bot_used_bomb": False,
            "game_over": False
        }
    
    if 'ai_chat_conversation_history' not in st.session_state:
        st.session_state.ai_chat_conversation_history = [
            {"role": "system", "content": """
You are a friendly game referee for Rock Paper Scissors Plus.
You explain rules, round outcomes, score updates, and the final result.
You never change game state or game rules.
You remember previous rounds via conversation history.
Keep your responses engaging but concise.
"""}
        ]
    
    if 'ai_referee_responses_list' not in st.session_state:
        st.session_state.ai_referee_responses_list = []
    
    if 'groq_ai_client' not in st.session_state:
        groq_api_key_from_env = os.getenv("GROQ_API_KEY")
        if groq_api_key_from_env and groq_api_key_from_env != "your-groq-api-key-here":
            st.session_state.groq_ai_client = AsyncGroq(api_key=groq_api_key_from_env)
        else:
            st.session_state.groq_ai_client = None

# Async function to call Groq API
async def get_agent_response(prompt: str):
    if not st.session_state.groq_ai_client:
        return "⚠️ Groq API key not configured. Please set GROQ_API_KEY in your .env file."
    
    try:
        # Add user prompt to conversation history
        st.session_state.ai_chat_conversation_history.append({"role": "user", "content": prompt})
        
        # Call Groq API
        response = await st.session_state.groq_ai_client.chat.completions.create(
            model="llama-3.1-8b-instant",
            messages=st.session_state.ai_chat_conversation_history,
            temperature=0.7,
            max_tokens=1000
        )
        
        # Extract response text
        response_text = response.choices[0].message.content
        
        # Add assistant response to conversation history
        st.session_state.ai_chat_conversation_history.append({"role": "assistant", "content": response_text})
        
        return response_text
        
    except Exception as e:
        return f"Sorry, I'm having trouble responding right now. ({str(e)})"

# Wrapper to run async function in Streamlit
def run_async(coro):
    try:
        loop = asyncio.get_event_loop()
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    
    return loop.run_until_complete(coro)

# Main app
def main():
    initialize_streamlit_session_state()
    
    # Header
    st.markdown('<h1 class="main-header">🪨📄✂️💣</h1>', unsafe_allow_html=True)
    st.markdown('<h2 style="text-align: center;">Rock Paper Scissors Plus</h2>', unsafe_allow_html=True)
    
    current_game_state = st.session_state.current_game_state
    
    # API Key Check
    if not st.session_state.groq_ai_client:
        st.error("🔑 Please configure your GROQ_API_KEY in the .env file to enable the AI referee!")
        st.info("Set GROQ_API_KEY=your-actual-api-key in the .env file, then restart the app.")
        return
    
    # Game Status Display
    if current_game_state["player_name"]:
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Round", f"{min(current_game_state['round'], 3)}/3")
        with col2:
            st.metric(f"{current_game_state['player_name']}", current_game_state['user_score'])
        with col3:
            st.metric("Bot", current_game_state['bot_score'])
        
        # Bomb status
        bomb_status_messages = []
        if current_game_state['user_used_bomb']:
            bomb_status_messages.append(f"{current_game_state['player_name']}: 💣 Used")
        else:
            bomb_status_messages.append(f"{current_game_state['player_name']}: 💣 Available")
            
        if current_game_state['bot_used_bomb']:
            bomb_status_messages.append("Bot: 💣 Used")
        else:
            bomb_status_messages.append("Bot: 💣 Available")
            
        st.info(" | ".join(bomb_status_messages))
    
    # Step 1: Get player name
    if not current_game_state["player_name"]:
        st.markdown("### Welcome! What's your name?")
        player_name_input = st.text_input("Enter your name:", key="name_input")
        
        if st.button("Start Game", type="primary") and player_name_input.strip():
            initialize_player_name(player_name_input, current_game_state)
            
            # Get welcome message from agent
            welcome_prompt = f"""
            The player's name is {current_game_state['player_name']}.
            Greet the player and welcome them to the game.
            """
            
            response = run_async(get_agent_response(welcome_prompt))
            st.session_state.ai_referee_responses_list.append(("🤖 Game Referee", response))
            
            # Get rules explanation
            rules_prompt = """
            Explain the rules of Rock Paper Scissors Plus in 5 lines.
            Moves: rock, paper, scissors, bomb.
            Bomb can be used only once.
            Game is best of 3 rounds.
            Invalid input wastes the round.
            """
            
            rules_response = run_async(get_agent_response(rules_prompt))
            st.session_state.ai_referee_responses_list.append(("📋 Rules", rules_response))
            
            st.rerun()
    
    # Display agent responses
    for sender, message in st.session_state.ai_referee_responses_list:
        with st.container():
            st.markdown(f'<div class="chat-message"><strong>{sender}:</strong><br>{message}</div>', unsafe_allow_html=True)
    
    # Step 2: Game Play
    if current_game_state["player_name"] and not current_game_state["game_over"]:
        if current_game_state["round"] <= 3:
            st.markdown(f"### Round {current_game_state['round']}/3 - Choose your move:")
            
            # Create move buttons
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                if st.button("🪨 Rock", key="rock", use_container_width=True):
                    handle_move("rock")
            
            with col2:
                if st.button("📄 Paper", key="paper", use_container_width=True):
                    handle_move("paper")
            
            with col3:
                if st.button("✂️ Scissors", key="scissors", use_container_width=True):
                    handle_move("scissors")
            
            with col4:
                bomb_disabled = current_game_state["user_used_bomb"]
                bomb_label = "💣 Bomb (Used)" if bomb_disabled else "💣 Bomb"
                if st.button(bomb_label, key="bomb", disabled=bomb_disabled, use_container_width=True):
                    handle_move("bomb")
    
    # Step 3: Game Over
    elif current_game_state["game_over"]:
        st.markdown("### 🎉 Game Over!")
        
        # Final results
        if current_game_state["user_score"] > current_game_state["bot_score"]:
            st.success(f"🏆 {current_game_state['player_name']} wins!")
        elif current_game_state["bot_score"] > current_game_state["user_score"]:
            st.error("🤖 Bot wins!")
        else:
            st.info("🤝 It's a tie!")
        
        # Reset button
        if st.button("🔄 Play Again", type="primary"):
            reset_game()
            st.rerun()

def handle_move(selected_user_move):
    current_game_state = st.session_state.current_game_state
    
    # Validate user move
    move_validation_result = validate_player_move(selected_user_move, current_game_state, "user")
    
    # Bot makes a move
    computer_selected_move = random.choice(AVAILABLE_GAME_MOVES)
    if not validate_player_move(computer_selected_move, current_game_state, "bot")["valid"]:
        computer_selected_move = random.choice(["rock", "paper", "scissors"])
    
    if not move_validation_result["valid"]:
        # Invalid move - round wasted
        current_game_state["round"] += 1
        
        prompt = f"""
        Round {current_game_state['round'] - 1}
        The player entered an invalid move: "{selected_user_move}".
        The round is wasted.
        Current score:
        {current_game_state['player_name']}: {current_game_state['user_score']}
        Bot: {current_game_state['bot_score']}
        Explain what happened.
        """
        
        response = run_async(get_agent_response(prompt))
        st.session_state.ai_referee_responses_list.append((f"⚠️ Round {current_game_state['round'] - 1}", response))
        
    else:
        # Valid move - play the round
        round_winner = determine_round_winner(selected_user_move, computer_selected_move)
        update_game_state_after_round(current_game_state, round_winner, selected_user_move, computer_selected_move)
        
        # Convert moves to emojis for display
        move_display_emojis = {
            "rock": "🪨", "paper": "📄", "scissors": "✂️", "bomb": "💣"
        }
        
        round_result_message = ""
        if round_winner == "user":
            round_result_message = f"🏆 {current_game_state['player_name']} wins this round!"
        elif round_winner == "bot":
            round_result_message = "🤖 Bot wins this round!"
        else:
            round_result_message = "🤝 Round tied!"
        
        # Display round result immediately
        st.success(f"""
        **Round {current_game_state['round'] - 1} Results:**
        
        {current_game_state['player_name']}: {move_display_emojis[selected_user_move]} {selected_user_move.title()}  
        Bot: {move_display_emojis[computer_selected_move]} {computer_selected_move.title()}
        
        {round_result_message}
        """)
        
        prompt = f"""
        Round {current_game_state['round'] - 1}
        Player move: {selected_user_move}
        Bot move: {computer_selected_move}
        Winner: {round_winner}
        Current score:
        {current_game_state['player_name']}: {current_game_state['user_score']}
        Bot: {current_game_state['bot_score']}
        Explain this round and the current status.
        """
        
        response = run_async(get_agent_response(prompt))
        st.session_state.ai_referee_responses_list.append((f"🎲 Round {current_game_state['round'] - 1}", response))
    
    # Check if game is over
    if current_game_state["round"] > 3:
        current_game_state["game_over"] = True
        
        # Determine final winner
        if current_game_state["user_score"] > current_game_state["bot_score"]:
            final_game_result = f"{current_game_state['player_name']} wins!"
        elif current_game_state["bot_score"] > current_game_state["user_score"]:
            final_game_result = "Bot wins!"
        else:
            final_game_result = "It's a tie!"
        
        final_prompt = f"""
        Game Over! All 3 rounds have been played.
        Final score:
        {current_game_state['player_name']}: {current_game_state['user_score']}
        Bot: {current_game_state['bot_score']}
        Result: {final_game_result}
        Explain the final result in a congratulatory or encouraging way.
        """
        
        final_response = run_async(get_agent_response(final_prompt))
        st.session_state.ai_referee_responses_list.append(("🏁 Final Result", final_response))
    
    st.rerun()

def reset_game():
    """Reset the game state for a new game"""
    st.session_state.current_game_state = {
        "player_name": None,
        "round": 1,
        "user_score": 0,
        "bot_score": 0,
        "user_used_bomb": False,
        "bot_used_bomb": False,
        "game_over": False
    }
    st.session_state.ai_chat_conversation_history = [
        {"role": "system", "content": """
You are a friendly game referee for Rock Paper Scissors Plus.
You explain rules, round outcomes, score updates, and the final result.
You never change game state or game rules.
You remember previous rounds via conversation history.
Keep your responses engaging but concise.
"""}
    ]
    st.session_state.ai_referee_responses_list = []

if __name__ == "__main__":
    main()
