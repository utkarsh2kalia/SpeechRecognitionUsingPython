{
 "cells": [
  {
   "cell_type": "code",
   "execution_count": 1,
   "metadata": {},
   "outputs": [],
   "source": [
    "import speech_recognition as sr"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {},
   "outputs": [],
   "source": [
    "r = sr.Recognizer()"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 3,
   "metadata": {},
   "outputs": [],
   "source": [
    "harvard = sr.AudioFile('input_read.wav')\n",
    "with harvard as source:\n",
    "    audio = r.record(source)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 4,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "speech_recognition.AudioData"
      ]
     },
     "execution_count": 4,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "# The context manager opens the file and reads its contents, storing the data in an AudioFile instance called source.\n",
    "# Then the record() method records the data from the entire file into an AudioData instance.\n",
    "# You can confirm this by checking the type of audio:\n",
    "type(audio)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 5,
   "metadata": {},
   "outputs": [
    {
     "data": {
      "text/plain": [
       "'the Purchase within the smooth flowing through the state without play background did it has a depth of about 30 days it took him like a river Rises after insert in Rampur to choose of lemons mix find the perfect used on the side of the how to search quilling art for the study was based advertising stockings hardstyle'"
      ]
     },
     "execution_count": 5,
     "metadata": {},
     "output_type": "execute_result"
    }
   ],
   "source": [
    "r.recognize_google(audio)"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": 2,
   "metadata": {},
   "outputs": [
    {
     "name": "stdout",
     "output_type": "stream",
     "text": [
      "I'm thinking of one of these words:\n",
      "apple, banana, grape, orange, mango, lemon\n",
      "You have 3 tries to guess which one.\n",
      "\n",
      "Guess 1. Speak!\n",
      "You said: Apple\n",
      "Incorrect. Try again.\n",
      "\n",
      "Guess 2. Speak!\n",
      "You said: banana\n",
      "Incorrect. Try again.\n",
      "\n",
      "Guess 3. Speak!\n",
      "I didn't catch that. What did you say?\n",
      "\n",
      "Guess 3. Speak!\n",
      "You said: orange\n",
      "Sorry, you lose!\n",
      "I was thinking of 'mango'.\n"
     ]
    }
   ],
   "source": [
    "import random\n",
    "import time\n",
    "\n",
    "import speech_recognition as sr\n",
    "\n",
    "\n",
    "def recognize_speech_from_mic(recognizer, microphone):\n",
    "    \"\"\"Transcribe speech from recorded from `microphone`.\n",
    "\n",
    "    Returns a dictionary with three keys:\n",
    "    \"success\": a boolean indicating whether or not the API request was\n",
    "               successful\n",
    "    \"error\":   `None` if no error occured, otherwise a string containing\n",
    "               an error message if the API could not be reached or\n",
    "               speech was unrecognizable\n",
    "    \"transcription\": `None` if speech could not be transcribed,\n",
    "               otherwise a string containing the transcribed text\n",
    "    \"\"\"\n",
    "    # check that recognizer and microphone arguments are appropriate type\n",
    "    if not isinstance(recognizer, sr.Recognizer):\n",
    "        raise TypeError(\"`recognizer` must be `Recognizer` instance\")\n",
    "\n",
    "    if not isinstance(microphone, sr.Microphone):\n",
    "        raise TypeError(\"`microphone` must be `Microphone` instance\")\n",
    "\n",
    "    # adjust the recognizer sensitivity to ambient noise and record audio\n",
    "    # from the microphone\n",
    "    with microphone as source:\n",
    "        recognizer.adjust_for_ambient_noise(source)\n",
    "        audio = recognizer.listen(source)\n",
    "\n",
    "    # set up the response object\n",
    "    response = {\n",
    "        \"success\": True,\n",
    "        \"error\": None,\n",
    "        \"transcription\": None\n",
    "    }\n",
    "\n",
    "    # try recognizing the speech in the recording\n",
    "    # if a RequestError or UnknownValueError exception is caught,\n",
    "    #     update the response object accordingly\n",
    "    try:\n",
    "        response[\"transcription\"] = recognizer.recognize_google(audio)\n",
    "    except sr.RequestError:\n",
    "        # API was unreachable or unresponsive\n",
    "        response[\"success\"] = False\n",
    "        response[\"error\"] = \"API unavailable\"\n",
    "    except sr.UnknownValueError:\n",
    "        # speech was unintelligible\n",
    "        response[\"error\"] = \"Unable to recognize speech\"\n",
    "\n",
    "    return response\n",
    "\n",
    "\n",
    "if __name__ == \"__main__\":\n",
    "    # set the list of words, maxnumber of guesses, and prompt limit\n",
    "    WORDS = [\"apple\", \"banana\", \"grape\", \"orange\", \"mango\", \"lemon\"]\n",
    "    NUM_GUESSES = 3\n",
    "    PROMPT_LIMIT = 5\n",
    "\n",
    "    # create recognizer and mic instances\n",
    "    recognizer = sr.Recognizer()\n",
    "    microphone = sr.Microphone()\n",
    "\n",
    "    # get a random word from the list\n",
    "    word = random.choice(WORDS)\n",
    "\n",
    "    # format the instructions string\n",
    "    instructions = (\n",
    "        \"I'm thinking of one of these words:\\n\"\n",
    "        \"{words}\\n\"\n",
    "        \"You have {n} tries to guess which one.\\n\"\n",
    "    ).format(words=', '.join(WORDS), n=NUM_GUESSES)\n",
    "\n",
    "    # show instructions and wait 3 seconds before starting the game\n",
    "    print(instructions)\n",
    "    time.sleep(3)\n",
    "\n",
    "    for i in range(NUM_GUESSES):\n",
    "        # get the guess from the user\n",
    "        # if a transcription is returned, break out of the loop and\n",
    "        #     continue\n",
    "        # if no transcription returned and API request failed, break\n",
    "        #     loop and continue\n",
    "        # if API request succeeded but no transcription was returned,\n",
    "        #     re-prompt the user to say their guess again. Do this up\n",
    "        #     to PROMPT_LIMIT times\n",
    "        for j in range(PROMPT_LIMIT):\n",
    "            print('Guess {}. Speak!'.format(i+1))\n",
    "            guess = recognize_speech_from_mic(recognizer, microphone)\n",
    "            if guess[\"transcription\"]:\n",
    "                break\n",
    "            if not guess[\"success\"]:\n",
    "                break\n",
    "            print(\"I didn't catch that. What did you say?\\n\")\n",
    "\n",
    "        # if there was an error, stop the game\n",
    "        if guess[\"error\"]:\n",
    "            print(\"ERROR: {}\".format(guess[\"error\"]))\n",
    "            break\n",
    "\n",
    "        # show the user the transcription\n",
    "        print(\"You said: {}\".format(guess[\"transcription\"]))\n",
    "\n",
    "        # determine if guess is correct and if any attempts remain\n",
    "        guess_is_correct = guess[\"transcription\"].lower() == word.lower()\n",
    "        user_has_more_attempts = i < NUM_GUESSES - 1\n",
    "\n",
    "        # determine if the user has won the game\n",
    "        # if not, repeat the loop if user has more attempts\n",
    "        # if no attempts left, the user loses the game\n",
    "        if guess_is_correct:\n",
    "            print(\"Correct! You win!\".format(word))\n",
    "            break\n",
    "        elif user_has_more_attempts:\n",
    "            print(\"Incorrect. Try again.\\n\")\n",
    "        else:\n",
    "            print(\"Sorry, you lose!\\nI was thinking of '{}'.\".format(word))\n",
    "            break"
   ]
  },
  {
   "cell_type": "code",
   "execution_count": null,
   "metadata": {},
   "outputs": [],
   "source": []
  }
 ],
 "metadata": {
  "kernelspec": {
   "display_name": "Python 3",
   "language": "python",
   "name": "python3"
  },
  "language_info": {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
   "file_extension": ".py",
   "mimetype": "text/x-python",
   "name": "python",
   "nbconvert_exporter": "python",
   "pygments_lexer": "ipython3",
   "version": "3.8.2"
  }
 },
 "nbformat": 4,
 "nbformat_minor": 4
}
