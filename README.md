# 안드로이드 다중 버전 관리
여러 빌드 환경을 가지고 있는 안드로이드 프로젝트의 경우, 빌드 환경별 VersionCode와 VersionName을 관리해야 하는 경우가 있습니다. 이 액션을 이용하면 원하는 빌드 환경(최대 3개까지 지원)의 버전을 선택해 관리할 수 있습니다.

기본적으로 VersionName은 SemVer를 따라 major.minor.patch의 형태로 관리하는 경우에 이 액션을 사용할 수 있으며, pull request에서 label을 이용하여 버전 증가를 원하는 빌드 환경을 선택하고 major, minor, patch 중 어떠한 버전을 증가시킬지 선택할 수 있습니다.

VersionCode의 경우, 선택한 빌드 스테이지의 VersionCode가 1씩 증가하는 형태로 액션이 동작합니다.

# 사용법
```yml
- name: Execute action
  id: bump_version
  uses: ./ 
  with:
    version_file_path: "./version.gradle"
    pr_labels: ${{ steps.pr-labels.outputs.labels }}
    version_name_dev: "version_name_test_dev"
    version_name_stg: "version_name_test_stg"
    version_name_prod: "version_name_test_prod"
    version_code_dev: "version_code_test_dev"
    version_code_stg: "version_code_test_stg"
    version_code_prod: "version_code_test_prod"
```

# 입력값
## `version_file_path(필수)`
버전들이 정의되어 있는 파일의 경로입니다.<br>
ex) app/version.gradle

## `pr_labels(필수)`
pull request에 지정된 label들을 문자열로 나타낸 것 입니다.<br>
인식 가능한 label의 종류는 **`dev, stg, prod, bump patch, bump minor, bump major`** 입니다. 어떤 빌드 환경을 선택할 지와 어떤 버전을 증가하고 싶은지 label을 통해 결정해야 합니다.<br>
이 때, label 내부에 있는 띄어쓰기는 '-'로 연결되어야 하고, label 끼리는 공백으로 구분되어야 합니다. (추후 업데이트 예정)<br>
ex) "dev bump-major"

## `version_name_dev/stg/prod(선택)`
프로젝트 내에서 사용 중인 versionName의 변수명을 입력합니다. 빌드 환경이 1개인 경우 dev, 2개인 경우 dev, stg, 3개인 경우 dev, stg, prod에 입력하면 됩니다.<br>
ex) "version_name_test_dev"

## `version_code_dev/stg/prod(선택)`
프로젝트 내에서 사용 중인 versionCode의 변수명을 입력합니다. 빌드 환경이 1개인 경우 dev, 2개인 경우 dev, stg, 3개인 경우 dev, stg, prod에 입력하면 됩니다.<br>
ex) "version_code_test_dev"

# 출력값
## `current_version_name`
선택한 빌드 환경의 버전 증가하기 전 버전 네임을 출력합니다.<br>
ex) ${{ steps.bump_version.outputs.current_version_name }}

## `current_version_code`
선택한 빌드 환경의 버전 증가하기 전 버전 코드를 출력합니다.<br>
ex) ${{ steps.bump_version.outputs.current_version_code }}

## `next_version_name`
선택한 빌드 환경의 버전 증가 후 버전 네임을 출력합니다.<br>
ex) ${{ steps.bump_version.outputs.next_version_name }}

## `next_version_code`
선택한 빌드 환경의 버전 증가 후 버전 코드을 출력합니다.<br>
ex) ${{ steps.bump_version.outputs.next_version_code }}
