import streamlit as st
import pandas as pd
import numpy as np
import joblib
from sklearn.datasets import load_iris
import matplotlib.pyplot as plt
import seaborn as sns

model = joblib.load('iris_model.pkl')
iris = load_iris()

st.title("🌸 Iris Flower Prediction App")
st.write("Enter flower features to predict its species:")

st.sidebar.header("Enter flower measurements:")
sepal_length = st.sidebar.slider('Sepal Length (cm)', 4.0, 8.0, 5.1)
sepal_width = st.sidebar.slider('Sepal Width (cm)', 2.0, 4.5, 3.5)
petal_length = st.sidebar.slider('Petal Length (cm)', 1.0, 7.0, 1.4)
petal_width = st.sidebar.slider('Petal Width (cm)', 0.1, 2.5, 0.2)

if st.sidebar.button("Predict"):

    input_data = pd.DataFrame([[sepal_length, sepal_width, petal_length, petal_width]],
                              columns=iris.feature_names)

    prediction = model.predict(input_data)[0]
    prediction_proba = model.predict_proba(input_data)[0]

    st.subheader("🔮 Prediction Result")
    st.write(f"Predicted Species: **{iris.target_names[prediction]}**")

    st.subheader("📈 Prediction Probability")
    proba_df = pd.DataFrame([prediction_proba], columns=iris.target_names)
    st.dataframe(proba_df)

    fig, ax = plt.subplots()
    sns.barplot(x=iris.target_names, y=prediction_proba, palette="viridis")
    ax.set_ylabel("Probability")
    ax.set_title("Prediction Confidence")
    st.pyplot(fig)


