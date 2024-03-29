from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from flask_restful import Api, Resource, reqparse
import cv2

app = Flask(__name__)
CORS(app)
api = Api(app)

net = cv2.dnn.readNetFromCaffe("deploy.prototxt", "mobilenet_iter_73000.caffemodel")

def count_people(image_path):
    image = cv2.imread(image_path)

    if image is None:
        print(f"Error: Unable to open the image file '{image_path}'. Check the file path/integrity.")
        return

    height, width = image.shape[:2]

    blob = cv2.dnn.blobFromImage(image, 0.007843, (300, 300), 127.5)
    net.setInput(blob)
    detections = net.forward()

    people_count = 0
    for i in range(detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.2:
            class_id = int(detections[0, 0, i, 1])
            if class_id == 15:
                people_count += 1

    return people_count

class PeopleCountResource(Resource):
    def post(self):
        # Check if the 'image' file is present in the request
        if 'image' not in request.files:
            return {'error': 'No image file provided'}

        # Get the image file from the request
        file = request.files['image']

        # Save the image to a temporary file
        image_path = 'temp.jpg'
        file.save(image_path)

        # Count people using the existing function
        people_count = count_people(image_path)

        # Return the result as JSON
        return {'people_count': people_count}

api.add_resource(PeopleCountResource, '/')

@app.route('/', methods=['GET', 'POST'])
def count_people_api():
    if request.method == 'POST':
        # Check if the 'image' file is present in the request
        if 'image' not in request.files:
            return jsonify({'error': 'No image file provided'})

        # Get the image file from the request
        file = request.files['image']

        # Save the image to a temporary file
        image_path = 'temp.jpg'
        file.save(image_path)

        # Count people using the existing function
        people_count = count_people(image_path)

        # Return the result as JSON
        return jsonify({'people_count': people_count})
    else:
        # Render a simple HTML page with a file upload form
        return render_template('crowd-counting.html')

if __name__ == "__main__":
    app.run(debug=True)