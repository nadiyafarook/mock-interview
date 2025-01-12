import cv2
import numpy as np
from tensorflow.keras.applications import ResNet50
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.models import Model
from tensorflow.keras.preprocessing.image import img_to_array, preprocess_input
import os

# Load the pre-trained ResNet50 model
def load_emotion_model():
    base_model = ResNet50(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
    
    # Add custom layers for emotion recognition
    x = base_model.output
    x = GlobalAveragePooling2D()(x)
    x = Dense(1024, activation='relu')(x)
    predictions = Dense(7, activation='softmax')(x)  # Assuming 7 emotion classes
    
    # Final model
    model = Model(inputs=base_model.input, outputs=predictions)
    
    # Load the trained weights
    model_path = os.path.join('models', 'emotion_resnet50_model.h5')
    model.load_weights(model_path)
    
    return model

# Function to detect emotions from video frames
def predict_emotion(frame, model):
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray_frame, 1.3, 5)

    for (x, y, w, h) in faces:
        face = frame[y:y + h, x:x + w]
        face = cv2.resize(face, (224, 224))
        face = img_to_array(face)
        face = np.expand_dims(face, axis=0)
        face = preprocess_input(face)

        # Predict emotion
        emotion_preds = model.predict(face)
        emotion_label = np.argmax(emotion_preds)
        return emotion_label
