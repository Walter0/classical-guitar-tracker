# 🎸 Classical Guitar Learning Tracker

A beautiful, earth-toned Streamlit application for tracking your classical guitar learning progress. Inspired by the words of Andrés Segovia: *"The guitar is a small orchestra. It is polyphonic. Every string is a different color, a different voice."*

## ✨ Features

### 📚 Goal Management
- **Unlimited Goals**: Create as many learning goals as you need
- **Flexible Naming**: No monthly restrictions - name your goals anything
- **Auto-Save**: Changes save automatically as you type
- **Goal Completion**: Mark goals as complete when finished (with confirmation)

### 📋 Task Organization  
- **Up to 5 Tasks** per goal with expandable task lists
- **Real-time Saving**: Tasks save as you type them
- **Add Task Button**: Easily expand your task list
- **Clean Interface**: Organized, distraction-free task management

### 📝 Practice Journaling
- **Dedicated Journal** for each goal
- **Manual Save System** with clear feedback
- **Persistent Storage**: Your reflections are never lost
- **Guided Prompts**: Built-in prompts to guide your reflections

### 🎨 Beautiful Design
- **Earth-Tone Theme**: Warm, easy-on-the-eyes color palette
- **Responsive Layout**: Clean, organized interface
- **Classical Inspiration**: Design inspired by classical music aesthetics
- **Segovia Quote**: Inspiring header quote on every page

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- pip (Python package manager)

### Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/Walter0/classical-guitar-tracker.git
   cd classical-guitar-tracker
   ```

2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   streamlit run app.py
   ```

4. **Open your browser** to `http://localhost:8501`

### 🖱️ Easy Launchers (Alternative)

For a more convenient experience, use the provided launcher files:

#### **macOS**
- **Double-click** `Guitar Tracker Launcher.command` to start the app
- Or run: `python3 launch.py`
- Create a Desktop shortcut by making an alias of the `.command` file

#### **Windows**  
- **Double-click** `Guitar Tracker Launcher.bat` to start the app
- Or run: `python launch.py`

#### **Cross-Platform Python Launcher**
- Run: `python3 launch.py` (or `python launch.py` on Windows)
- Automatically finds a free port and opens your browser
- Shows helpful status messages

*Note: The launchers automatically check for dependencies and install Streamlit if needed.*

## 🎯 How to Use

### Creating Your First Goal
1. Click "➕ Create New Goal" on the landing page
2. Enter a meaningful goal name (e.g., "Learn Bach's Minuet in G Major")
3. Add a description and completion criteria
4. Start adding practice tasks
5. Use the journal to track your daily practice

### Managing Tasks
- Type directly into task fields - they save automatically
- Click "➕ Add Task" to add more tasks (up to 5 per goal)
- Tasks are preserved when you switch between goals

### Using the Journal
- Write freely in the journal text area
- Click "💾 Save Journal" to save your entries
- Each goal has its own dedicated journal
- Use the built-in prompts to guide your reflection

### Completing Goals
- Click the small "✓" button next to a goal on the landing page
- Confirm the completion (this will delete the goal permanently)
- Use this feature when you've fully mastered a piece or technique

## 🎨 Color Palette

The app uses a carefully chosen earth-tone palette:

- **Background**: Warm Cream (`#f5f2e8`)
- **Primary**: Rich Brown (`#8b7355`) 
- **Secondary**: Sage Brown (`#a0956b`)
- **Accents**: Soft Tan (`#d4c4a0`)
- **Text**: Deep Brown (`#4a4035`)

## 🗄️ Data Storage

All your data is stored locally in a SQLite database (`guitar_tracker.db`):

- **Goals Table**: Stores goal information and metadata
- **Tasks Table**: Links practice tasks to specific goals
- **Journal Entries**: Preserves your daily reflections

### Data Privacy
- All data stays on your local machine
- No cloud storage or external services
- Complete privacy and control over your practice data

## 🛠️ Technical Details

### Built With
- **[Streamlit](https://streamlit.io/)**: Web application framework
- **SQLite**: Local database storage
- **Python 3.x**: Core application language

### File Structure
```
classical-guitar-tracker/
├── app.py                           # Main Streamlit application
├── launch.py                        # Cross-platform Python launcher
├── Guitar Tracker Launcher.command  # macOS launcher (double-click)
├── Guitar Tracker Launcher.bat      # Windows launcher (double-click)
├── requirements.txt                 # Python dependencies
├── README.md                       # Documentation
├── guitar_icon.png                 # Application icon
├── .gitignore                      # Git ignore rules
└── guitar_tracker.db               # SQLite database (created in home directory)
```

## 🤝 Contributing

Contributions are welcome! Please feel free to:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 License

This project is open source and available under the [MIT License](LICENSE).

## 🎵 Inspiration

*"The guitar is a small orchestra. It is polyphonic. Every string is a different color, a different voice."*  
**- Andrés Segovia**

This application is designed to help classical guitarists organize their practice and track their journey toward mastering this beautiful, complex instrument.

## 🎸 Happy Practicing!

May your practice sessions be productive and your musical journey be fulfilling!