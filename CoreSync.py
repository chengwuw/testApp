import streamlit as st
import pandas as pd
import numpy as np
import datetime
import matplotlib.pyplot as plt
import seaborn as sns
import calendar

st.set_page_config(page_title="CoreSync", layout="centered")

# ------------------- HEADER -------------------
st.title("🌱 CoreSync")
st.subheader("Track your movement, mood, and progress—your way.")

# ------------------- MODE SELECTION -------------------
mode = st.radio("What’s your current fitness goal?",
                ["Build a habit", "Track performance", "Recover or adapt"],
                horizontal=True)

st.markdown("---")

# ------------------- DAILY CHECK-IN -------------------
st.header("✅ Daily Check-In")

moved_today = st.checkbox("Did you move today?", value=False)
movement_type = st.selectbox("Type of activity",
                             ["Stretching", "Walking", "Workout", "Yoga", "Dance", "Other"])

# ------------------- MOOD AND PAIN TRACKING -------------------
st.header("🧠 Mood & Physical Check")

mood = st.slider("How are you feeling emotionally?", 1, 5, 3,
                 format="%d", help="1 = Low mood, 5 = Great mood")

pain = st.slider("Any physical discomfort or fatigue?", 1, 5, 3,
                 format="%d", help="1 = No pain, 5 = High pain")

# ------------------- PERFORMANCE METRICS -------------------
if mode == "Track performance":
    st.header("📊 Performance Metrics")
    st.number_input("Minutes of activity today", min_value=0, step=5)
    st.number_input("Distance covered (km)", min_value=0.0, step=0.1)
    st.number_input("Avg. heart rate (bpm)", min_value=0, step=1)
    st.number_input("Calories burned", min_value=0, step=10)

# ------------------- JOURNAL ENTRY -------------------
st.header("📝 Reflections or Notes")
journal = st.text_area("Write anything you'd like to remember about today's session...")

# ------------------- MEDIA UPLOAD -------------------
media_file = st.file_uploader("Upload a photo or video (optional)", type=["jpg", "png", "mp4"])

# ------------------- SUBMIT -------------------
if st.button("Save Entry"):
    st.success("Your entry has been saved for today!")
    st.balloons()

# ------------------- MOCK DATA GENERATION -------------------
activity_types = ["Stretching", "Walking", "Workout", "Yoga", "Dance", "Other"]
start_date = datetime.date.today() - datetime.timedelta(weeks=5)
dates = pd.date_range(start=start_date, periods=35)

mock_data = {
    "Date": [],
    "Activity": [],
    "Duration": []
}

for date in dates:
    for activity in activity_types:
        if np.random.rand() < 0.3:
            mock_data["Date"].append(date)
            mock_data["Activity"].append(activity)
            mock_data["Duration"].append(np.random.randint(10, 60))

df = pd.DataFrame(mock_data)

# ------------------- WEEKLY SUMMARY -------------------
st.markdown("---")
st.header("📅 Weekly Summary")

# Heatmap for Build a habit
# Heatmap for Build a habit
if mode == "Build a habit":
    st.subheader("Activity Heatmap")

    # User selects one activity at a time
    selected_activity = st.selectbox("Choose activity to view heatmap:", activity_types)

    # Prepare data
    df['Week'] = df['Date'].dt.strftime('%U')
    df['Day'] = df['Date'].dt.weekday

    subset = df[df['Activity'] == selected_activity]
    heatmap_df = subset.groupby(['Week', 'Day']).size().unstack(fill_value=0).reindex(columns=range(7), fill_value=0)

    # Only plot if there is data
    if not heatmap_df.empty:
        fig, ax = plt.subplots()
        sns.heatmap(heatmap_df, cmap="Greens", linewidths=0.5, linecolor='gray', cbar=False, ax=ax)
        ax.set_title(f"{selected_activity} Activity Heatmap")
        ax.set_xlabel("Day of Week")
        ax.set_ylabel("Week")
        ax.set_xticks(range(7))
        ax.set_xticklabels([calendar.day_abbr[d] for d in range(7)])
        st.pyplot(fig)
    else:
        st.info("No activity recorded for the selected type.")


# Graphs for Track performance
elif mode == "Track performance":
    st.subheader("Performance Over Time")
    df["Week"] = df["Date"].dt.strftime('%Y-%U')
    summary = df.groupby(["Week", "Activity"])["Duration"].sum().unstack(fill_value=0)
    st.line_chart(summary)

# Suggestion + Reflection for Recover or adapt
elif mode == "Recover or adapt":
    st.subheader("AI Summary and Suggestions")
    avg_duration = df.groupby("Activity")["Duration"].mean()
    for activity, avg in avg_duration.items():
        st.markdown(f"**{activity}**: Average session = {avg:.1f} min")
        if avg < 20:
            st.warning(f"Consider slightly longer {activity.lower()} sessions to boost recovery.")
        elif avg > 45:
            st.info(f"Your {activity.lower()} sessions are quite long. Balance with rest.")
        else:
            st.success(f"Your {activity.lower()} activity length looks optimal!")

# ------------------- FOOTER -------------------
st.markdown("---")
st.caption("CoreSync v1.0 – your flexible fitness companion")

