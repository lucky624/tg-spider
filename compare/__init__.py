import os
import hashlib
from db import *
import re

def comapre_files(file1, file2):
    f1 = open(file1, 'r')
    lines = f1.read()
    done_one = lines.split(' ')
    f1.close()

    f2 = open(file2, 'r')
    lines = f2.read()
    done_two = lines.split(' ')
    f2.close()

    for x in done_one:
        for z in done_two:
            if x == z:
                done_one.remove(x)
                done_two.remove(z)

    result=list(set(done_one) - set(done_two))
    return result

def get_hash_md5(filename):
    with open(filename, 'rb') as f:
        m = hashlib.md5()
        while True:
            data = f.read(8192)
            if not data:
                break
            m.update(data)
        return m.hexdigest()

def fast_scandir(dirname):
    subfolders= [f.path for f in os.scandir(dirname) if f.is_dir()]
    return subfolders


def compare(name):
    dirs = fast_scandir('/tmp/temp')

    needed_folders = []
    for folder in dirs:
        if '_changes' not in folder:
            if name in folder:
                needed_folders.append(folder)

    needed_folders.sort()

    try:
        last = needed_folders[-1]
        pre_last = needed_folders[-2]

        files_last = []
        files_pre_last = []

        files_last_sums = {}
        files_pre_last_sums = {}

        for root, dirs, files in os.walk(last):
            for name in files:
                files_last.append(os.path.join(root, name))

        for root, dirs, files in os.walk(pre_last):
            for name in files:
                files_pre_last.append(os.path.join(root, name))

        for file in files_last:
            hash = get_hash_md5(file)
            new_dict = {file : hash}
            files_last_sums.update(new_dict)

        for file in files_pre_last:
            hash = get_hash_md5(file)
            new_dict = {file: hash}
            files_pre_last_sums.update(new_dict)

        change_files_last = []


        files_last_sums_keys = list(files_last_sums.keys())
        files_pre_sums_keys = list(files_pre_last_sums.keys())

        for file in files_last_sums_keys:
            found = False
            for file_two in files_pre_sums_keys:
                if files_last_sums[file] == files_pre_last_sums[file_two]:
                    found = True
                    break
            if not found:
                change_files_last.append(file)


        if len(files_last_sums.keys()) == len(files_pre_last_sums.keys()):
            if len(change_files_last) == 1:
                for file in files_pre_sums_keys:
                    hash_pre = files_pre_last_sums[file]
                    found = False
                    for file_new in files_last_sums_keys:
                        hash_last = files_last_sums[file_new]
                        if hash_pre == hash_last:
                            found = True
                            break
                    if not found:
                        ignores = get_ignores()
                        result = comapre_files(change_files_last[0], file)
                        for ignore in ignores:
                            regexp = ignore[1]
                            base64_bytes = str(regexp).encode('ascii')

                            decode_string_bytes = base64.b64decode(base64_bytes)
                            decode_string = decode_string_bytes.decode("ascii")

                            for item in result:
                                try:
                                    found = re.search(regexp,item).group(0)
                                except:
                                    pass
                                if found :
                                    result.remove(item)

                        return('Изменили файл : ' + str(change_files_last) + '\n' + str(result))
            else:
                return ('Изменили несколько файлов : ' + str(change_files_last))
        elif len(files_last_sums.keys()) < len(files_pre_last_sums.keys()):
            return('Удалили файлы : ' + str(change_files_last))
        else:
            return('Добавили файлы : ' + str(change_files_last))
    except:
        return None

