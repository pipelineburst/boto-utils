import json
import boto3
from time import sleep

client = boto3.client('inspector2')

with open('event.json') as event_file:
  parsed_event = json.load(event_file)

repo_name_in = parsed_event["detail"]["repository-name"]
repo_name = repo_name_in.split("repository/")[-1]
print(repo_name)
image_tag = parsed_event['detail']['image-tags'][0]
print(image_tag)

while True:
    try:
        response = client.list_coverage(
                filterCriteria={
                    'ecrRepositoryName': [
                        {
                            'comparison': 'EQUALS',
                            'value': repo_name
                        }
                    ],
                    'ecrImageTags': [
                        {
                        'comparison': 'EQUALS',
                        'value': image_tag
                        }
                    ]
                },
        )
    except Exception as e:
        print('retrying list-coverage call...')
        sleep(5)
        continue

    print(response['coveredResources'][0]['scanStatus']['reason'])
    
    if response['coveredResources'][0]['scanStatus']['reason'] == "SUCCESSFUL" :
        print('all good, movint onto sbom export request...')

    break

while True:
    try:
        print('requesting sbom export...')
        print("Details of requested sbom export:")
        print(repo_name)
        print(image_tag)
        response1 = client.create_sbom_export(
                reportFormat='SPDX_2_3',
                resourceFilterCriteria={
                    'ecrRepositoryName': [
                        {
                            'comparison': 'EQUALS',
                            'value': repo_name
                        }
                    ],
                    'ecrImageTags': [
                        {
                        'comparison': 'EQUALS',
                        'value': image_tag
                        }
                    ]
                },
                s3Destination={
                    'bucketName': 'sbom-lake-u4jedu3',
                    'kmsKeyArn': 'arn:aws:kms:eu-west-1:069127586842:key/f70a8a11-2181-478d-9798-fbfe9e52870a'
                }
            )
    except Exception as e:
        print('retrying. sbom creation request... in spector is busy :-)')
        from time import sleep
        sleep(5)
        continue

    break
