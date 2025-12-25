import streamlit as st
import random
import statistics

# -----------------------------
# SIMULATION LOGIC
# -----------------------------
def simulate_system(
    wip,
    agents,
    avg_case_time,
    arrival_rate,
    simulation_hours,
    sla_hours,
    runs=500
):
    breach_probs = []
    final_queues = []

    for _ in range(runs):
        queue = wip
        time = 0
        completed = []

        while time < simulation_hours:
            arrivals = random.randint(
                max(0, arrival_rate - 3),
                arrival_rate + 3
            )
            queue += arrivals

            capacity = agents / avg_case_time
            processed = min(queue, capacity)
            queue -= processed

            for _ in range(int(processed)):
                completed.append(time + random.uniform(0.2, avg_case_time))

            time += 1

        breaches = sum(1 for t in completed if t > sla_hours)
        prob = breaches / max(1, len(completed))

        breach_probs.append(prob)
        final_queues.append(queue)

    return {
        "sla_breach_probability": round(statistics.mean(breach_probs) * 100, 2),
        "expected_backlog": round(statistics.mean(final_queues), 1)
    }

# -----------------------------
# STREAMLIT UI
# -----------------------------
st.set_page_config(
    page_title="Predictive Operations Center",
    layout="wide"
)

st.title("🚦 Predictive Process Simulation Dashboard")
st.caption("Proactive SLA Risk Forecasting & What-If Scenario Planning")

st.divider()

# -----------------------------
# INPUT PANEL
# -----------------------------
st.sidebar.header("Live Operational Inputs")

wip = st.sidebar.number_input(
    "Current Work In Progress (cases)",
    min_value=0,
    value=120
)

agents = st.sidebar.number_input(
    "Active Agents",
    min_value=1,
    value=10
)

arrival_rate = st.sidebar.slider(
    "Incoming Case Rate (cases/hour)",
    1, 50, 18
)

avg_case_time = st.sidebar.slider(
    "Avg Case Handling Time (hours)",
    0.1, 2.0, 0.6
)

sla_hours = st.sidebar.slider(
    "SLA Threshold (hours)",
    1, 12, 6
)

simulation_hours = st.sidebar.slider(
    "Forecast Window (hours)",
    1, 24, 8
)

run_sim = st.sidebar.button("▶ Run Simulation")

# -----------------------------
# OUTPUT
# -----------------------------
if run_sim:
    result = simulate_system(
        wip,
        agents,
        avg_case_time,
        arrival_rate,
        simulation_hours,
        sla_hours
    )

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "⚠ SLA Breach Probability",
        f"{result['sla_breach_probability']}%"
    )

    col2.metric(
        "📦 Expected Backlog",
        f"{result['expected_backlog']} cases"
    )

    col3.metric(
        "👥 Active Agents",
        agents
    )

    st.divider()

    # Risk Interpretation
    if result["sla_breach_probability"] > 70:
        st.error("🚨 HIGH RISK: Immediate intervention recommended.")
    elif result["sla_breach_probability"] > 40:
        st.warning("⚠ MODERATE RISK: Consider resource adjustments.")
    else:
        st.success("✅ LOW RISK: SLA likely to be met.")

    st.subheader("📊 What-If Scenario Examples")
    st.markdown("""
    - Add more agents  
    - Reduce arrival rate via throttling  
    - Automate low-complexity cases  
    """)

else:
    st.info("👈 Adjust inputs and click **Run Simulation** to forecast SLA risk.")
