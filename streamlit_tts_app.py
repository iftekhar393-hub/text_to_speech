# import streamlit as st
# import soundfile as sf
# import numpy as np
# import io
# import os

# # ── Page config ──────────────────────────────────────────────────────────────
# st.set_page_config(
#     page_title="Orpheus TTS Studio",
#     page_icon="🎙️",
#     layout="wide",
# )

# # ── Custom CSS ────────────────────────────────────────────────────────────────
# st.markdown("""
# <style>
# @import url('https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;700;800&display=swap');

# html, body, [class*="css"] {
#     font-family: 'Syne', sans-serif;
#     background-color: #0e0e11;
#     color: #f0ede8;
# }

# .main { background-color: #0e0e11; }

# h1, h2, h3 { font-family: 'Syne', sans-serif; font-weight: 800; }

# .stTextArea textarea {
#     background-color: #1a1a20 !important;
#     color: #f0ede8 !important;
#     border: 1px solid #2e2e38 !important;
#     border-radius: 8px !important;
#     font-family: 'Space Mono', monospace !important;
#     font-size: 14px !important;
# }

# .stSelectbox > div > div {
#     background-color: #1a1a20 !important;
#     border: 1px solid #2e2e38 !important;
#     color: #f0ede8 !important;
# }

# .stButton > button {
#     background: linear-gradient(135deg, #e85d26, #f0a500);
#     color: white;
#     font-family: 'Syne', sans-serif;
#     font-weight: 700;
#     font-size: 16px;
#     border: none;
#     border-radius: 8px;
#     padding: 12px 32px;
#     width: 100%;
#     transition: opacity 0.2s;
# }
# .stButton > button:hover { opacity: 0.85; }

# .emotion-pill {
#     display: inline-block;
#     background: #1e1e28;
#     border: 1px solid #2e2e38;
#     border-radius: 20px;
#     padding: 4px 14px;
#     margin: 4px;
#     font-size: 13px;
#     font-family: 'Space Mono', monospace;
#     cursor: pointer;
#     color: #f0ede8;
#     transition: background 0.2s;
# }
# .emotion-pill:hover { background: #e85d26; border-color: #e85d26; }

# .tag-inserted {
#     background: #e85d2622;
#     border: 1px solid #e85d26;
#     border-radius: 4px;
#     padding: 2px 8px;
#     font-family: 'Space Mono', monospace;
#     font-size: 12px;
#     color: #e85d26;
# }

# .info-box {
#     background: #1a1a20;
#     border-left: 3px solid #e85d26;
#     border-radius: 4px;
#     padding: 12px 16px;
#     margin: 8px 0;
#     font-size: 13px;
#     color: #aaa;
# }

# .section-label {
#     font-size: 11px;
#     font-family: 'Space Mono', monospace;
#     letter-spacing: 2px;
#     text-transform: uppercase;
#     color: #666;
#     margin-bottom: 6px;
# }

# .title-glow {
#     font-size: 48px;
#     font-weight: 800;
#     background: linear-gradient(135deg, #e85d26, #f0a500);
#     -webkit-background-clip: text;
#     -webkit-text-fill-color: transparent;
#     margin-bottom: 4px;
# }
# </style>
# """, unsafe_allow_html=True)

# # ── Header ────────────────────────────────────────────────────────────────────
# st.markdown('<div class="title-glow">🎙️ Orpheus TTS Studio</div>', unsafe_allow_html=True)
# st.markdown('<p style="color:#666; font-family: Space Mono, monospace; font-size:13px;">Kokoro ONNX · Emotion-Aware Text-to-Speech</p>', unsafe_allow_html=True)
# st.markdown("---")

# # ── All emotions from emotions.txt ────────────────────────────────────────────
# ALL_EMOTIONS = [
#     "happy", "normal", "disgust", "longer", "sad", "frustrated",
#     "slow", "excited", "whisper", "panicky", "curious", "surprise",
#     "fast", "crying", "deep", "sleepy", "angry", "high", "shout"
# ]

# EMOTION_COLORS = {
#     "happy": "#f0a500", "excited": "#f0a500", "surprise": "#f0a500",
#     "sad": "#4a9eff", "crying": "#4a9eff",
#     "angry": "#e85d26", "shout": "#e85d26", "frustrated": "#e85d26",
#     "whisper": "#9b59b6", "sleepy": "#9b59b6", "slow": "#9b59b6",
#     "panicky": "#e74c3c", "fast": "#e74c3c",
#     "disgust": "#27ae60", "curious": "#27ae60",
#     "deep": "#1abc9c", "high": "#1abc9c",
#     "normal": "#666", "longer": "#666",
# }

# # ── Voices ────────────────────────────────────────────────────────────────────
# VOICES = {
#     "af_bella": "Bella (American Female)",
#     "af_sarah": "Sarah (American Female)",
#     "am_adam": "Adam (American Male)",
#     "am_michael": "Michael (American Male)",
#     "bf_emma": "Emma (British Female)",
#     "bm_george": "George (British Male)",
#     "hf_alpha": "Alpha (Hindi Female)",
#     "hf_beta": "Beta (Hindi Female)",
#     "hm_omega": "Omega (Hindi Male)",
#     "hm_psi": "Psi (Hindi Male)",
# }

# LANG_MAP = {
#     "af_": "en-us", "am_": "en-us",
#     "bf_": "en-gb", "bm_": "en-gb",
#     "hf_": "hi",    "hm_": "hi",
# }

# # ── Layout ────────────────────────────────────────────────────────────────────
# left_col, right_col = st.columns([3, 2], gap="large")

# with left_col:
#     # ── Text input ────────────────────────────────────────────────────────────
#     st.markdown('<div class="section-label">Script / Text</div>', unsafe_allow_html=True)

#     if "text_input" not in st.session_state:
#         st.session_state.text_input = "Hello! Welcome to Orpheus TTS Studio."

#     text = st.text_area(
#         label="text_area",
#         value=st.session_state.text_input,
#         height=220,
#         label_visibility="collapsed",
#         key="main_text",
#         help="Type your text here. Use [emotion] tags inline e.g. [happy] or [whisper]"
#     )

#     # ── Emotion tag inserter ──────────────────────────────────────────────────
#     st.markdown('<div class="section-label" style="margin-top:16px;">Insert Emotion Tag</div>', unsafe_allow_html=True)
#     st.markdown(
#         '<div class="info-box">Click an emotion to insert its tag into your text at the cursor position. '
#         'Tags affect the speech <b>after</b> they appear. You can mix multiple emotions in one script.</div>',
#         unsafe_allow_html=True
#     )

#     # Emotion buttons in a grid
#     cols = st.columns(5)
#     for i, emotion in enumerate(ALL_EMOTIONS):
#         color = EMOTION_COLORS.get(emotion, "#666")
#         with cols[i % 5]:
#             if st.button(f"[{emotion}]", key=f"emotion_{emotion}"):
#                 current = st.session_state.get("main_text", "")
#                 st.session_state.text_input = current + f" [{emotion}] "
#                 st.rerun()

#     # ── Example scripts ───────────────────────────────────────────────────────
#     st.markdown('<div class="section-label" style="margin-top:16px;">Quick Examples</div>', unsafe_allow_html=True)
#     examples = {
#         "😄 Happy story": "I just found out I got the job! [happy] I cannot believe it, this is amazing! [excited] We have to celebrate tonight!",
#         "😢 Emotional shift": "Everything was going so well. [sad] But then, it all fell apart. [crying] I don't know what to do anymore.",
#         "😮 Suspense": "Something doesn't feel right. [panicky] Wait... did you hear that? [whisper] Don't make a sound.",
#         "😠 Angry rant": "I told you this would happen! [angry] Nobody ever listens! [frustrated] Next time, just trust me!",
#         "🌙 Bedtime": "[sleepy] It's getting late... [slow] Time to rest now... [whisper] Goodnight everyone.",
#         "🎭 Comedy": "So I walked into the meeting. [normal] Completely forgot my pants. [surprise] Everyone just stared. [curious] Nobody said a word.",
#     }
#     ex_cols = st.columns(3)
#     ex_list = list(examples.items())
#     for i, (label, script) in enumerate(ex_list):
#         with ex_cols[i % 3]:
#             if st.button(label, key=f"ex_{i}"):
#                 st.session_state.text_input = script
#                 st.rerun()

# with right_col:
#     # ── Voice & settings ──────────────────────────────────────────────────────
#     st.markdown('<div class="section-label">Voice</div>', unsafe_allow_html=True)
#     selected_voice_label = st.selectbox(
#         "voice_select",
#         options=list(VOICES.values()),
#         label_visibility="collapsed"
#     )
#     selected_voice_key = [k for k, v in VOICES.items() if v == selected_voice_label][0]
#     lang = LANG_MAP.get(selected_voice_key[:3], "en-us")

#     st.markdown('<div class="section-label" style="margin-top:16px;">Speed</div>', unsafe_allow_html=True)
#     speed = st.slider("speed_slider", min_value=0.5, max_value=2.0, value=1.0, step=0.1, label_visibility="collapsed")

#     st.markdown(f"""
#     <div class="info-box" style="margin-top:16px;">
#         <b>Voice:</b> {selected_voice_label}<br>
#         <b>Language:</b> {lang}<br>
#         <b>Speed:</b> {speed}x<br>
#         <b>Model:</b> kokoro-v1.0.onnx
#     </div>
#     """, unsafe_allow_html=True)

#     # ── How emotions work ─────────────────────────────────────────────────────
#     st.markdown('<div class="section-label" style="margin-top:16px;">How Emotion Tags Work</div>', unsafe_allow_html=True)
#     st.markdown("""
#     <div class="info-box">
#         <b>Inline tags</b> shift the emotion mid-sentence:<br><br>
#         <code>[happy] Great news!</code> → spoken happily<br>
#         <code>[whisper] Keep this secret</code> → whispered<br>
#         <code>[angry] I said NO!</code> → spoken angrily<br><br>
#         Tags stay active until the next tag appears.
#     </div>
#     """, unsafe_allow_html=True)

#     st.markdown('<div class="section-label" style="margin-top:16px;">All Available Emotions</div>', unsafe_allow_html=True)
#     emotion_display = ""
#     for e in ALL_EMOTIONS:
#         color = EMOTION_COLORS.get(e, "#666")
#         emotion_display += f'<span style="display:inline-block; background:{color}22; border:1px solid {color}; border-radius:12px; padding:2px 10px; margin:3px; font-size:12px; font-family:Space Mono,monospace; color:{color};">{e}</span>'
#     st.markdown(emotion_display, unsafe_allow_html=True)

# # ── Generate button ───────────────────────────────────────────────────────────
# st.markdown("---")
# gen_col1, gen_col2, gen_col3 = st.columns([1, 2, 1])
# with gen_col2:
#     generate = st.button("🎙️ Generate Speech", key="generate_btn")

# # ── Generation logic ──────────────────────────────────────────────────────────
# if generate:
#     final_text = st.session_state.get("main_text", text)

#     if not final_text.strip():
#         st.error("Please enter some text first.")
#     else:
#         try:
#             from kokoro_onnx import Kokoro

#             # Check model files exist
#             onnx_path = "kokoro-v1.0.onnx"
#             voices_path = "voices-v1.0.bin"

#             if not os.path.exists(onnx_path) or not os.path.exists(voices_path):
#                 st.error(
#                     f"Model files not found in current directory.\n\n"
#                     f"Make sure these files are in the same folder as this script:\n"
#                     f"- kokoro-v1.0.onnx\n"
#                     f"- voices-v1.0.bin"
#                 )
#             else:
#                 with st.spinner("Generating audio..."):
#                     kokoro = Kokoro(onnx_path, voices_path)
#                     samples, sample_rate = kokoro.create(
#                         final_text,
#                         voice=selected_voice_key,
#                         speed=speed,
#                         lang=lang,
#                     )

#                     # Convert to bytes for playback
#                     buf = io.BytesIO()
#                     sf.write(buf, samples, sample_rate, format="WAV")
#                     buf.seek(0)

#                 st.success("✅ Audio generated!")
#                 st.audio(buf, format="audio/wav")

#                 # Download button
#                 dl_col1, dl_col2, dl_col3 = st.columns([1, 2, 1])
#                 with dl_col2:
#                     st.download_button(
#                         label="⬇️ Download WAV",
#                         data=buf.getvalue(),
#                         file_name="orpheus_output.wav",
#                         mime="audio/wav",
#                     )

#         except ImportError:
#             st.error("kokoro-onnx is not installed. Run: pip install kokoro-onnx soundfile")
#         except Exception as e:
#             st.error(f"Error during generation: {str(e)}")

# # ── Footer ────────────────────────────────────────────────────────────────────
# st.markdown("---")
# st.markdown(
#     '<p style="text-align:center; color:#333; font-size:12px; font-family:Space Mono,monospace;">'
#     'Powered by Kokoro ONNX · Orpheus TTS Studio · Run locally on Windows</p>',
#     unsafe_allow_html=True
# )

###############################################################################################

# import streamlit as st
# import streamlit.components.v1 as components
# import soundfile as sf
# import io
# import os

# # ── Page config ───────────────────────────────────────────────────────────────
# st.set_page_config(
#     page_title="Orpheus TTS Studio",
#     page_icon="🎙️",
#     layout="wide",
#     initial_sidebar_state="collapsed",
# )

# # ── Global CSS ────────────────────────────────────────────────────────────────
# st.markdown("""
# <style>
# @import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Cabinet+Grotesk:wght@400;500;700;800&display=swap');

# html, body, [class*="css"] {
#     font-family: 'Cabinet Grotesk', sans-serif !important;
#     background: #080810 !important;
#     color: #e8e4f0 !important;
# }
# .main .block-container {
#     padding: 2rem 2.5rem 4rem !important;
#     max-width: 1400px !important;
# }
# section[data-testid="stSidebar"] { display: none; }
# #MainMenu, footer, header { visibility: hidden; }

# .stSelectbox label { display: none !important; }
# .stSelectbox > div > div {
#     background: #12121e !important;
#     border: 1.5px solid #252535 !important;
#     border-radius: 10px !important;
#     color: #e8e4f0 !important;
#     font-family: 'Cabinet Grotesk', sans-serif !important;
#     font-size: 15px !important;
#     padding: 4px 8px !important;
# }
# [data-baseweb="select"] * { color: #e8e4f0 !important; background: #12121e !important; }
# [data-baseweb="popover"] { background: #12121e !important; border: 1px solid #252535 !important; }

# .stSlider label { display: none !important; }
# .stSlider [data-baseweb="slider"] div[role="slider"] {
#     background: #7c6af7 !important;
#     border-color: #7c6af7 !important;
# }

# /* Hide the sync textarea completely */
# .stTextArea { display: none !important; }

# .stButton > button {
#     background: #1a1a2e !important;
#     color: #a78bfa !important;
#     font-family: 'DM Mono', monospace !important;
#     font-weight: 500 !important;
#     font-size: 12px !important;
#     border: 1.5px solid #252545 !important;
#     border-radius: 8px !important;
#     padding: 6px 10px !important;
#     width: 100% !important;
#     transition: all 0.2s !important;
# }
# .stButton > button:hover {
#     border-color: #7c6af7 !important;
#     background: #1e1e38 !important;
#     transform: translateY(-1px) !important;
# }

# .gen-btn .stButton > button {
#     background: linear-gradient(135deg, #f97316, #fb923c) !important;
#     color: #fff !important;
#     font-family: 'Cabinet Grotesk', sans-serif !important;
#     font-size: 17px !important;
#     font-weight: 700 !important;
#     padding: 14px 32px !important;
#     border-radius: 14px !important;
#     border: none !important;
#     box-shadow: 0 4px 24px #f9731640 !important;
# }
# .gen-btn .stButton > button:hover {
#     box-shadow: 0 8px 32px #f9731660 !important;
#     transform: translateY(-2px) !important;
# }

# .stDownloadButton > button {
#     background: #12121e !important;
#     border: 1.5px solid #252535 !important;
#     color: #a78bfa !important;
#     font-weight: 600 !important;
#     border-radius: 10px !important;
# }

# hr { border-color: #1a1a2e !important; margin: 1.5rem 0 !important; }
# </style>
# """, unsafe_allow_html=True)

# # ── Data ──────────────────────────────────────────────────────────────────────
# ALL_EMOTIONS = [
#     ("happy",      "#f59e0b", "😊"),
#     ("excited",    "#fb923c", "🤩"),
#     ("surprise",   "#facc15", "😮"),
#     ("sad",        "#60a5fa", "😢"),
#     ("crying",     "#818cf8", "😭"),
#     ("angry",      "#f87171", "😠"),
#     ("shout",      "#ef4444", "📢"),
#     ("frustrated", "#f97316", "😤"),
#     ("whisper",    "#c084fc", "🤫"),
#     ("sleepy",     "#a78bfa", "😴"),
#     ("slow",       "#94a3b8", "🐢"),
#     ("panicky",    "#fb7185", "😱"),
#     ("fast",       "#fb923c", "⚡"),
#     ("disgust",    "#34d399", "🤢"),
#     ("curious",    "#2dd4bf", "🤔"),
#     ("deep",       "#38bdf8", "🔊"),
#     ("high",       "#e879f9", "🎵"),
#     ("normal",     "#64748b", "😐"),
#     ("longer",     "#475569", "⏳"),
# ]

# VOICES = {
#     "af_bella":   ("Bella",   "🇺🇸", "American Female"),
#     "af_sarah":   ("Sarah",   "🇺🇸", "American Female"),
#     "am_adam":    ("Adam",    "🇺🇸", "American Male"),
#     "am_michael": ("Michael", "🇺🇸", "American Male"),
#     "bf_emma":    ("Emma",    "🇬🇧", "British Female"),
#     "bm_george":  ("George",  "🇬🇧", "British Male"),
#     "hf_alpha":   ("Alpha",   "🇮🇳", "Hindi Female"),
#     "hf_beta":    ("Beta",    "🇮🇳", "Hindi Female"),
#     "hm_omega":   ("Omega",   "🇮🇳", "Hindi Male"),
#     "hm_psi":     ("Psi",     "🇮🇳", "Hindi Male"),
# }

# LANG_MAP = {
#     "af_": "en-us", "am_": "en-us",
#     "bf_": "en-gb", "bm_": "en-gb",
#     "hf_": "hi",    "hm_": "hi",
# }

# EXAMPLES = [
#     ("😄 Good News",   "I just found out I got the job! [happy] I cannot believe it, this is amazing! [excited] We have to celebrate tonight!"),
#     ("😢 Heartbreak",  "Everything was going so well. [sad] But then, it all fell apart. [crying] I don't know what to do anymore."),
#     ("😱 Suspense",    "Something doesn't feel right here. [panicky] Wait... did you hear that? [whisper] Don't make a sound."),
#     ("😠 Angry Rant",  "I told you this would happen! [angry] Nobody ever listens to me! [frustrated] Next time, just trust me!"),
#     ("🌙 Bedtime",     "[sleepy] It's getting late now... [slow] Time to rest everyone... [whisper] Goodnight."),
#     ("🎭 Comedy",      "So I walked into the meeting. [normal] Completely forgot my pants. [surprise] Everyone just stared. [curious] Nobody said a word."),
# ]

# # ── Session state ─────────────────────────────────────────────────────────────
# if "script_text" not in st.session_state:
#     st.session_state.script_text = "Hello! Welcome to Orpheus TTS Studio. [happy] Let's create something amazing today!"
# if "pending_tag" not in st.session_state:
#     st.session_state.pending_tag = None

# # ── Header ────────────────────────────────────────────────────────────────────
# st.markdown("""
# <div style="display:flex;align-items:center;gap:16px;margin-bottom:4px;">
#   <div style="width:48px;height:48px;background:linear-gradient(135deg,#7c6af7,#a78bfa);
#               border-radius:14px;display:flex;align-items:center;justify-content:center;
#               font-size:24px;box-shadow:0 4px 20px #7c6af750;flex-shrink:0;">🎙️</div>
#   <div>
#     <div style="font-size:30px;font-weight:800;letter-spacing:-0.5px;
#                 background:linear-gradient(135deg,#e8e4f0 30%,#a78bfa);
#                 -webkit-background-clip:text;-webkit-text-fill-color:transparent;line-height:1.1;">
#       Orpheus TTS Studio
#     </div>
#     <div style="font-size:12px;color:#3a3a5a;font-family:'DM Mono',monospace;margin-top:2px;letter-spacing:1px;">
#       KOKORO ONNX &nbsp;·&nbsp; EMOTION-AWARE SPEECH SYNTHESIS
#     </div>
#   </div>
# </div>
# <hr/>
# """, unsafe_allow_html=True)

# # ── Layout ────────────────────────────────────────────────────────────────────
# left_col, right_col = st.columns([5, 3], gap="large")

# # ╔══════════════════════════════════════════════╗
# # ║  LEFT  —  Script Editor + Emotions           ║
# # ╚══════════════════════════════════════════════╝
# with left_col:

#     # Build emotion color map for JS
#     emotion_color_js = "{" + ",".join([f'"{e[0]}":"{e[1]}"' for e in ALL_EMOTIONS]) + "}"
#     pending_js = f'"{st.session_state.pending_tag}"' if st.session_state.pending_tag else "null"
#     init_text_js = repr(st.session_state.script_text)

#     editor_html = f"""<!DOCTYPE html>
# <html><head><meta charset="utf-8">
# <link href="https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&display=swap" rel="stylesheet">
# <style>
# * {{ box-sizing:border-box; margin:0; padding:0; }}
# body {{ background:transparent; }}

# .wrap {{
#   border: 2px solid #1e1e32;
#   border-radius: 16px;
#   overflow: hidden;
#   background: #0b0b18;
#   transition: border-color .25s, box-shadow .25s;
#   font-family: 'DM Mono', monospace;
# }}
# .wrap.focused {{
#   border-color: #7c6af7;
#   box-shadow: 0 0 0 4px #7c6af718, 0 8px 32px #00000060;
# }}

# /* ── Top bar ── */
# .topbar {{
#   background: #0e0e1e;
#   border-bottom: 1px solid #1a1a2c;
#   padding: 9px 14px;
#   display: flex;
#   align-items: center;
#   gap: 8px;
# }}
# .dot {{ width:10px;height:10px;border-radius:50%; }}
# .bar-title {{
#   flex:1; font-size:11px; letter-spacing:2px; text-transform:uppercase;
#   color:#2e2e50; margin-left:4px;
# }}
# .bar-right {{ display:flex; gap:14px; align-items:center; }}
# .bar-stat {{ font-size:11px; color:#2e2e50; }}
# .bar-stat b {{ color:#5a5a90; }}

# /* ── Line numbers + editor ── */
# .editor-body {{
#   display: flex;
#   min-height: 240px;
#   max-height: 340px;
# }}
# .linenos {{
#   background: #080814;
#   border-right: 1px solid #141424;
#   padding: 16px 10px 16px 12px;
#   min-width: 40px;
#   text-align: right;
#   font-size: 12px;
#   line-height: 1.75;
#   color: #252540;
#   user-select: none;
#   overflow: hidden;
# }}
# #editor {{
#   flex: 1;
#   min-height: 240px;
#   max-height: 340px;
#   overflow-y: auto;
#   padding: 16px 18px;
#   font-family: 'DM Mono', monospace;
#   font-size: 14px;
#   line-height: 1.75;
#   color: #c8c4e8;
#   outline: none;
#   white-space: pre-wrap;
#   word-break: break-word;
#   background: #0b0b18;
#   caret-color: #a78bfa;
# }}
# #editor:empty::before {{
#   content: 'Start typing your script here… Use emotion buttons below to insert tags inline.';
#   color: #1e1e38;
#   pointer-events: none;
# }}

# /* Emotion tag chips */
# .etag {{
#   display: inline;
#   border-radius: 5px;
#   padding: 1px 3px;
#   font-size: 12px;
#   font-weight: 500;
#   cursor: default;
#   user-select: none;
#   margin: 0 1px;
#   vertical-align: baseline;
# }}

# /* Status bar */
# .statusbar {{
#   background: #08080f;
#   border-top: 1px solid #141424;
#   padding: 5px 16px;
#   display: flex;
#   gap: 18px;
#   font-size: 11px;
#   color: #252540;
#   font-family: 'DM Mono', monospace;
# }}
# .s-item {{ display:flex; align-items:center; gap:5px; }}
# .s-dot {{ width:5px;height:5px;border-radius:50%;background:#7c6af7; }}
# #cursor-pos {{ color:#3a3a60; }}

# /* Scrollbar */
# #editor::-webkit-scrollbar {{ width:5px; }}
# #editor::-webkit-scrollbar-track {{ background:#08080f; }}
# #editor::-webkit-scrollbar-thumb {{ background:#1e1e38; border-radius:3px; }}
# </style>
# </head><body>

# <div class="wrap" id="wrap">
#   <div class="topbar">
#     <div class="dot" style="background:#ff5f57"></div>
#     <div class="dot" style="background:#febc2e"></div>
#     <div class="dot" style="background:#28c840"></div>
#     <span class="bar-title">Script Editor</span>
#     <div class="bar-right">
#       <span class="bar-stat"><b id="wc">0</b> words</span>
#       <span class="bar-stat"><b id="cc">0</b> chars</span>
#       <span class="bar-stat"><b id="tc">0</b> tags</span>
#     </div>
#   </div>

#   <div class="editor-body">
#     <div class="linenos" id="linenos">1</div>
#     <div id="editor" contenteditable="true" spellcheck="true"></div>
#   </div>

#   <div class="statusbar">
#     <div class="s-item"><div class="s-dot"></div><span style="color:#3a3a60">ready</span></div>
#     <div class="s-item" id="cursor-pos">Ln 1, Col 1</div>
#     <div class="s-item" id="mode-indicator" style="color:#3a3a60;">— INSERT —</div>
#   </div>
# </div>

# <textarea id="sync" style="display:none;"></textarea>

# <script>
# const COLORS = {emotion_color_js};
# const editor  = document.getElementById('editor');
# const sync    = document.getElementById('sync');
# const linenos = document.getElementById('linenos');
# const wrap    = document.getElementById('wrap');

# // ── Render plain text → highlighted DOM ──────────────────────────────────────
# function render(text) {{
#   const parts = text.split(/(\[[a-z]+\])/gi);
#   editor.innerHTML = '';
#   parts.forEach(part => {{
#     const m = part.match(/^\[([a-z]+)\]$/i);
#     if (m) {{
#       const tag = m[1].toLowerCase();
#       const col = COLORS[tag] || '#94a3b8';
#       const sp  = document.createElement('span');
#       sp.className = 'etag';
#       sp.contentEditable = 'false';
#       sp.dataset.tag = tag;
#       sp.style.cssText = `background:${{col}}20;color:${{col}};border:1px solid ${{col}}50;`;
#       sp.textContent = '[' + tag + ']';
#       editor.appendChild(sp);
#     }} else if (part) {{
#       editor.appendChild(document.createTextNode(part));
#     }}
#   }});
#   updateLineNos();
# }}

# // ── Extract plain text ────────────────────────────────────────────────────────
# function extract() {{
#   let t = '';
#   editor.childNodes.forEach(n => {{
#     if (n.nodeType === 3) t += n.textContent;
#     else if (n.classList?.contains('etag')) t += '[' + n.dataset.tag + ']';
#     else t += (n.innerText || n.textContent || '');
#   }});
#   return t;
# }}

# // ── Update stats ──────────────────────────────────────────────────────────────
# function updateStats() {{
#   const t = extract();
#   const words = t.trim() ? t.trim().split(/\\s+/).length : 0;
#   const tags  = (t.match(/\\[[a-z]+\\]/gi) || []).length;
#   document.getElementById('wc').textContent = words;
#   document.getElementById('cc').textContent = t.length;
#   document.getElementById('tc').textContent = tags;
#   sync.value = t;
#   sync.dispatchEvent(new Event('change'));
#   window.parent.postMessage({{type:'tts_update', text:t}}, '*');
# }}

# // ── Line numbers ──────────────────────────────────────────────────────────────
# function updateLineNos() {{
#   const text = extract();
#   const lines = text.split('\\n').length || 1;
#   linenos.innerHTML = Array.from({{length: lines}}, (_, i) => i+1).join('<br>');
# }}

# // ── Cursor position ───────────────────────────────────────────────────────────
# function updateCursor() {{
#   try {{
#     const sel = window.getSelection();
#     if (!sel.rangeCount) return;
#     const r = sel.getRangeAt(0).cloneRange();
#     r.selectNodeContents(editor);
#     r.setEnd(sel.getRangeAt(0).endContainer, sel.getRangeAt(0).endOffset);
#     const lines = r.toString().split('\\n');
#     document.getElementById('cursor-pos').textContent =
#       'Ln ' + lines.length + ', Col ' + (lines[lines.length-1].length+1);
#   }} catch(e) {{}}
# }}

# // ── Insert tag at cursor ──────────────────────────────────────────────────────
# function insertTag(tag) {{
#   editor.focus();
#   const col = COLORS[tag] || '#94a3b8';
#   const sp  = document.createElement('span');
#   sp.className = 'etag';
#   sp.contentEditable = 'false';
#   sp.dataset.tag = tag;
#   sp.style.cssText = `background:${{col}}20;color:${{col}};border:1px solid ${{col}}50;`;
#   sp.textContent = '[' + tag + ']';

#   const sel = window.getSelection();
#   if (sel.rangeCount) {{
#     const range = sel.getRangeAt(0);
#     range.deleteContents();
#     const before = document.createTextNode(' ');
#     const after  = document.createTextNode(' ');
#     range.insertNode(after);
#     range.insertNode(sp);
#     range.insertNode(before);
#     const nr = document.createRange();
#     nr.setStartAfter(after); nr.collapse(true);
#     sel.removeAllRanges(); sel.addRange(nr);
#   }} else {{
#     editor.appendChild(document.createTextNode(' '));
#     editor.appendChild(sp);
#     editor.appendChild(document.createTextNode(' '));
#   }}
#   updateStats(); updateLineNos();
# }}

# // ── Events ────────────────────────────────────────────────────────────────────
# editor.addEventListener('input', () => {{ updateStats(); updateLineNos(); }});
# editor.addEventListener('keyup', updateCursor);
# editor.addEventListener('mouseup', updateCursor);
# editor.addEventListener('focus', () => {{ wrap.classList.add('focused'); }});
# editor.addEventListener('blur',  () => {{ wrap.classList.remove('focused'); updateStats(); }});

# // Backspace on tag span
# editor.addEventListener('keydown', e => {{
#   if (e.key === 'Backspace') {{
#     const sel = window.getSelection();
#     if (!sel.rangeCount) return;
#     const range = sel.getRangeAt(0);
#     if (range.collapsed) {{
#       let prev = range.startContainer.previousSibling;
#       if (!prev && range.startOffset === 0)
#         prev = range.startContainer.parentNode?.previousSibling;
#       if (prev?.classList?.contains('etag')) {{
#         e.preventDefault();
#         prev.remove();
#         updateStats(); updateLineNos();
#       }}
#     }}
#   }}
# }});

# // ── Messages from Streamlit ───────────────────────────────────────────────────
# window.addEventListener('message', e => {{
#   if (!e.data) return;
#   if (e.data.type === 'insert_tag') insertTag(e.data.tag);
#   if (e.data.type === 'set_text')   {{ render(e.data.text); updateStats(); }}
# }});

# // ── Init ──────────────────────────────────────────────────────────────────────
# render({init_text_js});
# updateStats();

# // Pending tag from button click
# const PENDING = {pending_js};
# if (PENDING) setTimeout(() => insertTag(PENDING), 80);
# </script>
# </body></html>
# """

#     st.markdown('<p style="font-size:11px;font-family:DM Mono,monospace;letter-spacing:2px;text-transform:uppercase;color:#2e2e50;margin-bottom:8px;">✏️ Script Editor</p>', unsafe_allow_html=True)
#     components.html(editor_html, height=380, scrolling=False)

#     # Hidden sync textarea (invisible via CSS)
#     synced = st.text_area("__sync__", value=st.session_state.script_text, key="sync_area")
#     if synced:
#         st.session_state.script_text = synced

#     # ── Emotion palette ───────────────────────────────────────────────────────
#     st.markdown('<p style="font-size:11px;font-family:DM Mono,monospace;letter-spacing:2px;text-transform:uppercase;color:#2e2e50;margin:18px 0 6px;">🎭 Emotion Tags — click to insert</p>', unsafe_allow_html=True)

#     rows = [ALL_EMOTIONS[i:i+5] for i in range(0, len(ALL_EMOTIONS), 5)]
#     for row in rows:
#         cols = st.columns(len(row))
#         for j, (emo, color, icon) in enumerate(row):
#             with cols[j]:
#                 # Per-emotion color override via targeted CSS
#                 st.markdown(f"""<style>
#                 div[data-testid="column"]:nth-child({j+1}) .stButton > button {{
#                     background: {color}14 !important;
#                     border-color: {color}40 !important;
#                     color: {color} !important;
#                 }}
#                 div[data-testid="column"]:nth-child({j+1}) .stButton > button:hover {{
#                     background: {color}28 !important;
#                     border-color: {color} !important;
#                     box-shadow: 0 4px 12px {color}30 !important;
#                 }}
#                 </style>""", unsafe_allow_html=True)
#                 if st.button(f"{icon} {emo}", key=f"emo_{emo}"):
#                     st.session_state.script_text += f" [{emo}] "
#                     st.session_state.pending_tag = emo
#                     st.rerun()

#     st.session_state.pending_tag = None  # clear after render

#     # ── Quick examples ────────────────────────────────────────────────────────
#     st.markdown('<p style="font-size:11px;font-family:DM Mono,monospace;letter-spacing:2px;text-transform:uppercase;color:#2e2e50;margin:18px 0 6px;">⚡ Quick Examples</p>', unsafe_allow_html=True)
#     ex_cols = st.columns(3)
#     for i, (label, script) in enumerate(EXAMPLES):
#         with ex_cols[i % 3]:
#             if st.button(label, key=f"ex_{i}"):
#                 st.session_state.script_text = script
#                 st.rerun()

# # ╔══════════════════════════════════════════════╗
# # ║  RIGHT  —  Settings                          ║
# # ╚══════════════════════════════════════════════╝
# with right_col:

#     # ── Voice card ────────────────────────────────────────────────────────────
#     st.markdown("""
#     <div style="background:#0d0d1a;border:1.5px solid #1a1a2e;border-radius:16px;padding:20px 22px;margin-bottom:16px;">
#     <p style="font-size:11px;font-family:DM Mono,monospace;letter-spacing:2px;text-transform:uppercase;color:#2e2e50;margin-bottom:12px;">🎤 Voice</p>
#     """, unsafe_allow_html=True)

#     voice_keys  = list(VOICES.keys())
#     voice_labels = [f"{v[1]} {v[0]} — {v[2]}" for v in VOICES.values()]
#     sel_idx = st.selectbox("Voice", range(len(voice_labels)), format_func=lambda i: voice_labels[i], label_visibility="collapsed")
#     sel_key  = voice_keys[sel_idx]
#     vinfo    = VOICES[sel_key]
#     lang     = LANG_MAP.get(sel_key[:3], "en-us")

#     st.markdown(f"""
#     <div style="background:#08080f;border-radius:10px;padding:12px 14px;margin-top:12px;
#                 border:1px solid #141424;font-family:DM Mono,monospace;">
#       <div style="color:#2a2a48;font-size:11px;margin-bottom:5px;">SELECTED</div>
#       <div style="color:#a78bfa;font-size:16px;font-weight:500;">{vinfo[1]} {vinfo[0]}</div>
#       <div style="color:#303060;font-size:12px;margin-top:2px;">{vinfo[2]} &nbsp;·&nbsp; {lang}</div>
#     </div>
#     """, unsafe_allow_html=True)
#     st.markdown("</div>", unsafe_allow_html=True)

#     # ── Speed card ────────────────────────────────────────────────────────────
#     st.markdown("""
#     <div style="background:#0d0d1a;border:1.5px solid #1a1a2e;border-radius:16px;padding:20px 22px;margin-bottom:16px;">
#     <p style="font-size:11px;font-family:DM Mono,monospace;letter-spacing:2px;text-transform:uppercase;color:#2e2e50;margin-bottom:12px;">⏱ Speed</p>
#     """, unsafe_allow_html=True)
#     speed = st.slider("Speed", 0.5, 2.0, 1.0, 0.05, label_visibility="collapsed")
#     spd_pct   = int((speed - 0.5) / 1.5 * 100)
#     spd_color = "#60a5fa" if speed < 0.85 else "#34d399" if speed <= 1.2 else "#f59e0b" if speed <= 1.6 else "#f87171"
#     st.markdown(f"""
#     <div style="background:#08080f;border-radius:10px;padding:12px 14px;border:1px solid #141424;">
#       <div style="display:flex;justify-content:space-between;margin-bottom:7px;">
#         <span style="font-size:11px;color:#252540;font-family:DM Mono,monospace;">slow</span>
#         <span style="font-size:14px;color:{spd_color};font-weight:600;font-family:DM Mono,monospace;">{speed:.2f}×</span>
#         <span style="font-size:11px;color:#252540;font-family:DM Mono,monospace;">fast</span>
#       </div>
#       <div style="background:#111120;border-radius:4px;height:5px;overflow:hidden;">
#         <div style="background:linear-gradient(90deg,#7c6af7,{spd_color});width:{spd_pct}%;height:100%;border-radius:4px;transition:width .3s;"></div>
#       </div>
#     </div>
#     """, unsafe_allow_html=True)
#     st.markdown("</div>", unsafe_allow_html=True)

#     # ── Script stats card ─────────────────────────────────────────────────────
#     txt = st.session_state.script_text
#     wc  = len(txt.split()) if txt.strip() else 0
#     cc  = len(txt)
#     tc  = txt.count("[")
#     prev = (txt[:100] + "…") if len(txt) > 100 else txt

#     st.markdown(f"""
#     <div style="background:#0d0d1a;border:1.5px solid #1a1a2e;border-radius:16px;padding:20px 22px;margin-bottom:16px;">
#       <p style="font-size:11px;font-family:DM Mono,monospace;letter-spacing:2px;text-transform:uppercase;color:#2e2e50;margin-bottom:10px;">📊 Script Stats</p>
#       <div style="display:flex;gap:0;border-radius:10px;overflow:hidden;border:1px solid #141424;">
#         <div style="flex:1;text-align:center;padding:14px 8px;background:#08080f;border-right:1px solid #141424;">
#           <div style="color:#7c6af7;font-size:22px;font-weight:700;font-family:DM Mono,monospace;">{wc}</div>
#           <div style="color:#252545;font-size:10px;font-family:DM Mono,monospace;margin-top:2px;">WORDS</div>
#         </div>
#         <div style="flex:1;text-align:center;padding:14px 8px;background:#08080f;border-right:1px solid #141424;">
#           <div style="color:#7c6af7;font-size:22px;font-weight:700;font-family:DM Mono,monospace;">{cc}</div>
#           <div style="color:#252545;font-size:10px;font-family:DM Mono,monospace;margin-top:2px;">CHARS</div>
#         </div>
#         <div style="flex:1;text-align:center;padding:14px 8px;background:#08080f;">
#           <div style="color:#f59e0b;font-size:22px;font-weight:700;font-family:DM Mono,monospace;">{tc}</div>
#           <div style="color:#252545;font-size:10px;font-family:DM Mono,monospace;margin-top:2px;">TAGS</div>
#         </div>
#       </div>
#       <div style="background:#08080f;border-radius:8px;padding:10px 12px;margin-top:10px;
#                   border:1px solid #141424;font-size:12px;color:#303060;font-family:DM Mono,monospace;
#                   line-height:1.6;min-height:36px;">
#         {prev if prev.strip() else '<span style="color:#1a1a30">No text yet…</span>'}
#       </div>
#     </div>
#     """, unsafe_allow_html=True)

#     # ── Emotion reference ─────────────────────────────────────────────────────
#     st.markdown("""
#     <div style="background:#0d0d1a;border:1.5px solid #1a1a2e;border-radius:16px;padding:20px 22px;">
#     <p style="font-size:11px;font-family:DM Mono,monospace;letter-spacing:2px;text-transform:uppercase;color:#2e2e50;margin-bottom:12px;">📖 Tag Reference</p>
#     """, unsafe_allow_html=True)

#     groups = [
#         ("😊 Positive",  ["happy","excited","surprise"]),
#         ("😢 Sad",       ["sad","crying"]),
#         ("😠 Intense",   ["angry","shout","frustrated","panicky"]),
#         ("🤫 Soft",      ["whisper","sleepy","slow"]),
#         ("🎵 Pitch",     ["deep","high","fast"]),
#         ("😐 Neutral",   ["normal","longer","disgust","curious"]),
#     ]
#     emo_map = {e[0]: (e[1], e[2]) for e in ALL_EMOTIONS}
#     for glabel, names in groups:
#         chips = "".join([
#             f'<span style="background:{emo_map[n][0]}16;border:1px solid {emo_map[n][0]}45;'
#             f'color:{emo_map[n][0]};border-radius:6px;padding:2px 9px;font-size:11px;'
#             f'font-family:DM Mono,monospace;margin:2px;display:inline-block;">'
#             f'{emo_map[n][1]} {n}</span>'
#             for n in names if n in emo_map
#         ])
#         st.markdown(f"""
#         <div style="margin-bottom:10px;">
#           <div style="font-size:11px;color:#252545;margin-bottom:5px;">{glabel}</div>
#           {chips}
#         </div>""", unsafe_allow_html=True)

#     st.markdown("</div>", unsafe_allow_html=True)

# # ── Generate ──────────────────────────────────────────────────────────────────
# st.markdown("<hr/>", unsafe_allow_html=True)
# g1, g2, g3 = st.columns([1, 2, 1])
# with g2:
#     st.markdown('<div class="gen-btn">', unsafe_allow_html=True)
#     generate = st.button("🎙️  Generate Speech", key="gen_btn")
#     st.markdown('</div>', unsafe_allow_html=True)

# if generate:
#     final = st.session_state.script_text.strip()
#     if not final:
#         st.error("⚠️ Please write some text in the editor first.")
#     else:
#         try:
#             from kokoro_onnx import Kokoro
#             onnx_p   = "kokoro-v1.0.onnx"
#             voices_p = "voices-v1.0.bin"

#             if not os.path.exists(onnx_p) or not os.path.exists(voices_p):
#                 st.error("**Model files not found.** Place `kokoro-v1.0.onnx` and `voices-v1.0.bin` in the same folder.")
#             else:
#                 r1, r2, r3 = st.columns([1, 2, 1])
#                 with r2:
#                     with st.spinner("🎵 Synthesising audio…"):
#                         kokoro = Kokoro(onnx_p, voices_p)
#                         samples, sr = kokoro.create(final, voice=sel_key, speed=speed, lang=lang)
#                         buf = io.BytesIO()
#                         sf.write(buf, samples, sr, format="WAV")
#                         buf.seek(0)

#                     st.markdown("""
#                     <div style="background:#0a1a12;border:1.5px solid #22c55e44;border-radius:14px;
#                                 padding:16px 18px;margin-bottom:10px;">
#                       <div style="color:#22c55e;font-size:13px;font-weight:600;margin-bottom:10px;">
#                         ✅ Audio generated successfully
#                       </div>
#                     """, unsafe_allow_html=True)
#                     st.audio(buf, format="audio/wav")
#                     st.markdown("</div>", unsafe_allow_html=True)
#                     st.download_button("⬇️  Download WAV", buf.getvalue(), "orpheus_output.wav", "audio/wav")

#         except ImportError:
#             st.error("**kokoro-onnx not installed.** Run: `pip install kokoro-onnx soundfile`")
#         except Exception as e:
#             st.error(f"**Error:** {e}")

# # ── Footer ────────────────────────────────────────────────────────────────────
# st.markdown("""
# <div style="text-align:center;margin-top:3rem;padding-top:1.5rem;border-top:1px solid #0d0d1a;">
#   <span style="font-size:11px;color:#181828;font-family:DM Mono,monospace;letter-spacing:1px;">
#     ORPHEUS TTS STUDIO &nbsp;·&nbsp; KOKORO ONNX &nbsp;·&nbsp; LOCAL WINDOWS BUILD
#   </span>
# </div>
# """, unsafe_allow_html=True)

import streamlit as st
import streamlit.components.v1 as components
import soundfile as sf
import io
import os
import urllib.request

def download_file(url, filename):
    if not os.path.exists(filename):
        urllib.request.urlretrieve(url, filename)

download_file(
    "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/kokoro-v1.0.onnx",
    "kokoro-v1.0.onnx"
)

download_file(
    "https://github.com/thewh1teagle/kokoro-onnx/releases/download/model-files-v1.0/voices-v1.0.bin",
    "voices-v1.0.bin"
)

st.set_page_config(page_title="Orpheus TTS Studio", page_icon="🎙️", layout="wide", initial_sidebar_state="collapsed")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  GLOBAL CSS  —  charcoal/white high-contrast theme
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&family=JetBrains+Mono:wght@400;500&display=swap');

/* ── Base ── */
html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
    background: #111318 !important;
    color: #F0F0F5 !important;
}
.main .block-container {
    padding: 1.8rem 2.2rem 3rem !important;
    max-width: 1380px !important;
}
section[data-testid="stSidebar"], #MainMenu, footer, header { display:none !important; visibility:hidden !important; }

/* ── Hide sync textarea ── */
div[data-testid="stVerticalBlock"] > div:has(> div[data-testid="stTextArea"]) { display:none !important; }

/* ── Selectbox ── */
.stSelectbox > div > div {
    background: #1E2028 !important;
    border: 1.5px solid #2E3140 !important;
    border-radius: 10px !important;
    color: #F0F0F5 !important;
    font-size: 14px !important;
    min-height: 44px !important;
    padding: 2px 10px !important;
}
.stSelectbox > div > div:focus-within {
    border-color: #6C63FF !important;
    box-shadow: 0 0 0 3px rgba(108,99,255,0.15) !important;
}
[data-baseweb="select"] svg { color: #888 !important; }
[data-baseweb="select"] [data-testid="stMarkdownContainer"] p { color: #F0F0F5 !important; }
div[role="listbox"] { background: #1E2028 !important; border: 1px solid #2E3140 !important; border-radius: 10px !important; }
div[role="option"] { color: #F0F0F5 !important; padding: 10px 14px !important; }
div[role="option"]:hover { background: #2A2D3A !important; }
div[role="option"][aria-selected="true"] { background: #6C63FF22 !important; color: #A09BFF !important; }

/* ── Slider ── */
.stSlider > label { color: #9A9AB0 !important; font-size: 13px !important; font-weight: 500 !important; }
div[data-baseweb="slider"] [role="slider"] {
    background: #6C63FF !important;
    border-color: #6C63FF !important;
    box-shadow: 0 0 0 4px rgba(108,99,255,0.2) !important;
}
div[data-baseweb="slider"] > div > div > div:first-child {
    background: linear-gradient(90deg, #6C63FF, #A09BFF) !important;
}

/* ── All buttons base ── */
.stButton > button {
    background: #1E2028 !important;
    color: #C8C8D8 !important;
    border: 1.5px solid #2E3140 !important;
    border-radius: 9px !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 13px !important;
    font-weight: 500 !important;
    padding: 8px 12px !important;
    width: 100% !important;
    transition: all .18s ease !important;
    cursor: pointer !important;
}
.stButton > button:hover {
    background: #252830 !important;
    border-color: #6C63FF !important;
    color: #F0F0F5 !important;
    transform: translateY(-1px) !important;
}
.stButton > button:active { transform: translateY(0) !important; }

/* ── Download button ── */
.stDownloadButton > button {
    background: #1E2028 !important;
    border: 1.5px solid #2E3140 !important;
    color: #A09BFF !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    padding: 10px !important;
    width: 100% !important;
}
.stDownloadButton > button:hover {
    border-color: #6C63FF !important;
    background: #252830 !important;
}

/* ── Audio player ── */
.stAudio { background: #1E2028 !important; border-radius: 12px !important; padding: 12px !important; }
audio { width: 100%; border-radius: 8px; }

/* ── Alerts ── */
.stSuccess > div { background: #0F2A1A !important; border: 1px solid #22863a !important; border-radius:10px !important; color:#4ade80 !important; }
.stError > div   { background: #2A0F0F !important; border: 1px solid #7f1d1d !important; border-radius:10px !important; color:#f87171 !important; }

hr { border: none !important; border-top: 1px solid #22252F !important; margin: 1.4rem 0 !important; }
</style>
""", unsafe_allow_html=True)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  DATA
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
ALL_EMOTIONS = [
    ("happy",      "#F59E0B", "😊"),
    ("excited",    "#F97316", "🤩"),
    ("surprise",   "#EAB308", "😮"),
    ("sad",        "#60A5FA", "😢"),
    ("crying",     "#818CF8", "😭"),
    ("angry",      "#F87171", "😠"),
    ("shout",      "#EF4444", "📢"),
    ("frustrated", "#FB923C", "😤"),
    ("whisper",    "#C084FC", "🤫"),
    ("sleepy",     "#A78BFA", "😴"),
    ("slow",       "#94A3B8", "🐢"),
    ("panicky",    "#FB7185", "😱"),
    ("fast",       "#FB923C", "⚡"),
    ("disgust",    "#34D399", "🤢"),
    ("curious",    "#2DD4BF", "🤔"),
    ("deep",       "#38BDF8", "🔊"),
    ("high",       "#E879F9", "🎵"),
    ("normal",     "#94A3B8", "😐"),
    ("longer",     "#64748B", "⏳"),
]

VOICES = [
    ("af_bella",   "Bella",   "American Female", "🇺🇸", "en-us"),
    ("af_sarah",   "Sarah",   "American Female", "🇺🇸", "en-us"),
    ("am_adam",    "Adam",    "American Male",   "🇺🇸", "en-us"),
    ("am_michael", "Michael", "American Male",   "🇺🇸", "en-us"),
    ("bf_emma",    "Emma",    "British Female",  "🇬🇧", "en-gb"),
    ("bm_george",  "George",  "British Male",    "🇬🇧", "en-gb"),
    ("hf_alpha",   "Alpha",   "Hindi Female",    "🇮🇳", "hi"),
    ("hf_beta",    "Beta",    "Hindi Female",    "🇮🇳", "hi"),
    ("hm_omega",   "Omega",   "Hindi Male",      "🇮🇳", "hi"),
    ("hm_psi",     "Psi",     "Hindi Male",      "🇮🇳", "hi"),
]

EXAMPLES = [
    ("😄 Good News",  "I just found out I got the job! [happy] I cannot believe it, this is amazing! [excited] We have to celebrate tonight!"),
    ("😢 Heartbreak", "Everything was going so well. [sad] But then, it all fell apart. [crying] I don't know what to do anymore."),
    ("😱 Suspense",   "Something doesn't feel right. [panicky] Wait... did you hear that? [whisper] Don't make a sound."),
    ("😠 Rant",       "I told you this would happen! [angry] Nobody listens! [frustrated] Next time, just trust me!"),
    ("🌙 Bedtime",    "[sleepy] It's getting late... [slow] Time to rest now... [whisper] Goodnight everyone."),
    ("🎭 Comedy",     "So I walked into the meeting. [normal] Completely forgot my pants. [surprise] Everyone stared. [curious] Nobody said a word."),
]

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  SESSION STATE
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
if "script" not in st.session_state:
    st.session_state.script = "[happy] Hello! Welcome to Orpheus TTS Studio. Let's create something amazing."
if "pending_tag" not in st.session_state:
    st.session_state.pending_tag = None

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  HEADER
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.markdown("""
<div style="display:flex;align-items:center;gap:14px;padding-bottom:18px;border-bottom:1px solid #22252F;margin-bottom:22px;">
  <div style="width:46px;height:46px;background:linear-gradient(135deg,#6C63FF,#A09BFF);
              border-radius:12px;display:flex;align-items:center;justify-content:center;
              font-size:22px;flex-shrink:0;box-shadow:0 4px 16px rgba(108,99,255,0.35);">🎙️</div>
  <div>
    <div style="font-size:24px;font-weight:700;color:#F0F0F5;letter-spacing:-0.3px;line-height:1.2;">Orpheus TTS Studio</div>
    <div style="font-size:12px;color:#5A5A70;font-family:'JetBrains Mono',monospace;margin-top:1px;letter-spacing:0.5px;">
      KOKORO ONNX &nbsp;·&nbsp; EMOTION-AWARE SPEECH SYNTHESIS
    </div>
  </div>
</div>
""", unsafe_allow_html=True)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  LAYOUT
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
left, right = st.columns([3, 2], gap="large")

# ╔══════════════════════════════════════╗
# ║  LEFT — Editor + Emotions            ║
# ╚══════════════════════════════════════╝
with left:

    # ── Rich editor ──────────────────────────────────────────────────────────
    emo_color_js = "{" + ",".join([f'"{e[0]}":"{e[1]}"' for e in ALL_EMOTIONS]) + "}"
    pending_js   = f'"{st.session_state.pending_tag}"' if st.session_state.pending_tag else "null"

    EDITOR_HTML = f"""<!DOCTYPE html><html><head><meta charset="utf-8">
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
*{{box-sizing:border-box;margin:0;padding:0;}}
body{{background:transparent;font-family:'JetBrains Mono',monospace;}}

.shell{{
  border:1.5px solid #2E3140;
  border-radius:12px;
  overflow:hidden;
  background:#161820;
  transition:border-color .2s,box-shadow .2s;
}}
.shell.active{{
  border-color:#6C63FF;
  box-shadow:0 0 0 3px rgba(108,99,255,.12),0 8px 30px rgba(0,0,0,.4);
}}

/* toolbar */
.tbar{{
  background:#1A1D26;
  border-bottom:1px solid #22252F;
  padding:9px 14px;
  display:flex;align-items:center;gap:8px;
}}
.tbar-dot{{width:11px;height:11px;border-radius:50%;}}
.tbar-title{{
  flex:1;font-size:11px;letter-spacing:1.8px;text-transform:uppercase;
  color:#40405A;margin-left:6px;
}}
.tbar-stats{{display:flex;gap:16px;}}
.stat{{font-size:11px;color:#40405A;}}
.stat b{{color:#6C63FF;}}

/* editor area */
.ebody{{display:flex;}}
.lnums{{
  background:#12141C;
  border-right:1px solid #1E2028;
  padding:14px 10px 14px 12px;
  min-width:38px;text-align:right;
  font-size:12px;line-height:1.8;
  color:#30304A;user-select:none;
  overflow:hidden;
}}
#ed{{
  flex:1;
  padding:14px 16px;
  min-height:230px;max-height:320px;
  overflow-y:auto;
  font-family:'JetBrains Mono',monospace;
  font-size:13.5px;line-height:1.8;
  color:#E0E0EE;
  outline:none;
  white-space:pre-wrap;word-break:break-word;
  background:#161820;
  caret-color:#A09BFF;
}}
#ed:empty::before{{
  content:'Type your script here… click emotion buttons below to insert tags inline.';
  color:#2A2A40;pointer-events:none;
}}
.etag{{
  display:inline;
  border-radius:5px;
  padding:1px 4px;
  font-size:12px;font-weight:500;
  cursor:default;user-select:none;
  margin:0 1px;
}}

/* status bar */
.sbar{{
  background:#12141C;
  border-top:1px solid #1E2028;
  padding:5px 14px;
  display:flex;gap:16px;
  font-size:11px;color:#30304A;
}}
.s-ready{{color:#6C63FF;}}
#cur{{color:#3A3A58;}}

#ed::-webkit-scrollbar{{width:4px;}}
#ed::-webkit-scrollbar-track{{background:#12141C;}}
#ed::-webkit-scrollbar-thumb{{background:#2A2D3A;border-radius:3px;}}
</style></head><body>

<div class="shell" id="shell">
  <div class="tbar">
    <div class="tbar-dot" style="background:#FF5F57"></div>
    <div class="tbar-dot" style="background:#FEBC2E"></div>
    <div class="tbar-dot" style="background:#28C840"></div>
    <span class="tbar-title">Script Editor</span>
    <div class="tbar-stats">
      <span class="stat"><b id="wc">0</b> words</span>
      <span class="stat"><b id="cc">0</b> chars</span>
      <span class="stat"><b id="tc" style="color:#F59E0B">0</b> tags</span>
    </div>
  </div>

  <div class="ebody">
    <div class="lnums" id="lnums">1</div>
    <div id="ed" contenteditable="true" spellcheck="true"></div>
  </div>

  <div class="sbar">
    <span class="s-ready">● ready</span>
    <span id="cur">Ln 1, Col 1</span>
  </div>
</div>

<textarea id="sync" style="display:none"></textarea>

<script>
const COLORS = {emo_color_js};
const ed=document.getElementById('ed'),sync=document.getElementById('sync'),
      shell=document.getElementById('shell'),lnums=document.getElementById('lnums');

function render(text){{
  const parts=text.split(/(\[[a-z]+\])/gi);
  ed.innerHTML='';
  parts.forEach(p=>{{
    const m=p.match(/^\[([a-z]+)\]$/i);
    if(m){{
      const tag=m[1].toLowerCase(),col=COLORS[tag]||'#94A3B8';
      const sp=document.createElement('span');
      sp.className='etag';sp.contentEditable='false';sp.dataset.tag=tag;
      sp.style.cssText=`background:${{col}}22;color:${{col}};border:1px solid ${{col}}55;`;
      sp.textContent='['+tag+']';
      ed.appendChild(sp);
    }}else if(p) ed.appendChild(document.createTextNode(p));
  }});
  updateLnums();
}}

function extract(){{
  let t='';
  ed.childNodes.forEach(n=>{{
    if(n.nodeType===3) t+=n.textContent;
    else if(n.classList?.contains('etag')) t+='['+n.dataset.tag+']';
    else t+=(n.innerText||n.textContent||'');
  }});
  return t;
}}

function updateLnums(){{
  const lines=Math.max(1,extract().split('\\n').length);
  lnums.innerHTML=Array.from({{length:lines}},(_,i)=>i+1).join('<br>');
}}

function updateStats(){{
  const t=extract();
  const w=t.trim()?t.trim().split(/\\s+/).length:0;
  const tags=(t.match(/\\[[a-z]+\\]/gi)||[]).length;
  document.getElementById('wc').textContent=w;
  document.getElementById('cc').textContent=t.length;
  document.getElementById('tc').textContent=tags;
  sync.value=t;sync.dispatchEvent(new Event('change'));
  window.parent.postMessage({{type:'tts_upd',text:t}},'*');
  updateLnums();
}}

function updateCursor(){{
  try{{
    const sel=window.getSelection();if(!sel.rangeCount)return;
    const r=sel.getRangeAt(0).cloneRange();
    r.selectNodeContents(ed);
    r.setEnd(sel.getRangeAt(0).endContainer,sel.getRangeAt(0).endOffset);
    const lines=r.toString().split('\\n');
    document.getElementById('cur').textContent='Ln '+lines.length+', Col '+(lines[lines.length-1].length+1);
  }}catch(e){{}}
}}

function insertTag(tag){{
  ed.focus();
  const col=COLORS[tag]||'#94A3B8';
  const sp=document.createElement('span');
  sp.className='etag';sp.contentEditable='false';sp.dataset.tag=tag;
  sp.style.cssText=`background:${{col}}22;color:${{col}};border:1px solid ${{col}}55;`;
  sp.textContent='['+tag+']';
  const sel=window.getSelection();
  if(sel.rangeCount){{
    const range=sel.getRangeAt(0);range.deleteContents();
    const b=document.createTextNode(' '),a=document.createTextNode(' ');
    range.insertNode(a);range.insertNode(sp);range.insertNode(b);
    const nr=document.createRange();nr.setStartAfter(a);nr.collapse(true);
    sel.removeAllRanges();sel.addRange(nr);
  }}else{{
    ed.appendChild(document.createTextNode(' '));
    ed.appendChild(sp);
    ed.appendChild(document.createTextNode(' '));
  }}
  updateStats();
}}

ed.addEventListener('input',updateStats);
ed.addEventListener('keyup',updateCursor);
ed.addEventListener('mouseup',updateCursor);
ed.addEventListener('focus',()=>shell.classList.add('active'));
ed.addEventListener('blur', ()=>{{shell.classList.remove('active');updateStats();}});
ed.addEventListener('keydown',e=>{{
  if(e.key==='Backspace'){{
    const sel=window.getSelection();if(!sel.rangeCount)return;
    const range=sel.getRangeAt(0);if(!range.collapsed)return;
    let prev=range.startContainer.previousSibling;
    if(!prev&&range.startOffset===0) prev=range.startContainer.parentNode?.previousSibling;
    if(prev?.classList?.contains('etag')){{e.preventDefault();prev.remove();updateStats();}}
  }}
}});

window.addEventListener('message',e=>{{
  if(!e.data)return;
  if(e.data.type==='ins_tag') insertTag(e.data.tag);
  if(e.data.type==='set_txt'){{render(e.data.text);updateStats();}}
}});

render({repr(st.session_state.script)});
updateStats();
const PENDING={pending_js};
if(PENDING) setTimeout(()=>insertTag(PENDING),80);
</script></body></html>"""

    st.markdown('<p style="font-size:11px;font-weight:600;letter-spacing:1.5px;text-transform:uppercase;color:#5A5A70;margin-bottom:8px;">✏️ Script Editor</p>', unsafe_allow_html=True)
    components.html(EDITOR_HTML, height=390, scrolling=False)

    # Invisible sync textarea
    synced = st.text_area("_sync_", value=st.session_state.script, key="sync_area")
    if synced is not None:
        st.session_state.script = synced

    # ── Emotion Palette ───────────────────────────────────────────────────────
    st.markdown("""
    <div style="margin-top:20px;margin-bottom:10px;">
      <p style="font-size:11px;font-weight:600;letter-spacing:1.5px;text-transform:uppercase;color:#5A5A70;margin-bottom:4px;">🎭 Emotion Tags</p>
      <p style="font-size:12px;color:#40405A;margin:0;">Click a tag to insert it at your cursor position. Tags stay active until the next one.</p>
    </div>
    """, unsafe_allow_html=True)

    # Render 5 per row
    for row_start in range(0, len(ALL_EMOTIONS), 5):
        row = ALL_EMOTIONS[row_start:row_start+5]
        cols = st.columns(5)
        for j, (emo, color, icon) in enumerate(row):
            with cols[j]:
                # Inject per-button style using a wrapper class
                btn_id = f"ebtn_{emo}"
                st.markdown(f"""
                <style>
                div[data-testid="stButton"] button[kind="secondary"]#btn_{emo},
                .btn-wrap-{emo} .stButton > button {{
                    background: {color}12 !important;
                    border-color: {color}40 !important;
                    color: {color} !important;
                    font-size: 12px !important;
                    padding: 7px 6px !important;
                    font-family: 'JetBrains Mono', monospace !important;
                }}
                .btn-wrap-{emo} .stButton > button:hover {{
                    background: {color}25 !important;
                    border-color: {color}99 !important;
                    box-shadow: 0 3px 10px {color}30 !important;
                }}
                </style>
                <div class="btn-wrap-{emo}">
                """, unsafe_allow_html=True)
                pressed = st.button(f"{icon} {emo}", key=f"emo_{emo}")
                st.markdown("</div>", unsafe_allow_html=True)
                if pressed:

                    st.session_state.pending_tag = emo
                    st.rerun()

    st.session_state.pending_tag = None

    # ── Example Scripts ───────────────────────────────────────────────────────
    st.markdown('<p style="font-size:11px;font-weight:600;letter-spacing:1.5px;text-transform:uppercase;color:#5A5A70;margin-top:20px;margin-bottom:8px;">⚡ Quick Examples</p>', unsafe_allow_html=True)
    ex_cols = st.columns(3)
    for i, (label, script) in enumerate(EXAMPLES):
        with ex_cols[i % 3]:
            if st.button(label, key=f"ex_{i}"):
                st.session_state.script = script
                st.rerun()

# ╔══════════════════════════════════════╗
# ║  RIGHT — Settings                    ║
# ╚══════════════════════════════════════╝
with right:

    # ── Voice Selector ────────────────────────────────────────────────────────
    st.markdown("""
    <div style="background:#1A1D26;border:1.5px solid #2E3140;border-radius:14px;padding:20px 20px 16px;margin-bottom:16px;">
      <p style="font-size:11px;font-weight:600;letter-spacing:1.5px;text-transform:uppercase;color:#5A5A70;margin:0 0 14px;">🎤 Voice</p>
    """, unsafe_allow_html=True)

    # Group voices for a nicer display
    voice_labels = [f"{v[3]} {v[1]}  —  {v[2]}" for v in VOICES]
    sel_idx = st.selectbox("Voice", range(len(VOICES)), format_func=lambda i: voice_labels[i], label_visibility="collapsed")
    sel = VOICES[sel_idx]

    # Show selected voice detail card
    st.markdown(f"""
    <div style="background:#111318;border:1px solid #22252F;border-radius:10px;
                padding:13px 15px;margin-top:12px;display:flex;align-items:center;gap:12px;">
      <div style="font-size:28px;line-height:1;">{sel[3]}</div>
      <div>
        <div style="font-size:15px;font-weight:600;color:#F0F0F5;">{sel[1]}</div>
        <div style="font-size:12px;color:#5A5A70;margin-top:2px;">{sel[2]} &nbsp;·&nbsp;
          <span style="color:#6C63FF;font-family:'JetBrains Mono',monospace;">{sel[4]}</span>
        </div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # ── Speed ─────────────────────────────────────────────────────────────────
    st.markdown("""
    <div style="background:#1A1D26;border:1.5px solid #2E3140;border-radius:14px;padding:20px 20px 16px;margin-bottom:16px;">
      <p style="font-size:11px;font-weight:600;letter-spacing:1.5px;text-transform:uppercase;color:#5A5A70;margin:0 0 12px;">⏱ Speed</p>
    """, unsafe_allow_html=True)

    speed = st.slider("Speed", 0.5, 2.0, 1.0, 0.05, label_visibility="collapsed")
    pct   = int((speed - 0.5) / 1.5 * 100)
    sc    = "#60A5FA" if speed < 0.85 else "#6C63FF" if speed <= 1.15 else "#F59E0B" if speed <= 1.6 else "#F87171"
    label = "Slow" if speed < 0.85 else "Normal" if speed <= 1.15 else "Fast" if speed <= 1.6 else "Very Fast"

    st.markdown(f"""
    <div style="background:#111318;border:1px solid #22252F;border-radius:10px;padding:13px 15px;margin-top:4px;">
      <div style="display:flex;justify-content:space-between;align-items:center;margin-bottom:8px;">
        <span style="font-size:12px;color:#5A5A70;">{label}</span>
        <span style="font-size:18px;font-weight:700;color:{sc};font-family:'JetBrains Mono',monospace;">{speed:.2f}×</span>
      </div>
      <div style="background:#22252F;border-radius:4px;height:5px;overflow:hidden;">
        <div style="background:linear-gradient(90deg,#6C63FF,{sc});width:{pct}%;height:100%;border-radius:4px;"></div>
      </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

    # ── Script Stats ──────────────────────────────────────────────────────────
    txt  = st.session_state.script
    wc   = len(txt.split()) if txt.strip() else 0
    cc   = len(txt)
    tc   = txt.count("[")
    prev = (txt[:110] + "…") if len(txt) > 110 else txt

    st.markdown(f"""
    <div style="background:#1A1D26;border:1.5px solid #2E3140;border-radius:14px;padding:20px 20px 16px;margin-bottom:16px;">
      <p style="font-size:11px;font-weight:600;letter-spacing:1.5px;text-transform:uppercase;color:#5A5A70;margin:0 0 14px;">📊 Script Info</p>
      <div style="display:grid;grid-template-columns:1fr 1fr 1fr;gap:8px;margin-bottom:14px;">
        <div style="background:#111318;border:1px solid #22252F;border-radius:10px;padding:13px;text-align:center;">
          <div style="font-size:22px;font-weight:700;color:#6C63FF;font-family:'JetBrains Mono',monospace;">{wc}</div>
          <div style="font-size:10px;color:#40405A;margin-top:3px;letter-spacing:1px;text-transform:uppercase;">Words</div>
        </div>
        <div style="background:#111318;border:1px solid #22252F;border-radius:10px;padding:13px;text-align:center;">
          <div style="font-size:22px;font-weight:700;color:#6C63FF;font-family:'JetBrains Mono',monospace;">{cc}</div>
          <div style="font-size:10px;color:#40405A;margin-top:3px;letter-spacing:1px;text-transform:uppercase;">Chars</div>
        </div>
        <div style="background:#111318;border:1px solid #22252F;border-radius:10px;padding:13px;text-align:center;">
          <div style="font-size:22px;font-weight:700;color:#F59E0B;font-family:'JetBrains Mono',monospace;">{tc}</div>
          <div style="font-size:10px;color:#40405A;margin-top:3px;letter-spacing:1px;text-transform:uppercase;">Tags</div>
        </div>
      </div>
      <div style="background:#111318;border:1px solid #22252F;border-radius:10px;padding:11px 13px;
                  font-size:12px;color:#4A4A62;font-family:'JetBrains Mono',monospace;line-height:1.6;
                  min-height:38px;word-break:break-word;">
        {prev if prev.strip() else '<span style="color:#22252F">No text yet…</span>'}
      </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Tag Reference ─────────────────────────────────────────────────────────
    st.markdown("""
    <div style="background:#1A1D26;border:1.5px solid #2E3140;border-radius:14px;padding:20px 20px 16px;">
      <p style="font-size:11px;font-weight:600;letter-spacing:1.5px;text-transform:uppercase;color:#5A5A70;margin:0 0 14px;">📖 Tag Reference</p>
    """, unsafe_allow_html=True)

    groups = [
        ("😊 Positive",  ["happy","excited","surprise"]),
        ("😢 Sad",       ["sad","crying"]),
        ("😠 Intense",   ["angry","shout","frustrated","panicky"]),
        ("🤫 Soft",      ["whisper","sleepy","slow"]),
        ("🎵 Pitch",     ["deep","high","fast"]),
        ("😐 Neutral",   ["normal","longer","disgust","curious"]),
    ]
    emo_map = {e[0]: (e[1], e[2]) for e in ALL_EMOTIONS}

    for glabel, names in groups:
        chips = "".join([
            f'<span style="background:{emo_map[n][0]}16;border:1px solid {emo_map[n][0]}45;'
            f'color:{emo_map[n][0]};border-radius:6px;padding:3px 10px;font-size:11px;'
            f'font-family:JetBrains Mono,monospace;margin:2px 2px 2px 0;display:inline-block;">'
            f'{emo_map[n][1]} {n}</span>'
            for n in names if n in emo_map
        ])
        st.markdown(f"""
        <div style="margin-bottom:11px;">
          <div style="font-size:11px;color:#40405A;margin-bottom:5px;font-weight:500;">{glabel}</div>
          <div style="line-height:2;">{chips}</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("</div>", unsafe_allow_html=True)

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  GENERATE BUTTON
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
st.markdown("<hr/>", unsafe_allow_html=True)

g1, g2, g3 = st.columns([1, 2, 1])
with g2:
    st.markdown("""
    <style>
    div[data-testid="column"]:nth-child(2) > div:first-child > div:first-child .stButton > button {
        background: linear-gradient(135deg,#6C63FF,#9B93FF) !important;
        color: #fff !important;
        font-size: 16px !important;
        font-weight: 700 !important;
        padding: 15px 32px !important;
        border-radius: 12px !important;
        border: none !important;
        box-shadow: 0 4px 22px rgba(108,99,255,0.4) !important;
        letter-spacing: 0.3px !important;
    }
    div[data-testid="column"]:nth-child(2) > div:first-child > div:first-child .stButton > button:hover {
        box-shadow: 0 8px 32px rgba(108,99,255,0.55) !important;
        transform: translateY(-2px) !important;
    }
    </style>
    """, unsafe_allow_html=True)
    generate = st.button("🎙️  Generate Speech", key="gen_btn")

# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
#  GENERATION LOGIC
# ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
if generate:
    final = st.session_state.script.strip()
    if not final:
        st.error("⚠️ Write some text in the editor first.")
    else:
        try:
            from kokoro_onnx import Kokoro
            onnx_p, voc_p = "kokoro-v1.0.onnx", "voices-v1.0.bin"
            if not os.path.exists(onnx_p) or not os.path.exists(voc_p):
                st.error("**Model files not found.** Place `kokoro-v1.0.onnx` and `voices-v1.0.bin` in the same folder as this script.")
            else:
                r1, r2, r3 = st.columns([1, 2, 1])
                with r2:
                    with st.spinner("🎵 Synthesising audio…"):
                        kokoro = Kokoro(onnx_p, voc_p)
                        samples, sr = kokoro.create(final, voice=sel[0], speed=speed, lang=sel[4])
                        buf = io.BytesIO()
                        sf.write(buf, samples, sr, format="WAV")
                        buf.seek(0)

                    st.markdown("""
                    <div style="background:#0F2A1A;border:1px solid #22863a55;border-radius:12px;
                                padding:14px 16px;margin-bottom:12px;">
                      <div style="color:#4ADE80;font-size:13px;font-weight:600;margin-bottom:10px;">✅ Audio generated</div>
                    """, unsafe_allow_html=True)
                    st.audio(buf, format="audio/wav")
                    st.markdown("</div>", unsafe_allow_html=True)
                    st.download_button("⬇️  Download WAV", buf.getvalue(), "orpheus_output.wav", "audio/wav")

        except ImportError:
            st.error("**kokoro-onnx not installed.** Run: `pip install kokoro-onnx soundfile`")
        except Exception as e:
            st.error(f"**Error:** {e}")

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("""
<div style="text-align:center;margin-top:2.5rem;padding-top:1rem;border-top:1px solid #1A1D26;">
  <span style="font-size:11px;color:#22252F;font-family:'JetBrains Mono',monospace;letter-spacing:1px;">
    ORPHEUS TTS STUDIO &nbsp;·&nbsp; KOKORO ONNX &nbsp;·&nbsp; LOCAL WINDOWS BUILD
  </span>
</div>
""", unsafe_allow_html=True)
