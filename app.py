
import streamlit as st
import pandas as pd

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Healthcare Risk Analytics",
    page_icon="🏥",
    layout="wide"
)

# --------------------------------------------------
# LOAD DATA
# --------------------------------------------------

@st.cache_data
def load_data():
    return pd.read_csv("healthcare_risk_final.csv")

data = load_data()

# --------------------------------------------------
# HEADER
# --------------------------------------------------

st.title("🏥 Healthcare Risk Analytics")
st.caption(
    "Interactive patient risk stratification and healthcare analytics dashboard."
)

st.info(
    "This application is developed for educational and portfolio purposes. "
    "The risk framework is illustrative and is not a validated clinical "
    "decision-support tool."
)

# --------------------------------------------------
# TABS
# --------------------------------------------------

risk_tab, analytics_tab = st.tabs([
    "🩺 Risk Assessment",
    "📊 Patient Analytics"
])

# ==================================================
# TAB 1 — RISK ASSESSMENT
# ==================================================

with risk_tab:

    st.subheader("Patient Information")

    col1, col2 = st.columns(2)

    with col1:
        age = st.number_input(
            "Age",
            min_value=18,
            max_value=100,
            value=50
        )

    with col2:
        diagnosis = st.selectbox(
            "Primary Diagnosis",
            [
                "Arthritis",
                "Asthma",
                "COPD",
                "Cancer",
                "Diabetes",
                "Heart Disease",
                "Hypertension",
                "Kidney Disease",
                "Liver Disease",
                "Stroke"
            ]
        )

    st.subheader("🧪 Laboratory Information")

    lab1, lab2, lab3 = st.columns(3)

    with lab1:
        blood_sugar = st.number_input(
            "Blood Sugar",
            min_value=0.0,
            value=100.0,
            step=1.0
        )

    with lab2:
        cholesterol = st.number_input(
            "Cholesterol",
            min_value=0.0,
            value=180.0,
            step=1.0
        )

    with lab3:
        hemoglobin = st.number_input(
            "Hemoglobin",
            min_value=0.0,
            value=14.0,
            step=0.1
        )

    st.divider()

    high_risk_diagnoses = [
        "Heart Disease",
        "Stroke",
        "Cancer",
        "Kidney Disease",
        "Liver Disease",
        "COPD"
    ]

    if st.button(
        "Assess Patient Risk",
        type="primary",
        use_container_width=True
    ):

        risk_score = 0
        risk_factors = []

        if age > 65:
            risk_score += 1
            risk_factors.append("Age above 65")

        if diagnosis in high_risk_diagnoses:
            risk_score += 1
            risk_factors.append("Selected diagnosis")

        if blood_sugar > 120:
            risk_score += 1
            risk_factors.append("Elevated blood sugar")

        if cholesterol > 200:
            risk_score += 1
            risk_factors.append("Elevated cholesterol")

        if hemoglobin < 13:
            risk_score += 1
            risk_factors.append("Low hemoglobin")

        if risk_score == 0:
            risk_level = "LOW"
        elif risk_score <= 2:
            risk_level = "MODERATE"
        else:
            risk_level = "HIGH"

        st.subheader("📋 Risk Assessment Result")

        result1, result2, result3 = st.columns(3)

        with result1:
            st.metric("Risk Score", f"{risk_score} / 5")

        with result2:
            st.metric("Risk Level", risk_level)

        with result3:
            st.metric("Risk Indicators", len(risk_factors))

        if risk_level == "LOW":
            st.success("Low project-defined risk level.")
        elif risk_level == "MODERATE":
            st.warning("Moderate project-defined risk level.")
        else:
            st.error("High project-defined risk level.")

        st.markdown("#### Contributing Risk Indicators")

        if risk_factors:
            for factor in risk_factors:
                st.write(f"• {factor}")
        else:
            st.write(
                "No risk indicators were identified using "
                "the project scoring framework."
            )

        with st.expander("How is the risk score calculated?"):
            st.markdown("""
            One point is assigned for each project-defined indicator:

            - Age above 65
            - Selected higher-risk diagnosis
            - Blood Sugar above 120
            - Cholesterol above 200
            - Hemoglobin below 13

            **Risk categories**

            - 0 points → Low Risk
            - 1–2 points → Moderate Risk
            - 3–5 points → High Risk
            """)

# ==================================================
# TAB 2 — PATIENT ANALYTICS
# ==================================================

with analytics_tab:

    st.subheader("Patient Population Overview")

    total_patients = len(data)
    low_risk = (data["RiskLevel"] == "Low").sum()
    moderate_risk = (data["RiskLevel"] == "Moderate").sum()
    high_risk = (data["RiskLevel"] == "High").sum()

    m1, m2, m3, m4 = st.columns(4)

    with m1:
        st.metric("Total Patients", total_patients)

    with m2:
        st.metric("Low Risk", low_risk)

    with m3:
        st.metric("Moderate Risk", moderate_risk)

    with m4:
        st.metric("High Risk", high_risk)

    st.divider()

    # Charts displayed side-by-side
    chart1, chart2 = st.columns(2)

    with chart1:
        st.subheader("Risk Level Distribution")

        risk_distribution = (
            data["RiskLevel"]
            .value_counts()
            .reindex(["Low", "Moderate", "High"])
        )

        st.bar_chart(
            risk_distribution,
            height=350
        )

    with chart2:
        st.subheader("Patients by Diagnosis")

        diagnosis_distribution = (
            data["DiagnosisName"]
            .value_counts()
            .sort_values(ascending=False)
        )

        st.bar_chart(
            diagnosis_distribution,
            height=350
        )

    st.divider()

    # Additional metrics
    st.subheader("Healthcare Utilization")

    c1, c2 = st.columns(2)

    with c1:
        st.metric(
            "Average Treatment Cost",
            f"{data['TreatmentCost'].mean():,.2f}"
        )

    with c2:
        st.metric(
            "Average Length of Stay",
            f"{data['LengthOfStay'].mean():.1f} days"
        )

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.divider()

st.caption(
    "Healthcare Analytics Portfolio Project | "
    "SQL • Excel • Python • Risk Stratification • Streamlit"
)
