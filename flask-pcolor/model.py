import torch
from efficientnet_pytorch import EfficientNet
import torchvision.transforms as transforms
import torchvision.datasets as datasets
from torch.utils.data import DataLoader,Dataset
from PIL import Image
import matplotlib.pyplot as plt
import numpy as np
import os
def predict_pcolor(image_path):
    os.environ['CUDA_VISIBLE_DEVICES'] = '1'
    device = torch.device('cpu')  
    model = EfficientNet.from_pretrained('efficientnet-b0', num_classes=10)
    model.load_state_dict(torch.load('effi.pth', map_location=device))
    classes=['falldeep','fallmute','fallstrong','springbright','springlight', 'summerbright',
    'summerlight','summermute','winterbright','winterdeep']
    img = Image.open(f'./{image_path}')
    transform_norm = transforms.Compose([transforms.ToTensor(), 
    transforms.Resize((224,224)),transforms.Normalize( [0.485, 0.456, 0.406] , [0.229, 0.224, 0.225])])
    img_normalized = transform_norm(img).float()
    img_normalized = img_normalized.unsqueeze_(0)
    img_normalized = img_normalized.to(device)
    with torch.no_grad():
        model.eval()  
        output =model(img_normalized)
        index = output.data.cpu().numpy().argmax()
        class_name = classes[index]
        os.remove(f'./{image_path}')
        return class_name