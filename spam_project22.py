import streamlit as st
import joblib
import pandas as pd

model = joblib.load("spam_new.pkl")

st.markdown(
    """
<div style="
    text-align:center;
    padding:20px;
    border-radius:15px;
    background:rgba(255,255,255,0.1);
    backdrop-filter: blur(10px);
    box-shadow:0 4px 15px rgba(0,0,0,0.2);">
    <h1 style="
        color:#00BFFF;
        font-size:55px;
        margin:0;">
        📧 Spam Classifier Project
    </h1>
</div>
""",
    unsafe_allow_html=True,
)

# Sidebar
st.sidebar.markdown(
    """
    <div style="
        padding:16px;
        border-radius:14px;
        background: linear-gradient(135deg, rgba(0,191,255,0.18), rgba(76,205,196,0.18));
        border: 1px solid rgba(255,255,255,0.15);
        box-shadow: 0 6px 18px rgba(0,0,0,0.15);
    ">
        <div style="font-size:20px; font-weight:800; color:#00BFFF;">📌 Spam Classifier</div>
        <div style="margin-top:6px; font-size:13.5px; line-height:1.4; color:rgba(255,255,255,0.85);">
            Detect spam messages using a trained ML model.
        </div>
    </div>
    <div style="height:12px"></div>
    <div style="
        padding:14px;
        border-radius:14px;
        background: rgba(255,255,255,0.06);
        border: 1px solid rgba(255,255,255,0.12);
        box-shadow: 0 6px 18px rgba(0,0,0,0.12);
    ">
        <div style="font-weight:800; color:#4ecdc4; font-size:16px;">📈 Live Stats</div>
        <div style="margin-top:10px; display:flex; gap:10px; align-items:center;">
            <div style="flex:1; padding:10px; border-radius:12px; background: rgba(0,191,255,0.10);">
                <div style="font-size:12px; color:rgba(255,255,255,0.75);">Messages</div>
                <div style="font-size:22px; font-weight:900; color:#00BFFF;">0</div>
            </div>
            <div style="flex:1; padding:10px; border-radius:12px; background: rgba(255,107,107,0.10);">
                <div style="font-size:12px; color:rgba(255,255,255,0.75);">Predicted Spam</div>
                <div style="font-size:22px; font-weight:900; color:#ff6b6b;">0</div>
            </div>
        </div>
        <div style="margin-top:10px; font-size:12px; color:rgba(255,255,255,0.7);">
            (Stats update after you click Predict)
        </div>
    </div>
    <style>
      @keyframes pulse {
        0% { transform: scale(1); box-shadow: 0 0 0 rgba(0,191,255,0.0); }
        50% { transform: scale(1.02); box-shadow: 0 0 18px rgba(0,191,255,0.35); }
        100% { transform: scale(1); box-shadow: 0 0 0 rgba(0,191,255,0.0); }
      }
      .stats-card { animation: pulse 2.6s ease-in-out infinite; }
    </style>
    """,
    unsafe_allow_html=True,
)

# Lottie animation (embedded via HTML/JS)
# Note: requires st.components.v1
import streamlit.components.v1 as components

lottie_json_url = "https://lottie.host/6a2d9b8e-robot-ai-example.json"
components.html(
    f"""
    <div style='display:flex; justify-content:center; margin-top:6px;'>
      <div id='lottie_sidebar' style='width:120px; height:90px;'></div>
    </div>
    <script src='https://cdnjs.cloudflare.com/ajax/libs/bodymovin/5.12.2/lottie.min.js'></script>
    <script>
      (function() {{
        const el = document.getElementById('lottie_sidebar');
        if (!el || !window.lottie) return;
        window.lottie.destroy && window.lottie.destroy();
        window.lottie.loadAnimation({{
          container: el,
          renderer: 'svg',
          loop: true,
          autoplay: true,
          path: '{lottie_json_url}'
        }});
      }})();
    </script>
    """,
    height=120,
)


# Real stats placeholders (updated on predict)
st.sidebar.write("")
st.sidebar.caption("Developed by Aditya Pathak")

stats_messages = st.sidebar.empty()
stats_spam = st.sidebar.empty()

mode = st.sidebar.radio(
    "Choose prediction",
    options=["Single Message", "Bulk Message"],
    index=0,
    horizontal=False,
)



if mode == "Single Message":
    st.markdown(
        """
<h2 style="
    text-align:center;
    font-size:36px;
    font-weight:700;
    background: linear-gradient(to right, #ff6b6b, #4ecdc4);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;">
    🚀 Single Message Prediction
</h2>
""",
        unsafe_allow_html=True,
    )

    text = st.text_input("Enter Message")
    st.caption("Tip: paste a single line message here")

    if st.button("Predict", use_container_width=True):
        result = model.predict([text])
        is_spam = result[0] == "spam" if hasattr(result, "__len__") else result == "spam"

        # Attractive result card
        if is_spam:
            st.markdown(
                """
                <div style="
                    padding:16px;
                    border-radius:14px;
                    background: rgba(255,107,107,0.12);
                    border: 1px solid rgba(255,107,107,0.35);
                    box-shadow: 0 10px 25px rgba(255,107,107,0.15);
                ">
                    <div style="font-size:14px; color:rgba(255,255,255,0.8);">Prediction</div>
                    <div style="font-size:26px; font-weight:900; color:#ff6b6b;">⚠️ SPAM</div>
                    <div style="font-size:13px; color:rgba(255,255,255,0.75); margin-top:4px;">
                        This message is likely irrelevant/spam.
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )
        else:
            st.markdown(
                """
                <div style="
                    padding:16px;
                    border-radius:14px;
                    background: rgba(76,205,196,0.12);
                    border: 1px solid rgba(76,205,196,0.35);
                    box-shadow: 0 10px 25px rgba(76,205,196,0.15);
                ">
                    <div style="font-size:14px; color:rgba(255,255,255,0.8);">Prediction</div>
                    <div style="font-size:26px; font-weight:900; color:#4ecdc4;">✅ HAM</div>
                    <div style="font-size:13px; color:rgba(255,255,255,0.75); margin-top:4px;">
                        This message looks relevant/ham.
                    </div>
                </div>
                """,
                unsafe_allow_html=True,
            )

        # Confidence gauge (if model supports probabilities)
        confidence = None
        if hasattr(model, "predict_proba"):
            try:
                proba = model.predict_proba([text])
                # pick spam probability if we can locate class index
                if hasattr(model, "classes_") and isinstance(model.classes_, (list, tuple)):
                    classes = list(model.classes_)
                else:
                    classes = list(getattr(model, "classes_", []))

                if classes:
                    spam_idx = classes.index("spam") if "spam" in classes else None
                    if spam_idx is not None:
                        confidence = float(proba[0][spam_idx])
                    else:
                        confidence = float(max(proba[0]))
                else:
                    confidence = float(max(proba[0]))
            except Exception:
                confidence = None

        if confidence is not None:
            st.caption("Prediction confidence")
            st.progress(min(max(confidence, 0.0), 1.0))
            st.write(f"{confidence*100:.1f}%")

        stats_messages.metric("Messages", "1")
        stats_spam.metric("Predicted Spam", "1" if is_spam else "0")





else:
    st.markdown(
        """
<h2 style="
    text-align:center;
    font-size:36px;
    font-weight:700;
    background: linear-gradient(to right, #ff6b6b, #4ecdc4);
    -webkit-background-clip:text;
    -webkit-text-fill-color:transparent;">
    🚀 Bulk Message Prediction
</h2>
""",
        unsafe_allow_html=True,
    )

    file = st.file_uploader("Select file containing bulk messages, type = ['txt','csv']")

    if file is not None:
        df = pd.read_csv(file, header=None, names=["Msg"])
        st.dataframe(df)

        if st.button("Predict", key="b2"):
            df["result"] = model.predict(df.Msg)
            st.dataframe(df)

# Footer
st.markdown(
    """
    <div style="
        position:fixed;
        left:0;
        bottom:0;
        width:100%;
        padding:14px;
        text-align:center;
        background: rgba(0,0,0,0.65);
        color: rgba(255,255,255,0.9);
        backdrop-filter: blur(10px);
        border-top: 1px solid rgba(255,255,255,0.12);
        z-index: 9999;
    ">
        <span style="font-weight:800; color:#00BFFF;">📧 Spam Classifier</span>
        <span style="opacity:0.85;">| Built with Streamlit • Aditya Pathak</span>
    </div>

    <style>
      /* add bottom padding so footer doesn't cover content */
      .stApp { padding-bottom: 70px; }
    </style>
    """,
    unsafe_allow_html=True,
)

  
    




