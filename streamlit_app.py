import streamlit as st
import requests

from datetime import date, timedelta


# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

API_URL = "http://127.0.0.1:8000"

st.set_page_config(
    page_title="Taskly | Task Manager",
    page_icon="📋",
    layout="wide",
    initial_sidebar_state="expanded"
)


# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

st.markdown("""
<style>
    .stApp {
        background: #f5f7fb;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        max-width: 1450px;
    }

    h1, h2, h3 {
        color: #172033;
    }

    .dashboard-subtitle {
        color: #697386;
        font-size: 14px;
        margin-top: -12px;
        margin-bottom: 25px;
    }

    .metric-card {
        background: white;
        padding: 22px;
        border-radius: 16px;
        border: 1px solid #edf0f5;
        box-shadow: 0 4px 15px rgba(20, 30, 50, 0.05);
        min-height: 120px;
    }

    .metric-label {
        color: #647084;
        font-size: 13px;
        font-weight: 500;
    }

    .metric-value {
        color: #172033;
        font-size: 30px;
        font-weight: 750;
        margin-top: 8px;
    }

    .section-card {
        background: white;
        border: 1px solid #edf0f5;
        border-radius: 16px;
        padding: 20px;
        margin-bottom: 15px;
        box-shadow: 0 4px 15px rgba(20, 30, 50, 0.04);
    }

    .task-title {
        font-size: 16px;
        font-weight: 700;
        color: #202b40;
    }

    .task-description {
        color: #707b8d;
        font-size: 13px;
    }

    .task-meta {
        color: #6b7280;
        font-size: 12px;
    }

    .priority-score {
        background: #fff0df;
        color: #c66b18;
        border-radius: 7px;
        padding: 5px 9px;
        font-size: 12px;
        font-weight: 700;
    }

    div[data-testid="stMetric"] {
        background: white;
        padding: 16px;
        border-radius: 13px;
        border: 1px solid #edf0f5;
    }

    div[data-testid="stForm"] {
        border: none;
    }

    .stButton button {
        border-radius: 9px;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)


# --------------------------------------------------
# API FUNCTIONS
# --------------------------------------------------

def api_request(method, endpoint, **kwargs):
    try:
        response = requests.request(
            method,
            f"{API_URL}{endpoint}",
            timeout=5,
            **kwargs
        )

        if response.status_code >= 400:
            try:
                detail = response.json().get("detail", response.text)
            except ValueError:
                detail = response.text

            return None, str(detail)

        if response.status_code == 204 or not response.content:
            return {}, None

        return response.json(), None

    except requests.exceptions.ConnectionError:
        return None, "FastAPI backend is not running."

    except requests.exceptions.Timeout:
        return None, "API request timed out."

    except requests.exceptions.RequestException as error:
        return None, str(error)


def get_tasks():
    return api_request("GET", "/tasks")


def calculate_priority_score(task):
    """Dashboard sorting score; higher score means more urgent."""

    score = {
        "High": 12,
        "Medium": 8,
        "Low": 4
    }.get(task.get("priority", "Medium"), 4)

    difficulty = task.get("difficulty", 5)
    score += difficulty * 0.5

    due_date = task.get("due_date")

    if due_date:
        due = date.fromisoformat(due_date)
        days_left = (due - date.today()).days

        if days_left < 0:
            score += 10
        elif days_left == 0:
            score += 8
        elif days_left <= 2:
            score += 6
        elif days_left <= 7:
            score += 4
        else:
            score += 1

    return round(score, 1)


def get_due_status(task):
    due_date = task.get("due_date")

    if not due_date:
        return "No deadline"

    due = date.fromisoformat(due_date)
    days_left = (due - date.today()).days

    if days_left < 0:
        return "Overdue"

    if days_left == 0:
        return "Today"

    if days_left == 1:
        return "Tomorrow"

    return f"In {days_left} days"


def update_task(task_id, task_data):
    return api_request(
        "PUT",
        f"/tasks/{task_id}",
        json=task_data
    )


# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:
    st.title("📋 Taskly")
    st.caption("Smart Task Management")

    st.divider()

    st.subheader("Navigation")
    st.markdown("🏠 Dashboard")
    st.markdown("📌 All Tasks")
    st.markdown("📅 Upcoming Tasks")

    st.divider()

    st.subheader("➕ Add New Task")

    with st.form("add_task_form", clear_on_submit=True):

        new_id = st.number_input(
            "Task ID",
            min_value=1,
            step=1
        )

        new_title = st.text_input("Task Title")

        new_description = st.text_area("Description")

        new_priority = st.selectbox(
            "Priority",
            ["Low", "Medium", "High"],
            index=1
        )

        new_due_date = st.date_input(
            "Due Date",
            value=date.today() + timedelta(days=2)
        )

        new_duration = st.selectbox(
            "Estimated Duration",
            [
                "Very Short (0-1h)",
                "Short (1-3h)",
                "Medium (3-5h)",
                "Long (5h+)"
            ]
        )

        new_difficulty = st.slider(
            "Difficulty",
            min_value=1,
            max_value=12,
            value=5
        )

        add_button = st.form_submit_button(
            "➕ Create Task",
            use_container_width=True
        )

        if add_button:

            if not new_title.strip() or not new_description.strip():
                st.error("Title and description are required.")

            else:
                payload = {
                    "id": int(new_id),
                    "title": new_title.strip(),
                    "description": new_description.strip(),
                    "completed": False,
                    "due_date": new_due_date.isoformat(),
                    "priority": new_priority,
                    "duration": new_duration,
                    "difficulty": new_difficulty
                }

                result, error = api_request(
                    "POST",
                    "/tasks",
                    json=payload
                )

                if error:
                    st.error(error)
                else:
                    st.success("Task created successfully!")
                    st.rerun()


# --------------------------------------------------
# BACKEND CONNECTION
# --------------------------------------------------

health, health_error = api_request("GET", "/")

if not health:
    st.error("FastAPI backend is disconnected.")
    st.warning(health_error)
    st.info("Run `uvicorn main:app --reload` in another terminal.")
    st.stop()


# --------------------------------------------------
# LOAD TASKS
# --------------------------------------------------

tasks, error = get_tasks()

if error:
    st.error(error)
    st.stop()

active_tasks = [
    task for task in tasks
    if not task["completed"]
]

completed_tasks = [
    task for task in tasks
    if task["completed"]
]

urgent_tasks = [
    task for task in active_tasks
    if get_due_status(task) in ["Today", "Overdue"]
]

upcoming_tasks = [
    task for task in active_tasks
    if task.get("due_date")
    and date.fromisoformat(task["due_date"]) >= date.today()
]

ranked_tasks = sorted(
    active_tasks,
    key=calculate_priority_score,
    reverse=True
)


# --------------------------------------------------
# HEADER
# --------------------------------------------------

header_col1, header_col2 = st.columns([4, 1])

with header_col1:
    st.title("Your Tasks Dashboard")
    st.markdown(
        '<p class="dashboard-subtitle">'
        'AI-powered task prioritization and scheduling'
        '</p>',
        unsafe_allow_html=True
    )

with header_col2:
    st.write("")
    st.write("")
    if st.button("🔄 Refresh Dashboard", use_container_width=True):
        st.rerun()


# --------------------------------------------------
# STATISTICS
# --------------------------------------------------

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Active Tasks</div>
        <div class="metric-value">{len(active_tasks)}</div>
        <div style="color:#4777ec;">◷ In Progress</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Urgent Tasks</div>
        <div class="metric-value">{len(urgent_tasks)}</div>
        <div style="color:#e65b2e;">⚠ Needs Attention</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Completed</div>
        <div class="metric-value">{len(completed_tasks)}</div>
        <div style="color:#299d58;">✓ Finished Tasks</div>
    </div>
    """, unsafe_allow_html=True)


st.write("")


# --------------------------------------------------
# MAIN DASHBOARD LAYOUT
# --------------------------------------------------

left_column, right_column = st.columns([2.1, 1])


# --------------------------------------------------
# PRIORITY TASKS
# --------------------------------------------------

with left_column:

    with st.container(border=True):

        st.subheader("📈 Taskly")
        st.caption("Ranked by Priority Score")

        if not ranked_tasks:
            st.info("No active tasks. Add a new task to get started.")

        for task in ranked_tasks:

            score = calculate_priority_score(task)
            status = get_due_status(task)

            with st.container(border=True):

                task_col, score_col = st.columns([5, 1])

                with task_col:

                    st.markdown(
                        f"**{task['title']}**"
                    )

                    st.caption(task["description"])

                    meta1, meta2, meta3 = st.columns(3)

                    meta1.caption(
                        f"⚡ {task.get('priority', 'Medium')}"
                    )

                    meta2.caption(
                        f"📅 {status}"
                    )

                    meta3.caption(
                        f"🎯 Difficulty: {task.get('difficulty', 5)}/12"
                    )

                    st.caption(
                        f"⏱ {task.get('duration', 'Medium (3-5h)')}"
                    )

                with score_col:
                    st.markdown(
                        f'<span class="priority-score">{score} pts</span>',
                        unsafe_allow_html=True
                    )

                # Mark task complete
                completed = st.checkbox(
                    "Mark as completed",
                    value=task["completed"],
                    key=f"complete_{task['id']}"
                )

                if completed != task["completed"]:

                    payload = {
                        **task,
                        "completed": completed
                    }

                    result, error = update_task(task["id"], payload)

                    if error:
                        st.error(error)
                    else:
                        st.success("Task status updated!")
                        st.rerun()

                # Edit task
                with st.expander("✏️ Edit Task"):

                    with st.form(f"edit_{task['id']}"):

                        edit_title = st.text_input(
                            "Title",
                            value=task["title"]
                        )

                        edit_description = st.text_area(
                            "Description",
                            value=task["description"]
                        )

                        edit_priority = st.selectbox(
                            "Priority",
                            ["Low", "Medium", "High"],
                            index=["Low", "Medium", "High"].index(
                                task.get("priority", "Medium")
                            )
                        )

                        edit_due_date = st.date_input(
                            "Due Date",
                            value=(
                                date.fromisoformat(task["due_date"])
                                if task.get("due_date")
                                else date.today()
                            )
                        )

                        edit_duration = st.selectbox(
                            "Duration",
                            [
                                "Very Short (0-1h)",
                                "Short (1-3h)",
                                "Medium (3-5h)",
                                "Long (5h+)"
                            ],
                            index=[
                                "Very Short (0-1h)",
                                "Short (1-3h)",
                                "Medium (3-5h)",
                                "Long (5h+)"
                            ].index(task.get("duration", "Medium (3-5h)"))
                        )

                        edit_difficulty = st.slider(
                            "Difficulty",
                            1,
                            12,
                            task.get("difficulty", 5),
                            key=f"difficulty_{task['id']}"
                        )

                        save = st.form_submit_button("Save Changes")

                        if save:

                            if not edit_title.strip() or not edit_description.strip():
                                st.error("Please fill all required fields.")

                            else:

                                payload = {
                                    "id": task["id"],
                                    "title": edit_title.strip(),
                                    "description": edit_description.strip(),
                                    "completed": task["completed"],
                                    "due_date": edit_due_date.isoformat(),
                                    "priority": edit_priority,
                                    "duration": edit_duration,
                                    "difficulty": edit_difficulty
                                }

                                result, error = update_task(
                                    task["id"],
                                    payload
                                )

                                if error:
                                    st.error(error)
                                else:
                                    st.success("Task updated!")
                                    st.rerun()

                # Delete task
                if st.button(
                    "🗑️ Delete Task",
                    key=f"delete_{task['id']}"
                ):

                    result, error = api_request(
                        "DELETE",
                        f"/tasks/{task['id']}"
                    )

                    if error:
                        st.error(error)
                    else:
                        st.success("Task deleted!")
                        st.rerun()


# --------------------------------------------------
# UPCOMING TASKS
# --------------------------------------------------

with right_column:

    with st.container(border=True):

        st.subheader("📅 Upcoming Tasks")

        if not upcoming_tasks:
            st.info("No upcoming deadlines.")

        else:

            sorted_upcoming = sorted(
                upcoming_tasks,
                key=lambda task: task["due_date"]
            )

            for task in sorted_upcoming:

                status = get_due_status(task)

                with st.container(border=True):

                    st.markdown(f"**{task['title']}**")

                    if status == "Today":
                        st.error("🔴 Today")

                    elif status == "Tomorrow":
                        st.warning("🟡 Tomorrow")

                    else:
                        st.info(f"📅 {status}")

                    st.caption(
                        f"Priority: {task.get('priority', 'Medium')}"
                    )


# --------------------------------------------------
# COMPLETED TASKS
# --------------------------------------------------

st.divider()

st.subheader("✅ Completed Tasks")

if not completed_tasks:
    st.info("No completed tasks yet.")

else:

    for task in completed_tasks:

        with st.container(border=True):

            col1, col2 = st.columns([4, 1])

            with col1:
                st.markdown(f"~~{task['title']}~~")
                st.caption(task["description"])

            with col2:
                st.success("Completed")


# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "Taskly Dashboard | Built with Python, FastAPI and Streamlit"
)