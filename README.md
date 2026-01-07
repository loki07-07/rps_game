# 🪨📄✂️ Rock Paper Scissors Plus

An enhanced version of the classic Rock Paper Scissors game with AI-powered commentary and a special "bomb" move! Built with Streamlit and powered by Groq AI for intelligent game commentary.

## 🌟 Features

- **Classic Gameplay**: Traditional Rock, Paper, Scissors mechanics
- **Bomb Move**: Each player gets one special "bomb" move that beats everything
- **AI Referee**: Intelligent commentary and rule explanations powered by Groq AI
- **Interactive UI**: Clean, modern interface built with Streamlit
- **Score Tracking**: Keep track of wins, losses, and draws
- **Round-by-round History**: View detailed game progression

## 🎮 Game Rules

### Basic Moves
- **Rock** beats **Scissors**
- **Paper** beats **Rock**  
- **Scissors** beats **Paper**

### Special Move
- **Bomb** beats all other moves (Rock, Paper, Scissors)
- Each player can only use the bomb **once per game**
- If both players use bomb in the same round, it's a draw

## 🚀 Getting Started

### Prerequisites
- Python 3.7 or higher
- A Groq API key (get one from [Groq Console](https://console.groq.com))

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/loki07-07/rps_game.git
   cd rps_game
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables**
   ```bash
   # Copy the example environment file
   cp .env.example .env
   
   # Edit .env and add your Groq API key
   GROQ_API_KEY=your_actual_groq_api_key_here
   ```

4. **Run the application**
   ```bash
   streamlit run streamlit_app.py
   ```

5. **Open your browser**
   - The app will automatically open at `http://localhost:8501`
   - If not, navigate to the URL shown in your terminal

## 🎯 How to Play

1. **Enter Your Name**: Start by entering your player name
2. **Choose Your Move**: Select Rock, Paper, Scissors, or Bomb
3. **AI Commentary**: The AI referee will explain the round outcome
4. **Track Progress**: Watch your score and remaining bomb usage
5. **Strategic Play**: Save your bomb for the right moment!

## 🛠️ Project Structure

```
rps_game/
├── streamlit_app.py     # Main Streamlit application
├── tools.py            # Game logic and utility functions
├── state.py            # Game state management
├── requirements.txt     # Python dependencies
├── .env.example        # Environment variables template
├── .gitignore          # Git ignore rules
└── README.md           # This file
```

## 📁 File Descriptions

- **`streamlit_app.py`**: Main application file containing the UI and game flow
- **`tools.py`**: Core game logic including move validation and winner determination  
- **`state.py`**: Game state management functions
- **`requirements.txt`**: Required Python packages
- **`.env.example`**: Template for environment variables

## 🔧 Configuration

### Environment Variables

Create a `.env` file in the project root with:

```env
GROQ_API_KEY=your_groq_api_key_here
```

### Customization Options

You can modify the game by editing:
- **Available moves**: Change `AVAILABLE_GAME_MOVES` in `tools.py`
- **UI styling**: Modify the CSS in `streamlit_app.py`
- **AI personality**: Adjust the system prompt in the session state initialization

## 🤖 AI Features

The AI referee provides:
- **Rule explanations** for new players
- **Round-by-round commentary** on moves and outcomes
- **Strategic insights** about bomb usage
- **Game summary** and final results
- **Engaging conversation** throughout the game

## 🎨 UI Features

- **Responsive design** that works on desktop and mobile
- **Custom CSS styling** for a polished look
- **Interactive buttons** for move selection
- **Real-time score updates**
- **Chat-style AI commentary**

## 🐛 Troubleshooting

### Common Issues

1. **"Groq API key not configured" error**
   - Make sure your `.env` file exists and contains a valid `GROQ_API_KEY`
   - Restart the Streamlit app after adding the API key

2. **Module import errors**
   - Ensure all dependencies are installed: `pip install -r requirements.txt`
   - Check that you're in the correct directory

3. **Streamlit not starting**
   - Try: `python -m streamlit run streamlit_app.py`
   - Check if port 8501 is already in use

## 🚧 Development

### Running in Development Mode

```bash
# Run with auto-reload
streamlit run streamlit_app.py --server.runOnSave true

# Run on a different port
streamlit run streamlit_app.py --server.port 8502
```

### Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and test thoroughly
4. Commit your changes: `git commit -m 'Add feature-name'`
5. Push to the branch: `git push origin feature-name`
6. Submit a pull request

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

## 🙏 Acknowledgments

- Built with [Streamlit](https://streamlit.io/) for the web interface
- Powered by [Groq AI](https://groq.com/) for intelligent commentary
- Inspired by the classic Rock Paper Scissors game

## 📞 Support

If you encounter any issues or have questions:

1. Check the [Issues](https://github.com/loki07-07/rps_game/issues) page
2. Create a new issue with detailed information
3. Include error messages and steps to reproduce

---

**Happy Gaming! 🎮** Enjoy your enhanced Rock Paper Scissors experience with AI commentary!
