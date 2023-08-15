import re
import os

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
def decode_labels(labels):
    label_list = labels.split(',')
    print(label_list)
    if 'dev' in label_list and version_code_dev is not None and version_name_dev is not None:
        version_code = int(version_code_dev)
        major_version = int(version_name_dev
.split('.')[0])
        minor_version = int(version_name_dev
.split('.')[1])
        patch_version = int(version_name_dev
.split('.')[2])

        if 'bump patch' in label_list:
            bump_patch(version_code_dev_variable_name, version_name_dev_variable_name, version_code, major_version, minor_version, patch_version)
        if 'bump minor' in label_list:
            bump_minor(version_code_dev_variable_name, version_name_dev_variable_name, version_code, major_version, minor_version, patch_version)
        if 'bump major' in label_list:
            bump_major(version_code_dev_variable_name, version_name_dev_variable_name, version_code, major_version, minor_version, patch_version)

    if 'stg' in label_list and version_code_stg is not None and version_name_stg is not None:
        version_code = int(version_code_stg)
        major_version = int(version_name_stg.split('.')[0])
        minor_version = int(version_name_stg.split('.')[1])
        patch_version = int(version_name_stg.split('.')[2])

        if 'bump patch' in label_list:
            bump_patch(version_code_stg_variable_name, version_name_stg_variable_name, version_code, major_version, minor_version, patch_version)
        if 'bump minor' in label_list:
            bump_minor(version_code_stg_variable_name, version_name_stg_variable_name, version_code, major_version, minor_version, patch_version)
        if 'bump major' in label_list:
            bump_major(version_code_stg_variable_name, version_name_stg_variable_name, version_code, major_version, minor_version, patch_version)

    if 'prod' in label_list and version_code_prod is not None and version_name_prod is not None:
        version_code = int(version_code_prod)
        major_version = int(version_name_prod.split('.')[0])
        minor_version = int(version_name_prod.split('.')[1])
        patch_version = int(version_name_prod.split('.')[2])

        if 'bump patch' in label_list:
            bump_patch(version_code_prod_variable_name, version_name_prod_variable_name, version_code, major_version, minor_version, patch_version)
        if 'bump minor' in label_list:
            bump_minor(version_code_prod_variable_name, version_name_prod_variable_name, version_code, major_version, minor_version, patch_version)
        if 'bump major' in label_list:
            bump_major(version_code_prod_variable_name, version_name_prod_variable_name, version_code, major_version, minor_version, patch_version)

# 버전 올리는 함수
def bump_patch(vc_variable_name, vn_variable_name, version_code, major_version, minor_version, patch_version):
    print(f"Current version : {major_version}.{minor_version}.{patch_version}")
    env_file = os.getenv('GITHUB_ENV')
    with open(env_file, "a") as my_file:
        my_file.write(f"CURRENT_VERSION_NAME={major_version}.{minor_version}.{patch_version}\n")
        my_file.write(f"CURRENT_VERSION_CODE={version_code}\n")

    patch_version += 1
    version_code += 1
    write_gradle_version(vc_variable_name, vn_variable_name, version_code, f"{major_version}.{minor_version}.{patch_version}")

def bump_minor(vc_variable_name, vn_variable_name, version_code, major_version, minor_version, patch_version):
    print(f"Current version : {major_version}.{minor_version}.{patch_version}")
    env_file = os.getenv('GITHUB_ENV')
    with open(env_file, "a") as my_file:
        my_file.write(f"CURRENT_VERSION_NAME={major_version}.{minor_version}.{patch_version}\n")
        my_file.write(f"CURRENT_VERSION_CODE={version_code}\n")

    patch_version = 0
    minor_version += 1
    version_code += 1
    write_gradle_version(vc_variable_name, vn_variable_name, version_code, f"{major_version}.{minor_version}.{patch_version}")

def bump_major(vc_variable_name, vn_variable_name, version_code, major_version, minor_version, patch_version):
    print(f"Current version : {major_version}.{minor_version}.{patch_version}")
    env_file = os.getenv('GITHUB_ENV')
    with open(env_file, "a") as my_file:
        my_file.write(f"CURRENT_VERSION_NAME={major_version}.{minor_version}.{patch_version}\n")
        my_file.write(f"CURRENT_VERSION_CODE={version_code}\n")

    major_version += 1
    minor_version = 0
    patch_version = 0
    version_code += 1
    write_gradle_version(vc_variable_name, vn_variable_name, version_code, f"{major_version}.{minor_version}.{patch_version}")

if __name__ == '__main__':
    # 변수화
    gradle_file_path = os.environ.get('FILE-PATH')

    # 변수화
    pr_labels = os.environ.get('PR-LABELS')

    # 변수화
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

    decode_labels(pr_labels)