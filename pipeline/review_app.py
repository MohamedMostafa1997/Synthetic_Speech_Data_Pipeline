import json
import streamlit as st


with open("data/reviewed/reviewed.json", "r", encoding="utf-8") as file:
    samples = json.load(file)


st.title("Synthetic Speech Review")


for sample in samples:
    st.subheader(f"Sample {sample['id']}")

    st.write(f"Text: {sample['text']}")
    st.write(f"Prediction: {sample['prediction']}")
    st.write(f"WER: {round(sample['wer'], 2)}")
    st.write(f"Accepted: {sample['accepted']}")

    audio_file = open(sample["audio"], "rb")
    st.audio(audio_file.read(), format="audio/wav")

    st.divider()