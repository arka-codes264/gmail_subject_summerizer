import streamlit as st
import google.generativeai as genai

# ── Page config ────────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="SubjectCraft – AI Subject Line Generator",
    page_icon="✉️",
    layout="centered",
)

# ── CSS ────────────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;0,900;1,700&family=Lora:ital,wght@0,400;0,500;1,400&family=DM+Mono&display=swap');

html, body, [class*="css"] {
    font-family: 'Lora', serif;
}

.stApp {
    background-color: #f5f0e8;
    color: #1a1410;
}

header[data-testid="stHeader"] { display: none; }

/* ── Masthead ── */
.masthead {
    border-top: 3px solid #1a1410;
    border-bottom: 1px solid #1a1410;
    padding: 1.4rem 0 1.2rem 0;
    text-align: center;
    margin-bottom: 0.5rem;
}
.masthead-eyebrow {
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: #7a6a55;
    margin-bottom: 0.5rem;
}
.masthead h1 {
    font-family: 'Playfair Display', serif;
    font-size: 3.6rem;
    font-weight: 900;
    letter-spacing: -1.5px;
    line-height: 1;
    color: #1a1410;
    margin: 0;
}
.masthead-sub {
    font-family: 'Lora', serif;
    font-style: italic;
    color: #7a6a55;
    font-size: 0.95rem;
    margin-top: 0.5rem;
}

/* ── Section label ── */
.section-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.65rem;
    letter-spacing: 0.2em;
    text-transform: uppercase;
    color: #7a6a55;
    border-bottom: 1px solid #c8bfaa;
    padding-bottom: 0.3rem;
    margin: 1.6rem 0 0.6rem 0;
}

/* ── Input overrides ── */
textarea {
    background: #faf7f2 !important;
    border: 1px solid #c8bfaa !important;
    border-radius: 6px !important;
    color: #1a1410 !important;
    font-family: 'Lora', serif !important;
    font-size: 0.93rem !important;
    line-height: 1.7 !important;
}
textarea:focus {
    border-color: #1a1410 !important;
    box-shadow: none !important;
}
input[type="password"] {
    background: #faf7f2 !important;
    border: 1px solid #c8bfaa !important;
    border-radius: 6px !important;
    color: #1a1410 !important;
    font-family: 'DM Mono', monospace !important;
    font-size: 0.85rem !important;
}
input[type="password"]:focus {
    border-color: #1a1410 !important;
    box-shadow: none !important;
}

label[data-testid="stWidgetLabel"] p {
    font-family: 'DM Mono', monospace !important;
    font-size: 0.7rem !important;
    letter-spacing: 0.12em !important;
    text-transform: uppercase !important;
    color: #7a6a55 !important;
}

/* ── Button ── */
.stButton > button {
    background: #1a1410;
    color: #f5f0e8;
    font-family: 'Playfair Display', serif;
    font-weight: 700;
    font-size: 1rem;
    letter-spacing: 0.03em;
    border: none;
    border-radius: 6px;
    padding: 0.7rem 2.5rem;
    width: 100%;
    cursor: pointer;
    transition: background 0.2s, transform 0.15s;
    margin-top: 0.8rem;
}
.stButton > button:hover {
    background: #3d2f1f;
    transform: translateY(-1px);
}

/* ── Result card ── */
.result-card {
    background: #1a1410;
    border-radius: 10px;
    padding: 2rem 2.2rem;
    margin-top: 2rem;
    position: relative;
}
.result-label {
    font-family: 'DM Mono', monospace;
    font-size: 0.6rem;
    letter-spacing: 0.25em;
    text-transform: uppercase;
    color: #7a6a55;
    margin-bottom: 0.8rem;
}
.result-subject {
    font-family: 'Playfair Display', serif;
    font-size: 1.75rem;
    font-weight: 700;
    color: #f5f0e8;
    line-height: 1.35;
    margin: 0;
}
.result-divider {
    border: none;
    border-top: 1px solid #3d3028;
    margin: 1.2rem 0;
}
.result-tip {
    font-family: 'Lora', serif;
    font-style: italic;
    font-size: 0.82rem;
    color: #9a8a75;
}

/* ── Examples strip ── */
.example-strip {
    display: flex;
    gap: 0.6rem;
    flex-wrap: wrap;
    margin-top: 0.5rem;
}
.example-chip {
    background: #ede8de;
    border: 1px solid #c8bfaa;
    border-radius: 4px;
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    color: #5a4a35;
    padding: 0.25rem 0.65rem;
    cursor: pointer;
}

/* ── Footer ── */
.footer {
    border-top: 1px solid #c8bfaa;
    margin-top: 3rem;
    padding-top: 1rem;
    text-align: center;
    font-family: 'DM Mono', monospace;
    font-size: 0.7rem;
    color: #9a8a75;
    letter-spacing: 0.08em;
}

/* ── Alerts ── */
.stAlert {
    border-radius: 6px !important;
    font-family: 'Lora', serif !important;
    font-size: 0.88rem !important;
}
</style>
""", unsafe_allow_html=True)


# ── Masthead ───────────────────────────────────────────────────────────────────
st.markdown("""
<div class="masthead">
    <div class="masthead-eyebrow">✦ Powered by Google Gemini ✦</div>
    <h1>SubjectCraft</h1>
    <div class="masthead-sub">The AI-powered subject line that gets your email opened</div>
</div>
""", unsafe_allow_html=True)


# ── Prompts ────────────────────────────────────────────────────────────────────
SYSTEM_PROMPT = (
    "You are a professional Email Marketer and Psychology expert. "
    "Your goal is to extract the core intent of an email and provide a "
    "concise, high-open-rate subject line. Output only the subject line text — "
    "no quotes, no punctuation at the end unless it's a question mark, no explanation."
)

USER_PROMPT_PREFIX = (
    "Analyze the following email content. Identify the sender's goal and "
    "write a professional, appropriately toned subject line that matches "
    "the context (e.g., student, corporate, freelance, or personal). "
    "Make it punchy, relevant, and curiosity-inducing."
)

# Example emails for quick-fill
EXAMPLES = {
    "🤝 Networking": (
        "Dear Raj, I hope this email finds you well. I found your profile through "
        "Canva and was impressed with your work in UI. I'd love to connect and "
        "hear more about your experience. Best regards, Arka."
    ),
    "📄 Job Application": (
        "Dear Hiring Manager, I am a final year B.Tech student specializing in "
        "Machine Learning. I came across your open Data Science internship role "
        "and would love to apply. I have attached my resume for your consideration."
    ),
    "💼 Client Follow-up": (
        "Hi Sarah, just following up on the proposal I sent over last Tuesday "
        "regarding the website redesign project. Please let me know if you have "
        "any questions or if you'd like to schedule a call to discuss further."
    ),
    "🙏 Thank You": (
        "Dear Professor Mehta, I wanted to express my sincere gratitude for "
        "your guidance during my final year project. Your feedback helped me "
        "greatly improve my research methodology and final report."
    ),
}


# ── API Key ────────────────────────────────────────────────────────────────────
st.markdown('<div class="section-label">01 — API Configuration</div>', unsafe_allow_html=True)
api_key = st.text_input(
    "Gemini API Key",
    type="password",
    placeholder="AIza...",
    help="Free key at aistudio.google.com/app/apikey",
)

# ── Email Input ────────────────────────────────────────────────────────────────
st.markdown('<div class="section-label">02 — Your Email Body</div>', unsafe_allow_html=True)

# Quick-fill example buttons
st.markdown("**Quick-fill an example:**")
cols = st.columns(len(EXAMPLES))
for i, (label, body) in enumerate(EXAMPLES.items()):
    if cols[i].button(label, key=f"ex_{i}"):
        st.session_state["email_body"] = body

email_body = st.text_area(
    "Paste your email content below",
    value=st.session_state.get("email_body", ""),
    height=200,
    placeholder="Dear [Name], I hope this message finds you well...",
    key="email_input",
)

# ── Tone selector ──────────────────────────────────────────────────────────────
st.markdown('<div class="section-label">03 — Tone Preference (Optional)</div>', unsafe_allow_html=True)
tone = st.select_slider(
    "Adjust the tone of the subject line",
    options=["Formal", "Professional", "Neutral", "Friendly", "Casual"],
    value="Professional",
)

# ── Generate ───────────────────────────────────────────────────────────────────
generate_btn = st.button("✦ Generate Subject Line")

if generate_btn:
    if not api_key.strip():
        st.error("🔑  Please enter your Gemini API key.")
        st.stop()
    if not email_body.strip():
        st.error("✉️  Please paste your email content first.")
        st.stop()

    with st.spinner("Reading between the lines..."):
        try:
            genai.configure(api_key=api_key.strip())

            model = genai.GenerativeModel(
                model_name="gemini-2.5-flash",
                system_instruction=SYSTEM_PROMPT,
            )

            full_prompt = (
                f"{USER_PROMPT_PREFIX}\n"
                f"Tone preference: {tone}\n\n"
                f"Email Content:\n{email_body.strip()}"
            )

            response = model.generate_content(full_prompt)
            subject = response.text.strip().strip('"').strip("'")

            # Store result
            st.session_state["last_subject"] = subject

        except Exception as e:
            err = str(e)
            if "API_KEY" in err.upper() or "invalid" in err.lower() or "credential" in err.lower():
                st.error("🔑  Invalid Gemini API key. Please double-check it.")
            elif "quota" in err.lower():
                st.error("⚠️  API quota exceeded. Wait a moment and try again.")
            else:
                st.error(f"Something went wrong: `{err}`")
            st.stop()

# ── Result display ─────────────────────────────────────────────────────────────
if "last_subject" in st.session_state and st.session_state["last_subject"]:
    subject = st.session_state["last_subject"]

    tips = {
        "Formal": "Formal tone: clear hierarchy, no contractions.",
        "Professional": "Professional tone: crisp, goal-oriented, respects the reader's time.",
        "Neutral": "Neutral tone: balanced and universally readable.",
        "Friendly": "Friendly tone: warm opener, approachable language.",
        "Casual": "Casual tone: conversational, great for warm contacts.",
    }

    st.markdown(f"""
    <div class="result-card">
        <div class="result-label">✦ Suggested Subject Line</div>
        <div class="result-subject">{subject}</div>
        <hr class="result-divider">
        <div class="result-tip">💡 {tips.get(tone, '')}</div>
    </div>
    """, unsafe_allow_html=True)

    # Copy button via clipboard trick
    st.code(subject, language=None)
    st.caption("👆 Click the copy icon on the right to copy your subject line")

    # Regenerate nudge
    st.markdown(
        "<div style='text-align:center; margin-top:1rem; font-family: DM Mono, monospace; "
        "font-size:0.75rem; color:#7a6a55;'>Not quite right? Adjust the tone and click Generate again.</div>",
        unsafe_allow_html=True,
    )

# ── Footer ─────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="footer">
    SubjectCraft · Built with Streamlit + Google Gemini · API keys are never stored
</div>
""", unsafe_allow_html=True)