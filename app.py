import streamlit as st
import matplotlib.pyplot as plt
from water_jug import solve

st.set_page_config(page_title="Water-Jug AI Solver", page_icon="💧", layout="centered")
st.title("💧 Intelligent Water-Jug Problem Solver")
st.caption("Explore how AI search algorithms solve the classic water-jug puzzle.")

with st.sidebar:
    st.header("Problem setup")
    cap_a = st.number_input("Jug A capacity (litres)", min_value=1, max_value=100, value=4, step=1)
    cap_b = st.number_input("Jug B capacity (litres)", min_value=1, max_value=100, value=3, step=1)
    target = st.number_input("Target quantity (litres)", min_value=0, max_value=100, value=2, step=1)
    algorithm = st.selectbox("Search algorithm", ["BFS", "DFS", "UCS", "GREEDY", "ASTAR"])
    run = st.button("Solve problem", type="primary", use_container_width=True)

st.markdown("**How to read a state:** `(A, B)` means the amount of water currently in Jug A and Jug B.")
if run:
    try:
        st.session_state["result"] = solve(int(cap_a), int(cap_b), int(target), algorithm)
        st.session_state["step"] = 0
        st.session_state["setup"] = (int(cap_a), int(cap_b), int(target), algorithm)
    except ValueError as exc:
        st.error(str(exc))

result = st.session_state.get("result")
if result:
    if not result["found"]:
        st.warning(result.get("message", "No solution found."))
    else:
        states = result["states"]
        actions = result["actions"]
        cap_a, cap_b, target, algorithm = st.session_state["setup"]
        st.success(f"Solution found using {algorithm} in {len(actions)} operations.")
        c1, c2, c3 = st.columns(3)
        c1.metric("Operations", len(actions))
        c2.metric("States expanded", result["expanded"])
        c3.metric("Time", f'{result["elapsed_ms"]:.3f} ms')

        if "step" not in st.session_state:
            st.session_state["step"] = 0
        st.subheader("Step-by-step simulation")
        step = st.session_state["step"]
        left, middle, right = st.columns([1, 1, 2])
        if left.button("← Previous", disabled=step == 0, use_container_width=True):
            st.session_state["step"] -= 1
            st.rerun()
        if middle.button("Next →", disabled=step >= len(states)-1, use_container_width=True):
            st.session_state["step"] += 1
            st.rerun()
        right.write(f"**Step {step} of {len(states)-1}**")

        a, b = states[step]
        fig, ax = plt.subplots(figsize=(6, 3))
        ax.set_xlim(0, 2.5)
        ax.set_ylim(0, max(cap_a, cap_b) * 1.18)
        for x, amount, capacity, label in [(0.35, a, cap_a, "Jug A"), (1.45, b, cap_b, "Jug B")]:
            ax.add_patch(plt.Rectangle((x, 0), 0.65, capacity, fill=False, linewidth=2))
            if amount:
                ax.add_patch(plt.Rectangle((x, 0), 0.65, amount, alpha=0.55))
            ax.text(x + 0.325, capacity + 0.15, f"{label}\n{amount}/{capacity} L",
                    ha="center", va="bottom", fontsize=10)
        ax.set_xticks([])
        ax.set_ylabel("Litres")
        ax.set_title("Current water levels")
        ax.spines[["top", "right", "bottom"]].set_visible(False)
        st.pyplot(fig)
        plt.close(fig)

        st.write(f"**Current state:** `{states[step]}`")
        if step > 0:
            st.info(f"Operation: {actions[step-1]}")
        elif step == 0:
            st.info("Initial state: both jugs are empty.")

        with st.expander("View complete solution path", expanded=True):
            for i, state in enumerate(states):
                label = "Start" if i == 0 else actions[i-1]
                st.write(f"{i}. **{label}** → `{state}`")

        with st.expander("About the selected algorithm"):
            descriptions = {
                "BFS": "Breadth-First Search explores states level by level. With equal move costs, it finds a solution with the fewest operations.",
                "DFS": "Depth-First Search follows one path deeply before backtracking. It may find a solution that is not the shortest.",
                "UCS": "Uniform Cost Search expands the lowest-cost path first. Here every operation costs 1.",
                "GREEDY": "Greedy Best-First Search chooses the state that appears closest to the target using a simple heuristic.",
                "ASTAR": "A* combines path cost g(n) and heuristic h(n). This version uses a safe but weak heuristic of 1 for non-goal states."
            }
            st.write(descriptions[algorithm])
else:
    st.info("Enter the jug capacities and target in the sidebar, then select **Solve problem**.")
