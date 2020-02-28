File structure:
```
root.
├───Datasets
├───models
│   └───__pycache__
├───networks
├───notebooks
├───Uploads
├───utils
│   ├───templates
│   └───__pycache__
└───weights
```
To use this run ```$ python main.py``` in the root directory

```main.py``` first renders a template for uploading files with category names, and then train a Pytorch image classifier model on the uploaded images. It then provides for prediction on a new image uploaded by the user and allows the model to be downloaded.

html templates are saved in the ```utils/templates``` folder

Uploaded files are saved in the ```Uploads``` directory in relevent folders created based on the category names provided by user while uploading images. These category names are used as labels for training

```models/tr_lng_model.py``` is where image transformations, and RESNET re-training happens. It returns, the model object and the best validation score across different epochs

```Datasets``` folder is used to store the train and validation sets created using the uploaded images

The trained model is saved in the ```weights``` folder
