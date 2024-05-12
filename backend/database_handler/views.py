import io
import os
import uuid
import json
import base64

import numpy as np
from PIL import Image

from urllib.parse import urlparse

from django.http import JsonResponse

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.decorators import api_view

from .models import PatientImage, UserAccount
from .serializers import PatientImageSerializer


@api_view(['POST'])
def addImage(request):
    image = getPilImage(request)
    email = request.POST['email']

    imageMediaPath = getImageMediaPath()
    savePath = os.path.join(os.getcwd(), 'media', imageMediaPath)
    image.save(savePath)
    
    user = UserAccount.objects.get(email=email)
    patientImage = PatientImage.objects.create(image=imageMediaPath, user=user)
    patientImage.save()
    
    return JsonResponse({'image_id': patientImage.image_id})


def getPilImage(request):
    image = request.FILES['image'].read()
    return Image.open(io.BytesIO(image))


def getImageMediaPath():
    randomIdentifier = uuid.uuid4()
    return os.path.join('images', f"image_{randomIdentifier}.jpg")


@api_view(['POST'])
def getImageCountForUser(request):
    data = json.loads(request.body)
    email = data['email']
    if email == '':
        return JsonResponse({'imageCount': 0})
    
    user = UserAccount.objects.get(email=email)
    imageCount = PatientImage.objects.filter(user=user).count()

    return JsonResponse({'imageCount': imageCount})


class getImagesForUser(APIView):
    def post(self, request):
        data = request.data
        email = data['email']
        
        user = UserAccount.objects.get(email=email)
        images = PatientImage.objects.filter(user=user).order_by('-image_id')
        serializer = PatientImageSerializer(images, many=True)
        
        return Response(serializer.data)
    
    
@api_view(['POST'])
def getImageFromUrl(request):
    data = json.loads(request.body)
    imageUrl = data['imageUrl']
    
    pilImage = getPilImageFromUrl(imageUrl)
    uriImage = convertPilToUri(pilImage)
    
    return JsonResponse({'image': uriImage})


def getPilImageFromUrl(imageUrl):
    imageFileName = os.path.basename(urlparse(imageUrl).path)
    imageFullPath = os.path.join(os.getcwd(), 'media', 'images', imageFileName)
    
    return Image.open(imageFullPath)  


def convertPilToUri(pilImage):
    buffered = io.BytesIO()
    pilImage.save(buffered, format='JPEG')
    data_uri = base64.b64encode(buffered.getvalue()).decode()
    
    return f"data:image/jpeg;base64,{data_uri}"


@api_view(['POST'])
def deleteImage(request):
    data = json.loads(request.body)
    imageId = data['image_id']
    
    image = PatientImage.objects.get(image_id=imageId)
    image.delete()
    
    return JsonResponse({'message': 'The object was successfully deleted!'})


@api_view(['POST'])
def setPredictedClass(request):
    data = json.loads(request.body)
    imageId = data['image_id']
    predictedClass = data['predicted_class']
    
    image = PatientImage.objects.get(image_id=imageId)
    image.classification = predictedClass
    image.save()
    
    return JsonResponse({'message': 'The predicted class was successfully set!'})
    