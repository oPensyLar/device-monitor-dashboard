import zipfile
import os


class Compress:

    def __init__(self):
        pass

    def build(self, current, muchos_files, output_file_path):
        zip_handle = zipfile.ZipFile(output_file_path, "w", zipfile.ZIP_DEFLATED)

        for c_file in muchos_files:
            if os.path.isdir(c_file):
                for root, dirs, files in os.walk(c_file):
                    for file in files:
                        original_file_path = os.path.join(root, file)

                        d_name = os.path.basename(current)
                        pos = original_file_path.find(d_name)
                        pos += len(d_name) + 1
                        compress_file_name = original_file_path[pos:]
                        zip_handle.write(original_file_path, compress_file_name)

            else:
                file_name = os.path.basename(c_file)
                zip_handle.write(c_file, file_name)