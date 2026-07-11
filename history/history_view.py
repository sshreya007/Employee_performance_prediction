import streamlit as st
import pandas as pd
from database.models import get_predictions, delete_prediction
from components.design_system import inject_css
from utils.helpers import PERFORMANCE_LABELS, rating_color

EMOJI = {1: "🔴", 2: "🟡", 3: "🟢", 4: "⭐"}


def _section(title: str):
    st.markdown(f"""
    <div style="display:flex; align-items:center; gap:10px; margin:20px 0 12px;">
      <div style="font-family:'Space Grotesk',sans-serif; font-size:15px;
           font-weight:700; color:#C4B5FD;">{title}</div>
      <div style="flex:1; height:1px;
           background:linear-gradient(90deg,rgba(124,58,237,0.4),transparent);"></div>
    </div>
    """, unsafe_allow_html=True)


def show():
    inject_css()

    st.markdown("""
    <style>
    section[data-testid="stMain"] > div > div {
      padding: 28px 36px 48px !important;
    }
    </style>
    """, unsafe_allow_html=True)

    username = st.session_state.get("username", "")
    records  = get_predictions(username)

    # ── Header ────────────────────────────────────────────────
    st.markdown("""
    <div style="margin-bottom:24px;">
      <div style="font-family:'Space Grotesk',sans-serif; font-size:28px;
           font-weight:800; color:#F1F5F9; margin-bottom:4px;">
        📋 Prediction History
      </div>
      <div style="font-size:14px; color:#475569;">
        All predictions made by your account, most recent first.
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Empty state ───────────────────────────────────────────
    if not records:
        st.markdown("""
        <div style="text-align:center; padding:60px 20px;
             background:rgba(255,255,255,0.02);
             border:1px dashed rgba(124,58,237,0.25);
             border-radius:18px; margin-top:20px;">
          <div style="font-size:48px; margin-bottom:16px;">🔮</div>
          <div style="font-family:'Space Grotesk',sans-serif; font-size:20px;
               font-weight:700; color:#C4B5FD; margin-bottom:8px;">
            No predictions yet
          </div>
          <div style="font-size:14px; color:#475569;">
            Head to Prediction to get started.
          </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='height:16px'></div>", unsafe_allow_html=True)
        if st.button("Go to Prediction →", type="primary"):
            st.session_state["app_page"] = "prediction"
            st.rerun()
        return

    # ── KPI summary ───────────────────────────────────────────
    avg_rating  = sum(r["prediction"] for r in records) / len(records)
    outstanding = sum(1 for r in records if r["prediction"] == 4)
    low_count   = sum(1 for r in records if r["prediction"] == 1)

    c1, c2, c3, c4 = st.columns(4, gap="small")
    c1.metric("🔮  Total Predictions", len(records))
    c2.metric("📈  Avg Rating",        f"{avg_rating:.2f} / 4")
    c3.metric("⭐  Outstanding",        outstanding)
    c4.metric("🔴  At-Risk",           low_count)

    st.divider()

    # ── Tabs: Cards view + Table view ─────────────────────────
    tab1, tab2 = st.tabs(["🃏  Cards View", "📊  Table View"])

    with tab1:
        _section("Recent Predictions")

        for r in records:
            color = rating_color(r["prediction"])
            emoji = EMOJI.get(r["prediction"], "")
            label = PERFORMANCE_LABELS.get(r["prediction"], "")
            emp   = r["employee_name"] or "Unnamed Employee"
            date  = r["created_at"][:10]
            dept  = r["department"] or "—"
            role  = r["job_role"]   or "—"
            conf  = r["confidence"]

            col_main, col_badge = st.columns([5, 1], gap="small")

            with col_main:
                st.markdown(f"""
                <div style="
                  background: rgba(255,255,255,0.025);
                  border: 1px solid rgba(124,58,237,0.18);
                  border-left: 4px solid {color};
                  border-radius: 14px;
                  padding: 16px 20px;
                  margin-bottom: 2px;
                  transition: all 0.2s;
                ">
                  <div style="display:flex; justify-content:space-between; align-items:flex-start;">
                    <div>
                      <div style="font-weight:700; font-size:15px;
                           color:#E2E8F0; margin-bottom:4px;">{emp}</div>
                      <div style="font-size:12px; color:#475569;">
                        {dept} &nbsp;·&nbsp; {role} &nbsp;·&nbsp; {date}
                      </div>
                    </div>
                    <div style="text-align:right; flex-shrink:0; margin-left:16px;">
                      <div style="font-size:24px;">{emoji}</div>
                      <div style="font-size:13px; font-weight:700;
                           color:{color}; margin-top:2px;">{label}</div>
                      <div style="font-size:11px; color:#475569;">{conf:.0%} conf.</div>
                    </div>
                  </div>
                </div>
                """, unsafe_allow_html=True)

            with col_badge:
                if st.button("🗑️", key=f"del_{r['id']}", help="Delete this prediction"):
                    delete_prediction(r["id"], username)
                    st.success("Deleted.")
                    st.rerun()

            st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

    with tab2:
        _section("All Predictions")

        rows = []
        for r in records:
            rows.append({
                "ID":          r["id"],
                "Employee":    r["employee_name"] or "—",
                "Department":  r["department"],
                "Job Role":    r["job_role"],
                "Rating":      f"{EMOJI.get(r['prediction'],'')} {PERFORMANCE_LABELS.get(r['prediction'],'')}",
                "Confidence":  f"{r['confidence']:.0%}",
                "Date":        r["created_at"][:16],
            })

        df = pd.DataFrame(rows)
        st.dataframe(df.drop(columns=["ID"]),
                     use_container_width=True, hide_index=True)

        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)

        # ── Bulk delete ───────────────────────────────────────
        _section("🗑️ Delete a Record")
        ids       = [r["id"] for r in records]
        label_map = {
            r["id"]: f"ID {r['id']}  —  {r['employee_name'] or 'Unnamed'}  ({r['created_at'][:10]})"
            for r in records
        }
        choice = st.selectbox("Select prediction", options=ids,
                              format_func=lambda i: label_map[i])

        col_del, _ = st.columns([1, 3])
        with col_del:
            if st.button("🗑️  Delete Selected", type="secondary", use_container_width=True):
                delete_prediction(choice, username)
                st.success("Deleted successfully.")
                st.rerun()