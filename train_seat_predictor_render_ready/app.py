import streamlit as st

st.set_page_config(
    page_title="Train Seat Scenery Predictor",
    page_icon="🚆"
)

st.title("🚆 Train Seat Scenery Predictor 🌄")

st.write("Predicting your completely unreliable train window view!")

route = st.text_input(
    "Train Route",
    placeholder="Example: Kochi to Chennai"
)

side = st.selectbox(
    "Coach Side",
    ["Select a side", "Left Side", "Right Side"]
)

seat = st.text_input(
    "Seat Number",
    placeholder="Example: 42"
)

if st.button("Predict My View 🔮"):

    if route and side != "Select a side" and seat:

        # Fun prediction calculation
        seed = sum(
            ord(c) for c in (route + side + seat).lower()
        )

        score = round(5 + (seed % 41) / 10, 1)

        trees = 40 + (seed % 51)

        buildings = 10 + ((seed // 3) % 31)

        wall = max(1, 100 - trees - buildings)

        st.success("Prediction Complete! 🎉")

        st.subheader(f"🌄 Scenery Quality: {score}/10")

        st.write(f"🌳 Trees: {trees}%")

        st.write(f"🏢 Buildings: {buildings}%")

        st.write(f"🧱 Random Wall: {wall}%")

        st.caption(
            "⚠️ Accuracy is scientifically questionable."
        )

    else:

        st.warning(
            "Please fill in all the details!"
        )
