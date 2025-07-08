import streamlit as st
import datetime

# Define your custom checklist
part_list = [
    "Dash VIN", "Door VIN", "LF Corner", "RF Corner",
    "RR Corner", "LR Corner", "Odometer", "Dash",
    "Headliner", "LF Seat", "LF Carpet", "LF Door Trim"
]

st.set_page_config(page_title="SnapScope Checklist Mode", layout="centered")
st.title("📋 SnapScope™ – Checklist Mode")

# Initialize session state
if "done_parts" not in st.session_state:
    st.session_state.done_parts = []

if "unit_name" not in st.session_state:
    st.session_state.unit_name = ""

# Unit Info
st.subheader("📦 Set Folder Name (e.g., VIN, Plate, or Unit ID)")
st.session_state.unit_name = st.text_input("Unit/Folder Name", value=st.session_state.unit_name)

# Suggested Folder
today = datetime.date.today().strftime("%Y-%m-%d")
folder_name = f"SnapScope_{today}_{st.session_state.unit_name}" if st.session_state.unit_name else f"SnapScope_{today}"
st.code(f"📁 Suggested Folder: {folder_name}")

# Checklist Display
st.subheader("✅ Photo Checklist")

for i, part in enumerate(part_list):
    is_done = part in st.session_state.done_parts
    cols = st.columns([5, 1, 2])

    # Display part name
    cols[0].markdown(f"**{i+1:02d}_{part.replace(' ', '_')}**")
    
    # Copy label to clipboard
    if cols[1].button("📋", key=f"copy_{part}"):
        st.toast(f"Copied: {i+1:02d}_{part.replace(' ', '_')}.jpg", icon="📎")
        st.code(f"{i+1:02d}_{part.replace(' ', '_')}.jpg")

    # Mark complete
    if not is_done and cols[2].button("Mark Done ✅", key=f"done_{part}"):
        st.session_state.done_parts.append(part)

# Progress bar
progress = len(st.session_state.done_parts) / len(part_list)
st.progress(progress, text=f"{len(st.session_state.done_parts)} of {len(part_list)} complete")

# Reset
if st.button("🔁 Restart Checklist"):
    st.session_state.done_parts = []
