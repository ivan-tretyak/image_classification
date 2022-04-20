import base64
import io
from torchvision import transforms
from PIL import Image
import torch
from algorithm.model_transform import SwinTransformer


def string_to_PIL(base64string):
    base = base64.b64decode(base64string)
    return Image.open(io.BytesIO(base))

def get_tensor_by_PIL(pil, size):
    img = pil.resize(size).convert('RGB')
    convert_tensor = transforms.ToTensor()
    tensor = convert_tensor(img)
    return tensor.unsqueeze(0)

def main(model, clss, PIL_image):
    cls_index = model.forward(get_tensor_by_PIL(PIL_image, (384, 384))).argmax()
    return clss[cls_index]

def get_clss():
    clss = []
    with open('algorithm/classes.txt') as f:
        for line in f:
            clss.append(line.replace('\n', ''))
    return clss

def load_model():
    model = SwinTransformer(img_size=384, drop_path_rate=0.2,
                            embed_dim=192, depths=[2, 2, 18, 2],
                            num_heads=[6, 12, 24, 48], window_size=12)
    model.load_state_dict(torch.load('algorithm/swin_large_patch4_window12_384_22kto1k.pth')['model'])
    return model