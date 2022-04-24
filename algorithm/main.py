import base64
import io
import re

import torchvision
from torchvision import transforms
from PIL import Image


def string_to_PIL(json):
    base = base64.b64decode(json['data']['src'])
    return Image.open(io.BytesIO(base))

def get_tensor_by_PIL(pil, size):
    img = pil.resize(size).convert('RGB')
    convert_tensor = transforms.ToTensor()
    tensor = convert_tensor(img)
    return tensor.unsqueeze(0)

def main(model, json):
    clss = get_clss()
    pil_image = string_to_PIL(json)
    cls_index = model.forward(get_tensor_by_PIL(pil_image, (384, 384))).argmax()
    cls = clss[cls_index]
    cls_number = re.match('n\d{8}', cls)[0]
    cls = cls.split(f"{cls_number} ")
    cls[0] = cls_number
    return cls

def get_clss():
    clss = []
    with open('algorithm/classes.txt') as f:
        for line in f:
            clss.append(line.replace('\n', ''))
    return clss

def load_model():
    model = torchvision.models.efficientnet_b7(pretrained=True)
    model.eval()
    return model