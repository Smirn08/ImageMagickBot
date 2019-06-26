import torch
from scipy import misc

import torchvision.models as models

from model_backend import *


class StyleTransferModel:
    def __init__(self):
        self.device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
        print(f'bot running on: {self.device}')

        self.cnn = models.vgg19(pretrained=True).features.eval()

    def transfer_style(self, content_img, style_img):
        content_img = process_image(content_img)
        style_img = process_image(style_img)

        input_img = content_img.clone()

        output = self.run_style_transfer(
            self.cnn, cnn_normalization_mean,
            cnn_normalization_std, content_img,
            style_img, input_img
        ).cpu()

        return misc.toimage(output[0])

    def run_style_transfer(
        self, cnn, normalization_mean, normalization_std,
        content_img, style_img, input_img, num_steps=500,
        style_weight=100000, content_weight=1
    ):
        """Run the style transfer."""

        print('Building the style transfer model..')

        model, style_losses, content_losses = get_style_model_and_losses(
            cnn, normalization_mean, normalization_std,
            style_img, content_img, self.device
        )
        optimizer = get_input_optimizer(input_img)

        print('Optimizing..')
        run = [0]
        while run[0] <= num_steps:

            def closure():
                """correct the values
                это для того, чтобы значения тензора картинки не
                выходили за пределы [0;1]
                """

                input_img.data.clamp_(0, 1)

                optimizer.zero_grad()
                model(input_img)
                style_score = 0
                content_score = 0

                for sl in style_losses:
                    style_score += sl.loss
                for cl in content_losses:
                    content_score += cl.loss

                # взвешивание ошибки
                style_score *= style_weight
                content_score *= content_weight

                loss = style_score + content_score
                loss.backward()

                run[0] += 1
                if run[0] % 50 == 0:
                    print(f'run {run}:')
                    print(f'Style Loss : {style_score.item():4f} Content Loss: {content_score.item():4f}')
                    print()

                return style_score + content_score

            optimizer.step(closure)

        # a last correction...
        input_img.data.clamp_(0, 1)

        return input_img.detach()
