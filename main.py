from flask import Flask, request, send_file, render_template
import json
import os
from io import BytesIO

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/transform', methods=['POST'])
def transform():
    uploaded_file = request.files['worldfile']
    if not uploaded_file:
        return "No file uploaded", 400

    data = json.load(uploaded_file)

    # Modify terrainmap heights
    heights_str = data['Singletons']['TerrainMap']['Heights']['Array']
    heights = list(map(int, heights_str.strip().split()))
    updated_heights = [h + 5 for h in heights]  # change 5 to -5 to lower
    data['Singletons']['TerrainMap']['Heights']['Array'] = ' '.join(map(str, updated_heights))

    # Modify Z coordinates in entities
    for entity in data.get("Entities", []):
        try:
            entity['Components']['BlockObject']['Coordinates']['Z'] += 5
        except (KeyError, TypeError):
            continue

    output = BytesIO()
    json.dump(data, output, indent=2)
    output.seek(0)

    return send_file(output, as_attachment=True, download_name='world_transformed.json', mimetype='application/json')

if __name__ == '__main__':
    app.run(debug=True)
