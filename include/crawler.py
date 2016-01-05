import os
import sys

class crawl(object):

    def get_filepaths(self, directory):
        file_paths = []  # List which will store all of the full filepaths.
        # Walk the tree.
        for root, dirs, files in os.walk(directory):
            for filename in files:
                filepath = os.path.join(root, filename)
                file_paths.append(filepath)
        return file_paths
