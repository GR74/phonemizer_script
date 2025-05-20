**🎙️ Phonemizer**
Phonemizer is an interactive GUI tool for converting words and phrases into ARPAbet phoneme sequences, generating corresponding EEG signal slices for each phoneme, and exporting synchronized .tsv, .csv, and .txt files for downstream analysis or modeling.

🔬 Core Features
🧠 Phoneme Extraction: Converts user input into ARPAbet phoneme sequences using CMU Dictionary and G2P fallback.

📊 EEG Alignment: For each phoneme, extracts 256 EEG samples (1 second of data) starting at the first 0.000000 time entry from pre-recorded DLR_*.txt EEG files.

🔀 Gap Insertion: Adds randomized phoneme EEG snippets as pseudorandom "gaps" between words.

📁 Output Formats:

.tsv: Raw tab-separated EEG data

.csv: Cleaned EEG matrix with timestamp and original index

.txt: Identical copy of .tsv for compatibility or sharing

🗣️ Text-to-Speech Integration: Instantly pronounce the entered phrase.

📋 Clipboard Copy: Copy phoneme output for quick use elsewhere.

💻 User-Friendly GUI: Built with tkinter for smooth interaction.

📂 Output Structure
sql
Copy
Edit
/eeg
    DLR_*.txt        ← raw EEG files per phoneme
/eeg_culmination_csv
    hello_world.tsv  ← tab-separated EEG data
/eeg_culmination_txt
    hello_world.txt  ← mirrored copy of TSV
hello_world_eeg.csv  ← formatted CSV with timestamp & channel columns
🛠 Technologies Used
Python 3

tkinter – GUI

nltk, g2p_en – Phoneme conversion

pandas – CSV/TSV handling

pyttsx3 – Offline text-to-speech

pyperclip – Clipboard integration

python phoneme_pronouncer_pro.py
🧪 Sample Use Case
Type in: hello world
View: HH AH L OW, W ER L D
Output: EEG .tsv + .txt + .csv files with each mapped phoneme, with randomized inter-word EEG buffer segments.

🧠 Potential Applications
Neuroscience / EEG research

Speech-brain mapping

BCI (Brain-Computer Interface) model training

Linguistics + phoneme-time alignment

AI-based EEG signal synthesis
