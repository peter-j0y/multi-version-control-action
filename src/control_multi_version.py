import re
import os
from enum import Enum, auto

class VersionCategory(Enum):
    REVISION = auto()
    PATCH = auto()
    MINOR = auto()
    MAJOR = auto()

# version_name 읽는 함수
def read_gradle_version_name(gradle_file_path, variable_name):
    with open(gradle_file_path, 'r') as file:
        gradle_content = file.read()

    pattern = f'{variable_name} = "(.+)"'
    match = re.search(pattern, gradle_content)

    if match:
        return match.group(1)
    else:
        return None

# version_code 읽는 함수
def read_gradle_version_code(gradle_file_path, variable_name):
    with open(gradle_file_path, 'r') as file:
        gradle_content = file.read()

    pattern = f'{variable_name} = (\\d+)'
    match = re.search(pattern, gradle_content)

    if match:
        return int(match.group(1))
    else:
        return None

# gradle 파일에 버전 업데이트(쓰는) 함수
def write_gradle_version(vc_variable_name, vn_variable_name, new_version_code, new_version_name):
    with open(gradle_file_path, 'r') as file:
        gradle_content = file.read()

    vn_pattern = f'{vn_variable_name} = ".+"'
    vn_new_line = f'{vn_variable_name} = "{new_version_name}"'
    print(vn_new_line)
    updated_content = re.sub(vn_pattern, vn_new_line, gradle_content)

    vc_pattern = f'{vc_variable_name} = (\\d+)'
    vc_new_line = f'{vc_variable_name} = {new_version_code}'
    print(vc_new_line)
    updated_content = re.sub(vc_pattern, vc_new_line, updated_content)

    with open(gradle_file_path, 'w') as file:
        file.write(updated_content)

    print(f"Updated version : {new_version_name}")
    env_file = os.getenv('GITHUB_ENV')
    with open(env_file, 'a') as env_file:
        print(env_file)
        env_file.write(f"NEXT_VERSION_NAME={new_version_name}\n")
        env_file.write(f"NEXT_VERSION_CODE={new_version_code}\n")
        

# label들을 해석하는 함수
def decode_labels(labels, version_name_dev, version_name_stg, version_name_prod, version_code_dev, version_code_stg, version_code_prod):
    label_list = labels.split(' ')
    print(label_list)

    args = {
        'dev': {'version_code': version_code_dev, 'version_name': version_name_dev, 'version_code_variable_name': version_code_dev_variable_name, 'version_name_variable_name': version_name_dev_variable_name},
        'stg': {'version_code': version_code_stg, 'version_name': version_name_stg, 'version_code_variable_name': version_code_stg_variable_name, 'version_name_variable_name': version_name_stg_variable_name},
        'prod': {'version_code': version_code_prod, 'version_name': version_name_prod, 'version_code_variable_name': version_code_prod_variable_name, 'version_name_variable_name': version_name_prod_variable_name}
    }
    
    # dev, stg, prod 일괄적으로 bump
    if 'all' in label_list:
        for arg in args.values():
            update_version(arg, label_list)
    # 선택한 빌드 환경만 bump
    else:
        for arg_key, arg in args.items():
            if arg_key in label_list and arg['version_code'] is not None and arg['version_name'] is not None:
                update_version(arg, label_list)

def update_version(arg, label_list):
    version_code = int(arg['version_code'])
    print(arg['version_name'])
    major_version, minor_version, patch_version, revision_version = map(int, arg['version_name'].split('.'))

    for version_type in list(VersionCategory):
        if f'bump-{version_type.name.lower()}' in label_list:
            bump_version(version_type, arg['version_code_variable_name'], arg['version_name_variable_name'], version_code, major_version, minor_version, patch_version, revision_version)

# 버전 올리는 함수
def bump_version(version_category, vc_variable_name, vn_variable_name, version_code, major_version, minor_version, patch_version, revision_version) :
    print(f"Current version : {major_version}.{minor_version}.{patch_version}.{revision_version}")
    env_file = os.getenv('GITHUB_ENV')

    with open(env_file, "a") as my_file:
        my_file.write(f"CURRENT_VERSION_NAME={major_version}.{minor_version}.{patch_version}.{revision_version}\n")
        my_file.write(f"CURRENT_VERSION_CODE={version_code}\n")

    # version_code는 항상 증가
    version_code += 1

    if version_category is VersionCategory.REVISION:
        revision_version += 1
    elif version_category is VersionCategory.PATCH:
        revision_version = 0
        patch_version += 1
    elif version_category is VersionCategory.MINOR:
        revision_version = 0
        patch_version = 0
        minor_version += 1
    elif version_category is VersionCategory.MAJOR:
        revision_version = 0
        patch_version = 0
        minor_version = 0
        major_version += 1
        
    write_gradle_version(vc_variable_name, vn_variable_name, version_code, f"{major_version}.{minor_version}.{patch_version}.{revision_version}")

if __name__ == '__main__':
    gradle_file_path = os.environ.get('FILE-PATH')

    pr_labels = os.environ.get('PR-LABELS')

    version_name_dev_variable_name = os.environ.get('VERSION-NAME-DEV')
    version_name_stg_variable_name = os.environ.get('VERSION-NAME-STG')
    version_name_prod_variable_name = os.environ.get('VERSION-NAME-PROD')
    version_code_dev_variable_name = os.environ.get('VERSION-CODE-DEV')
    version_code_stg_variable_name = os.environ.get('VERSION-CODE-STG')
    version_code_prod_variable_name = os.environ.get('VERSION-CODE-PROD')

    version_name_dev = read_gradle_version_name(gradle_file_path, version_name_dev_variable_name)
    version_name_stg = read_gradle_version_name(gradle_file_path, version_name_stg_variable_name)
    version_name_prod = read_gradle_version_name(gradle_file_path, version_name_prod_variable_name)

    version_code_dev = read_gradle_version_code(gradle_file_path, version_code_dev_variable_name)
    version_code_stg = read_gradle_version_code(gradle_file_path, version_code_stg_variable_name)
    version_code_prod = read_gradle_version_code(gradle_file_path, version_code_prod_variable_name)

    decode_labels(pr_labels, version_name_dev, version_name_stg, version_name_prod, version_code_dev, version_code_stg, version_code_prod)