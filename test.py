import json
import random
import tkinter as tk
from tkinter import font as tkfont
import pygame
import sys, os

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.dirname(__file__), relative_path)
pygame.mixer.init()

with open(resource_path("questions.json"), "r", encoding="utf-8") as f:
    data = json.load(f)

# ── Palette ──────────────────────────────────────────────
BG          = "#0F1117"
CARD_BG     = "#1A1D27"
CARD_BORDER = "#2A2D3E"
ACCENT      = "#6C63FF"
ACCENT2     = "#FF6584"
TEXT_MAIN   = "#EAEAF5"
TEXT_SUB    = "#8B8FA8"
TEXT_GREEN  = "#4DFFA0"
BTN_BG      = "#23263A"
BTN_HOVER   = "#2E3250"
BTN_PLAY    = "#6C63FF"
BTN_PLAY_H  = "#5A52E0"

questions = []
current   = 0
total     = 5

# ── Helpers ──────────────────────────────────────────────
def on_enter(e, w, color): w.config(bg=color)
def on_leave(e, w, color): w.config(bg=color)

def make_btn(parent, text, cmd, bg=BTN_BG, hover=BTN_HOVER,
             fg=TEXT_MAIN, font_size=11, pady=10, padx=20, radius=False):
    btn = tk.Button(
        parent, text=text, command=cmd,
        bg=bg, fg=fg, activebackground=hover, activeforeground=fg,
        font=body_font if font_size == 11 else title_font,
        relief="flat", bd=0, cursor="hand2",
        pady=pady, padx=padx
    )
    btn.bind("<Enter>", lambda e: btn.config(bg=hover))
    btn.bind("<Leave>", lambda e: btn.config(bg=bg))
    return btn

# ── App Logic ─────────────────────────────────────────────
def start():
    global questions, current
    all_q = []
    for topic, qs in data.items():
        for q in qs:
            all_q.append({**q, "topic": topic})
    random.shuffle(all_q)
    questions = all_q[:total]
    current = 0
    show_start_screen(False)
    load_question()

def load_question():
    q = questions[current]
    # Progress bar
    pct = (current) / total
    progress_fill.place(relwidth=pct, relheight=1)
    progress_text.config(text=f"{current+1} / {total}")
    # Badge
    badge_label.config(text=f"  {q['topic']}  •  Câu {q['id']}  ")
    # Reset card
    question_label.config(text="🎧  Nghe và đoán câu hỏi...", fg=TEXT_SUB)
    meaning_label.config(text="")
    for btn in action_btns:
        btn.config(state="normal")

def play_audio():
    try:
        pygame.mixer.music.load(resource_path(questions[current]["audio"]))
        pygame.mixer.music.play()
        animate_play()
    except Exception as e:
        question_label.config(text=f"⚠️  Không tìm thấy file audio", fg=ACCENT2)

def animate_play():
    play_btn.config(text="◉  Đang phát...")
    root.after(1500, lambda: play_btn.config(text="▶   Phát Audio"))

def show_question():
    question_label.config(text=questions[current]["question_en"], fg=TEXT_MAIN)

def show_meaning():
    meaning_label.config(text=questions[current]["question_vi"], fg=TEXT_GREEN)

def next_q():
    global current
    current += 1
    if current >= total:
        finish_screen()
        return
    pct = current / total
    progress_fill.place(relwidth=pct, relheight=1)
    load_question()

def finish_screen():
    progress_fill.place(relwidth=1, relheight=1)
    progress_text.config(text=f"{total} / {total}")
    badge_label.config(text="  ✅  Hoàn thành!  ")
    question_label.config(
        text="🎉  Bạn đã luyện xong\n5 câu hỏi hôm nay!", fg=ACCENT
    )
    meaning_label.config(text="Nhấn Shuffle để tiếp tục luyện tập.", fg=TEXT_SUB)
    for btn in action_btns:
        btn.config(state="disabled")

def show_start_screen(visible=True):
    if visible:
        start_frame.place(relx=0, rely=0, relwidth=1, relheight=1)
    else:
        start_frame.place_forget()

# ── Window ────────────────────────────────────────────────
root = tk.Tk()
root.title("Listening Trainer")
root.geometry("520x640")
root.resizable(False, False)
root.configure(bg=BG)

# Fonts
title_font  = tkfont.Font(family="Georgia",      size=18, weight="bold")
sub_font    = tkfont.Font(family="Georgia",      size=13, weight="bold")
body_font   = tkfont.Font(family="Helvetica",    size=11)
small_font  = tkfont.Font(family="Helvetica",    size=9)
badge_font  = tkfont.Font(family="Helvetica",    size=9,  weight="bold")
q_font      = tkfont.Font(family="Georgia",      size=14)
meaning_fnt = tkfont.Font(family="Helvetica",    size=12, slant="italic")
big_font    = tkfont.Font(family="Georgia",      size=22, weight="bold")

# ── Header ────────────────────────────────────────────────
header = tk.Frame(root, bg=CARD_BG, height=70)
header.pack(fill="x")
header.pack_propagate(False)

tk.Label(header, text="🎧", bg=CARD_BG, fg=ACCENT,
         font=tkfont.Font(size=22)).place(x=20, rely=0.5, anchor="w")
tk.Label(header, text="Listening Trainer", bg=CARD_BG, fg=TEXT_MAIN,
         font=title_font).place(x=62, rely=0.5, anchor="w")

shuffle_btn = make_btn(header, "⟳  Shuffle", start,
                       bg=ACCENT, hover=BTN_PLAY_H, fg="white",
                       font_size=11, pady=7, padx=16)
shuffle_btn.place(relx=1, x=-16, rely=0.5, anchor="e")

# Divider
tk.Frame(root, bg=CARD_BORDER, height=1).pack(fill="x")

# ── Progress ──────────────────────────────────────────────
prog_outer = tk.Frame(root, bg=BG, height=40)
prog_outer.pack(fill="x", padx=24, pady=(14, 4))

tk.Label(prog_outer, text="Tiến độ", bg=BG, fg=TEXT_SUB,
         font=small_font).pack(side="left")
progress_text = tk.Label(prog_outer, text="0 / 5", bg=BG, fg=TEXT_SUB,
                          font=small_font)
progress_text.pack(side="right")

prog_bar_bg = tk.Frame(root, bg=BTN_BG, height=6)
prog_bar_bg.pack(fill="x", padx=24)
progress_fill = tk.Frame(prog_bar_bg, bg=ACCENT, height=6)
progress_fill.place(relwidth=0, relheight=1)

# ── Badge ─────────────────────────────────────────────────
badge_frame = tk.Frame(root, bg=BG)
badge_frame.pack(anchor="w", padx=24, pady=(14, 0))
badge_label = tk.Label(
    badge_frame, text="  BTVN  •  Câu  ",
    bg=ACCENT, fg="white", font=badge_font,
    padx=4, pady=3
)
badge_label.pack()

# ── Card ──────────────────────────────────────────────────
card = tk.Frame(root, bg=CARD_BG, bd=0,
                highlightbackground=CARD_BORDER, highlightthickness=1)
card.pack(fill="x", padx=24, pady=12)

question_label = tk.Label(
    card, text="Nhấn  ⟳ Shuffle  để bắt đầu",
    bg=CARD_BG, fg=TEXT_SUB,
    font=q_font, wraplength=440,
    justify="center", pady=36, padx=20
)
question_label.pack(fill="x")

tk.Frame(card, bg=CARD_BORDER, height=1).pack(fill="x", padx=16)

meaning_label = tk.Label(
    card, text="",
    bg=CARD_BG, fg=TEXT_GREEN,
    font=meaning_fnt, wraplength=440,
    justify="center", pady=18, padx=20
)
meaning_label.pack(fill="x")

# ── Play Button ───────────────────────────────────────────
play_btn = make_btn(root, "▶   Phát Audio", play_audio,
                    bg=BTN_PLAY, hover=BTN_PLAY_H, fg="white",
                    font_size=12, pady=13, padx=30)
play_btn.pack(pady=(4, 0), ipadx=10)

# ── Action Buttons ────────────────────────────────────────
action_row = tk.Frame(root, bg=BG)
action_row.pack(pady=10, fill="x", padx=24)

btn_show_q = make_btn(action_row, "👀  Hiện câu hỏi", show_question,
                      pady=10, padx=10)
btn_show_m = make_btn(action_row, "📖  Xem nghĩa", show_meaning,
                      pady=10, padx=10)
btn_next   = make_btn(action_row, "Tiếp theo  ➜", next_q,
                      bg=ACCENT2, hover="#e0506e", fg="white",
                      pady=10, padx=10)

btn_show_q.pack(side="left", expand=True, fill="x", padx=(0, 6))
btn_show_m.pack(side="left", expand=True, fill="x", padx=(0, 6))
btn_next.pack(side="left", expand=True, fill="x")

action_btns = [btn_show_q, btn_show_m, btn_next, play_btn]

# ── Footer ────────────────────────────────────────────────
tk.Frame(root, bg=CARD_BORDER, height=1).pack(fill="x", pady=(8, 0))
tk.Label(root, text="TOEIC Part 2  •  Question Response",
         bg=BG, fg=TEXT_SUB, font=small_font).pack(pady=8)

# ── Start overlay ─────────────────────────────────────────
start_frame = tk.Frame(root, bg=BG)
start_frame.place(relx=0, rely=0, relwidth=1, relheight=1)

tk.Label(start_frame, text="🎧", bg=BG,
         font=tkfont.Font(size=48)).pack(pady=(100, 8))
tk.Label(start_frame, text="Listening Trainer",
         bg=BG, fg=TEXT_MAIN, font=big_font).pack()
tk.Label(start_frame,
         text=f"Random từ toàn bộ {sum(len(v) for v in data.values())} câu hỏi",
         bg=BG, fg=TEXT_SUB, font=body_font).pack(pady=6)

start_main_btn = make_btn(
    start_frame, "Bắt đầu luyện tập  ", start,
    bg=ACCENT, hover=BTN_PLAY_H, fg="white",
    font_size=13, pady=14, padx=30
)
start_main_btn.pack(pady=28)

root.mainloop()