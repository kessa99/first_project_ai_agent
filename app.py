import streamlit as st
from audio_recorder_streamlit import audio_recorder
import pdfplumber
import io

st.set_page_config(
    page_title="AI Financial Assistant",
    page_icon="💰",
    layout="centered",
)

# ── Responsive CSS ─────────────────────────────────────────────────────────────
st.markdown("""
<style>
  /* ── Global ── */
  html, body, [data-testid="stAppViewContainer"] {
    font-family: "Inter", "Segoe UI", sans-serif;
  }

  /* ── Page max-width & padding ── */
  .main .block-container {
    max-width: 780px;
    padding: 1.5rem 1rem 2rem;
    margin: 0 auto;
  }

  /* ── Header ── */
  .app-header {
    text-align: center;
    margin-bottom: 1.5rem;
  }
  .app-header h1 {
    font-size: clamp(1.4rem, 4vw, 2rem);
    font-weight: 700;
    margin-bottom: 0.2rem;
  }
  .app-header p {
    color: #6b7280;
    font-size: clamp(0.8rem, 2.5vw, 0.95rem);
    margin: 0;
  }

  /* ── Chat bubble overrides ── */
  [data-testid="stChatMessage"] {
    border-radius: 12px;
    padding: 0.6rem 0.8rem;
    margin-bottom: 0.5rem;
  }

  /* ── Input card ── */
  .input-card {
    background: #f9fafb;
    border: 1px solid #e5e7eb;
    border-radius: 16px;
    padding: 1.2rem 1rem;
    margin-top: 1rem;
  }

  /* ── Input section labels ── */
  .section-label {
    font-size: 0.8rem;
    font-weight: 600;
    color: #374151;
    text-transform: uppercase;
    letter-spacing: 0.05em;
    margin-bottom: 0.35rem;
  }

  /* ── Textarea full-width ── */
  textarea {
    border-radius: 10px !important;
    font-size: 0.95rem !important;
  }

  /* ── Accessory row (audio + image) ── */
  .accessory-row {
    display: flex;
    flex-wrap: wrap;
    gap: 1rem;
    margin-top: 0.9rem;
  }
  .accessory-box {
    flex: 1 1 180px;
    background: #fff;
    border: 1px solid #e5e7eb;
    border-radius: 12px;
    padding: 0.8rem 1rem;
  }
  .accessory-box p { margin: 0; }

  /* ── Send / clear buttons ── */
  .stButton > button {
    border-radius: 10px !important;
    font-weight: 600 !important;
    transition: transform 0.1s ease;
  }
  .stButton > button:active { transform: scale(0.97); }

  /* ── File uploader compact ── */
  [data-testid="stFileUploader"] {
    background: transparent !important;
    border: none !important;
    padding: 0 !important;
  }
  [data-testid="stFileUploader"] section {
    border: 1.5px dashed #d1d5db !important;
    border-radius: 10px !important;
    padding: 0.6rem !important;
  }

  /* ── Audio recorder centering ── */
  .audio-wrap {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    flex-wrap: wrap;
  }

  /* ── Responsive: stack everything on small screens ── */
  @media (max-width: 520px) {
    .main .block-container { padding: 1rem 0.6rem 1.5rem; }
    .accessory-box { flex: 1 1 100%; }
  }
</style>
""", unsafe_allow_html=True)

# ── Session state ─────────────────────────────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []
if "audio_bytes" not in st.session_state:
    st.session_state.audio_bytes = None
if "uploaded_image" not in st.session_state:
    st.session_state.uploaded_image = None
if "uploaded_pdf_text" not in st.session_state:
    st.session_state.uploaded_pdf_text = None

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("""
<div class="app-header">
  <h1>💰 AI Financial Assistant</h1>
  <p>Analysez vos achats et obtenez des conseils financiers personnalisés</p>
</div>
""", unsafe_allow_html=True)

# ── Chat history ──────────────────────────────────────────────────────────────
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg.get("image"):
            st.image(msg["image"], width=220)
        if msg.get("audio"):
            st.audio(msg["audio"], format="audio/wav")
        st.markdown(msg["content"])

# ── Input panel ───────────────────────────────────────────────────────────────
st.markdown('<div class="input-card">', unsafe_allow_html=True)

st.markdown('<div class="section-label">✏️ Message texte</div>', unsafe_allow_html=True)
user_text = st.text_area(
    "message",
    placeholder="Ex : Je veux acheter un iPhone 15 Pro à 1200 €. Est-ce raisonnable ?",
    height=110,
    label_visibility="collapsed",
)

# Accessory row: audio + image
st.markdown('<div class="accessory-row">', unsafe_allow_html=True)

col_audio, col_image = st.columns([1, 1], gap="medium")

with col_audio:
    st.markdown('<div class="section-label">🎙 Audio</div>', unsafe_allow_html=True)
    st.markdown('<div class="audio-wrap">', unsafe_allow_html=True)
    audio_bytes = audio_recorder(
        text="Cliquer pour enregistrer",
        recording_color="#e74c3c",
        neutral_color="#3b82f6",
        icon_name="microphone",
        icon_size="lg",
        pause_threshold=3.0,
    )
    st.markdown('</div>', unsafe_allow_html=True)
    if audio_bytes:
        st.session_state.audio_bytes = audio_bytes
        st.audio(audio_bytes, format="audio/wav")
        st.caption("✓ Audio enregistré")

with col_image:
    st.markdown('<div class="section-label">🖼 Fichier (image ou PDF)</div>', unsafe_allow_html=True)
    uploaded_file = st.file_uploader(
        "fichier",
        type=["png", "jpg", "jpeg", "webp", "pdf"],
        label_visibility="collapsed",
    )
    if uploaded_file:
        if uploaded_file.type == "application/pdf":
            raw = uploaded_file.read()
            with pdfplumber.open(io.BytesIO(raw)) as pdf:
                pages_text = [p.extract_text() or "" for p in pdf.pages]
            st.session_state.uploaded_pdf_text = "\n".join(pages_text)
            st.session_state.uploaded_image = None
            st.success(f"PDF chargé : {uploaded_file.name} ({len(pdf.pages)} page(s))")
            with st.expander("Aperçu du texte extrait"):
                st.text(st.session_state.uploaded_pdf_text[:1000] + ("…" if len(st.session_state.uploaded_pdf_text) > 1000 else ""))
        else:
            st.session_state.uploaded_image = uploaded_file.read()
            st.session_state.uploaded_pdf_text = None
            st.image(st.session_state.uploaded_image, use_column_width=True)

st.markdown('</div>', unsafe_allow_html=True)  # accessory-row

# Action buttons
st.markdown("<br>", unsafe_allow_html=True)
btn_send, btn_clear, _ = st.columns([2, 2, 3], gap="small")
with btn_send:
    send = st.button("Envoyer ➤", type="primary", use_container_width=True)
with btn_clear:
    if st.button("🗑 Effacer", use_container_width=True):
        st.session_state.messages = []
        st.session_state.audio_bytes = None
        st.session_state.uploaded_image = None
        st.rerun()

st.markdown('</div>', unsafe_allow_html=True)  # input-card

# ── Handle submission ─────────────────────────────────────────────────────────
if send:
    has_text  = bool(user_text and user_text.strip())
    has_audio = st.session_state.audio_bytes is not None
    has_image = st.session_state.uploaded_image is not None
    has_pdf   = st.session_state.uploaded_pdf_text is not None

    if not has_text and not has_audio and not has_image and not has_pdf:
        st.warning("Veuillez saisir un message, enregistrer un audio ou joindre un fichier.")
    else:
        display_text = user_text.strip() if has_text else "*(message audio)*"

        # Append PDF content to the prompt sent to the agent
        agent_prompt = display_text
        if has_pdf:
            agent_prompt += f"\n\n--- Contenu du document joint ---\n{st.session_state.uploaded_pdf_text}"

        st.session_state.messages.append({
            "role": "user",
            "content": display_text + (" *(+ PDF joint)*" if has_pdf else ""),
            "audio": st.session_state.audio_bytes if has_audio else None,
            "image": st.session_state.uploaded_image if has_image else None,
        })

        with st.spinner("L'agent réfléchit…"):
            try:
                from agent import agent
                response = agent.invoke({"messages": [("human", agent_prompt)]})
                answer = response["messages"][-1].content
            except Exception as exc:
                answer = f"⚠️ Erreur lors de l'appel à l'agent : {exc}"

        st.session_state.messages.append({"role": "assistant", "content": answer})
        st.session_state.audio_bytes     = None
        st.session_state.uploaded_image  = None
        st.session_state.uploaded_pdf_text = None
        st.rerun()
