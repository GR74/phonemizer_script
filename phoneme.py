from g2p_en import G2p
import nltk
from nltk.corpus import cmudict
import tkinter as tk
from tkinter import messagebox
import pyttsx3
import random
import os

# Download required NLTK data
nltk.download('averaged_perceptron_tagger')
nltk.download('cmudict')

# Initialize engines and resources
cmu = cmudict.dict()
g2p = G2p()
engine = pyttsx3.init()

# ARPAbet phoneme reference
ARPAbet_PHONEMES = """
AA - as in 'odd'
AE - as in 'at'
AH - as in 'hut'
AO - as in 'ought'
AW - as in 'cow'
AY - as in 'hide'
B  - as in 'be'
CH - as in 'cheese'
D  - as in 'dee'
DH - as in 'thee'
EH - as in 'Ed'
ER - as in 'hurt'
EY - as in 'ate'
F  - as in 'fee'
G  - as in 'green'
HH - as in 'he'
IH - as in 'it'
IY - as in 'eat'
JH - as in 'gee'
K  - as in 'key'
L  - as in 'lee'
M  - as in 'me'
N  - as in 'knee'
NG - as in 'sing'
OW - as in 'oat'
OY - as in 'toy'
P  - as in 'pee'
R  - as in 'read'
S  - as in 'sea'
SH - as in 'she'
T  - as in 'tea'
TH - as in 'theta'
UH - as in 'hood'
UW - as in 'two'
V  - as in 'vee'
W  - as in 'we'
Y  - as in 'yield'
Z  - as in 'zee'
ZH - as in 'pleasure'
"""

phoneme_to_number = {
    "AA": 1,
    "AE": 2,
    "AH": 3,
    "AO": 4,
    "AW": 5,
    "AY": 6,
    "B": 7,
    "CH": 8,
    "D": 9,
    "DH": 10,
    "EH": 11,
    "ER": 12,
    "EY": 13,
    "F": 14,
    "G": 15,
    "HH": 16,
    "IH": 17,
    "IY": 18,
    "JH": 19,
    "K": 20,
    "L": 21,
    "M": 22,
    "N": 23,
    "NG": 24,
    "OW": 25,
    "OY": 26,
    "P": 27,
    "R": 28,
    "S": 29,
    "SH": 30,
    "T": 31,
    "TH": 32,
    "UH": 33,
    "UW": 34,
    "V": 35,
    "W": 36,
    "Y": 37,
    "Z": 38,
    "ZH": 39
}

# Utility functions
def strip_stress(phoneme_seq):
    return [ph.strip("012") for ph in phoneme_seq]

def get_phonemes_any(word):
    word_lower = word.lower()
    if word_lower in cmu:
        return [strip_stress(cmu[word_lower][0])] 
    else:
        return [strip_stress(g2p(word))]

def show_phonemes():
    word_input = entry.get()
    if not word_input.strip():
        messagebox.showerror("Error", "Please enter a word or phrase.")
        return

    words = word_input.strip().split()
    all_phonemes = []
    phonemes_for_display = []

    # Collect phonemes for each word
    for w in words:
        ph = get_phonemes_any(w)
        phonemes_for_display.append(ph[0])  # First variant
        all_phonemes.append(ph[0])

    # Display phonemes in the GUI
    output_display = ''
    for w, ph_list in zip(words, phonemes_for_display):
        output_display += f"{w}: {' '.join(ph_list)}\n"
    result_label.config(text=f"Phonemes:\n{output_display.strip()}")

    output_folder = r"C:\Users\gowri\phonemes\eeg_culmination"
    os.makedirs(output_folder, exist_ok=True)
    output_file_path = os.path.join(output_folder, f"{'_'.join(words)}.txt")
    eeg_base_path = r"C:\Users\gowri\phonemes\eeg"

    with open(output_file_path, "w") as word_output:
        for word_idx, (w, phoneme_list) in enumerate(zip(words, all_phonemes)):
            word_output.write(f"--- Word: {w} ---\n")
            print(f"[INFO] Processing word: {w}")
            
            for idx, p in enumerate(phoneme_list):
                num = phoneme_to_number.get(p, -1)
                if num == -1:
                    word_output.write(f"Unrecognized phoneme '{p}'\n\n")
                    print(f"[WARNING] Unrecognized phoneme: {p}")
                    continue

                eeg_file_path = os.path.join(eeg_base_path, f"DLR_{num}_1.txt")
                if os.path.exists(eeg_file_path):
                    with open(eeg_file_path, "r") as eeg_file:
                        eeg_data = eeg_file.read()
                        word_output.write(f"[Phoneme: {p} | Num: {num}]\n{eeg_data}\n\n")
                else:
                    word_output.write(f"EEG data not found for phoneme '{p}' (number {num})\n\n")
                    print(f"[ERROR] EEG data not found for phoneme '{p}' (number {num})")

            # Insert pseudorandom gap after each word except the last one
            if word_idx < len(all_phonemes) - 1:
                random_phoneme = random.choice(list(phoneme_to_number.keys()))
                random_num = phoneme_to_number[random_phoneme]
                random_eeg_file = os.path.join(eeg_base_path, f"DLR_{random_num}_1.txt")
                
                if os.path.exists(random_eeg_file):
                    with open(random_eeg_file, "r") as rand_eeg:
                        rand_data = rand_eeg.read()
                        word_output.write(f"[Pseudorandom Gap: Phoneme {random_phoneme} | Num: {random_num}]\n{rand_data}\n\n")
                        print(f"[INFO] Added pseudorandom gap using phoneme '{random_phoneme}'")
                else:
                    word_output.write(f"[Pseudorandom Gap: EEG file missing for {random_phoneme} (Num: {random_num})]\n\n")
                    print(f"[WARNING] Pseudorandom EEG file missing for {random_phoneme} (Num: {random_num})")

    print(f"[INFO] Processing complete for: {word_input}")

def pronounce_word():
    word = entry.get()
    if not word.strip():
        messagebox.showerror("Error", "Please enter a word or phrase.")
        return
    engine.say(word)
    engine.runAndWait()

def on_enter(e):
    e.widget['bg'] = "#4a90e2"

def on_leave(e):
    e.widget['bg'] = "#357ABD"

# GUI setup
root = tk.Tk()
root.title("🎙️ Phoneme Pronouncer Pro")
root.geometry("600x700")
root.configure(bg="#1e1e2e")
root.resizable(False, False)

# Fonts & Colors
FONT_TITLE = ("Segoe UI", 20, "bold")
FONT_NORMAL = ("Segoe UI", 12)
FONT_MONO = ("Courier New", 10)
FG_COLOR = "#f8f8f2"
BG_COLOR = "#1e1e2e"
ENTRY_BG = "#2e2e3e"
BTN_BG = "#357ABD"
BTN_FG = "#ffffff"

# Title
tk.Label(root, text="Phoneme Pronouncer Pro", font=FONT_TITLE, fg="#89ddff", bg=BG_COLOR).pack(pady=20)

# Entry
tk.Label(root, text="Type a word or phrase below:", font=FONT_NORMAL, fg=FG_COLOR, bg=BG_COLOR).pack()
entry = tk.Entry(root, font=("Segoe UI", 14), width=30, bg=ENTRY_BG, fg=FG_COLOR, insertbackground=FG_COLOR, relief="flat")
entry.pack(ipady=6, pady=10)

# Buttons
btn_frame = tk.Frame(root, bg=BG_COLOR)
btn_frame.pack(pady=10)

btn1 = tk.Button(btn_frame, text="🔍 Get Phonemes", command=show_phonemes, font=FONT_NORMAL, bg=BTN_BG, fg=BTN_FG, activebackground="#4a90e2", relief="flat", padx=20, pady=8, cursor="hand2")
btn1.pack(side="left", padx=10)
btn1.bind("<Enter>", on_enter)
btn1.bind("<Leave>", on_leave)

btn2 = tk.Button(btn_frame, text="🔊 Pronounce", command=pronounce_word, font=FONT_NORMAL, bg=BTN_BG, fg=BTN_FG, activebackground="#4a90e2", relief="flat", padx=20, pady=8, cursor="hand2")
btn2.pack(side="left", padx=10)
btn2.bind("<Enter>", on_enter)
btn2.bind("<Leave>", on_leave)

# Output Label
result_label = tk.Label(root, text="", wraplength=500, justify="center", font=("Consolas", 13), bg=BG_COLOR, fg="#a6e3a1")
result_label.pack(pady=20)

# ARPAbet Reference
tk.Label(root, text="📘 ARPAbet Phoneme Reference", font=("Segoe UI", 14, "bold"), fg="#ffcb6b", bg=BG_COLOR).pack(pady=(10, 0))

phoneme_text = tk.Text(root, height=15, width=60, font=FONT_MONO, bg="#2e2e3e", fg=FG_COLOR, bd=0, relief="flat")
phoneme_text.pack(pady=10)
phoneme_text.insert(tk.END, ARPAbet_PHONEMES)
phoneme_text.configure(state='disabled')

# Run it
root.mainloop()
