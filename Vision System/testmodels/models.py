import torchvision
def get_model(min_size=800):
    # initialize the model
    model = torchvision.models.detection.keypointrcnn_resnet50_fpn(pretrained=True,
                                                                   num_keypoints=17, 
                                                                   min_size=min_size)
    return model