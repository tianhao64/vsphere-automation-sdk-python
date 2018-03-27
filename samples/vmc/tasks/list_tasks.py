#!/usr/bin/env python

"""
* *******************************************************
* Copyright (c) VMware, Inc. 2018. All Rights Reserved.
* SPDX-License-Identifier: MIT
* *******************************************************
*
* DISCLAIMER. THIS PROGRAM IS PROVIDED TO YOU "AS IS" WITHOUT
* WARRANTIES OR CONDITIONS OF ANY KIND, WHETHER ORAL OR WRITTEN,
* EXPRESS OR IMPLIED. THE AUTHOR SPECIFICALLY DISCLAIMS ANY IMPLIED
* WARRANTIES OR CONDITIONS OF MERCHANTABILITY, SATISFACTORY QUALITY,
* NON-INFRINGEMENT AND FITNESS FOR A PARTICULAR PURPOSE.
"""

__author__ = 'VMware, Inc.'

import argparse

from tabulate import tabulate
from vmware.vapi.vmc.client import create_vmc_client


class ListTasks(object):
    """
    List all tasks in an org

    Sample Prerequisites:
        - An organization associated with the calling user.
    """

    def __init__(self):
        parser = argparse.ArgumentParser(
            formatter_class=argparse.ArgumentDefaultsHelpFormatter)

        parser.add_argument('-r', '--refresh-token',
                            required=True,
                            help='VMware Cloud API refresh token')

        parser.add_argument('-o', '--org-id',
                            required=True,
                            help='Organization identifier.')

        args = parser.parse_args()

        self.refresh_token = args.refresh_token
        self.org_id = args.org_id

        # Login to VMware Cloud on AWS
        self.vmc_client = create_vmc_client(self.refresh_token)

        # Check if the organization exists
        orgs = self.vmc_client.Orgs.list()
        if self.org_id not in [org.id for org in orgs]:
            raise ValueError("Org with ID {} doesn't exist".format(self.org_id))

    def list_tasks(self):
        tasks = self.vmc_client.orgs.Tasks.list(self.org_id)

        print('\n# Example: List all tasks in {}:'.format(self.org_id))
        headers = ['ID', 'Status', 'Progress', 'Started', 'User']
        table = []
        for task in tasks:
            table.append([task.id, task.status, task.progress_percent,
                          task.start_time, task.user_name])
        print(tabulate(table, headers))


def main():
    list_tasks = ListTasks()
    list_tasks.list_tasks()


if __name__ == '__main__':
    main()
