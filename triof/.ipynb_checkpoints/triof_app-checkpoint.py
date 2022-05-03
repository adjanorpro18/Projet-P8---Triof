from flask import Flask, render_template, request
from src.utils import *
from base64 import b64encode
import numpy as np
from io import BytesIO

app = Flask(__name__)


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/start')
def insert():
    open_waste_slot()
    picture, path_return = take_trash_picture()
    PIL_image = Image.fromarray(np.uint8(picture)).convert('RGB')
    data = BytesIO()
    PIL_image.save(data, "JPEG")
    
    data64 = b64encode(data.getvalue()) 
    PIL_image = u'data:img;base64,'+ data64.decode('utf-8') 

    return render_template('insert.html', picture= PIL_image, path=path_return)


@app.route('/waste/pick-type', methods=['POST'])
def pick_type():
    close_waste_slot()
    picture, path_return = take_trash_picture()
    PIL_image = Image.fromarray(np.uint8(picture)).convert('RGB')
    data = BytesIO()
    PIL_image.save(data, "JPEG")
    
    data64 = b64encode(data.getvalue()) 
    PIL_image = u'data:img;base64,'+ data64.decode('utf-8') 

    img = str(request.form['path_return'])
    # print(img)

    pred = predictions(img)

    return render_template('type.html', picture= PIL_image, path=path_return, prediction= pred)

    
    

    # picture, path_return = take_trash_picture()
    # PIL_image = Image.fromarray(np.uint8(picture)).convert('RGB')
    # data = BytesIO()
    # img_show = PIL_image.save(data, "JPEG")
    # pred = predictions(img)
    # print(pred)
   
    
    return render_template('type.html', prediction = pred)


@app.route('/confirmation', methods=['POST'])
def confirmation():
    waste_type = request.form['type']

    process_waste(waste_type)
    return render_template('confirmation.html')




if __name__ == "__main__":
    app.run(debug=True)
