import io
from PIL import Image as im
import torch
from django.shortcuts import render
from django.views.generic.edit import CreateView
from .db import crop_analysis
from .forms import ImageUploadForm

def post(request):
    form = ImageUploadForm(request.POST, request.FILES)
    if form.is_valid():
        img = request.FILES.get('image')
        
        uploaded_img_qs = img
        img_bytes = uploaded_img_qs
        img = im.open(img_bytes)

        # Change this to the correct path
        path_hubconfig = "C:/Users/bkimathi/Desktop/app/Cropdetection/yolov5"
        path_weightfile = "C:/Users/bkimathi/Desktop/app/Cropdetection/Trained Models/last.pt"  
        model = torch.hub.load(path_hubconfig, 'custom',
                               path=path_weightfile, source='local')

        results = model(img, size=128)
        results.render()
        for img in results.imgs:
            img_base64 = im.fromarray(img)
            img_base64.save("media/yolo_out", format="JPEG")

        inference_img = "/media/yolo_out"

        form = ImageUploadForm()
        context = {
                "form": form,
                "inference_img": inference_img
            }
        return render(request, 'Cropdetection/Analysis.html', context)

    else:
        form = ImageUploadForm()
        context = {
            "form": form
        }
        return render(request, 'Cropdetection/Analysis.html', context)
        
        
def report_table(request):
    analysis_table = crop_analysis.objects.all()
    context = {'analysis_table':analysis_table}

    return render(request, 'Cropdetection/data.html', context)
        
        
def dashboard(request):
    
    return render(request, 'Cropdetection/index.html')            