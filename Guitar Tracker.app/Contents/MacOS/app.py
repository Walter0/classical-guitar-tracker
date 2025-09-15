import streamlit as st
import sqlite3
import datetime
from pathlib import Path

# Database setup
DB_PATH = Path("guitar_tracker.db")

def migrate_database():
    """Migrate database schema if needed"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Check if header_text column exists
    cursor.execute("PRAGMA table_info(goals)")
    columns = [column[1] for column in cursor.fetchall()]
    
    # Add header_text column if it doesn't exist
    if 'header_text' not in columns:
        print("Migrating database: Adding header_text column...")
        cursor.execute('ALTER TABLE goals ADD COLUMN header_text TEXT DEFAULT ""')
        conn.commit()
        print("Database migration completed!")
    
    conn.close()

def init_database():
    """Initialize the SQLite database with required tables"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Goals table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS goals (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            month INTEGER,
            year INTEGER,
            name TEXT,
            description TEXT,
            completion_criteria TEXT,
            header_text TEXT DEFAULT "",
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    # Tasks table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            goal_id INTEGER,
            task_description TEXT,
            task_order INTEGER,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (goal_id) REFERENCES goals (id)
        )
    ''')
    
    # Journal entries table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS journal_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            goal_id INTEGER,
            content TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (goal_id) REFERENCES goals (id)
        )
    ''')
    
    conn.commit()
    conn.close()

def get_current_goal():
    """Get or create goal for current month/year"""
    now = datetime.datetime.now()
    month, year = now.month, now.year
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM goals WHERE month = ? AND year = ?', (month, year))
    goal = cursor.fetchone()
    
    if not goal:
        # Create new goal for this month
        cursor.execute('''
            INSERT INTO goals (month, year, name, description, completion_criteria, header_text)
            VALUES (?, ?, "", "", "", "")
        ''', (month, year))
        conn.commit()
        goal_id = cursor.lastrowid
        goal = (goal_id, month, year, "", "", "", "", None, None)
    
    conn.close()
    return goal

def get_all_goals():
    """Get all goals from database for landing page"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM goals ORDER BY year DESC, month DESC')
    goals = cursor.fetchall()
    
    conn.close()
    return goals

def get_goal_by_id(goal_id):
    """Get specific goal by ID"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM goals WHERE id = ?', (goal_id,))
    goal = cursor.fetchone()
    
    conn.close()
    return goal

def create_new_goal():
    """Create a new goal (not tied to any specific month)"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Just create a new goal with current date for reference
    now = datetime.datetime.now()
    month, year = now.month, now.year
    
    # Create new goal - always creates a new one regardless of month
    cursor.execute('''
        INSERT INTO goals (month, year, name, description, completion_criteria, header_text)
        VALUES (?, ?, "", "", "", "")
    ''', (month, year))
    conn.commit()
    goal_id = cursor.lastrowid
    
    # Create initial empty journal entry for the new goal
    cursor.execute('''
        INSERT INTO journal_entries (goal_id, content)
        VALUES (?, "")
    ''', (goal_id,))
    conn.commit()
    
    # Fetch the newly created goal
    cursor.execute('SELECT * FROM goals WHERE id = ?', (goal_id,))
    new_goal = cursor.fetchone()
    
    conn.close()
    return new_goal

def delete_goal(goal_id):
    """Delete a goal and all associated data (tasks, journal entries)"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Delete associated journal entries
    cursor.execute('DELETE FROM journal_entries WHERE goal_id = ?', (goal_id,))
    
    # Delete associated tasks
    cursor.execute('DELETE FROM tasks WHERE goal_id = ?', (goal_id,))
    
    # Delete the goal itself
    cursor.execute('DELETE FROM goals WHERE id = ?', (goal_id,))
    
    conn.commit()
    conn.close()

def save_goal(goal_id, name, description, completion_criteria, header_text=None):
    """Save goal information"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    if header_text is not None:
        cursor.execute('''
            UPDATE goals 
            SET name = ?, description = ?, completion_criteria = ?, header_text = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (name, description, completion_criteria, header_text, goal_id))
    else:
        cursor.execute('''
            UPDATE goals 
            SET name = ?, description = ?, completion_criteria = ?, updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        ''', (name, description, completion_criteria, goal_id))
    
    conn.commit()
    conn.close()

def get_tasks(goal_id):
    """Get all tasks for a goal"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('SELECT * FROM tasks WHERE goal_id = ? ORDER BY task_order', (goal_id,))
    tasks = cursor.fetchall()
    
    conn.close()
    return tasks

def save_tasks(goal_id, tasks):
    """Save tasks for a goal"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Delete existing tasks
    cursor.execute('DELETE FROM tasks WHERE goal_id = ?', (goal_id,))
    
    # Insert new tasks
    for i, task in enumerate(tasks):
        if task.strip():  # Only save non-empty tasks
            cursor.execute('''
                INSERT INTO tasks (goal_id, task_description, task_order)
                VALUES (?, ?, ?)
            ''', (goal_id, task.strip(), i))
    
    conn.commit()
    conn.close()

def get_journal_content(goal_id):
    """Get journal content for a goal"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    cursor.execute('SELECT content FROM journal_entries WHERE goal_id = ? ORDER BY updated_at DESC LIMIT 1', (goal_id,))
    result = cursor.fetchone()
    
    conn.close()
    return result[0] if result else ""

def save_journal_content(goal_id, content):
    """Save journal content"""
    try:
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        # Check if journal entry exists
        cursor.execute('SELECT id FROM journal_entries WHERE goal_id = ?', (goal_id,))
        existing = cursor.fetchone()
        
        if existing:
            cursor.execute('''
                UPDATE journal_entries 
                SET content = ?, updated_at = CURRENT_TIMESTAMP
                WHERE goal_id = ?
            ''', (content, goal_id))
            print(f"Updated journal for goal_id {goal_id}")
        else:
            cursor.execute('''
                INSERT INTO journal_entries (goal_id, content)
                VALUES (?, ?)
            ''', (goal_id, content))
            print(f"Inserted new journal for goal_id {goal_id}")
        
        conn.commit()
        conn.close()
        print(f"Journal saved successfully. Content length: {len(content)}")
    except Exception as e:
        print(f"Error saving journal: {e}")

def show_landing_page():
    """Display the landing page with all goals"""
    # Landing page header
    st.markdown("""
    <div class="month-header">
        <h1 class="month-title">🎸 Classical Guitar Learning Tracker</h1>
        <p class="header-quote">"The guitar is a small orchestra. It is polyphonic. Every string is a different color, a different voice." - Andrés Segovia 🎸</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Get all goals (fresh from database each time)
    goals = get_all_goals()
    
    
    # Add refresh button
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown('<div class="section-header">📚 Your Goal Sheets</div>', unsafe_allow_html=True)
    with col2:
        if st.button("🔄 Refresh", key="refresh_landing"):
            st.rerun()
    
    if goals:
        # Display goals as clickable cards
        for goal in goals:
            goal_id, month, year, name, description, completion_criteria, header_text, created_at, updated_at = goal
            
            # Create a display name for the goal
            if name and name.strip():
                display_name = name.strip()
            else:
                display_name = f"Untitled Goal #{goal_id}"
            
            # Format creation date
            if created_at:
                try:
                    created_date = datetime.datetime.strptime(created_at, '%Y-%m-%d %H:%M:%S')
                    date_str = created_date.strftime('%B %d, %Y')
                except:
                    date_str = f"{datetime.date(year, month, 1).strftime('%B %Y')}"
            else:
                date_str = f"{datetime.date(year, month, 1).strftime('%B %Y')}"
            
            # Create clickable goal card
            col1, col2 = st.columns([4, 1])
            
            with col1:
                st.markdown(f"""
                <div style="
                    background-color: #faf9f7;
                    padding: 1rem 1.5rem;
                    border-radius: 10px;
                    margin: 0.5rem 0;
                    border: 1px solid #e8dcc0;
                    cursor: pointer;
                ">
                    <h3 style="margin: 0; color: #6b5b47; font-size: 1.2rem;">{display_name}</h3>
                    {f'<p style="margin: 0.5rem 0 0.5rem 0; color: #8b7355; font-size: 0.9rem;">{description[:100]}...</p>' if description and len(description) > 100 else f'<p style="margin: 0.5rem 0 0.5rem 0; color: #8b7355; font-size: 0.9rem;">{description}</p>' if description else ''}
                    <p style="margin: 0; color: #a0956b; font-size: 0.8rem; font-style: italic;">
                        Created: {date_str}
                    </p>
                </div>
                """, unsafe_allow_html=True)
            
            with col2:
                if st.button("Open", key=f"open_goal_{goal_id}"):
                    st.session_state.current_page = "goal"
                    st.session_state.selected_goal_id = goal_id
                    st.rerun()
                
                # Small Complete button with confirmation (less prominent to avoid accidental clicks)
                st.markdown("""
                <style>
                .tiny-complete-btn button {
                    font-size: 0.6rem !important;
                    padding: 0.1rem 0.3rem !important;
                    background-color: #e0d6c0 !important;
                    color: #8b7355 !important;
                    border: 1px solid #d4c4a0 !important;
                    min-height: 1.5rem !important;
                    width: 2.5rem !important;
                    border-radius: 3px !important;
                }
                .tiny-complete-btn button:hover {
                    background-color: #d4c4a0 !important;
                }
                </style>
                """, unsafe_allow_html=True)
                
                with st.container():
                    st.markdown('<div class="tiny-complete-btn">', unsafe_allow_html=True)
                    if st.button("✓", key=f"complete_goal_{goal_id}", help="Mark this goal as completed and delete it"):
                        st.session_state[f'show_confirm_{goal_id}'] = True
                        st.rerun()
                    st.markdown('</div>', unsafe_allow_html=True)
                
                # Show confirmation dialog if delete was requested
                if st.session_state.get(f'show_confirm_{goal_id}', False):
                    st.warning(f"⚠️ Are you sure you want to complete and delete '{display_name}'? This cannot be undone.")
                    col_yes, col_no = st.columns(2)
                    with col_yes:
                        if st.button("Yes, Delete", key=f"confirm_yes_{goal_id}"):
                            delete_goal(goal_id)
                            st.session_state[f'show_confirm_{goal_id}'] = False
                            st.success(f"Goal '{display_name}' completed and deleted!")
                            st.rerun()
                    with col_no:
                        if st.button("Cancel", key=f"confirm_no_{goal_id}"):
                            st.session_state[f'show_confirm_{goal_id}'] = False
                            st.rerun()
    else:
        st.info("No goal sheets yet. Click 'Create New Goal' to get started!")
    
    # Create new goal button
    if st.button("➕ Create New Goal", key="create_new_goal"):
        # Create a new goal (always creates a fresh one)
        new_goal = create_new_goal()
        new_goal_id = new_goal[0]
        st.session_state.current_page = "goal"
        st.session_state.selected_goal_id = new_goal_id
        
        # Clear ALL session state that might interfere with new goal initialization
        keys_to_clear = ['tasks', 'num_tasks', 'journal_content']
        for key in list(st.session_state.keys()):
            if (key.startswith('task_') or 
                key.startswith('journal_content_') or 
                key.startswith('journal_last_saved_') or 
                key.startswith('add_task_') or 
                key.startswith('save_journal_') or 
                key in keys_to_clear):
                del st.session_state[key]
        
        # Initialize fresh session state for the new goal
        st.session_state.num_tasks = 1
        st.session_state.tasks = [""]
        st.session_state[f'journal_content_{new_goal_id}'] = ""
        st.session_state.journal_content = ""
        # Initialize last saved state to empty (since it's a new goal with empty journal)
        st.session_state[f'journal_last_saved_{new_goal_id}'] = ""
        
        st.rerun()

def apply_custom_css():
    """Apply custom CSS for earth tone styling"""
    st.markdown("""
    <style>
    .main {
        background-color: #f5f2e8;
    }
    
    .stApp {
        background-color: #f5f2e8;
    }
    
    .stApp > header {
        background-color: transparent;
    }
    
    .month-header {
        background: linear-gradient(90deg, #8b7355 0%, #a0956b 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        text-align: center;
        margin-bottom: 2rem;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
    }
    
    .month-title {
        font-size: 2.5rem;
        font-weight: 300;
        margin: 0;
        letter-spacing: 2px;
    }
    
    .header-quote {
        font-size: 0.9rem;
        font-weight: 300;
        margin: 0.5rem 0 0 0;
        color: rgba(255, 255, 255, 0.8);
        font-style: italic;
        letter-spacing: 0.5px;
    }
    
    /* Header text input styling */
    .header-input {
        background: transparent !important;
        border: 2px solid rgba(255, 255, 255, 0.3) !important;
        border-radius: 10px !important;
        color: white !important;
        font-size: 2.5rem !important;
        font-weight: 300 !important;
        letter-spacing: 2px !important;
        text-align: center !important;
        padding: 0.5rem 1rem !important;
        margin: 0 !important;
        width: 100% !important;
    }
    
    .header-input:focus {
        border-color: rgba(255, 255, 255, 0.6) !important;
        box-shadow: 0 0 0 2px rgba(255, 255, 255, 0.2) !important;
        outline: none !important;
    }
    
    .header-input::placeholder {
        color: rgba(255, 255, 255, 0.7) !important;
    }
    
    .section-header {
        color: #6b5b47;
        font-size: 1.2rem;
        font-weight: 600;
        margin-bottom: 1rem;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid #d4c4a0;
    }
    
    .stTextInput > div > div > input {
        background-color: #faf9f7;
        border: 1px solid #d4c4a0;
        border-radius: 5px;
        color: #4a4035;
    }
    
    /* Goal name input specific styling - match section header */
    .goal-name-section input {
        font-size: 1.2rem !important;
        color: #6b5b47 !important;
        font-weight: 600 !important;
        height: 80px !important;
    }
    
    .goal-name-section .stTextInput > div > div > input {
        font-size: 1.2rem !important;
        color: #6b5b47 !important;
        font-weight: 600 !important;
        height: 80px !important;
    }
    
    .goal-name-section div[data-testid="stTextInput"] input {
        font-size: 1.2rem !important;
        color: #6b5b47 !important;
        font-weight: 600 !important;
        height: 80px !important;
    }
    
    .stTextArea > div > div > textarea {
        background-color: #faf9f7;
        border: 1px solid #d4c4a0;
        border-radius: 5px;
        color: #4a4035;
        font-family: 'Georgia', serif;
    }
    
    .stButton > button {
        background-color: #8b7355;
        color: white;
        border-radius: 20px;
        border: none;
        padding: 0.5rem 1rem;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        background-color: #6b5b47;
        transform: translateY(-1px);
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
    }
    
    .task-section {
        background-color: #faf9f7;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border: 1px solid #e8dcc0;
    }
    
    .journal-section {
        background-color: #f9f7f4;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border: 1px solid #e8dcc0;
        min-height: 400px;
    }
    
    .add-task-btn {
        display: inline-flex;
        align-items: center;
        justify-content: center;
        width: 40px;
        height: 40px;
        border-radius: 50%;
        background-color: #a0956b;
        color: white;
        font-size: 1.5rem;
        font-weight: bold;
        border: none;
        cursor: pointer;
        margin: 0.5rem 0;
    }
    </style>
    """, unsafe_allow_html=True)

def show_goal_page(goal_id=None):
    """Display the goal page for a specific goal or current month"""
    # Goal page rendering
    
    # Get goal - either specific goal or current month goal
    if goal_id:
        goal = get_goal_by_id(goal_id)
        if not goal:
            st.error("Goal not found!")
            return
    else:
        goal = get_current_goal()
        goal_id = goal[0]
    
    # Initialize session state for tasks - only if not already set for this goal
    existing_tasks = get_tasks(goal_id)
    
    # Check if this is a different goal or first time initialization
    current_goal_key = f'current_goal_id_{goal_id}'
    if (current_goal_key not in st.session_state or 
        st.session_state.get('selected_goal_id') != goal_id or
        'num_tasks' not in st.session_state):
        
        # Initialize from database
        st.session_state.num_tasks = len(existing_tasks) if existing_tasks else 1
        st.session_state.tasks = [task[2] for task in existing_tasks] if existing_tasks else [""]
        st.session_state[current_goal_key] = goal_id
    
    # Ensure tasks list is properly sized (always do this)
    while len(st.session_state.tasks) < st.session_state.num_tasks:
        st.session_state.tasks.append("")
    
    # Initialize journal content for this goal - always ensure it exists
    # Get fresh content from database each time
    journal_from_db = get_journal_content(goal_id)
    
    # Initialize session state for this goal if not set
    journal_key = f'journal_content_{goal_id}'
    if journal_key not in st.session_state:
        st.session_state[journal_key] = journal_from_db
    
    # Initialize "last saved" tracking for save status
    last_saved_key = f'journal_last_saved_{goal_id}'
    if last_saved_key not in st.session_state:
        st.session_state[last_saved_key] = journal_from_db
    
    # Always set the current journal content
    st.session_state.journal_content = st.session_state.get(journal_key, journal_from_db)
    
    # Navigation button back to landing page
    if st.button("← Back to All Goals", key="back_to_landing"):
        st.session_state.current_page = "landing"
        # Clear selected goal ID
        if 'selected_goal_id' in st.session_state:
            del st.session_state.selected_goal_id
        st.rerun()
    
    # Dynamic Header Section - shows goal name or fallback to date
    goal_name_from_db = goal[3] if goal[3] else ""
    header_text = goal_name_from_db.strip() if goal_name_from_db.strip() else datetime.datetime.now().strftime("%B %Y")
    st.markdown(f"""
    <div class="month-header">
        <h1 class="month-title">{header_text}</h1>
        <p class="header-quote">"The guitar is a small orchestra. It is polyphonic. Every string is a different color, a different voice." - Andrés Segovia 🎸</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Goal Input Section
    st.markdown('<div class="section-header">🎯 S.M.A.R.T Goal</div>', unsafe_allow_html=True)
    
    # Apply inline style directly to the text input
    st.markdown("""
    <style>
    /* Use very specific selectors to override Streamlit defaults */
    div[data-testid="stTextInput"]:has(input[aria-label="Goal Name"]) input,
    .stTextInput:has(input[aria-label="Goal Name"]) input,
    input[aria-label="Goal Name"] {
        font-size: 1.2rem !important;
        color: #6b5b47 !important;
        font-weight: 600 !important;
        height: 80px !important;
        line-height: normal !important;
        padding: 0 10px !important;
        margin: 0 !important;
        text-align: left !important;
        box-sizing: border-box !important;
        transform: translateY(-17px) !important;
        position: relative !important;
    }
    
    /* Fallback with element attribute selector */
    input[placeholder*="Bach"] {
        font-size: 1.2rem !important;
        color: #6b5b47 !important;
        font-weight: 600 !important;
        height: 80px !important;
        line-height: normal !important;
        padding: 0 10px !important;
        margin: 0 !important;
        text-align: left !important;
        box-sizing: border-box !important;
        transform: translateY(-17px) !important;
        position: relative !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    goal_name = st.text_input(
        "Goal Name",
        value=goal[3],
        placeholder="e.g., Learn Bach's Minuet in G Major",
        help="Brief, clear name for your monthly goal",
        key="goal_name_input"
    )
    
    # JavaScript injection to force styling if CSS fails
    st.markdown("""
    <script>
    setTimeout(function() {
        const goalInput = document.querySelector('input[placeholder*="Bach"]');
        if (goalInput) {
            goalInput.style.fontSize = '1.2rem';
            goalInput.style.color = '#6b5b47';
            goalInput.style.fontWeight = '600';
            goalInput.style.height = '80px';
            goalInput.style.lineHeight = 'normal';
            goalInput.style.padding = '0 10px';
            goalInput.style.margin = '0';
            goalInput.style.textAlign = 'left';
            goalInput.style.boxSizing = 'border-box';
            goalInput.style.transform = 'translateY(-17px)';
            goalInput.style.position = 'relative';
        }
    }, 1000);
    </script>
    """, unsafe_allow_html=True)
    
    goal_description = st.text_area(
        "Goal Description & Completion Criteria",
        value=f"{goal[4]}\n\n{goal[5]}" if goal[4] or goal[5] else "",
        height=100,
        placeholder="Describe your goal in detail and define what completion looks like...",
        help="What exactly do you want to achieve and how will you know you've succeeded?"
    )
    
    # Auto-save goal when changed - but avoid infinite loops with empty values
    goal_desc_comparison = f"{goal[4]}\n\n{goal[5]}" if goal[4] or goal[5] else ""
    
    # Only save if there are actual meaningful changes (not empty to empty)
    should_save = False
    if goal_name.strip() != (goal[3] or "").strip():
        should_save = True
    elif goal_description.strip() != goal_desc_comparison.strip():
        should_save = True
    
    if should_save:
        # Split description into description and criteria
        desc_parts = goal_description.split('\n\n', 1)
        description = desc_parts[0] if len(desc_parts) > 0 else ""
        criteria = desc_parts[1] if len(desc_parts) > 1 else ""
        save_goal(goal_id, goal_name, description, criteria)
        # Force refresh of goal data
        st.rerun()
    
    st.markdown("---")
    
    # Tasks Section
    st.markdown('<div class="section-header">📋 Practice Tasks</div>', unsafe_allow_html=True)
    
    
    # Debug info (remove after testing)
    # st.write(f"Debug: num_tasks = {st.session_state.num_tasks}, tasks = {st.session_state.tasks}")
    
    # Ensure we have at least one task slot
    if st.session_state.num_tasks < 1:
        st.session_state.num_tasks = 1
    
    # Ensure tasks list is properly sized
    while len(st.session_state.tasks) < st.session_state.num_tasks:
        st.session_state.tasks.append("")
    
    # Display task input fields
    for i in range(st.session_state.num_tasks):
        task_value = st.session_state.tasks[i] if i < len(st.session_state.tasks) else ""
        
        new_task = st.text_input(
            f"Task {i+1}",
            value=task_value,
            key=f"task_{goal_id}_{i}",  # Make key unique per goal
            placeholder=f"Enter practice task {i+1}..."
        )
        
        if new_task != task_value:
            # Update the tasks list
            if i >= len(st.session_state.tasks):
                st.session_state.tasks.extend([""] * (i - len(st.session_state.tasks) + 1))
            st.session_state.tasks[i] = new_task
            save_tasks(goal_id, st.session_state.tasks)
    
    # Add task button (only show if less than 5 tasks)
    if st.session_state.num_tasks < 5:
        add_task_key = f"add_task_{goal_id}"
        if st.button("➕ Add Task", key=add_task_key):
            # Ensure we don't exceed the list bounds
            if st.session_state.num_tasks < 5:
                st.session_state.num_tasks += 1
                # Ensure tasks list is properly sized
                while len(st.session_state.tasks) < st.session_state.num_tasks:
                    st.session_state.tasks.append("")
                # Save the updated task structure to prevent loss on rerun
                save_tasks(goal_id, st.session_state.tasks)
                st.rerun()
    
    st.markdown("---")
    
    # Journal Section
    st.markdown('<div class="section-header">📝 Practice Journal</div>', unsafe_allow_html=True)
    
    # Ensure we always have a journal content value - use multiple fallbacks
    current_journal_value = st.session_state.get('journal_content', '')
    if not current_journal_value:
        # Fallback to goal-specific session state
        journal_key = f'journal_content_{goal_id}'
        current_journal_value = st.session_state.get(journal_key, '')
    
    # Always render the journal text area
    new_journal_content = st.text_area(
        "Daily Practice Reflections",
        value=current_journal_value,
        height=400,
        placeholder="""Record your daily practice sessions here...
|
• What did you work on today?
• What challenges did you face?
• What breakthroughs or improvements did you notice?
• How did you feel about your practice session?
• What will you focus on tomorrow?
|
This is your personal space for reflection and growth.""",
        help="This is the heart of your tracker - write freely about your practice journey. Save status updates when you click outside this text area.",
        label_visibility="collapsed",
        key=f"journal_text_area_{goal_id}"
    )
    
    # Note: Save status updates when text area loses focus (standard Streamlit behavior)
    
    # Manual save button
    if st.button("💾 Save Journal", key=f"save_journal_{goal_id}"):
        # Save to both goal-specific and general session state
        journal_key = f'journal_content_{goal_id}'
        st.session_state.journal_content = new_journal_content
        st.session_state[journal_key] = new_journal_content
        # Save to database
        save_journal_content(goal_id, new_journal_content)
        # Update the "last saved" state to match current content
        st.session_state[f'journal_last_saved_{goal_id}'] = new_journal_content
        st.success("✅ Journal saved successfully!")
        st.rerun()  # Refresh to clear the success message
    
    # Footer info
    st.markdown("---")
    st.markdown(
        '<div style="text-align: center; color: #8b7355; font-style: italic; padding: 1rem;">🎸 Your classical guitar learning journey - one day at a time 🎸</div>',
        unsafe_allow_html=True
    )

def main():
    """Main function with page navigation"""
    st.set_page_config(
        page_title="Classical Guitar Learning Tracker",
        page_icon="🎸",
        layout="wide",
        initial_sidebar_state="collapsed"
    )
    
    # Apply custom styling
    apply_custom_css()
    
    # Initialize database
    init_database()
    
    # Run database migration if needed
    migrate_database()
    
    # Initialize page state
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "landing"
    
    # Route to appropriate page
    if st.session_state.current_page == "landing":
        show_landing_page()
    elif st.session_state.current_page == "goal":
        goal_id = st.session_state.get('selected_goal_id', None)
        show_goal_page(goal_id)

if __name__ == "__main__":
    main()
