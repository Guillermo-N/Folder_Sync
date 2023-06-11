#!/usr/bin/python3

from time import sleep
import argparse
import pathlib
import hashlib
import logging
import signal
import shutil
import sys
import os

def main(args, logger):

  # Check src & dst directories exists
  # Create them otherwise
  if not os.path.exists(args.src):
    os.makedirs(args.src)

  if not os.path.exists(args.dst):
    os.makedirs(args.dst)


  # Files tracking dictionaries
  old_file_historic = dict()
  file_historic = dict()

  # Directories tracking lists
  old_dir_historic = []
  dir_historic = []

  # Main loop
  while True:

    # Storing last iteration historics
    old_file_historic = file_historic
    old_dir_historic = dir_historic
    
    # Resetting historics
    file_historic = dict()
    dir_historic = []

    # Walking src dir updating new historic
    for src_path, dirs, files in os.walk(args.src, topdown=True):

      in_folder_path = os.path.relpath(src_path, args.src)

      for file in files:
        file_path = os.path.join(in_folder_path, file)
        if file_path not in file_historic:
          file_hash = file_fingerprint(os.path.join(src_path, file))
          file_historic[file_path] = file_hash

      for dir in dirs:
        dir_path = os.path.join(in_folder_path, dir)
        dir_historic.append(dir_path)

    
    # File sets operations
    created_files = set(file_historic.keys()).difference(set(old_file_historic.keys()))
    deleted_files = set(old_file_historic.keys()).difference(set(file_historic.keys()))

    mantained_files = set(old_file_historic.keys()).intersection(set(file_historic.keys()))
    modified_files = [file for file in mantained_files if old_file_historic[file] != file_historic[file]]

    # Dir sets operations
    created_dirs = set(dir_historic).difference(set(old_dir_historic))
    deleted_dirs = set(old_dir_historic).difference(set(dir_historic))


    # Walking dst directory removing contents
    for dst_path, dirs, files in os.walk(args.dst, topdown=False):

      in_folder_path = os.path.relpath(dst_path, args.dst)

      # Constructing src & dst paths
      src_current_dir = os.path.normpath(os.path.join(args.src, in_folder_path))
      dst_current_dir = os.path.normpath(os.path.join(args.dst, in_folder_path))

      for dir in dirs:
        dir_path = os.path.join(in_folder_path, dir)
        dst_dir_path = os.path.join(dst_current_dir, dir)

        if dir_path in deleted_dirs:
          try:
            os.rmdir(dst_dir_path)
            logger.info(f'Directory {dir_path} deleted.')
          except OSError as e:
            logger.warning(f'Directory {dir_path} not empy on dest, skipping.')
          
      for file in files:

        src_file_path = os.path.join(src_current_dir, file)
        dst_file_path = os.path.join(dst_current_dir, file)

        file_path = os.path.join(in_folder_path, file)

        if file_path in modified_files:
          shutil.copy(src_file_path, dst_file_path)
          logging.info(f'File {file_path} updated')
        elif file_path in deleted_files:
          os.remove(dst_file_path)
          logger.info(f'File {file_path} deleted')


    # Creating new dirs in dst
    for dir in created_dirs:
      dst = os.path.normpath(os.path.join(args.dst, dir))
      os.makedirs(dst, exist_ok=True)
      logger.info(f'Directory {dir} created.')

    # Creating new files in dst
    for file in created_files:
      src = os.path.normpath(os.path.join(args.src, file))
      dst = os.path.normpath(os.path.join(args.dst, file))
      shutil.copy(src, dst)
      logger.info(f'File {file} created.')


  sleep(args.delta)



def file_fingerprint(file_path):
  """
    Creates the fingerprint of a file

    Args:
        file_path (str): Path to the file.

    Returns:
        str: SHA256 diggest in case the file exists, None otherwise.
    """
  if not (os.path.exists(file_path) and os.path.isfile(file_path)):
    return None
  
  hash_object = hashlib.sha256()
  #hash_object.update(file_name.encode())
  with open(file_path, 'rb') as file:
    # Read the file in chunks for efficient memory usage
    chunk_size = 4096
    for chunk in iter(lambda: file.read(chunk_size), b''):
      # Update the hash object with the chunk
      hash_object.update(chunk)

    # Get the hexadecimal representation of the hash value
    file_fingerprint = hash_object.hexdigest()

  return file_fingerprint

def signal_handler(signal, frame):
  print("\n\tExiting folder sync.\n")
  sys.exit(0) # Success exit


if __name__ == '__main__':
  signal.signal(signal.SIGTERM, signal_handler)
  signal.signal(signal.SIGINT, signal_handler)

  # Create an option (argument) parser
  parser = argparse.ArgumentParser(description='Folder sync utility demo.')

  # Define script optoins
  parser.add_argument('-s', '--src', default='../folder_sync/source', type=pathlib.Path, help='source folder')
  parser.add_argument('-d', '--dst', default='destination', type=pathlib.Path, help='destination folder')
  parser.add_argument('-u', '--delta', default=1, type=int, help='update interval (delta)')
  parser.add_argument('-l', '--log', default='folder_sync.log', type=pathlib.Path, help='log file path')


  # Parsing  options
  args = parser.parse_args()

  # Create a logger
  logger = logging.getLogger()
  logger.setLevel(logging.DEBUG)

  # Create a stream handler for console output
  stream_handler = logging.StreamHandler()
  stream_handler.setLevel(logging.DEBUG)

  # Create a file handler for log file output
  file_handler = logging.FileHandler(args.log)
  file_handler.setLevel(logging.DEBUG)

  # Create a formatter and set it for both handlers
  formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
  stream_handler.setFormatter(formatter)
  file_handler.setFormatter(formatter)

  # Add the handlers to the logger
  logger.addHandler(stream_handler)
  logger.addHandler(file_handler)

  main(args, logger)