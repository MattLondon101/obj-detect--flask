import os 
from flask import Flask, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
os.chdir(os.getcwd())
cuwd=os.getcwd()

app = Flask(__name__)

from keras.models import load_model 
from keras.backend import set_session
from skimage.transform import resize 
import matplotlib.pyplot as plt
import tensorflow as tf
import numpy as np 

print("Loading model") 
global sess

sess = tf.Session()
# sess=tf.compat.v1.Session()

set_session(sess)
# tf.compat.v1.keras.backend.set_session(sess)

global model 

modelfile=os.path.join(cuwd,'mlweb3/my_cifar10_model.h5')

model = load_model(modelfile) 
global graph
graph = tf.get_default_graph()

@app.route('/', methods=['GET', 'POST']) 
def main_page():
    if request.method == 'POST':
        file = request.files['file']
        filename = secure_filename(file.filename)
        file.save(os.path.join(cuwd,'mlweb3/uploads', filename))
        return redirect(url_for('prediction', filename=filename))
    return render_template('index.html')

@app.route('/mlweb3/prediction/<filename>') 
def prediction(filename):
    #Step 1
    my_image = plt.imread(os.path.join(cuwd,'mlweb3/uploads', filename))
    #Step 2
    my_image_re = resize(my_image, (32,32,3))
    
    #Step 3
    with graph.as_default():
      set_session(sess)
      probabilities = model.predict(np.array( [my_image_re,] ))[0,:]
      print(probabilities)
      #Step 4
      number_to_class = ['airplane', 'automobile', 'bird', 'cat', 'deer', 'dog', 'frog', 'horse', 'ship', 
'truck']
      index = np.argsort(probabilities)
      predictions = {
        "class1":number_to_class[index[9]],
        "class2":number_to_class[index[8]],
        "class3":number_to_class[index[7]],
        "prob1":probabilities[index[9]],
        "prob2":probabilities[index[8]],
        "prob3":probabilities[index[7]],
      }
    #Step 5
    return render_template('predict.html', predictions=predictions)

app.run(host='0.0.0.1', port=80)
