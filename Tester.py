import os
import unittest
import WatchDog
import shutil
import logging


TEST_PATH = r"C:\Users\Ream\Desktop\test"
TEST_FILE = os.path.join(TEST_PATH, "File.txt")

class MockLog(logging.Logger):
    last_log = ""

    def info(self, msg, **kwargs):
        self.last_log = msg


class WatchDogTest(unittest.TestCase):
    def tearDown(self):
        for filename in os.listdir(TEST_PATH):
            file_path = os.path.join(TEST_PATH, filename)
            try:
                if os.path.isfile(file_path) or os.path.islink(file_path):
                    os.unlink(file_path)
                elif os.path.isdir(file_path):
                    shutil.rmtree(file_path)
            except Exception as e:
                print('Failed to delete %s. Reason: %s' % (file_path, e))

    def setUp(self):
        self.mock_log = MockLog("mock")
        self.watch_dog = WatchDog.WatchDog(TEST_PATH, self.mock_log)
        self.watch_dog._get_entities()
        self.watch_dog.is_first_run = False

    def testNewDir(self):
        os.mkdir(os.path.join(TEST_PATH, 'test1'))
        self.watch_dog._get_entities()
        self.assertIn(f"test1 added", self.mock_log.last_log)

    def testNewFile(self):
        with open(TEST_FILE, "w") as f:
            f.write("Test")
        self.watch_dog._get_entities()
        self.assertIn(f"{TEST_FILE} added", self.mock_log.last_log)

    def testModified(self):
        self.testNewFile()
        with open(TEST_FILE, "a") as f:
            f.write("Test2")
        self.watch_dog._get_entities()
        self.assertIn(f"{TEST_FILE} modified", self.mock_log.last_log)

    def testDeletedFile(self):
        with open(TEST_FILE, "w") as f:
            f.write("Test3")
        self.watch_dog._get_entities()
        os.remove(f"{TEST_FILE}")
        self.watch_dog._get_entities()
        self.assertIn(f"{TEST_FILE} deleted", self.mock_log.last_log)


if __name__ == '__main__':
    unittest.main()
