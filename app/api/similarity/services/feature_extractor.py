import tensorflow as tf
import tensorflow_hub as hub
from PIL import Image
import numpy as np
from app.config.settings import model_settings

class FeatureExtractor:
    def __init__(self , model_url, width, height):
        self.layer = hub.KerasLayer(model_url)
        self.model = tf.keras.Sequential([self.layer])
        self.IMAGE_SHAPE=(width, height)
    

    def extract(self, image: Image.Image) -> np.ndarray:
        file = image.resize(self.IMAGE_SHAPE)
        # file = np.stack((file,)*3, axis=-1)
        file = np.array(file)/255.0
        embedding = self.model.predict(file[np.newaxis, ...])
        vgg16_feature_np = np.array(embedding)
        flattended_feature = vgg16_feature_np.flatten()

        return flattended_feature
    
    


feature_extractor = FeatureExtractor(
    model_settings.MODEL_URL,
    model_settings.IMAGE_WIDTH,
    model_settings.IMAGE_HEIGHT
)

