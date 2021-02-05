from flask import Flask, render_template, url_for, request, jsonify
import numpy as np
import io
import re
import base64
import cv2
from PIL import Image
import tensorflow as tf

new_model = tf.keras.models.load_model('my_model.h5')

app = Flask(__name__)

@app.route('/')
def hello_world():
	return render_template('home.html')




@app.route('/imgrec', methods=['POST'])
def hello_image():
	######### reading image from from server
    image_b64 = request.values['imageBase64']
    #print(image_b64)

    ######### removing some information like data:img:base64
    ######### this is string data
    image_data = re.sub('^data:image/.+;base64,', '', image_b64)
    #print(image_data)

    ######### converting string data into bytes
    imgdata = base64.b64decode(image_data)
    print(len(imgdata))

    print ('Image received and ready to be processed')

    
    #########-----DATA PREPROCESSING, FROM string to bytes to array -----##############
    # NOTES-----a string is a sequence of characters, ie unicode codepoints; these are an abstract concept, and can't be directly stored on disk. A byte string is a sequence of, unsurprisingly, bytes - things that can be stored on disk. The mapping between them is an encoding 
    img=np.frombuffer(imgdata, np.uint8) #converting byte data to 1-D numpy array
    print(img.shape)
    img=cv2.imdecode(img, cv2.IMREAD_COLOR) #converting 1-D array to original canvas data of shape 500x500x3
    print(img.shape) #same as shape of canvas i.e, 500x500 x3(see html file)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY) # converting image to GRAY, i.e, shape becomes 500x500
    print(img.shape)
    img = cv2.resize(img, dsize=(28, 28), interpolation=cv2.INTER_AREA) # resizing to required 28x28, INTER_AREA IS USED WHEN SHRINKING AND OTHER INTERPOLATION METHOD SUCH AS INTER_CUBIC INTER_LINEAR etc WHILE ENLARGING 
    img = img/255
    print(img.shape)
   

    ###############----PREDICTION----###########################
    prediction = new_model.predict(img.reshape(1,28,28)) #input (batch_size, dimensions)
    #outputs 1-d of shape equals to number of classes
    print(np.argmax(prediction)) #getting the index of highest value
    print(f'the number is {np.argmax(prediction)}')
    resp_dict = {'pred': int(np.argmax(prediction))} # making dictionary to send it back through POST request

    #resp = jsonify(resp_dict)
    return jsonify(resp_dict)


if __name__ == '__main__':
	app.run(debug = True)
