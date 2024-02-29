### converts text files to audio mp3s ###

import os
import boto3

pollyClient = boto3.client('polly')
s3Client = boto3.client('s3')


if 'BUCKET_NAME' not in os.environ:
  BUCKET_NAME = 'labstack-prewarm-b7fe3055-191e-4815--storagebucket-ioxcmvkyk4y3'
  AUDIO_FILES_PREFIX='CreateAudioLambda'
else:
  BUCKET_NAME = os.environ['BUCKET_NAME']
  AUDIO_FILES_PREFIX = os.environ['AUDIO_FILES_PREFIX']

def lambda_handler(event, context):
    # List text files in S3 bucket
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.list_objects_v2
    
    responseListObjects = s3Client.list_objects_v2(Bucket=BUCKET_NAME)
    
    # Read each file from S3 Bucket
    # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.get_object
    
    for eachTextFile in responseListObjects['Contents']:
        key = eachTextFile['Key']
        length = len(key)
        fileExtension = key[length-3:length]
        if eachTextFile['Size'] > 0 and fileExtension == 'txt':
            responseGetObject = s3Client.get_object(
                Bucket=BUCKET_NAME,
                Key=key
            )
            text = responseGetObject['Body'].read().decode("utf-8")
            print(key)

            # Create a Polly speech synthesis task
            # https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/polly.html#Polly.Client.start_speech_synthesis_task

            # Call Polly StartSpeechSynthesisTask here for each text in the variable "text"
            response = pollyClient.start_speech_synthesis_task(
                Engine='neural',
                LanguageCode='en-US',
                OutputS3BucketName = BUCKET_NAME,
                OutputS3KeyPrefix=AUDIO_FILES_PREFIX,
                OutputFormat='mp3',
                SampleRate='24000',
                TextType='text',
                Text=text,
                VoiceId='Joanna')
    print('Successfully completed!')
    return
