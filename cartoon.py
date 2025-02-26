import cv2
import numpy as np
import requests
import tensorflow as tf
from huggingface_hub import snapshot_download
from PIL import Image


def resize_crop(image):
    h, w, c = np.shape(image)
    if min(h, w) > 720:
        if h > w:
            h, w = int(720 * h / w), 720
        else:
            h, w = 720, int(720 * w / h)
    image = cv2.resize(image, (w, h), interpolation=cv2.INTER_AREA)
    h, w = (h // 8) * 8, (w // 8) * 8
    image = image[:h, :w, :]
    return image


def download_image(url):
    image = Image.open(requests.get(url, stream=True).raw)
    image = image.convert("RGB")
    image = np.array(image)
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    return image


def preprocess_image(image):
    image = resize_crop(image)
    image = image.astype(np.float32) / 127.5 - 1
    image = np.expand_dims(image, axis=0)
    image = tf.constant(image)
    return image


model_path = snapshot_download("sayakpaul/whitebox-cartoonizer")
loaded_model = tf.saved_model.load(model_path)
concrete_func = loaded_model.signatures["serving_default"]




def cartoonize(save_path, image):
    image_url = "https://huggingface.co/spaces/sayakpaul/cartoonizer-demo-onnx/resolve/main/mountain.jpeg"
    image = download_image(image_url)
    preprocessed_image = preprocess_image(image)
    result = concrete_func(preprocessed_image)["final_output:0"]
    output = (result[0].numpy() + 1.0) * 127.5
    output = np.clip(output, 0, 255).astype(np.uint8)
    output = cv2.cvtColor(output, cv2.COLOR_BGR2RGB)
    output_image = Image.fromarray(output)
    output_image.save(save_path)


