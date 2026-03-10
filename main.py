import streamlit as st
from ai_engine import ask_luna
import psutil
import os

from security.event_logger import clear_logs, read_logs
from memory import remember, recall, clear_chat_memory, get_personal, save_personal
from startup import add_to_startup
from internet import search_web
from system_scan import run_full_scan
from download_monitor import get_download_alerts
from security_engine import start_security_engine
from security.threat_detector import check_running_processes
from security.ai_security import detect_malware_patterns
from security.network_monitor import monitor_connections
from security.ai_reasoning_security import analyze_behavior
from security.file_sandbox import scan_file
from security.quarantine import quarantine_file


# ---------- PAGE CONFIG ----------
st.set_page_config(
    page_title="Luna",
    page_icon="🌙",
    layout="wide"
)

# ---------- STYLE ----------
st.markdown("""
<style>
.stApp {
    background-color:#0f172a;
    color:white;
}
section[data-testid="stSidebar"] {
    background-color:#020617;
}
[data-testid="stChatMessage"]{
    border-radius:12px;
}
button{
    border-radius:8px !important;
}
</style>
""", unsafe_allow_html=True)

st.title("🌙 Luna AI Assistant")


# ---------- START SECURITY ENGINE ----------
if "engine_started" not in st.session_state:

    try:
        start_security_engine()
    except Exception as e:
        st.warning(f"Security engine failed: {e}")

    st.session_state.engine_started = True


# ---------- STARTUP ----------
if "startup_added" not in st.session_state:

    exe_path = os.path.abspath("Luna.exe")

    if os.path.exists(exe_path):
        try:
            add_to_startup(exe_path)
        except:
            pass

    st.session_state.startup_added = True


# ---------- CHAT MEMORY ----------
if "messages" not in st.session_state:
    st.session_state.messages = []


# ---------- SIDEBAR ----------
with st.sidebar:

    st.header("🌙 Luna Control")

    # PROFILE
    st.subheader("🧠 Personal Profile")

    profile = get_personal() or {}

    if profile:
        for k,v in profile.items():
            st.info(f"{k.capitalize()} : {v}")
    else:
        st.warning("No profile saved")

    st.divider()

    # SYSTEM MONITOR
    st.subheader("💻 System Monitor")

    cpu = psutil.cpu_percent()
    ram = psutil.virtual_memory().percent

    st.write("CPU Usage")
    st.progress(cpu/100)

    st.write("RAM Usage")
    st.progress(ram/100)

    st.caption(f"CPU: {cpu}% | RAM: {ram}%")

    st.divider()

    # SECURITY LOGS
    st.subheader("📜 Security Logs")

    logs = read_logs(limit=20) or []

    with st.expander("View Logs"):

        if logs:
            for log in logs:
                st.text(log)
        else:
            st.info("No logs yet")

    col1,col2 = st.columns(2)

    with col1:

        if st.button("🧹 Clear Logs"):

            clear_logs()
            st.success("Logs cleared")
            st.rerun()

    with col2:

        if logs:
            log_text = "\n".join(logs)

            st.download_button(
                "⬇ Download Logs",
                log_text,
                file_name="luna_security_logs.txt"
            )

    st.divider()

    # MEMORY CONTROL
    st.subheader("🧠 Memory")

    if st.button("🧹 Clear Chat Memory"):

        clear_chat_memory()
        st.session_state.messages = []

        st.success("Chat memory cleared")

    st.divider()

    # SECURITY TOOLS
    st.subheader("🛡 Security Tools")

    if st.button("🔎 Run Full Security Scan"):

        with st.spinner("Scanning system..."):
            scan = run_full_scan() or {}

        st.success("Scan completed")

        processes = scan.get("running_processes", [])

        ai_alerts = analyze_behavior(processes)

        if ai_alerts:
            for alert in ai_alerts:
                st.warning(alert)

        with st.expander("Running Processes"):
            st.write(scan.get("running_processes", []))

        with st.expander("Executable Files"):
            st.write(scan.get("suspicious_downloads", []))

        with st.expander("Installed Apps"):
            st.write(scan.get("installed_apps", []))


# ---------- REAL TIME SECURITY ----------
st.subheader("🛡 Real-Time Security Monitor")

download_alerts = get_download_alerts() or []
process_alerts = check_running_processes() or []
network_alerts = monitor_connections() or []

if not download_alerts and not process_alerts and not network_alerts:
    st.success("System secure — no threats detected")


for alert in download_alerts:

    st.error(f"⚠ Suspicious Download: {alert}")

    if os.path.exists(alert):

        result = scan_file(alert)

        if result.get("risk") == "HIGH":

            msg = quarantine_file(alert)
            st.warning(msg)


for alert in process_alerts:
    st.warning(f"⚠ Suspicious Process: {alert}")


for alert in network_alerts:
    st.error(f"🌐 Network Threat: {alert}")


# ---------- CHAT DISPLAY ----------
for msg in st.session_state.messages:

    with st.chat_message(msg["role"]):
        st.write(msg["content"])


# ---------- USER INPUT ----------
user_input = st.chat_input("Ask Luna anything...")

if user_input:

    st.session_state.messages.append({"role":"user","content":user_input})

    with st.chat_message("user"):
        st.write(user_input)

    text = user_input.lower()

    ai_reply = None
    prompt = None


    # MALWARE PATTERN CHECK
    threats = detect_malware_patterns(user_input)

    if threats:

        ai_reply = f"⚠ Suspicious command patterns detected:\n{threats}"


    # PERSONAL MEMORY
    elif "my name is" in text:

        name = user_input.split("is")[-1].strip()
        save_personal("name",name)

        ai_reply = f"Nice to meet you {name}. I'll remember your name."


    elif "i study" in text:

        study = user_input.split("study")[-1].strip()
        save_personal("study",study)

        ai_reply = "Got it. I'll remember what you study."


    elif "my interest is" in text:

        interest = user_input.split("is")[-1].strip()
        save_personal("interest",interest)

        ai_reply = "Saved your interest."


    # INTERNET SEARCH
    elif text.startswith("search:"):

        query = user_input.replace("search:","").strip()

        results = search_web(query)

        prompt=f"""
You are Luna AI.

Internet results:
{results}

Question:
{query}

Give a helpful answer.
"""


    # SECURITY SCAN
    elif "security scan" in text:

        scan = run_full_scan()

        ai_reply=f"""
Security Scan Results

Running Processes:
{scan.get("running_processes",[])}

Downloads:
{scan.get("suspicious_downloads",[])}

Installed Apps:
{scan.get("installed_apps",[])}
"""


    # NORMAL CHAT
    else:

        memory = recall(limit=5)
        profile = get_personal()

        prompt=f"""
You are Luna AI assistant.

User Profile:
{profile}

Memory:
{memory}

User message:
{user_input}

Give a helpful answer.
"""


    # ---------- AI RESPONSE ----------
    if ai_reply is None and prompt:

        with st.chat_message("assistant"):

            with st.spinner("Luna thinking..."):

                ai_reply = ask_luna(prompt)

                st.write(ai_reply)

    else:

        with st.chat_message("assistant"):
            st.write(ai_reply)


    if ai_reply:

        remember("assistant",ai_reply)

        st.session_state.messages.append(
            {"role":"assistant","content":ai_reply}
        )


# ---------- FOOTER ----------
st.markdown("---")
st.caption("🌙 Luna • Hybrid AI Assistant (Offline + Online)")