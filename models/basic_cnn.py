
import numpy as np
import torch
import torchvision
import torchvision.transforms as transforms
from torch.autograd import Variable
import torch.nn.functional as F

class SimpleCNN(torch.nn.Module):
    def __init__(self):
        super(SimpleCNN,self).__init__()
        self.conv1 = toch.nn.Conv2d(3,18,kernel_size=3,stride=1,padding=1)
        self.pool = toch.nn.MaxPool2d(kernel_size=2,stride=2,padding=0)
        
        self.fc1 = 