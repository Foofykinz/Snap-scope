import streamlit as st
from PIL import Image
import os
import io
import zipfile

# --- CONFIG ---
MODES = {
    "Standard Interior Scope": [
        "Dash VIN", "Door VIN", "LF Corner", "RF Corner", "RR Corner", "LR Corner",
        "Odometer", "Dash", "Headliner", "LF Seat", "LF Carpet", "LF Door Trim"
    ],
    # Add more modes here (e.g., Hail, Flood, Theft)
}

st.set_page_config(page_title="SnapScope™ 2.0", layout="centered")
st.title("📸 SnapScope™ 2.0 – Guided Photo Capture")

# --- INIT STATE ---
if "mode" not in st.session_state:
    st.session_state.mode = None
if "index" not in st.session_state:
    st.session_state.index = 0
if "photos_taken" not in st.session_state:
    st.session_state.photos_taken = {}

# --- MODE SELECTION ---
if st.session_state.mode is None:
    st.subheader("🧠 Choose a Photo Template")
    st.session_state.mode = st.selectbox("Select a mode:", list(MODES.keys()))
    if st.button("Start Capture"):
        st.rerun()
    st.stop()

part_list = MODES[st.session_state.mode]

# --- COMPLETED ---
if st.session_state.index >= len(part_list):
    st.success("✅ All photos captured and saved.")
    
    # Offer download of zip file
    if st.button("📦 Download All Labeled Photos"):
        zip_buffer = io.BytesIO()
        with zipfile.ZipFile(zip_buffer, "w") as zipf:
            for part, file in st.session_state.photos_taken.items():
                folder = f"labeled_photos/{part.replace(' ', '_')}"
                os.makedirs(folder, exist_ok=True)
                filename = os.path.join(folder, file.name)
                with open(filename, "wb") as f:
                    f.write(file.getbuffer())
                zipf.write(filename, arcname=f"{part.replace(' ', '_')}/{file.name}")
        st.download_button(
            label="Download ZIP",
            data=zip_buffer.getvalue(),
            file_name="SnapScope_Photos.zip",
            mime="application/zip"
        )
    st.stop()

# --- CURRENT STEP ---
current_part = part_list[st.session_state.index]
st.markdown(f"### 📷 Step {st.session_state.index + 1} of {len(part_list)} – **{current_part}**")

upload_type = st.radio("Choose input method:", ["📁 Upload", "📷 Use Camera"])

if upload_type == "📁 Upload":
    file = st.file_uploader("Upload a photo", type=["jpg", "jpeg", "png"], key=current_part)
else:
    file = st.camera_input("Take photo with your camera", key=current_part)

if file:
    st.image(file, caption=f"{current_part}", use_container_width=True)

    col1, col2, col3 = st.columns(3)
    if col1.button("⬅️ Back", disabled=st.session_state.index == 0):
        st.session_state.index = max(0, st.session_state.index - 1)
        st.experimental_rerun()

    if col2.button("⏭️ Skip"):
        st.session_state.index += 1
        st.experimental_rerun()

    if col3.button("✅ Save & Continue"):
        st.session_state.photos_taken[current_part] = file
        st.session_state.index += 1
        st.experimental_rerun()
else:
    st.info("📸 Upload or capture a photo to continue.")

