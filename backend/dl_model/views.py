import io
import os

import numpy as np
from PIL import Image

from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

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
    
    image = np.array(image, dtype='float64')
    image = np.expand_dims(image, axis=0)
    image /= 255.
    
    return JsonResponse({'prediction': 0})
    
    
def getPilImage(request):
    image = request.FILES['image'].read()
    image = Image.open(io.BytesIO(image))
    return image.convert('RGB')