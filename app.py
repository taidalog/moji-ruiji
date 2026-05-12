import streamlit as st
from src import string_metric as sm

st.title("moji-ruiji")

s1 = st.text_area("元テキスト", "ここにテキストを入力してください")
s2 = st.text_area("入力テキスト", "ここにもテキストを入力してください！")

jsim = sm.StringMetric_jaroSimilarity(s1, s2)
m = st.metric(label="類似度", value=float(jsim))

if st.button("類似度を計算"):
    jsim = sm.StringMetric_jaroSimilarity(s1, s2)
    m.metric(label="類似度", value=float(jsim))
