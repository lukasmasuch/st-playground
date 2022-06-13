import streamlit as st
import time
import os
import json

current_counter = st.empty()
current_session_counters = st.empty()

while True:
    if "rerun_counter" not in st.session_state:
        st.session_state["rerun_counter"] = 1
    
    current_counter.text(f"Rerun counter: " + str(st.session_state["rerun_counter"]))
    session_id = st._get_script_run_ctx().session_id
    
    session_records_path = "./sessions_records"
    os.makedirs(session_records_path, exist_ok=True)

    with open(os.path.join(session_records_path, f"{str(session_id)}"), "w") as myfile:
        myfile.write(str(st.session_state["rerun_counter"]))

    session_files = [f for f in os.listdir(session_records_path) if os.path.isfile(os.path.join(session_records_path, f))]
    session_counters = dict()
    for file in session_files:
        with open(os.path.join(session_records_path, file), "r") as myfile:
            session_counters[file] = int(myfile.read())

    current_session_counters.json(session_counters)

    st.session_state["rerun_counter"] += 1
    time.sleep(60)

