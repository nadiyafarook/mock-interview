def generate_feedback(emotion_history):
    # Count occurrences of each emotion
    emotion_count = {}
    for emotion in emotion_history:
        if emotion in emotion_count:
            emotion_count[emotion] += 1
        else:
            emotion_count[emotion] = 1

    # Generate feedback based on predominant emotion
    predominant_emotion = max(emotion_count, key=emotion_count.get)
    
    feedback_text = f"Throughout the interview, you mostly expressed {predominant_emotion} emotions."
    
    # Customize feedback
    if predominant_emotion == 'Happy':
        feedback_text += " You seemed confident and positive!"
    elif predominant_emotion == 'Sad' or predominant_emotion == 'Fear':
        feedback_text += " You might need to work on staying more relaxed."
    else:
        feedback_text += " Keep practicing to express your emotions clearly."

    return feedback_text
