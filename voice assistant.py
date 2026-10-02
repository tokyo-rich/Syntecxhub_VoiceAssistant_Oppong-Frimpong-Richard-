"""
Personal Voice Assistant
--------------------------------------------
Syntecxhub AI Internship - Week 4, Project 1

This program listens for a command (by voice OR typed text), figures out
what you want using simple RULE MAPPING (similar idea to the expert
system from an earlier week), performs the action, and speaks the
response back to you.

Pipeline:
    1. LISTEN   -> get the user's command (speech-to-text, or typed input)
    2. UNDERSTAND -> match the command text against known rules/keywords
    3. ACT      -> run the matching action (tell time, open a site, etc.)
    4. RESPOND  -> speak the result out loud (text-to-speech)

Two modes are supported:
    - Voice mode: uses the `speech_recognition` and `pyttsx3` libraries.
    - Text mode: works everywhere, no microphone/speakers needed. This is
      useful for testing, demos, or environments without audio hardware.

Install (for voice mode) with:
    pip install SpeechRecognition pyttsx3 pyaudio
"""

import sys
import webbrowser
import datetime

# ---------------------------------------------------------
# STEP 0: Try to load voice libraries. If unavailable, we
# simply fall back to text mode so the program still runs.
# ---------------------------------------------------------
try:
    import speech_recognition as sr
    import pyttsx3
    VOICE_AVAILABLE = True
except ImportError:
    VOICE_AVAILABLE = False


def speak(text):
    """
    Output the assistant's response.
    In voice mode: speaks it aloud using text-to-speech.
    In text mode: just prints it.
    """
    print(f"Assistant: {text}")
    if VOICE_AVAILABLE and USE_VOICE:
        try:
            engine = pyttsx3.init()
            engine.say(text)
            engine.runAndWait()
        except Exception as e:
            # If the speaker/engine fails, we don't crash - just log it.
            print(f"(voice output failed: {e})")


def listen():
    """
    Get a command from the user.
    In voice mode: records audio from the microphone and converts to text.
    In text mode: just reads typed input.
    Returns the command as a lowercase string, or "" if nothing understood.
    """
    if VOICE_AVAILABLE and USE_VOICE:
        recognizer = sr.Recognizer()
        try:
            with sr.Microphone() as source:
                print("Listening...")
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source, timeout=5)
            command = recognizer.recognize_google(audio)
            print(f"You said: {command}")
            return command.lower()
        except sr.WaitTimeoutError:
            speak("I didn't hear anything.")
        except sr.UnknownValueError:
            speak("Sorry, I couldn't understand that.")
        except sr.RequestError:
            speak("Speech service is unavailable right now.")
        except Exception as e:
            speak(f"Microphone error: {e}")
        return ""
    else:
        # Text-mode fallback
        command = input("Type a command: ")
        return command.lower()


# ---------------------------------------------------------
# STEP 1: Define command rules.
# Each rule maps a set of trigger keywords to an action function.
# This is the same "rule mapping" idea mentioned in the project spec -
# IF the command contains these keywords, THEN do this action.
# ---------------------------------------------------------

def action_tell_time(command):
    now = datetime.datetime.now().strftime("%I:%M %p")
    speak(f"The current time is {now}.")


def action_tell_date(command):
    today = datetime.datetime.now().strftime("%A, %B %d, %Y")
    speak(f"Today's date is {today}.")


def action_open_google(command):
    speak("Opening Google.")
    webbrowser.open("https://www.google.com")


def action_open_youtube(command):
    speak("Opening YouTube.")
    webbrowser.open("https://www.youtube.com")


def action_search_web(command):
    # Extract the search term after the trigger word "search for" / "search"
    for trigger in ["search for", "search"]:
        if trigger in command:
            query = command.split(trigger, 1)[1].strip()
            if query:
                speak(f"Searching the web for {query}.")
                webbrowser.open(f"https://www.google.com/search?q={query}")
                return
    speak("What would you like me to search for?")


def action_greet(command):
    speak("Hello! How can I help you today?")


def action_help(command):
    speak("You can ask me for the time, the date, to open Google or "
          "YouTube, to search the web, or say goodbye to exit.")


def action_exit(command):
    speak("Goodbye! Have a great day.")
    sys.exit(0)


# RULES: list of (keywords, action) pairs, checked in order.
RULES = [
    (["what time", "current time", "tell me the time"], action_tell_time),
    (["what date", "today's date", "what day"], action_tell_date),
    (["open google"], action_open_google),
    (["open youtube"], action_open_youtube),
    (["search"], action_search_web),
    (["hello", "hi there", "hey"], action_greet),
    (["help", "what can you do"], action_help),
    (["exit", "quit", "goodbye", "bye"], action_exit),
]


def handle_command(command):
    """
    STEP 2 & 3: Understand the command by matching it against RULES,
    then ACT by calling the matching action function.
    """
    if not command:
        return  # nothing understood, just loop again

    for keywords, action in RULES:
        if any(keyword in command for keyword in keywords):
            action(command)
            return

    # No rule matched
    speak("Sorry, I don't know how to do that yet. Say 'help' for a list of commands.")


def main():
    global USE_VOICE

    print("=" * 50)
    print(" PERSONAL VOICE ASSISTANT")
    print("=" * 50)

    if VOICE_AVAILABLE:
        choice = input("Use voice mode? (y/n): ").strip().lower()
        USE_VOICE = (choice == "y")
    else:
        print("(speech_recognition/pyttsx3 not installed - running in text mode)")
        USE_VOICE = False

    speak("Assistant ready. Say 'help' to see what I can do, or 'exit' to quit.")

    while True:
        command = listen()
        handle_command(command)


if __name__ == "__main__":
    main()
