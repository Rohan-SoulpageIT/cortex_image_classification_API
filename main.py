import os
#import magic
#import urllib.request
import io
from utils.app import app
from PIL import Image
import torch
from flask import Flask, flash, request, redirect, render_template, send_file
from models import tr_lng_model
from utils.data_base import ImageData
from utils.data_base import db

@app.route('/')
def index():        
    return render_template('upload.html')

@app.route('/',methods=['POST'])
def upload():
    if request.method == 'POST':
        files = request.files.getlist('files[]')
        cat_name = request.form.get('cls')
        for file in files:
            if file:
                #storing the values in the database
                newfile = ImageData(name = file.filename,pic = file.read())
                db.session.add(newfile)
                db.session.commit()
                #storing the images in the upload folder
                loc = os.path.join(app.config['UPLOAD_FOLDER'],cat_name)
                print("\nThe location")
                print(loc)
                if not os.path.isdir(loc):
                    os.mkdir(loc)
                file.save(os.path.join(loc, file.filename))

        return redirect('/')

model = {}
def predict(imb):
    image = Image.open(io.BytesIO(imb))
    tnsr = tr_lng_model.data_transforms['val'](image).unsqueeze(0)
    outputs = model(tnsr)
    _, preds = outputs.max(1)
    predId = preds.item()
    return predId
    
@app.route('/build')
def classifier():
    global model
#    score = 0.9459
    model,score = tr_lng_model.build_model()
    score = round(score,3)
    return render_template('predict.html',score=score)

@app.route('/output', methods=['POST'])
def prediction():
    if request.method == 'POST':
        file= request.files['file']
        img_bytes = file.read()
    predId = predict(img_bytes)
    pred = "The image belongs to the category: {}".format(tr_lng_model.class_folders[predId])
    return render_template('output.html',pred=pred)

@app.route('/return_model')
def download_model():
    PATH = os.path.join('.\weights','model.pt')
    torch.save(model.state_dict(),PATH)
    model_loc = os.path.join("..\weights","model.pt")
    return send_file(model_loc)


if __name__ == "__main__":
    app.run()