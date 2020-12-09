import os
import numpy as np
import keras
from keras_preprocessing import image
from flask import Flask, redirect, url_for, request, render_template,flash
from werkzeug.utils import secure_filename
import sqlite3


# Define a flask app
app = Flask(__name__)

app.config['SECRET_KEY'] = '50e097b3bfa5bb9ce953'

model = keras.models.load_model('PlantDNet.h5', compile=False)

def model_predict(img_path, model):
    img = image.load_img(img_path, grayscale=False, target_size=(64, 64))
    show_img = image.load_img(img_path, grayscale=False, target_size=(64, 64))
    x = image.img_to_array(img)
    x = np.expand_dims(x, axis=0)
    x = np.array(x, 'float32')
    x /= 255
    preds = model.predict(x)
    return preds


@app.route('/', methods=['GET'])
def index():
    # Main page
    return render_template('index.html')


@app.route('/predict', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        # Get the file from post request
        f = request.files['file']

        # Save the file to ./uploads
        basepath = os.path.dirname(__file__)
        file_path = os.path.join(
            basepath, 'uploads', secure_filename(f.filename))
        f.save(file_path)

        # Make prediction
        preds = model_predict(file_path, model)
        print(preds[0])

        # x = x.reshape([64, 64]);
        disease_class = ['Pepper__bell___Bacterial_spot',    'Pepper__bell___healthy', 'Potato___Early_blight','Potato___Late_blight', 'Potato___healthy', 'Tomato_Bacterial_spot', 'Tomato_Early_blight', 'Tomato_Late_blight', 'Tomato_Leaf_Mold','Tomato_Septoria_leaf_spot',
'Tomato_Spider_mites_Two_spotted_spider_mite','Tomato__Target_Spot','Tomato__Tomato_ YellowLeaf__Curl_Virus','Tomato__Tomato_mosaic_virus', 'Tomato_healthy']
        a = preds[0]
        ind = np.argmax(a)
        print('Prediction:', disease_class[ind])

        result = disease_class[ind]
        id =int(ind)
        if(id!=1 and id!=4 and id!=14):
                count=1
                conn = sqlite3.connect('plant_result.db')

                c = conn.cursor()
                c.execute("SELECT * FROM sampletb WHERE id=:id",{'id':id+1})

                #print(c.fetchall())
                global data
                data = c.fetchall()
                print(data)
                #print(data[0])
                conn.commit()
                c.close()
                conn.close()
        return result
    return None

@app.route('/remedies', methods=['GET', 'POST'])
def remedies():
    name = data[0][1]
    reason = data[0][2]
    treatment = data[0][3]
    return render_template('remedies.html',name=name, reason=reason,    treat=treatment)


if __name__ == '__main__':
    app.run()
