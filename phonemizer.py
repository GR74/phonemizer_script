from g2p_en import G2p
import nltk
from nltk.corpus import cmudict
import tkinter as tk
from tkinter import messagebox
import pyttsx3
import random
import os
import threading
import string
import pandas as pd
import pyperclip  # For clipboard operations

# Download required NLTK data (one-time)
nltk.download('averaged_perceptron_tagger')
nltk.download('cmudict')

# Initialize engines and resources
cmu = cmudict.dict()
g2p = G2p()

# Initialize TTS engine in a thread-safe way
engine = None

def init_tts_engine():
    global engine
    engine = pyttsx3.init()

threading.Thread(target=init_tts_engine).start()

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

# Phoneme to number mapping
phoneme_to_number = {
    "AA": 1, "AE": 2, "AH": 3, "AO": 4, "AW": 5, "AY": 6,
    "B": 7, "CH": 8, "D": 9, "DH": 10, "EH": 11, "ER": 12,
    "EY": 13, "F": 14, "G": 15, "HH": 16, "IH": 17, "IY": 18,
    "JH": 19, "K": 20, "L": 21, "M": 22, "N": 23, "NG": 24,
    "OW": 25, "OY": 26, "P": 27, "R": 28, "S": 29, "SH": 30,
    "T": 31, "TH": 32, "UH": 33, "UW": 34, "V": 35, "W": 36,
    "Y": 37, "Z": 38, "ZH": 39
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
    word_input = entry.get().strip()
    if not word_input:
        messagebox.showerror("Error", "Please enter a word or phrase.")
        return

    words = [w.strip(string.punctuation) for w in word_input.split()]
    words = [w for w in words if w]  # Remove empty strings

    all_phonemes = []
    phonemes_for_display = []

    for w in words:
        ph = get_phonemes_any(w)
        phonemes_for_display.append(ph[0])
        all_phonemes.append(ph[0])

    output_display = '\n'.join([f"{w}: {' '.join(ph_list)}" for w, ph_list in zip(words, phonemes_for_display)])
    result_label.config(text=f"Phonemes:\n{output_display}")

    base_dir = os.path.dirname(os.path.abspath(__file__))
    output_folder = os.path.join(base_dir, "eeg_culmination_csv")
    eeg_base_path = os.path.join(base_dir, "eeg")

    try:
        os.makedirs(output_folder, exist_ok=True)
    except Exception as e:
        messagebox.showerror("Error", f"Could not create output folder: {e}")
        return

    safe_words = [w[:10] for w in words]
    output_file_path = os.path.join(output_folder, f"{'_'.join(safe_words)}.tsv")

    txt_output_folder = os.path.join(base_dir, "eeg_culmination_txt")
    os.makedirs(txt_output_folder, exist_ok=True)
    txt_output_file_path = os.path.join(txt_output_folder, f"{'_'.join(safe_words)}.txt")



    with open(output_file_path, "w", encoding="utf-8") as word_output:
        for word_idx, (w, phoneme_list) in enumerate(zip(words, all_phonemes)):
            print(f"[INFO] Processing word: {w}")

            for p in phoneme_list:
                num = phoneme_to_number.get(p, -1)
                if num == -1:
                    print(f"[WARNING] Unrecognized phoneme: {p}")
                    continue

                eeg_file_path = os.path.join(eeg_base_path, f"DLR_{num}_1.txt")
                if os.path.exists(eeg_file_path):
                    with open(eeg_file_path, "r", encoding="utf-8") as eeg_file:
                        lines = eeg_file.readlines()

                        # Find the first line where the first column is "0.000000"
                        start_index = -1
                        for idx, line in enumerate(lines):
                            first_col = line.strip().split("\t")[0]
                            if first_col == "0.000000":
                                start_index = idx
                                break

                        if start_index != -1 and start_index + 256 <= len(lines):
                            word_output.writelines(lines[start_index:start_index + 256])
                        else:
                            print(f"[WARNING] Not enough lines after start index {start_index} in file {eeg_file_path}")

                else:
                    msg = f"EEG data not found for phoneme '{p}' (number {num})\n\n"
                    word_output.write(msg)
                    print(f"[ERROR] EEG data not found for phoneme '{p}' (number {num})")

            if word_idx < len(all_phonemes) - 1:
                random_phoneme = random.choice(list(phoneme_to_number.keys()))
                random_num = phoneme_to_number[random_phoneme]
                random_eeg_file = os.path.join(eeg_base_path, f"DLR_{random_num}_1.txt")

                if os.path.exists(random_eeg_file):
                    with open(random_eeg_file, "r", encoding="utf-8") as rand_eeg:
                        rand_lines = rand_eeg.readlines()

                        # Find the first line where the first column is "0.000000"
                        start_index = -1
                        for idx, line in enumerate(rand_lines):
                            first_col = line.strip().split("\t")[0]
                            if first_col == "0.000000":
                                start_index = idx
                                break

                        if start_index != -1 and start_index + 256 <= len(rand_lines):
                            word_output.writelines(rand_lines[start_index:start_index + 256])
                        else:
                            print(f"[WARNING] Not enough lines after start index {start_index} in file {random_eeg_file}")
                else:
                    msg = f"[Pseudorandom Gap: EEG file missing for {random_phoneme} (Num: {random_num})]\n\n"
                    word_output.write(msg)
                    print(f"[WARNING] Pseudorandom EEG file missing for {random_phoneme} (Num: {random_num})")
        # Write the same content to .txt file
    with open(txt_output_file_path, "w", encoding="utf-8") as txt_output:
        with open(output_file_path, "r", encoding="utf-8") as tsv_source:
            txt_output.write(tsv_source.read())

    print(f"[INFO] Also saved mirrored EEG file to: {txt_output_file_path}")

    print(f"[INFO] Processing complete for: {word_input}")
    messagebox.showinfo("Success", f"Output saved to:\n{output_file_path}")
    csv_output_path = output_file_path.replace(".tsv", "_eeg.csv")
    try:
        convert_eeg_tsv_to_csv(output_file_path, csv_output_path)
        print(f"[INFO] Converted EEG TSV to CSV at: {csv_output_path}")
    except Exception as e:
        print(f"[ERROR] Failed to convert TSV to CSV: {e}")

def pronounce_word():
    word = entry.get().strip()
    if not word:
        messagebox.showerror("Error", "Please enter a word or phrase.")
        return
    if engine is None:
        messagebox.showerror("Error", "Speech engine not ready yet. Try again shortly.")
        return
    engine.say(word)
    engine.runAndWait()

def copy_phonemes():
    phoneme_text = result_label.cget("text")
    if not phoneme_text or phoneme_text == "Phonemes:":
        messagebox.showwarning("Nothing to Copy", "No phonemes available yet.")
        return
    try:
        pyperclip.copy(phoneme_text)
        messagebox.showinfo("Copied", "Phonemes copied to clipboard!")
    except Exception as e:
        messagebox.showerror("Copy Error", f"Failed to copy to clipboard:\n{e}")

def on_enter(e):
    e.widget['bg'] = "#4a90e2"

def on_leave(e):
    e.widget['bg'] = "#357ABD"

# GUI Setup
root = tk.Tk()
root.title("🎙️ Phoneme Pronouncer Pro")
root.geometry("600x750")
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

# Entry Field
tk.Label(root, text="Type a word or phrase below:", font=FONT_NORMAL, fg=FG_COLOR, bg=BG_COLOR).pack()
entry = tk.Entry(root, font=("Segoe UI", 14), width=30, bg=ENTRY_BG, fg=FG_COLOR, insertbackground=FG_COLOR, relief="flat")
entry.pack(ipady=6, pady=10)

# Buttons
btn_frame = tk.Frame(root, bg=BG_COLOR)
btn_frame.pack(pady=10)

btn1 = tk.Button(btn_frame, text="🔍 Get Phonemes", command=show_phonemes, font=FONT_NORMAL, bg=BTN_BG, fg=BTN_FG,
                 activebackground="#4a90e2", relief="flat", padx=20, pady=8, cursor="hand2")
btn1.pack(side="left", padx=10)
btn1.bind("<Enter>", on_enter)
btn1.bind("<Leave>", on_leave)

btn2 = tk.Button(btn_frame, text="🔊 Pronounce", command=pronounce_word, font=FONT_NORMAL, bg=BTN_BG, fg=BTN_FG,
                 activebackground="#4a90e2", relief="flat", padx=20, pady=8, cursor="hand2")
btn2.pack(side="left", padx=10)
btn2.bind("<Enter>", on_enter)
btn2.bind("<Leave>", on_leave)

# New Copy Button
btn3 = tk.Button(btn_frame, text="📋 Copy Phonemes", command=copy_phonemes, font=FONT_NORMAL, bg=BTN_BG, fg=BTN_FG,
                 activebackground="#4a90e2", relief="flat", padx=20, pady=8, cursor="hand2")
btn3.pack(side="left", padx=10)
btn3.bind("<Enter>", on_enter)
btn3.bind("<Leave>", on_leave)
# Result Label
result_label = tk.Label(root, text="", wraplength=500, justify="center", font=("Consolas", 13), bg=BG_COLOR, fg="#a6e3a1")
result_label.pack(pady=20)

# ARPAbet Reference
tk.Label(root, text="📘 ARPAbet Phoneme Reference", font=("Segoe UI", 14, "bold"), fg="#ffcb6b", bg=BG_COLOR).pack(pady=(10, 0))

phoneme_text = tk.Text(root, height=15, width=60, font=FONT_MONO, bg="#2e2e3e", fg=FG_COLOR, bd=0, relief="flat")
phoneme_text.pack(pady=10)
phoneme_text.insert(tk.END, ARPAbet_PHONEMES)
phoneme_text.configure(state='disabled')

def convert_eeg_tsv_to_csv(input_tsv_path: str, output_csv_path: str):
    """
    Convert EEG .tsv file into .csv with original Index and cumulative Time in seconds.
    Each 256 samples = 1 second of EEG data.
    """
    headers = [
        "Index", "Fp1", "Fp2", "F3", "F4", "T5", "T6", "O1", "O2", "F7", "F8", "C3", "C4",
        "T3", "T4", "P3", "P4", "Accel Channel 0", "Accel Channel 1", "Accel Channel 2",
        "Other", "Other", "Other", "Other", "Other", "Other", "Other",
        "Analog Channel 0", "Analog Channel 1", "Analog Channel 2", "Timestamp", "Other"
    ]

    eeg_channels = [
        "Fp1", "Fp2", "F3", "F4", "T5", "T6", "O1", "O2",
        "F7", "F8", "C3", "C4", "T3", "T4", "P3", "P4"
    ]

    df = pd.read_table(input_tsv_path, sep="\t", header=None)
    df.columns = headers

    num_rows = len(df)

    # Time in seconds: 256 rows = 1 second
    time_col = [round(i / 256, 8) for i in range(num_rows)]

    # Extract EEG + add Time, keep original Index from TSV
    df_eeg = df[["Index"] + eeg_channels].copy()
    df_eeg.insert(1, "Timestamp", time_col)

    df_eeg.to_csv(output_csv_path, index=False)


# Run Application
root.mainloop()