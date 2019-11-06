from flask import Flask, render_template, url_for, request, jsonify
import numpy as np
import io
import re
import base64
import cv2
from PIL import Image
import tensorflow as tf

new_model = tf.keras.models.load_model('my_model.h5')

image_dict = {}
global i
i=0
app = Flask(__name__)

@app.route('/')
def hello_world():
	return render_template('home.html')




@app.route('/imgrec', methods=['POST'])
def hello_image():
    global i
	######### reading image from from server
    image_b64 = request.values['imageBase64']

    ######### removing some information like data:img:base64
    ######### this is string data
    image_data = re.sub('^data:image/.+;base64,', '', image_b64)     #.decode('base64')

    ######### converting string data into bytes
    imgdata = base64.b64decode(image_data)

    ######### saving image received from server to local images folder
    image_dict[i]=i
    #filename = 'some_img.jpg'
    with open('images/'+f'{image_dict[i]}'+'.jpg', 'wb') as f:
        f.write(imgdata)

    print ('Image received and saved')
    
    ######### loading and showing data directly without saving locally
    """
    image = Image.open(io.BytesIO(imgdata)).convert('L')
    img = np.array(image)
    img = np.resize(img, (28,28,1))
    img = img/255
    print(img.shape)
    """

    cim = cv2.imread('images/'+f'{image_dict[i]}'+'.jpg', -1)
    g_img = cv2.cvtColor(cim, cv2.COLOR_BGR2GRAY)
    resized = cv2.resize(g_img, (28,28), interpolation = cv2.INTER_AREA)/255

    prediction = new_model.predict_classes(resized.reshape(1,28,28))
    print(prediction)
    print(f'the number is {prediction[0]}')
    resp_dict = {'pred': int(prediction[0])}

    #resp = jsonify(resp_dict)
    i = i+1
    return jsonify(resp_dict)


if __name__ == '__main__':
	app.run(debug = True)
