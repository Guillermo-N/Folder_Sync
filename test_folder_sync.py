#!./venv/bin/python3

"""
This file can be ignored; it was used during the development of folder_sync.py to automate specific use cases for convenience.

Please note that this file does not cover all possible use cases but rather focuses on a subset that was useful during the development process.
"""

import subprocess
import os
import folder_sync
import shutil
import signal
import time


class TestFolderSyncFileFingerprints:

    file_path = './fingerprint_test_dir/hash_test'

    def setup_method(self):

        # Create the resource
        os.makedirs('./fingerprint_test_dir')
        open('./fingerprint_test_dir/hash_test', 'a').close()

    def teardown_method(self):

        # Delete the resource
        shutil.rmtree('./fingerprint_test_dir')

    def test_file_data_mod(self):

        # File before adding data
        hash_1 = folder_sync.file_fingerprint(self.file_path)

        # Append data to the file
        with open(self.file_path, 'a') as file:
            file.write("Hello World!")

        # Fingerprint after apendin data
        hash_2 = folder_sync.file_fingerprint(self.file_path)

        # Fingerprints shouldn't match
        assert hash_1 != hash_2

    def test_file_name_mod(self):

        # Finger print of file before rename
        hash_1 = folder_sync.file_fingerprint(self.file_path)

        # File rename
        os.rename(self.file_path, self.file_path + '.txt')

        # Fingerpirnt of file after rename
        hash_2 = folder_sync.file_fingerprint(self.file_path + '.txt')

        # Checking they are the same
        assert hash_1 == hash_2


class TestFileSync:

    src_path = './test_src'
    dst_path = './test_dst'

    def setup_method(self):

        # Start folder sync script
        self.process = subprocess.Popen(
            ['python3', 'folder_sync.py',
             '-u', '0.05',
             '-s', TestFileSync.src_path,
             '-d', TestFileSync.dst_path
             ]
        )

    def teardown_method(self):

        # Stop folder_sync script
        self.process.terminate()

        # Delete the resource
        del self.process
        shutil.rmtree(TestFileSync.src_path)
        shutil.rmtree(TestFileSync.dst_path)

    def test_create_file(self):

        time.sleep(0.5)
        file = 'hello'

        # Create file with contents
        with open(os.path.join(TestFileSync.src_path, file), 'w') as f:
            f.write('Hello World!')
        time.sleep(0.5)

        # Computting file fingerprints in src & dst
        fingerprint_file_src = folder_sync.file_fingerprint(
            os.path.join(TestFileSync.src_path, file))
        fingerprint_file_dst = folder_sync.file_fingerprint(
            os.path.join(TestFileSync.dst_path, file))

        # Check if those fingerprints match
        assert fingerprint_file_src == fingerprint_file_dst

    def test_update_file(self):

        time.sleep(0.5)
        file = 'hello_v2'
        file_content = 'Hello World 2!'

        # Create plane file in src
        open(os.path.join(TestFileSync.src_path, file), 'w').close()
        time.sleep(0.5)

        # Check if the file has already sync
        if os.path.exists(os.path.join(TestFileSync.src_path, file)):
            # Appending contents to file in src
            with open(os.path.join(TestFileSync.src_path, file), 'a') as f:
                f.write(file_content)
            time.sleep(0.5)
        else:
            # Plain file sync problem
            raise Exception("File wasn't sync")

        # Computting file fingerprints in src & dst
        fingerprint_file_src = folder_sync.file_fingerprint(
            os.path.join(TestFileSync.src_path, file))
        fingerprint_file_dst = folder_sync.file_fingerprint(
            os.path.join(TestFileSync.dst_path, file))

        # Check if those fingerprints match
        assert fingerprint_file_src == fingerprint_file_dst

    def test_create_dir(self):
        time.sleep(0.5)
        dir = 'dir1'

        # Create dir
        os.mkdir(os.path.join(TestFileSync.src_path, dir))
        time.sleep(0.5)

        # Check dir is sync
        assert os.path.exists(os.path.join(TestFileSync.dst_path, dir))

    def test_create_nested_dirs(self):
        time.sleep(0.5)
        dirs = 'lvl-1/lvl-2/lvl-3'

        # Create nested dirs
        os.makedirs(os.path.join(TestFileSync.src_path, dirs))
        time.sleep(0.5)

        # Check if those where sync correctly
        assert os.path.exists(os.path.join(TestFileSync.dst_path, dirs))

    def test_file_creation_in_src(self):
        """
        Test for creating a file in a path that was sych

        Steps
            Create a path of folders in the source directory.
            While the folders are being synchronized, create a file midway in this path in the destination directory.
            Remove all the folders from the source directory.

        Result
            All empty synchronized folders should be removed from the destination directory.
            Folders in the path where the file is located should persist in the destination directory.
        """

        time.sleep(0.5)
        dirs = 'one/two/three/four'
        halfway_dir = 'one/two'
        file = 'somefile.txt'

        # Create dirs recursively
        os.makedirs(os.path.join(TestFileSync.src_path, dirs))
        time.sleep(0.5)

        # Creating file in dest halfway the dir structure
        open(
            os.path.join(
                TestFileSync.dst_path,
                halfway_dir,
                file),
            'w').close()

        # Delete dir structure recursively
        shutil.rmtree(os.path.join(TestFileSync.src_path, 'one'))
        time.sleep(0.5)

        # Check if file still on dst
        assert os.path.exists(os.path.join(
            TestFileSync.dst_path, halfway_dir, file))
