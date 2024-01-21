# app.py
from flask import Flask, render_template, send_from_directory
from config import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, S3_BUCKET, S3_REGION
import boto3
from botocore.exceptions import NoCredentialsError

app = Flask(__name__)

# AWS S3 Configuration


# Initialize the S3 client
s3 = boto3.client('s3', region_name=S3_REGION, aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)


@app.route('/play/<path:filename>')
def play(filename):
    try:
        # Generate a temporary URL for the S3 object
        url = s3.generate_presigned_url('get_object',
                                       Params={'Bucket': S3_BUCKET, 'Key': filename},
                                       ExpiresIn=3600)  # URL expires in 1 hour (adjust as needed)
        return render_template('index.html', video_url=url)
    except NoCredentialsError:
        return 'AWS credentials not available.'
    except Exception as e:
        return f'Error: {str(e)}'

if __name__ == '__main__':
    app.run(debug=True)
