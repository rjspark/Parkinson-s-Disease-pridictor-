import numpy as np
from flask import Flask, request, render_template
import pickle

# Initialize Flask app
app = Flask(__name__)

# Load the trained model
model = pickle.load(open('model.pkl', 'rb'))

# Route for homepage
@app.route('/')
def index():
    return render_template("index.html")

# Route to handle prediction
@app.route('/predict', methods=['POST'])
def predict():
    try:
        # Get the input text from the form
        input_text = request.form['text']

        # Convert comma-separated string into a numpy array
        input_values = input_text.split(',')
        np_data = np.asarray(input_values, dtype=np.float32).reshape(1, -1)

        # Perform prediction
        prediction = model.predict(np_data)

        # Interpret the result
        if prediction[0] == 1:
            output = "⚠️ This person  has Parkinson's Disease."
        else:
            output = "✅ This person is not having Parkinson's Disease."

        return render_template("index.html", message=output)

    except Exception as e:
        # Handle errors like wrong input format
        return render_template("index.html", message=f"❌ Error: {str(e)}")

# Run the Flask app
if __name__ == "__main__":
    app.run(debug=True)