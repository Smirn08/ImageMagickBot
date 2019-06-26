import re

import torch
from scipy import misc
from PIL import Image

import torch.onnx
from torchvision import transforms

from transformer_net import TransformerNet


def load_image(filename, size=None, scale=None):
    img = Image.open(filename)
    if size is not None:
        img = img.resize((size, size), Image.ANTIALIAS)
    elif scale is not None:
        img = img.resize((int(img.size[0] / scale), int(img.size[1] / scale)), Image.ANTIALIAS)
    return img


def stylize(img_stream, style_type):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    content_image = load_image(img_stream, scale=None)
    content_transform = transforms.Compose([
        transforms.ToTensor(),
        transforms.Lambda(lambda x: x.mul(255))
    ])
    content_image = content_transform(content_image)
    content_image = content_image.unsqueeze(0).to(device)

    with torch.no_grad():
        style_model = TransformerNet()
        models_dir = './saved_models/'
        state_dict = torch.load(models_dir + '{}'.format(style_type))
        for k in list(state_dict.keys()):
            if re.search(r'in\d+\.running_(mean|var)$', k):
                del state_dict[k]
        style_model.load_state_dict(state_dict)
        style_model.to(device)
        output = style_model(content_image).cpu()
    return misc.toimage(output[0])
