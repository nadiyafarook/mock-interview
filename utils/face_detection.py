import cv2
import numpy as np
from tensorflow import keras
from keras_vggface.vggface import VGGFace
from keras_vggface.utils import preprocess_input
from tensorflow.keras.models import load_model # type: ignore

# Load face detection model (ResNet50 pre-trained on VGGFace2)
face_model = VGGFace(model='resnet50', include_top=False, input_shape=(224, 224, 3), pooling='avg')

# Load pre-trained emotion recognition model
emotion_model = load_model('models/emotion_model.h5')

# Emotion label mapping
emotion_dict = {0: 'Angry', 1: 'Disgust', 2: 'Fear', 3: 'Happy', 4: 'Sad', 5: 'Surprise', 6: 'Neutral'}

def detect_faces_and_emotions(frame):
    # Resize frame to 224x224 for face detection
    resized_frame = cv2.resize(frame, (224, 224))
    preprocessed_frame = np.expand_dims(resized_frame, axis=0)
    preprocessed_frame = preprocess_input(preprocessed_frame, version=2)

    # Face embeddings
    face_embeddings = face_model.predict(preprocessed_frame)

    # Emotion prediction based on face embedding
    emotion_prediction = emotion_model.predict(face_embeddings)
    emotion = np.argmax(emotion_prediction)
    emotion_label = emotion_dict[emotion]

    return emotion_label
