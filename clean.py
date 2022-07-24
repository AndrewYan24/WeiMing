import os

clean_path = 'require'
del_list = os.listdir(clean_path)
for f in del_list:
    file_path = os.path.join(clean_path, f)
    if os.path.isfile(clean_path):
        os.remove(clean_path)