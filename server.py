from flask import Flask, render_template, request, jsonify
from flask_bootstrap import Bootstrap
from tensorflow.keras.models import Sequential, save_model, load_model
import cv2
import numpy as np


app = Flask(__name__)
Bootstrap(app)

@app.route('/', methods=['GET',"POST"])
def main():

	if request.method == 'POST':

		imagefile = request.get_json()
		image_path = "./uploads/" + imagefile.filename
		imagefile.save(image_path)
		
		model = load_model("./models/model_covid", compile = True)
		images = []
		image = cv2.imread(image_path)

		if image.shape[2]==1:

			print(image.shape[2])
			image = np.dstack([image, image, image])

		image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
		image = cv2.resize(image, (224, 224))
		image = image / 255.0 # Normalize images to range [0,1]

		images.append(image)

		images = np.array(images)

		prediction = model.predict(images)
		#print(prediction)

		#prediction = np.round(prediction[0][1]*100,2)
		prediction = np.round(prediction[0][1]*100,2)


		#return jsonify({"result": prediction})
		return jsonify({"result": "POST"})
	
	else:
		return jsonify({"result": "GET"})
if __name__ == '__main__':
	app.run(debug=True)