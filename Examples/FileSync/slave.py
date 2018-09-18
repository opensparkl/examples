"""
Copyright 2018 SPARKL Limited

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

  http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.

Simple implementation of FileSync/Slave service.
"""
import os
from base64 import b64decode


def put(event):
    """
    (Over)writes a directory or file.
    """
    is_dir = event['data']['is_dir']
    path = event['data']['path']

    if is_dir:
        os.makedirs(path, exist_ok=True)
    else:
        binary = b64decode(event['data']['bytes'])

    with open(path, 'wb') as file:
        file.write(binary)


def delete(event):
    """
    Deletes a directory or file. If the slave is not in sync,
    this may cause an exception which is caught.
    """
    is_dir = event['data']['is_dir']
    path = event['data']['path']

    try:
        if is_dir:
            os.rmdir(path)
        else:
            os.remove(path)
    except BaseException as exception:
        print(exception)


def move(event):
    """
    Moves (renames) a directory or file. If the slave is not in sync,
    this may cause an exception which is caught.
    """
    old = event['data']['old']
    path = event['data']['path']

    try:
        os.replace(old, path)
    except BaseException as exception:
        print(exception)


def onopen(service):
    """
    SPARKL callback sets implementation dict.
    """
    print("Slave listener started in {cwd}".format(
        cwd=os.getcwd()))

    service.impl = {
        'Mix/Slave/Put':    put,
        'Mix/Slave/Delete': delete,
        'Mix/Slave/Move':   move}


def onclose(_service):
    """
    SPARKL callback
    """
    print("Slave listener stopped")
