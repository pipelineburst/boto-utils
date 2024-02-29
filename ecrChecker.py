#!/usr/bin/python

import argparse
from enum import unique
import json
import os
import boto3
import datetime as dt
from matplotlib.font_manager import json_dump
import pandas as pd
    
def get_ecr_id():
    client = boto3.client('ecr')
    response = client.describe_registry()    
    registry_id = response["registryId"]
    return registry_id

def list_ecr_repos(registry_id):
    client = boto3.client('ecr')
    response = client.describe_repositories(
        registryId=registry_id,
    )    
    for i in response["repositories"]:
        print(i["repositoryName"])
    
def main():
    get_ecr_id()
    list_ecr_repos(registry_id=get_ecr_id())

if __name__ == "__main__":
    main()