from flask import Flask, request, send_file, jsonify
from rembg import remove
from PIL import Image
import io
import os
import logging
import traceback

app = Flask(__name__)
logging.basicConfig(level=logging.DEBUG)

@app.route('/')
def index():
    return app.send_static_file('index.html')

@app.route('/remove_background', methods=['POST'])
def remove_background():
    app.logger.info('Received request to remove background')
    if 'file' not in request.files:
        app.logger.error('No file part in the request')
        return jsonify({'error': 'No file part'}), 400
    
    file = request.files['file']
    if file.filename == '':
        app.logger.error('No selected file')
        return jsonify({'error': 'No selected file'}), 400
    
    if file:
        try:
            app.logger.info(f'Processing file: {file.filename}')
            input_image = Image.open(file.stream)
            app.logger.info(f'Image opened successfully. Size: {input_image.size}, Mode: {input_image.mode}')
            
            output_image = remove(input_image)
            app.logger.info('Background removed successfully')
            
            img_io = io.BytesIO()
            output_image.save(img_io, 'PNG')
            img_io.seek(0)
            app.logger.info('Image saved to BytesIO successfully')
            
            return send_file(img_io, mimetype='image/png')
        except Exception as e:
            app.logger.error(f'Error processing image: {str(e)}')
            app.logger.error(traceback.format_exc())
            return jsonify({'error': f'Error processing image: {str(e)}'}), 500
    
    return jsonify({'error': 'Unknown error'}), 500

if __name__ == '__main__':
    app.run(debug=True)