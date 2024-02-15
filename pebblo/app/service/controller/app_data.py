import json
import os
from pebblo.app.enums import CacheDir
from pebblo.app.libs.logger import logger

dir_path = os.listdir(CacheDir.home_dir.value)
all_apps = {}
for app_dir in dir_path:
    app_path = f'{CacheDir.home_dir.value}/{app_dir}/{CacheDir.metadata_file_path.value}'
    with open(app_path, "r") as output:
        cred_json = json.load(output)
        print(cred_json)
        all_apps['name'] = cred_json.get('name')

logger.info(f'---- ALL apps {all_apps} -----')