import io
from PIL import Image as im
import torch
from django.shortcuts import render
from django.views.generic.edit import CreateView
from .db import crop_analysis,CropIdentification
from .forms import ImageUploadForm
import datetime
import base64
import tensorflow as tf
import tensorflow_hub as hub
import numpy as np

class_labels ={ 0 : 'jute', 1 : 'maize', 2 : 'rice', 3 : 'sugarcane', 4 : 'tomato', 5 : 'wheat'}
tfmodel = tf.keras.models.load_model("C:/Users/bkimathi/app/Cropdetection/Trained Models/2022-03-02-12_07-cropdetectionmodel.h5")
IMG_SIZE = 224

def getcrop(img):
    # turn image into numerical tensors
    image = tf.image.decode_jpeg(img, channels=3)
    # covert colour channel values
    image = tf.image.convert_image_dtype(image, tf.float32)
    # resize image
    image = tf.image.resize(image, size=[IMG_SIZE, IMG_SIZE])
    image = np.expand_dims(image, axis=0)
    pred = tfmodel.predict(image)
    pred_crop = class_labels[np.argmax(pred)]
    return pred_crop


def post(request):
    form = ImageUploadForm(request.POST, request.FILES)
    if form.is_valid():
        image = request.FILES.get('image')
        
        img = image.file.read()
        
        #decode image from bytes
        encoded_img = im.open(image)       


        pred_crop = getcrop(img)


        if pred_crop == 'tomato':
            path_hubconfig = "C:/Users/bkimathi/app/Cropdetection/yolov5"
            path_weightfile = "C:/Users/bkimathi/app/Cropdetection/Trained Models/last.pt"  
            
            
            model = torch.hub.load(path_hubconfig, 'custom',
                               path=path_weightfile, source='local')
            results = model(encoded_img, size=128)
            results.render()
            for img in results.imgs:
                img_base64 = im.fromarray(img)
                img_base64.save("media/yolo_out", format="JPEG")

            inference_img = "/media/yolo_out"
            post = crop_analysis()
            post.Analysis_REF_No 
            post.Crop = pred_crop
            #post.Status = Status
            post.Date_created = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            #post.Image = inference_img
            post.save()
            form = ImageUploadForm()
            context = {
                "form": form,
                "inference_img": inference_img
            }
    
        else:
            message = print('Crop is not in detection Class')
            context = {"message": message}
    
    else:
        form = ImageUploadForm()
        context = {
            "form": form
        }
    return render(request, 'Cropdetection/Analysis.html', context)    
 
        
def report_table(request):
    analysis_table = crop_analysis.objects.all()
    context = {'analysis_table': analysis_table}

    return render(request, 'Cropdetection/data.html', context)
        
        
def dashboard(request):
    
    return render(request, 'Cropdetection/index.html')            