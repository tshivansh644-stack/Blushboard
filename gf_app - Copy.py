import streamlit as st
import datetime
import time
import json
import random
import os
from collections import defaultdict

# ==========================================
# 🌸 1. INITIALIZATION & CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="Blushboard",
    page_icon="🌸",
    layout="centered",
    initial_sidebar_state="collapsed"
)

# DATABASE FILE PATH
DB_FILE = "blushboard_data.json"

# ===== LOAD DATA FROM FILE =====
def load_data():
    """Load all data from JSON file"""
    if os.path.exists(DB_FILE):
        try:
            with open(DB_FILE, "r") as f:
                return json.load(f)
        except:
            return {}
    return {}

def save_data(data):
    """Save all data to JSON file"""
    try:
        with open(DB_FILE, "w") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        st.error(f"Error saving data: {e}")

# Initialize Session States for persistent storage across multi-page wipes
if "current_page" not in st.session_state:
    st.session_state.current_page = "Dashboard"

if "logs" not in st.session_state:
    st.session_state.logs = load_data()

if "meds_config" not in st.session_state:
    st.session_state.meds_config = []

if "study_session" not in st.session_state:
    st.session_state.study_session = {
        "active": False,
        "subject": "",
        "target_hours": 0,
        "target_minutes": 0,
        "start_timestamp": 0.0,
        "accumulated_time": 0.0,
        "paused": False,
        "pause_timestamp": 0.0
    }

if "splash_done" not in st.session_state:
    st.session_state.splash_done = False

# Notification throttling state
if "last_teaser_ts" not in st.session_state:
    st.session_state.last_teaser_ts = 0.0
if "dashboard_arrived_ts" not in st.session_state:
    st.session_state.dashboard_arrived_ts = 0.0

# Get dates for timing calculation
TODAY = datetime.date.today()

# ==========================================
# 🎀 2. ROMANTIC COQUETTE INJECTED CSS
# ==========================================
COQUETTE_STIKERS = ["🧸", "🎀", "☕", "🕯️", "🐱", "💝", "🌸", "🐇", "🦢", "🍒"]
random.seed(42)

sticker_css = ""
for i, sticker in enumerate(COQUETTE_STIKERS):
    top = random.randint(12, 88)
    left = random.randint(5, 90)
    sticker_css += f"""
    .sticker-{i} {{
        position: fixed;
        top: {top}vh;
        left: {left}vw;
        font-size: 1.8rem;
        opacity: 0.25;
        pointer-events: none;
        z-index: 0;
    }}
    """

style_payload = f"""
<style>
    {sticker_css}
    @import url('https://fonts.googleapis.com/css2?family=Fredoka:wght@300..700&display=swap');
    
    html, body, [data-testid="stAppViewContainer"] {{
        background-color: #fff0f3 !important;
        font-family: 'Fredoka', sans-serif !important;
        color: #4a2c3a !important;
    }}
    
    .stButton>button {{
        background-color: #ffe5ec !important;
        color: #4a2c3a !important;
        border: 2px solid #ffc2d1 !important;
        border-radius: 20px !important;
        padding: 0.5rem 1.5rem !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 6px rgba(255, 179, 193, 0.2) !important;
    }}
    
    .stButton>button:hover {{
        background-color: #ffc2d1 !important;
        transform: translateY(-2px) !important;
    }}
    
    div[data-testid="stTextInput"]>div>div>input,
    div[data-testid="stNumberInput"]>div>div>input,
    div[data-testid="stSelectbox"]>div>div {{
        border-radius: 15px !important;
        border: 2px solid #ffc2d1 !important;
        background-color: #ffffff !important;
        color: #4a2c3a !important;
    }}
    
    .dashboard-card {{
        background: rgba(255, 240, 243, 0.8);
        border: 2px dashed #ffb3c1;
        border-radius: 24px;
        padding: 25px;
        text-align: center;
        margin-bottom: 20px;
        cursor: pointer;
        transition: transform 0.2s ease, box-shadow 0.2s ease;
    }}
    
    .dashboard-card:hover {{
        transform: scale(1.03);
        box-shadow: 0 10px 20px rgba(255, 179, 193, 0.3);
    }}
    
    .water-count-text {{
        color: #4a2c3a !important;
        font-size: 3rem !important;
        font-weight: bold !important;
        margin: 15px 0 !important;
    }}

    /* Splash Screen Styling */
    .splash-container {{
        position: fixed;
        top: 0; left: 0; width: 100vw; height: 100vh;
        background-color: #fff0f3;
        z-index: 999999;
        display: flex;
        justify-content: center;
        align-items: center;
        font-family: 'Fredoka', sans-serif;
    }}
    
    .splash-content-1 {{
        font-size: 4rem;
        color: #ff4d6d;
        font-weight: bold;
        animation: fadeSequence 5s forwards;
        text-align: center;
    }}
    
    @keyframes fadeSequence {{
        0% {{ opacity: 0; transform: scale(0.9); }}
        10% {{ opacity: 1; transform: scale(1); }}
        40% {{ opacity: 1; }}
        45% {{ opacity: 0; }}
        55% {{ opacity: 0; }}
        65% {{ opacity: 1; }}
        90% {{ opacity: 1; }}
        100% {{ opacity: 0; }}
    }}
</style>
"""
st.markdown(style_payload, unsafe_allow_html=True)

# Render background decorative graphics
for i, sticker in enumerate(COQUETTE_STIKERS):
    st.markdown(f'<div class="sticker-{i}">{sticker}</div>', unsafe_allow_html=True)

# ==========================================
# 🎬 3. SPLASH SCREEN (PROPERLY FIXED)
# ==========================================
if not st.session_state.splash_done:
    placeholder = st.empty()
    with placeholder.container():
        st.markdown("""
            <div class="splash-container" id="splash-main">
                <div id="splash-text" class="splash-content-1">BlushBoard 🎀</div>
            </div>
            <script>
                setTimeout(function() {
                    var textEl = document.getElementById("splash-text");
                    textEl.innerHTML = "From Baccha For My Dumb Girl ❤️";
                }, 2200);
                
                setTimeout(function() {
                    var splashMain = document.getElementById("splash-main");
                    splashMain.style.display = "none";
                }, 5000);
            </script>
        """, unsafe_allow_html=True)
    time.sleep(5.5)
    placeholder.empty()
    st.session_state.splash_done = True
    st.rerun()

# ==========================================
# 🌐 4. JAVASCRIPT NOTIFICATION INJECTOR
# ==========================================
notification_js = """
<script>
function requestNotificationPermission() {
    if (!("Notification" in window)) {
        console.log("This browser does not support desktop notification");
    } else if (Notification.permission === "granted") {
        // Already granted
    } else if (Notification.permission !== "denied") {
        Notification.requestPermission();
    }
}
setTimeout(requestNotificationPermission, 1000);

function sendTeasingNotification(title, message) {
    if (Notification.permission === "granted") {
        new Notification(title, { body: message, icon: "https://em-content.zobj.net/source/apple/391/ribbon_1f380.png" });
    }
}
window.sendTeasingNotification = sendTeasingNotification;
</script>
"""
st.markdown(notification_js, unsafe_allow_html=True)

def dispatch_notification(title, body):
    st.markdown(f"""
    <script>
    if (window.sendTeasingNotification) {{
        window.sendTeasingNotification("{title}", "{body}");
    }}
    </script>
    """, unsafe_allow_html=True)

# Throttled teasing notifications
NOTIF_MIN_INTERVAL = 15 * 60
NOTIF_SOFT_DELAY = 8

if st.session_state.current_page == "Dashboard":
    now_ts = time.time()

    if st.session_state.dashboard_arrived_ts == 0.0:
        st.session_state.dashboard_arrived_ts = now_ts

    since_last = now_ts - st.session_state.last_teaser_ts
    since_arrived = now_ts - st.session_state.dashboard_arrived_ts

    if (
        since_last >= NOTIF_MIN_INTERVAL
        and since_arrived >= NOTIF_SOFT_DELAY
        and random.random() < 0.20
    ):
        teasing_prompts = [
            ("Hey Dumb Girl! 🎀", "Did you lose your phone or keys again today? Check your pockets!"),
            ("Excuse me! ☕", "Did you actually eat a full healthy meal or just snacks?"),
            ("Put the phone down! 📱", "Stop mindless scrolling on Instagram right now, mister is watching!"),
            ("Stay Hydrated! 💧", "Drink some water right now, yes, right now!")
        ]
        alert = random.choice(teasing_prompts)
        dispatch_notification(alert[0], alert[1])
        st.session_state.last_teaser_ts = now_ts
else:
    st.session_state.dashboard_arrived_ts = 0.0

# ==========================================
# 📅 5. TOP-RIGHT ELEGANT DATE PICKER
# ==========================================
col_title, col_date = st.columns([2, 1])
with col_title:
    if st.session_state.current_page == "Dashboard":
        st.markdown("<h1 style='margin:0; padding:0; color:#4a2c3a;'>🌸 Blushboard</h1>", unsafe_allow_html=True)
    else:
        if st.button("⬅️ Back to Main Menu"):
            st.session_state.current_page = "Dashboard"
            st.rerun()
with col_date:
    selected_date = st.date_input("📅 View Target Archive:", TODAY, label_visibility="collapsed")

selected_date_str = selected_date.strftime("%Y-%m-%d")

if selected_date_str not in st.session_state.logs:
    st.session_state.logs[selected_date_str] = {
        "things_i_did": [],
        "boyfriend_notes": [],
        "meds": {},
        "water_intake": 0,
        "period": False,
        "menstrual_stage": "Menstrual Phase 🩸",
        "symptoms": [],
        "mood": "Cozy 🎀",
        "last_period_date": None,
        "period_history": []
    }
    save_data(st.session_state.logs)

IS_ACTIVE_TODAY = (selected_date == TODAY)

# ==========================================
# 🗂️ 6. PAGE DISPLAY PIPELINE ENGINE
# ==========================================

# --- PAGE A: MAIN DASHBOARD MENU ---
if st.session_state.current_page == "Dashboard":
    st.markdown("<p style='text-align: center; font-style: italic; color: #a27086;'>\"The elegant navigation hub tailored for my favorite person.\"</p>", unsafe_allow_html=True)
    st.write("---")

    row1_col1, row1_col2 = st.columns(2)
    row2_col1, row2_col2 = st.columns(2)
    row3_col1, _ = st.columns([1, 1])

    with row1_col1:
        st.markdown('<div class="dashboard-card"><h3>💊 Meds Tracker</h3><p>Manage dynamic intake time windows</p></div>', unsafe_allow_html=True)
        if st.button("Open Meds Hub", key="btn_meds"):
            st.session_state.current_page = "Meds Tracker"
            st.rerun()

    with row1_col2:
        st.markdown('<div class="dashboard-card"><h3>💧 Water Log</h3><p>Ensure standard hydration parameters</p></div>', unsafe_allow_html=True)
        if st.button("Open Hydration Hub", key="btn_water"):
            st.session_state.current_page = "Water Log"
            st.rerun()

    with row2_col1:
        st.markdown('<div class="dashboard-card"><h3>📚 Study Hub</h3><p>Deep focus engine with playlists</p></div>', unsafe_allow_html=True)
        if st.button("Open Study Hub", key="btn_study"):
            st.session_state.current_page = "Study Hub"
            st.rerun()

    with row2_col2:
        st.markdown('<div class="dashboard-card"><h3>🩸 Cycle Period Tracker</h3><p>Monitor comprehensive physiological health logs</p></div>', unsafe_allow_html=True)
        if st.button("Open Period Tracker", key="btn_periods"):
            st.session_state.current_page = "Period Tracker"
            st.rerun()

    with row3_col1:
        st.markdown('<div class="dashboard-card"><h3>❤️ Connecting Loved Ones</h3><p>Share daily items & updates</p></div>', unsafe_allow_html=True)
        if st.button("Open Relationship Hub", key="btn_connecting"):
            st.session_state.current_page = "Relationship Hub"
            st.rerun()


# --- PAGE B: MEDICATION MANAGEMENT ---
elif st.session_state.current_page == "Meds Tracker":
    st.markdown("<h2>💊 Isolated Medication Log Window</h2>", unsafe_allow_html=True)
    st.write(f"Tracking Schedule Records for: **{selected_date_str}**")

    st.write("---")
    st.markdown("### ➕ Add Custom Scheduled Medicine")
    if not IS_ACTIVE_TODAY:
        st.info("🔒 Medication lists and logs can only be customized and adjusted on the current calendar day.")
    else:
        new_med_name = st.text_input("Medicine Name:", placeholder="e.g., Vitamin C Tablet")
        new_med_time = st.time_input("Target Daily Intake Time Window:", value=datetime.time(9, 0))
        if st.button("Add Registered Medicine Slot"):
            if new_med_name.strip() != "":
                time_str = new_med_time.strftime("%H:%M")
                if {"name": new_med_name.strip(), "time": time_str} not in st.session_state.meds_config:
                    st.session_state.meds_config.append({"name": new_med_name.strip(), "time": time_str})
                    st.success(f"Successfully configured active target slot for: {new_med_name}")
                    st.rerun()

    st.write("---")
    st.markdown("### 🗓️ Active Scheduled Checklist")
    if not st.session_state.meds_config:
        st.info("No customized medicines configured yet. Use the dynamic field above to register your slots!")
    else:
        for index, med_obj in enumerate(st.session_state.meds_config):
            m_name = med_obj["name"]
            m_time = med_obj["time"]

            st.markdown(f"#### 💊 {m_name}")
            st.caption(f"Strict delivery operational targeting window: **{m_time}**")

            current_status = st.session_state.logs[selected_date_str]["meds"].get(m_name, False)
            st.write(f"Status Verify: {'✅ Intake Logged' if current_status else '❌ Not Marked Yet'}")

            is_locked = False

            if not IS_ACTIVE_TODAY:
                is_locked = True
            else:
                now = datetime.datetime.now()
                sched_hour, sched_min = map(int, m_time.split(":"))
                sched_datetime = datetime.datetime.combine(TODAY, datetime.time(sched_hour, sched_min))
                difference_seconds = (now - sched_datetime).total_seconds()

                if abs(difference_seconds) > 300:
                    is_locked = True

            if is_locked:
                st.button("Toggle Verification Status", key=f"btn_med_lock_{index}", disabled=True)
            else:
                if st.button("Toggle Verification Status", key=f"btn_med_active_{index}"):
                    st.session_state.logs[selected_date_str]["meds"][m_name] = not current_status
                    save_data(st.session_state.logs)
                    st.success("Log parameters updated.")
                    st.rerun()
            
            if is_locked and not st.session_state.logs[selected_date_str]["meds"].get(m_name, False):
                if not IS_ACTIVE_TODAY:
                    st.info("🔒 Historical or future archive record is marked read-only.")
                else:
                    st.info("🔒 Intake validation engine is locked. Toggle opens strictly within a 10-minute window (5m before/after scheduled time).")


# --- PAGE C: CLEAN WATER LOG HUB ---
elif st.session_state.current_page == "Water Log":
    st.markdown("<h2>💧 Daily Water Log</h2>", unsafe_allow_html=True)
    st.write(f"Hydration Log for: **{selected_date_str}**")

    current_water = st.session_state.logs[selected_date_str]["water_intake"]

    display_suffix = "Glass" if current_water == 1 else "Glasses"
    st.markdown(f'<div class="water-count-text">{current_water} {display_suffix}</div>', unsafe_allow_html=True)
    st.caption("Target Framework Recommendation: 8 Glasses Daily")

    st.write("---")
    if not IS_ACTIVE_TODAY:
        st.warning("🔒 Viewing archive log frame. Fluid parameter mutation controls are locked.")
    else:
        if st.button("➕ Add 1 Glass"):
            st.session_state.logs[selected_date_str]["water_intake"] += 1
            save_data(st.session_state.logs)
            st.rerun()


# --- PAGE D: COMPREHENSIVE MENSTRUAL RECOVERY SYSTEM ---
elif st.session_state.current_page == "Period Tracker":
    st.markdown("<h2>🩸 Menstrual Cycle & Stage Health Hub</h2>", unsafe_allow_html=True)
    st.write(f"Physiological Metric Records for: **{selected_date_str}**")
    st.write("---")

    day_log = st.session_state.logs[selected_date_str]

    def calculate_period_stats(logs_dict):
        """Calculate average cycle length and period duration"""
        period_dates = []
        
        for date_str in sorted(logs_dict.keys()):
            log_data = logs_dict[date_str]
            if log_data.get("last_period_date"):
                try:
                    period_dates.append(datetime.datetime.strptime(log_data["last_period_date"], "%Y-%m-%d").date())
                except:
                    pass
        
        period_dates = sorted(list(set(period_dates)))
        
        if len(period_dates) < 1:
            return None, None, None
        
        cycle_lengths = []
        if len(period_dates) >= 2:
            for i in range(1, len(period_dates)):
                cycle_length = (period_dates[i] - period_dates[i-1]).days
                if 20 <= cycle_length <= 35:
                    cycle_lengths.append(cycle_length)
        
        avg_cycle = sum(cycle_lengths) / len(cycle_lengths) if cycle_lengths else 28
        avg_period_duration = 5
        last_period = period_dates[-1]
        
        return avg_cycle, avg_period_duration, last_period

    avg_cycle, avg_duration, last_period_date = calculate_period_stats(st.session_state.logs)

    if not IS_ACTIVE_TODAY:
        st.info("🔒 Viewing Read-Only Archive Records Matrix.")
        st.write(f"**Period Active Status:** {'🩸 On Active Period Cycle Day' if day_log.get('period', False) else '❌ No Active Menstruation Logged'}")
        st.write(f"**Menstrual Cycle Phase Stage:** {day_log.get('menstrual_stage', 'Unknown')}")
        st.write(f"**Logged Clinical Symptoms:** {', '.join(day_log.get('symptoms', [])) if day_log.get('symptoms') else 'None'}")
        st.write(f"**Tracked Emotional Mood State:** {day_log.get('mood', 'Not Logged')}")
        
        if day_log.get("last_period_date"):
            st.markdown("---")
            st.markdown("### 📊 Your Period Data")
            st.write(f"**Last Period Date:** {day_log.get('last_period_date')}")
    
    else:
        st.markdown("### 📅 Period Tracking Setup")
        
        default_date = TODAY
        if day_log.get("last_period_date"):
            try:
                default_date = datetime.datetime.strptime(day_log.get("last_period_date"), "%Y-%m-%d").date()
            except:
                default_date = TODAY
        
        last_period_input = st.date_input(
            "📍 When was your last period? (Pick the date)",
            value=default_date,
            key="last_period_picker_unique_v2"
        )
        
        st.write("---")
        
        if avg_cycle and last_period_date:
            st.markdown("### 📊 Your Cycle Predictions")
            
            predicted_next = last_period_date + datetime.timedelta(days=int(avg_cycle))
            days_until_next = (predicted_next - TODAY).days
            
            col_pred1, col_pred2 = st.columns(2)
            
            with col_pred1:
                st.metric("📈 Average Cycle Length", f"{int(avg_cycle)} days", label_visibility="visible")
                st.metric("⏱️ Average Period Duration", f"{int(avg_duration)} days", label_visibility="visible")
            
            with col_pred2:
                st.metric("🩸 Last Period Started", last_period_date.strftime("%b %d, %Y"), label_visibility="visible")
                if days_until_next >= 0:
                    st.metric("🔮 Next Period Expected", predicted_next.strftime("%b %d, %Y"), delta=f"{days_until_next} days from now", label_visibility="visible")
                else:
                    st.metric("🔮 Next Period Expected", predicted_next.strftime("%b %d, %Y"), delta=f"{abs(days_until_next)} days ago", label_visibility="visible")
            
            st.write("---")
        else:
            st.info("💡 Add more period dates to see predictions!")
        
        is_period = st.checkbox("🩸 Mark as Active Period Cycle Day", value=day_log.get("period", False))

        stages = ["Menstrual Phase 🩸", "Follicular Phase 🌱", "Ovulation Phase 🥚", "Luteal Phase 🍂"]
        current_stg = day_log.get("menstrual_stage", "Menstrual Phase 🩸")
        stg_idx = stages.index(current_stg) if current_stg in stages else 0
        sel_stage = st.selectbox("Menstrual Cycle Phase / Stage:", stages, index=stg_idx)

        symptom_options = ["Cramps ⚡", "Bloating 🎈", "Headaches 🧠", "Fatigue 🥱", "Backache 🎒", "Nausea 🤢"]
        saved_symptoms = day_log.get("symptoms", [])
        sel_symptoms = st.multiselect("Track Present Physiological Symptoms:", symptom_options, default=[s for s in saved_symptoms if s in symptom_options])

        mood_options = ["Happy 🥰", "Emotional 🥺", "Irritated ⚡", "Tired 🥱", "Cozy 🎀", "Energetic ⚡"]
        current_mood = day_log.get("mood", "Cozy 🎀")
        mood_idx = mood_options.index(current_mood) if current_mood in mood_options else 0
        sel_mood = st.selectbox("Log Present Emotional State Mood:", mood_options, index=mood_idx)

        if st.button("💾 Save Health Hub Metrics"):
            st.session_state.logs[selected_date_str]["period"] = is_period
            st.session_state.logs[selected_date_str]["menstrual_stage"] = sel_stage
            st.session_state.logs[selected_date_str]["symptoms"] = sel_symptoms
            st.session_state.logs[selected_date_str]["mood"] = sel_mood
            st.session_state.logs[selected_date_str]["last_period_date"] = last_period_input.strftime("%Y-%m-%d")
            save_data(st.session_state.logs)
            st.success("✅ Menstrual metrics and symptom tables saved securely.")
            st.rerun()


# --- PAGE E: DEEP FOCUS ENGINE HUB ---
elif st.session_state.current_page == "Study Hub":
    if st.session_state.study_session["active"]:
        st.markdown("<h1 style='text-align: center; color: #ff4d6d;'>🕊️ Deep Focus Mode Active</h1>", unsafe_allow_html=True)
        st.markdown(f"<h3 style='text-align: center;'>{st.session_state.study_session['subject'].upper()}</h3>", unsafe_allow_html=True)
        st.write("---")
        
        current_now = time.time()
        session_data = st.session_state.study_session

        session_duration = session_data["accumulated_time"]
        if not session_data["paused"]:
            session_duration += (current_now - session_data["start_timestamp"])

        # Calculate days, hours, minutes, seconds
        total_seconds = int(session_duration)
        days = total_seconds // 86400
        hours = (total_seconds % 86400) // 3600
        minutes = (total_seconds % 3600) // 60
        seconds = total_seconds % 60

        total_goal_seconds = (session_data["target_hours"] * 3600) + (session_data["target_minutes"] * 60)
        progress_ratio = min(total_seconds / max(total_goal_seconds, 1), 1.0)
        
        st.progress(progress_ratio)

        # Real-time countdown display
        st.markdown(f"""
        <div style="
            background: linear-gradient(135deg, #ffb3c1, #ffc2d1);
            border-radius: 15px;
            padding: 40px;
            text-align: center;
            margin: 30px 0;
            box-shadow: 0 4px 10px rgba(255, 179, 193, 0.3);
        ">
            <h1 style="color: #4a2c3a; margin: 0; font-size: 3.5rem; font-weight: bold;">
                {days:02d}D : {hours:02d}H : {minutes:02d}M : {seconds:02d}S
            </h1>
            <p style="color: #4a2c3a; margin: 15px 0 0 0; font-size: 1.1rem;">
                Goal: {session_data['target_hours']}h {session_data['target_minutes']}m
            </p>
        </div>
        """, unsafe_allow_html=True)

        st.write("---")
        st.markdown("##### 🎵 Study Hub Integrated Music Playlists")
        music_tracks = {
            "🌸 Focus Playlist 1": "https://open.spotify.com/embed/playlist/07UHFyiPyJBz3AN4tqbnba?utm_source=generator",
            "🎀 Focus Playlist 2": "https://open.spotify.com/embed/playlist/37i9dQZF1EIgKXhXqo61vc?utm_source=generator",
            "🧸 Focus Playlist 3": "https://open.spotify.com/embed/playlist/52OWMxwRgSI8EjerBNu2He?utm_source=generator",
            "🍓 Focus Playlist 4": "https://open.spotify.com/embed/playlist/1URfoVZ0TuxvwulPDIuSfv?utm_source=generator"
        }
        chosen_track = st.selectbox("Select Active Audio Stream Environment:", list(music_tracks.keys()))
        
        st.markdown(f"""
        <iframe 
            style="border-radius:12px; margin-top: 15px;" 
            src="{music_tracks[chosen_track]}" 
            width="100%" 
            height="380" 
            frameBorder="0" 
            allow="autoplay; clipboard-write; encrypted-media; fullscreen; picture-in-picture">
        </iframe>
        """, unsafe_allow_html=True)

        st.write("---")
        col_ctrl1, col_ctrl2, col_ctrl3 = st.columns(3)

        with col_ctrl1:
            if not session_data["paused"]:
                if st.button("⏸️ Pause Session"):
                    st.session_state.study_session["paused"] = True
                    st.session_state.study_session["accumulated_time"] += (time.time() - session_data["start_timestamp"])
                    st.rerun()
            else:
                if st.button("▶️ Resume Session"):
                    st.session_state.study_session["paused"] = False
                    st.session_state.study_session["start_timestamp"] = time.time()
                    st.rerun()

        with col_ctrl2:
            if st.button("🛑 Stop Focus Period"):
                st.session_state.study_session_confirm = True

        if getattr(st.session_state, "study_session_confirm", False):
            st.markdown("<p style='color:red; font-weight:bold;'>⚠️ Are you completely sure you want to end your focus session early?</p>", unsafe_allow_html=True)
            col_conf1, col_conf2 = st.columns(2)
            with col_conf1:
                if st.button("Yes, End It"):
                    formatted_time = f"{days}d {hours}h {minutes}m {seconds}s"
                    final_logged_str = f"Studied {session_data['subject']} for {formatted_time} (Target Goal: {session_data['target_hours']}h {session_data['target_minutes']}m)"
                    if "study_history" not in st.session_state.logs[selected_date_str]:
                        st.session_state.logs[selected_date_str]["study_history"] = []

                    st.session_state.logs[selected_date_str]["study_history"].append(final_logged_str)
                    st.session_state.study_session["active"] = False
                    st.session_state.study_session_confirm = False
                    save_data(st.session_state.logs)
                    st.rerun()
            with col_conf2:
                if st.button("No, Keep Studying"):
                    st.session_state.study_session_confirm = False
                    st.rerun()

        # Auto-refresh to update timer every second
        time.sleep(1)
        st.rerun()

    else:
        st.markdown("<h2>📚 Study Hub Dashboard Setup</h2>", unsafe_allow_html=True)

        if not IS_ACTIVE_TODAY:
            st.warning("🔒 Deep focus session allocation routines are unavailable outside of active target calendar windows.")
        else:
            in_subject = st.text_input("Enter Focus Subject Objective:", placeholder="e.g., Physics")

            st.markdown("##### Manual Target Duration Specification:")
            dur_col1, dur_col2 = st.columns(2)
            with dur_col1:
                in_hours = st.number_input("Hours:", min_value=0, max_value=12, value=1, step=1)
            with dur_col2:
                in_minutes = st.number_input("Minutes:", min_value=0, max_value=59, value=15, step=1)

            if st.button("🚀 Ignite Deep Focus Block Window"):
                if in_subject.strip() == "":
                    st.error("Please provide structural focus target subjects.")
                elif in_hours == 0 and in_minutes == 0:
                    st.error("Target time metrics parameters cannot be zero boundaries.")
                else:
                    st.session_state.study_session = {
                        "active": True,
                        "subject": in_subject,
                        "target_hours": in_hours,
                        "target_minutes": in_minutes,
                        "start_timestamp": time.time(),
                        "accumulated_time": 0.0,
                        "paused": False,
                        "pause_timestamp": 0.0
                    }
                    st.rerun()

        st.write("---")
        st.markdown("### 📖 Focus Session Historical Archive Logs")
        log_expander_flag = st.checkbox("📖 Expand Historical Archives Logs", value=False)
        if log_expander_flag:
            day_history = st.session_state.logs[selected_date_str].get("study_history", [])
            if not day_history:
                st.info("No validated focus milestones logged inside this target framework timeframe.")
            else:
                for record in day_history:
                    st.markdown(f"* `{record}`")


# --- PAGE F: RELATIONSHIP CORE HUB ---
elif st.session_state.current_page == "Relationship Hub":
    st.markdown("<h2>❤️ Connecting Loved Ones Hub</h2>", unsafe_allow_html=True)
    st.write(f"Archive Configuration Logs Matrix: **{selected_date_str}**")
    st.write("---")

    st.markdown("### 🏃 THINGS I DID")
    current_things_did = st.session_state.logs[selected_date_str]["things_i_did"]

    if not current_things_did:
        st.info("No interactive timeline entries generated yet. Log is fresh and empty.")
    else:
        for item in current_things_did:
            st.markdown(f" * `{item}`")

    if not IS_ACTIVE_TODAY:
        st.caption("🔒 Read-only metrics locked on this historical tracking link frame.")
    else:
        new_action = st.text_input("Add New Daily Action Log Entry:", key="input_action_tracker")
        if st.button("Save Action Logging Block"):
            if new_action.strip() != "":
                st.session_state.logs[selected_date_str]["things_i_did"].append(new_action.strip())
                save_data(st.session_state.logs)
                st.success("Item saved securely.")
                st.rerun()

    st.write("---")

    st.markdown("### 💌 THINGS I WANT MY BOYFRIEND TO KNOW")
    expand_secret_notes = st.checkbox("💌 Unroll Secret Relationship History Notes", value=False)

    if expand_secret_notes:
        current_bf_notes = st.session_state.logs[selected_date_str]["boyfriend_notes"]
        st.markdown("#### `Running Archived Relationship Message Data:`")
        if not current_bf_notes:
            st.info("No structural messages logged yet inside this archive space.")
        else:
            for note in current_bf_notes:
                st.markdown(f"> 💝 *\"{note}\"*")

    if not IS_ACTIVE_TODAY:
        st.caption("🔒 Entry modification parameters locked on historical frame arrays.")
    else:
        new_note = st.text_area("Write something sweet or drop an update:", key="input_sweet_note_field")
        if st.button("Transmit Note To Hidden Vault Archive Link"):
            if new_note.strip() != "":
                st.session_state.logs[selected_date_str]["boyfriend_notes"].append(new_note.strip())
                save_data(st.session_state.logs)
                st.success("Note saved securely inside the hidden loop database framework.")
                st.rerun()

save_data(st.session_state.logs)
