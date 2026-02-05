Feature: Single Speaker
  As a recorder, with one speaker in the meeting, I want to turn the audio into transcript.

  Scenario: Small single speaker audio file transcription
    Given OpenAI transcription API replys the following when the model is "gpt-4o-transcribe-diarize":
    """
    {
      "text": "Hello, how are you?",
    }
    """
    When I convert the audio file "small-single-speaker.wav" into transcript
    Then the transcript should be "Hello, how are you?"
