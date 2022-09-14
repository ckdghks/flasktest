from torchinfo import summary
import timm
import cv2
import torch
import numpy as np
import matplotlib.pyplot as plt
from visdom import Visdom
from torchvision.models.feature_extraction import get_graph_node_names, create_feature_extractor
import torchvision
import torch.onnx

# model_list = timm.list_models('swin*',pretrained=True)
# model = timm.create_model('swinv2_tiny_window16_256', pretrained=True)
model = timm.create_model('resnet50d', pretrained=True)
# summary(model)
# print(model.default_cfg)

# # export model
# params = model.state_dict()
# dummy_data = torch.empty(1, 3, 256, 256, dtype= torch.float32)
# torch.onnx.export(model, dummy_data, "res50d.onnx")

img = cv2.imread('./static/images/test.jpg', cv2.IMREAD_COLOR)
# img = cv2.resize(img, (224, 224))

image= torch.as_tensor(np.array(img, dtype=np.float32)).transpose(2, 0)[None]

feature_output = model.forward_features(image)

def visualize_feature_output(t):
    plt.imshow(t[0].transpose(0, 2).sum(-1).detach().numpy())
    plt.show()


model = timm.create_model('resnet50d', pretrained=True, features_only=True)
out = model(image)
print(len(out))

# for o in out:
#     visualize_feature_output(o)


model = timm.create_model('resnet50d', pretrained=True, exportable=True)
nodes, _ = get_graph_node_names(model)
# print(nodes)


features = {'act1': 'out'}
features = {'layer4.2.act3': 'out'}
feature_extractor = create_feature_extractor(model, return_nodes=features)

out = feature_extractor(image)
plt.imshow(out['out'][0].transpose(0, 2).sum(-1).detach().numpy())
plt.show()
print(out['out'][0].transpose(0, 2).sum(-1).detach().numpy().shape) # (15, 20)
