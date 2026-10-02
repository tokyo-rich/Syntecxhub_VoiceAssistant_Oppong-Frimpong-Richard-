# Syntecxhub AI Internship — Week 4, Project 1
## Personal Voice Assistant

A command-based assistant that listens (by voice or typed text),
understands your request through rule mapping, performs the action,
and responds back to you.

### Files
- `voice_assistant.py` — the complete program

### How it works
1. **Listen**: captures your command — either spoken (via microphone and
   speech-to-text) or typed (text-mode fallback, no hardware needed).
2. **Understand**: matches the command text against a set of keyword
   rules (e.g. "search" → web search action).
3. **Act**: runs the matching action — tells the time/date, opens a
   website, performs a web search, etc.
4. **Respond**: speaks the result back (text-to-speech), or prints it
   in text mode.

### How to run

**Text mode (no setup needed):**
```bash
python3 voice_assistant.py
```
If `speech_recognition` / `pyttsx3` aren't installed, it automatically
runs in text mode — just type your commands.

**Voice mode:**
```bash
pip install SpeechRecognition pyttsx3 pyaudio
python3 voice_assistant.py
```
Then choose `y` when asked to use voice mode.

### Sample commands
- "what time is it"
- "what's today's date"
- "open google"
- "open youtube"
- "search for python tutorials"
- "hello"
- "help"
- "exit" / "quit" / "bye"

### Error handling
- Handles no microphone input (timeout), unrecognized speech, and
  missing speech service gracefully.
- Falls back to text mode automatically if voice libraries aren't
  installed, so the program always runs.

### Requirements
- Python 3.x
- Optional (for voice mode): `SpeechRecognition`, `pyttsx3`, `pyaudio`
