#!/usr/bin/python

import argparse
from enum import unique
import json
import os
import boto3
import datetime as dt
from matplotlib.font_manager import json_dump
import pandas as pd
    
def list_recovery_points_as_json(vault_name,max_res):
    client = boto3.client('backup')
    response = client.list_recovery_points_by_backup_vault(
        BackupVaultName=vault_name,
        MaxResults=max_res
    )    
    print(json.dumps(response, indent=4, sort_keys=True, default=str))


def list_recovery_points_by_date(vault_name, max_res):
    client = boto3.client('backup')
    response = client.list_recovery_points_by_backup_vault(
        BackupVaultName=vault_name,
        MaxResults=max_res,
        ByCreatedBefore=dt.datetime(2023, 12, 1)
    )
    
    for i in response['RecoveryPoints']:
        print(i["RecoveryPointArn"] + " " + str(i["CreationDate"]))

def list_vault_names():
    client = boto3.client('backup')
    response = client.list_backup_vaults(
        ByVaultType="BACKUP_VAULT"
    )    
    for i in response['BackupVaultList']:
        print(i["BackupVaultName"] + " " + str(i["CreationDate"]))

def main():
    vault_name = "VAULT-WEEKLY-CICD-SWE-DEV"
    max_res = 3
    list_vault_names()
    # list_recovery_points_as_json(vault_name,max_res)
    # list_recovery_points_by_date(vault_name, max_res)
    
if __name__ == "__main__":
    main()