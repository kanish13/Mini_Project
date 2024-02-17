import os
from flask import Flask, request, jsonify, send_from_directory
from werkzeug.utils import secure_filename
from flask_cors import CORS, cross_origin
import boto3
import learn,db
from dotenv import load_dotenv


load_dotenv('.env')

app = Flask(__name__)
cors = CORS(app)



@app.route('/geturl', methods=['POST'])
@cross_origin()
def upload_pdf():

    load_dotenv()

    s3 = boto3.client(
        's3',
        aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
        aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY')
    )
    try:
        presigned_url = s3.generate_presigned_url(
            ClientMethod='put_object',
            Params={
                'Bucket': "probe-test-alpha",
                'Key': request.json['filename'],
            },
            ExpiresIn=15 * 60  
        )
        return jsonify({'success': True, 'message': 'URL generated!', 'presigned_url': presigned_url}), 201

    except Exception as e:
        print(f'Error uploading PDF: {e}')
        return jsonify({'error': 'Error uploading PDF'}), 500


@app.route('/query', methods=['POST'])
@cross_origin()
def answer():
    request_body = request.json
    ans = learn.query(request_body['pdf_url'],request_body['system_prompt'],request_body['query'])
    db.write_query(request_body['query'],ans,request_body['pdf_url'])
    return jsonify({'message': "Responded to query", 'answer': ans})

@app.route('/history', methods=['GET'])
@cross_origin()
def write_to_db():
    history=db.get_queries()
    return jsonify({'message': "Retrieved all past queries", 'history': history})

if __name__ == '__main__':
    app.run(debug=True)
