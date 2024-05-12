import io
import os

import numpy as np
from PIL import Image

from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

from keras.applications.vgg19 import preprocess_input
from .model_architecture import chexnet_model

model = chexnet_model()

base_dir = os.path.dirname(os.path.abspath(__file__))
weights_path = os.path.join(base_dir, 'weights.h5')
model.load_weights(weights_path)
print('*'*50, 'Model loaded', '*'*50)

class_mapping = {
    0: 'atelectasis',
    1: 'effusion',
    2: 'infiltration',
    3: 'no_finding',
    4: 'nodule',
    5: 'pneumonia'
}

@api_view(['POST'])
def inference(request):
    image = getPilImage(request)
    image = image.resize((224, 224))
    
    image = np.array(image)
    image = image.reshape((1, image.shape[0], image.shape[1], image.shape[2]))
    image = preprocess_input(image)
    
    predictions = model.predict(image)
    max_index = np.argmax(predictions)
    predicted_class = class_mapping[max_index]
    
    return JsonResponse({'prediction': predicted_class})
    
    
def getPilImage(request):
    image = request.FILES['image'].read()
    image = Image.open(io.BytesIO(image))
    return image.convert('RGB')