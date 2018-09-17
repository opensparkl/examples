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

Simple implementation of FileSync/Master service.
"""
import os
import sparkl_cli as sparkl
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from base64 import b64encode


class CustomHandler(FileSystemEventHandler):
  """
  Watchdog handler callbacks marshal arguments and
  invoke the functions corresponding to the notify
  operations on the master service.
  """
  def __init__(self, service):
    self.service = service

  def on_created(self, event):
    binary = bytearray()
    if not event.is_directory:
      with open(event.src_path, mode='rb') as file:
        binary = file.read()

    put(self.service, event.is_directory, event.src_path, binary)

  def on_deleted(self, event):
      delete(self.service, event.is_directory, event.src_path)

  def on_modified(self, event):
    binary = bytearray()
    if not event.is_directory:
      with open(event.src_path, mode='rb') as file:
        binary = file.read()
      put(self.service, event.is_directory, event.src_path, binary)

  def on_moved(self, event):
    move(self.service, event.is_directory, event.src_path, event.dest_path)


def onopen(service):
  """
  SPARKL callback initialises the observer with an instance
  of the custom watchdog handler class.
  """
  event_handler = CustomHandler(service)
  service.observer = Observer()
  service.observer.schedule(event_handler, '.', recursive=True)
  service.observer.start()
  print("Master watchdog started in {cwd}".format(
    cwd=os.getcwd()))


def onclose(service):
  """
  SPARKL callback waits for the observer to stop before exiting.
  """
  service.observer.stop()
  service.observer.join()
  print("Master watchdog stopped")


def put(service, is_dir, path, binary):
  base64 = b64encode(binary).decode('utf-8')
  service.notify({
    'notify': 'Mix/Master/Put',
    'data': {
      'is_dir': is_dir,
      'path':   path,
      'bytes':  base64}})


def delete(service, is_dir, path):
  service.notify({
    'notify': 'Mix/Master/Delete',
    'data': {
      'is_dir': is_dir,
      'path': path}})


def move(service, is_dir, old, path):
  service.notify({
    'notify': 'Mix/Master/Move',
    'data': {
      'is_dir': is_dir,
      'old': old,
      'path': path}})
