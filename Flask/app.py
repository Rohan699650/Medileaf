from flask import Flask, request, jsonify
from flask_cors import CORS
import tensorflow as tf
import numpy as np
from PIL import Image
import io
import os
import re # Import regular expression module

app = Flask(__name__)
CORS(app, origins=["http://localhost:3000"])

# --- Model Loading ---
try:
    model = tf.keras.models.load_model('trained_effb2.h5')
    print("Model loaded successfully!")
except Exception as e:
    print(f"Error loading model: {e}")
    model = None

# --- Class Names Loading ---
CLASS_NAMES = []
try:
    with open('classes.txt', 'r') as f:
        CLASS_NAMES = [line.strip() for line in f.readlines()]
    print(f"Loaded {len(CLASS_NAMES)} class names from classes.txt")
except FileNotFoundError:
    print("Error: classes.txt not found. Prediction names will not be available.")
except Exception as e:
    print(f"Error reading classes.txt: {e}")

# --- Data Loading Functions ---

def load_disease_data(filepath='diseases.txt'):
    disease_map = {}
    try:
        with open(filepath, 'r') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                if ':' in line:
                    disease, leaves = line.split(':', 1)
                    disease_map[disease.strip().lower()] = [leaf.strip() for leaf in leaves.split(',')]
        print(f"Loaded {len(disease_map)} disease entries from {filepath}")
    except FileNotFoundError:
        print(f"Error: {filepath} not found.")
    except Exception as e:
        print(f"Error reading {filepath}: {e}")
    return disease_map

# Function to load disease-to-remedy mapping with numbered disease headers
def load_remedy_data(filepath='remedies.txt'):
    remedy_map = {}
    current_disease = None
    current_remedies = []
    line_num = 0 # For better error reporting
    try:
        with open(filepath, 'r', encoding='utf-8') as f: # Specify encoding for safety
            for line in f:
                line_num += 1
                stripped_line = line.strip() # Use a different variable name

                if not stripped_line: # Skip empty lines
                    continue

                # Debug print for each line being processed
                print(f"Processing line {line_num}: '{stripped_line}'")

                # Check for a new disease heading: starts with a number, a period, and a space
                match = re.match(r'^\d+\.\s(.+)', stripped_line) # Capture the disease name
                if match:
                    # If we were collecting remedies for a previous disease, save them
                    if current_disease and current_remedies:
                        remedy_map[current_disease.lower()] = current_remedies
                        print(f"  Saved '{current_disease.lower()}': {remedy_map[current_disease.lower()]}")

                    # Extract the disease name from the captured group
                    current_disease = match.group(1).strip()
                    current_remedies = [] # Reset for the new disease
                    print(f"  New disease header found: '{current_disease}'")
                elif stripped_line.startswith('• ') and current_disease: # Remedy bullet point
                    remedy_point = stripped_line[2:].strip()
                    current_remedies.append(remedy_point)
                    print(f"  Remedy point added: '{remedy_point}'")
                else:
                    print(f"  Skipping line {line_num}: Does not match disease header or remedy format.")


            # Save the last collected remedies after the loop ends
            if current_disease and current_remedies:
                remedy_map[current_disease.lower()] = current_remedies
                print(f"  Saved final '{current_disease.lower()}': {remedy_map[current_disease.lower()]}")

        print(f"Loaded {len(remedy_map)} remedy entries from {filepath}")
        print(f"Full DISEASE_TO_REMEDIES map: {remedy_map}") # DEBUG: Print the whole map
    except FileNotFoundError:
        print(f"Error: {filepath} not found.")
    except Exception as e:
        print(f"Error reading {filepath} at line {line_num}: {e}")
    return remedy_map

# --- Load data once when the app starts ---
DISEASE_TO_LEAVES = load_disease_data()
DISEASE_TO_REMEDIES = load_remedy_data()


# --- Image Preprocessing Function ---
def preprocess_image(image):
    img = Image.open(io.BytesIO(image)).resize((260, 260))
    if img.mode != 'RGB':
        img = img.convert('RGB')
    img_array = np.array(img) / 255.0
    img_array = np.expand_dims(img_array, axis=0)
    return img_array

# --- Flask Routes ---

@app.route('/')
def index():
    return "Welcome to the Leaf Disease Prediction API!"

@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({'error': 'Model not loaded'}), 500

    if 'file' not in request.files:
        return jsonify({'error': 'No file part'}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({'error': 'No selected file'}), 400

    if file:
        try:
            img_bytes = file.read()
            processed_image = preprocess_image(img_bytes)
            prediction = model.predict(processed_image)
            predicted_class_index = np.argmax(prediction)
            confidence = prediction[0][predicted_class_index]

            predicted_class_name = "Unknown"
            if CLASS_NAMES and 0 <= predicted_class_index < len(CLASS_NAMES):
                predicted_class_name = CLASS_NAMES[predicted_class_index]

            result = {
                'predicted_class': predicted_class_name,
                'confidence': float(confidence)
            }
            return jsonify(result)
        except Exception as e:
            return jsonify({'error': f'Error processing image: {e}'}), 500

    return jsonify({'error': 'Something went wrong'}), 500

@app.route('/get_leaves', methods=['GET'])
def get_leaves():
    disease = request.args.get('disease', '').strip().lower()
    leaves = DISEASE_TO_LEAVES.get(disease, [])
    if leaves:
        return jsonify({"leaves": leaves})
    else:
        return jsonify({"error": "Disease not found or no leaves associated", "leaves": []}), 404

@app.route("/remedy", methods=["POST"])
def get_remedy():
    data = request.get_json()
    disease = data.get("disease", "").strip().lower()

    # Retrieve remedy as a list of strings
    remedies = DISEASE_TO_REMEDIES.get(disease, ["No remedy available."])
    print(f"Request for remedy: '{disease}' -> Result: {remedies}") # DEBUG: Log incoming request and result
    return jsonify({"remedy": remedies}) # Send a list

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')