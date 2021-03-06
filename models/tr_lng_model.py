import matplotlib.pyplot as plt
import time
import random
import os
import copy
import shutil 
import torch
import torch.nn as nn
import torch.optim as optim
from torch.optim import lr_scheduler
from torchvision import transforms, datasets, models

# Data augmentation and normalization for training
# Just normalization for validation
data_transforms = {
    'train': transforms.Compose([
        transforms.RandomResizedCrop(224),
        transforms.RandomHorizontalFlip(),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ]),
    'val': transforms.Compose([
        transforms.Resize(256),
        transforms.CenterCrop(224),
        transforms.ToTensor(),
        transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
    ]),
}

uploads = "Uploads"
class_folders = [os.path.basename(x[0]) for x in os.walk(uploads)][1:]

def build_model():
    
    
    loc = "Datasets"
    train = os.path.join(loc,'train')
    val = os.path.join(loc,'val')
    
    if not os.path.isdir(train):
        os.mkdir(train)
    if not os.path.isdir(val):
        os.mkdir(val)
                
    def file_copy(files,phase,label,src=uploads,dst=loc):
        for i in files:
            sr = os.path.join(src,label,i)
            dt = os.path.join(dst,phase,label,i)
            shutil.copy(sr,dt)
    global class_folders
    class_folders = [os.path.basename(x[0]) for x in os.walk(uploads)][1:]
    
    for folder in class_folders:
        fdir = os.path.join(uploads,folder)
        image_list = os.listdir(fdir)
        val_list = [image_list.pop(random.randint(0,len(image_list)-1)) for i in range(int(len(image_list)*.1))]
        label = os.path.basename(folder)
    
        for phase in ['train','val']:
            if not os.path.isdir(os.path.join(loc,phase,label)):
                os.mkdir(os.path.join(loc,phase,label)) 
        file_copy(image_list,phase='train',label=label)
        file_copy(val_list,phase='val',label=label)
    
    data_dir = 'Datasets'
    image_datasets = {x: datasets.ImageFolder(os.path.join(data_dir, x),
                                              data_transforms[x])
                      for x in ['train', 'val']}
    dataloaders = {x: torch.utils.data.DataLoader(image_datasets[x], batch_size=4,
                                                 shuffle=True)
                  for x in ['train', 'val']}
    dataset_sizes = {x: len(image_datasets[x]) for x in ['train', 'val']}
    class_names = image_datasets['train'].classes
    
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    
    def train_model(model, criterion, optimizer, scheduler, num_epochs=25):
        since = time.time()
    
        best_model_wts = copy.deepcopy(model.state_dict())
        best_acc = 0.0
    
        for epoch in range(num_epochs):
            print('Epoch {}/{}'.format(epoch, num_epochs - 1))
            print('-' * 10)
    
            # Each epoch has a training and validation phase
            for phase in ['train', 'val']:
                if phase == 'train':
                    model.train()  # Set model to training mode
                else:
                    model.eval()   # Set model to evaluate mode
    
                running_loss = 0.0
                running_corrects = 0
    
                # Iterate over data.
                for inputs, labels in dataloaders[phase]:
                    inputs = inputs.to(device)
                    labels = labels.to(device)
    
                    # zero the parameter gradients
                    optimizer.zero_grad()
    
                    # forward
                    # track history if only in train
                    with torch.set_grad_enabled(phase == 'train'):
                        outputs = model(inputs)
                        _, preds = torch.max(outputs, 1)
                        loss = criterion(outputs, labels)
    
                        # backward + optimize only if in training phase
                        if phase == 'train':
                            loss.backward()
                            optimizer.step()
    
                    # statistics
                    running_loss += loss.item() * inputs.size(0)
                    running_corrects += torch.sum(preds == labels.data)
                if phase == 'train':
                    scheduler.step()
    
                epoch_loss = running_loss / dataset_sizes[phase]
                epoch_acc = running_corrects.double() / dataset_sizes[phase]
    
                print('{} Loss: {:.4f} Acc: {:.4f}'.format(
                    phase, epoch_loss, epoch_acc))
    
                # deep copy the model
                if phase == 'val' and epoch_acc > best_acc:
                    best_acc = epoch_acc
                    best_model_wts = copy.deepcopy(model.state_dict())
    
    
        time_elapsed = time.time() - since
        print('Training complete in {:.0f}m {:.0f}s'.format(
            time_elapsed // 60, time_elapsed % 60))
        print('Best val Acc: {:4f}'.format(best_acc))
    
        # load best model weights
        model.load_state_dict(best_model_wts)
        return model, best_acc.item()
    
    def visualize_model(model, num_images=6):
        was_training = model.training
        model.eval()
        images_so_far = 0
        fig = plt.figure()
    
        with torch.no_grad():
            for i, (inputs, labels) in enumerate(dataloaders['val']):
                inputs = inputs.to(device)
                labels = labels.to(device)
    
                outputs = model(inputs)
                _, preds = torch.max(outputs, 1)
    
                for j in range(inputs.size()[0]):
                    images_so_far += 1
                    ax = plt.subplot(num_images//2, 2, images_so_far)
                    ax.axis('off')
                    ax.set_title('predicted: {}'.format(class_names[preds[j]]))
                    imshow(inputs.cpu().data[j])
    
                    if images_so_far == num_images:
                        model.train(mode=was_training)
                        return
            model.train(mode=was_training)
    
    #Using pre-trained weights
            
    # model_ft = models.resnet18(pretrained=True)
           
    # num_ftrs = model_ft.fc.in_features
    #model_ft.fc = nn.Linear(num_ftrs, 2)
    #model_ft = model_ft.to(device)
    #criterion = nn.CrossEntropyLoss()
    #optimizer_ft = optim.SGD(model_ft.parameters(), lr=0.001, momentum=0.9)
    #exp_lr_scheduler = lr_scheduler.StepLR(optimizer_ft, step_size=7, gamma=0.1)
    #model_ft = train_model(model_ft, criterion, optimizer_ft, exp_lr_scheduler,num_epochs=25)
    #visualize_model(model_ft)
    
    
    #######################################################################
    ######    pre-trained model - as-it-is, except the final layer   ######
    #######################################################################
            
    model_conv = models.resnet18(pretrained=True)
    
    for param in model_conv.parameters():
        param.requires_grad = False
    
    num_ftrs = model_conv.fc.in_features
    model_conv.fc = nn.Linear(num_ftrs, len(class_names))
    
    model_conv = model_conv.to(device)
    
    criterion = nn.CrossEntropyLoss()
    
    optimizer_conv = optim.SGD(model_conv.fc.parameters(), lr=0.001, momentum=0.9)
    exp_lr_scheduler = lr_scheduler.StepLR(optimizer_conv, step_size=7, gamma=0.1)
    
    model_conv = train_model(model_conv, criterion, optimizer_conv,
                             exp_lr_scheduler, num_epochs=1)
    
    return model_conv


    #visualize_model(model_conv)
if __name__ == "__main__":
    build_model()


#https://pytorch.org/tutorials/beginner/transfer_learning_tutorial.html