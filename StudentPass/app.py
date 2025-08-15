import streamlit as st
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
import shap
import numpy as np

# -------------------------------
# Page Config & Theme
# -------------------------------
st.set_page_config(page_title="StudentPass", page_icon="🎓", layout="wide")
primary_color = "#4B79A1"  # StudentPass branding
secondary_color = "#F4D35E"

st.markdown(f"""
<style>
[data-testid="stSidebar"] {{
    background-color: {primary_color};
}}
.stButton>button {{
    background-color: {secondary_color};
    color: black;
}}
</style>
""", unsafe_allow_html=True)

# -------------------------------
# Load Model
# -------------------------------
@st.cache_data
def load_model():
    return joblib.load("model/performance_pipeline.pkl")

model = load_model()

# -------------------------------
# Feature lists
# -------------------------------
categorical_features = ['school','sex','address','famsize','Pstatus','Mjob','Fjob','reason','guardian',
                        'schoolsup','famsup','paid','activities','nursery','higher','internet','romantic','dataset']
numeric_features = ['age','Medu','Fedu','traveltime','studytime','failures','famrel','freetime',
                    'goout','Dalc','Walc','health','absences','G1','G2','G3']

# -------------------------------
# Sidebar Navigation
# -------------------------------
st.sidebar.title("StudentPass")
app_mode = st.sidebar.selectbox("Choose the page:",
                                ["Home", "Single Prediction", "Batch Prediction", "Statistics", "About"])

# -------------------------------
# Helper Functions
# -------------------------------
def get_dynamic_options(df, col):
    if df[col].dtype == 'object':
        return df[col].unique().tolist()
    return None

# -------------------------------
# Home Page
# -------------------------------
if app_mode == "Home":
    st.title("🎓 StudentPass")
    st.markdown("""
    Welcome to **StudentPass**, your student performance predictor.
    
    **Features:**
    - Predict student pass/fail outcome
    - Single prediction or batch predictions via CSV
    - View statistics and charts
    - Understand model predictions with explanations
    """)

# -------------------------------
# Single Prediction Page
# -------------------------------
elif app_mode == "Single Prediction":
    st.title("Single Student Prediction")
    
    sample_file = st.file_uploader("Upload CSV for dynamic categorical options (optional)", type="csv", key="single_sample")
    sample_df = pd.read_csv(sample_file) if sample_file else None

    with st.form("single_prediction_form"):
        st.subheader("Categorical Features")
        cat_inputs = {}
        for col in categorical_features:
            if sample_df is not None and col in sample_df.columns:
                options = get_dynamic_options(sample_df, col)
                if options is not None:
                    cat_inputs[col] = st.selectbox(col, options=options)
                else:
                    cat_inputs[col] = st.text_input(col)
            else:
                # Default options for known categorical features
                if col in ['schoolsup','famsup','paid','activities','nursery','higher','internet','romantic']:
                    cat_inputs[col] = st.selectbox(col, ["yes", "no"])
                elif col == 'school':
                    cat_inputs[col] = st.selectbox(col, ["GP", "MS"])
                elif col == 'address':
                    cat_inputs[col] = st.selectbox(col, ["U", "R"])
                elif col == 'famsize':
                    cat_inputs[col] = st.selectbox(col, ["GT3", "LE3"])
                elif col == 'Pstatus':
                    cat_inputs[col] = st.selectbox(col, ["T", "A"])
                elif col in ['Mjob','Fjob']:
                    cat_inputs[col] = st.selectbox(col, ["teacher","health","services","at_home","other"])
                elif col == 'reason':
                    cat_inputs[col] = st.selectbox(col, ["home","reputation","course","other"])
                elif col == 'guardian':
                    cat_inputs[col] = st.selectbox(col, ["mother","father","other"])
                else:
                    cat_inputs[col] = st.text_input(col)

        st.subheader("Numeric Features")
        num_inputs = {}
        for col in numeric_features:
            if sample_df is not None and col in sample_df.columns:
                min_val = int(sample_df[col].min())
                max_val = int(sample_df[col].max())
                median_val = int(sample_df[col].median())
            else:
                min_val, max_val, median_val = 0, 100, 0
            num_inputs[col] = st.number_input(col, min_value=min_val, max_value=max_val, value=median_val)

        submitted = st.form_submit_button("Predict")

        if submitted:
            input_df = pd.DataFrame([{**cat_inputs, **num_inputs}])
            
            if 'dataset' not in df.columns:
                input_df['dataset'] = 'student_mat'  # or any default value used during training

            prediction = model.predict(input_df)[0]
            st.success(f"Predicted Performance: **{prediction}**")

            # -------------------------------
            # SHAP Explanation
            # -------------------------------
            try:
                explainer = shap.Explainer(model.predict, input_df)
                shap_values = explainer(input_df)
                st.subheader("Feature Importance (SHAP)")
                shap.initjs()
                shap.plots.bar(shap_values, show=False)
            except Exception as e:
                st.warning("SHAP explanation could not be generated. Model may not be compatible.")


# -------------------------------
# Batch Prediction Page
# -------------------------------
elif app_mode == "Batch Prediction":
    st.title("Batch Prediction via CSV Upload")
    st.markdown("Upload CSV file with student data to get predictions.")

    uploaded_file = st.file_uploader("Choose a CSV file", type="csv")
    
    # Fallback to local CSV if no upload
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
    else:
        try:
            df = pd.read_csv("student_mat.csv")
            st.info("No CSV uploaded. Using local student_mat.csv as default dataset.")
        except FileNotFoundError:
            df = None
            st.warning("No CSV uploaded and local student_mat.csv not found. Please upload a CSV.")

    # Proceed if df is available
    if df is not None:
        st.write("Data Preview:")
        st.dataframe(df.head())

        if st.button("Predict Batch"):
            
            if 'dataset' not in df.columns:
                df['dataset'] = 'student_mat'  # or any default value used during training

            preds = model.predict(df)
            df["Prediction"] = preds
            st.success("Predictions added to data")
            st.dataframe(df.head())
            
            # -------------------------------
            # Interactive Charts
            # -------------------------------
            st.subheader("Prediction Counts")
            pred_counts = df["Prediction"].value_counts()
            fig, ax = plt.subplots()
            sns.barplot(x=pred_counts.index, y=pred_counts.values, palette="coolwarm", ax=ax)
            ax.set_ylabel("Count")
            st.pyplot(fig)

            st.subheader("Pass/Fail Pie Chart")
            fig2, ax2 = plt.subplots()
            ax2.pie(pred_counts.values, labels=pred_counts.index, autopct="%1.1f%%", colors=["#4B79A1","#F4D35E"])
            st.pyplot(fig2)

            # Download option
            csv = df.to_csv(index=False).encode()
            st.download_button("Download Predictions CSV", data=csv, file_name="predictions.csv", mime="text/csv")

# -------------------------------
# Statistics Page
# -------------------------------
elif app_mode == "Statistics":
    st.title("Student Data Statistics")
    st.markdown("Upload dataset to view charts and statistics.")
    
    uploaded_file = st.file_uploader("Upload CSV for statistics", type="csv", key="stats")
    if uploaded_file:
        df = pd.read_csv(uploaded_file)
        st.write(df.describe())

        st.subheader("Correlation Heatmap")
        fig, ax = plt.subplots(figsize=(10,8))
        sns.heatmap(df.corr(), annot=True, cmap="coolwarm", ax=ax)
        st.pyplot(fig)

        st.subheader("Feature Distributions")
        feature = st.selectbox("Select feature for histogram", numeric_features)
        fig2, ax2 = plt.subplots()
        sns.histplot(df[feature], kde=True, ax=ax2, color=secondary_color)
        st.pyplot(fig2)

# -------------------------------
# About Page
# -------------------------------
elif app_mode == "About":
    st.title("About StudentPass")
    st.markdown("""
    **StudentPass** is a web application built with Streamlit to predict student performance.
    
    **Technologies used:**
    - Python, Streamlit
    - scikit-learn
    - pandas, matplotlib, seaborn
    - Joblib for model persistence
    - SHAP for explainability

    Developed to help educators and students understand performance trends and predictions.
    """)
