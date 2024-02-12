# cspc_apply_server
> 신입부원 모집을 위한 backend API server

**Stack**
* Django
* drf_yasg (swagger)
* django_rest_framework
* Docker


## DEV (local)
로컬에서 개발할 때 가이드 

로컬에서 sqlite3 local DB를 사용함 (배포용 DB와 별도)

### 소스코드 다운로드
```bash
git clone https://github.com/CSPCLAB/cspc_apply_server.git
```

### 가상환경 세팅
```bash
cd ./app
conda activate env # 가상환경 세팅  (python -m venv venv)
pip install -r requirements.txt

```

### 실행
```bash
python manage.py makemigrations
python manage.py migrate
python manage.py runserver
```
한번 실행하면 자동으로 secret_key를 저장하는 .env파일 생성
> SECRET_KEY는 소스코드, 깃허브에 올리지 말 것!

### branch rule
master 브런치로 바로 push는 불가능

작업 시, 새로운 브런치 추가
```bash
git branch new_branch
git checkout new_branch
```

vscode git 기능 사용 or
```bash
git add file
git commit -m "커밋 메세지"
git push --set-upstream origin new_branch 
```

이후 github 페이지에서 PR 생성 후 테스트 통과 시, merge



## DEPLOY
`git action`을 통해 `master` 브런치에 push or PR merge 시, 자동으로 배포

웬만해서 master로 바로 push하지 말고, PR을 통해 test후 배포하는 것을 권장

직접 배포해야 하는 상황이 있다면 (ex DB migration 충돌)
```bash
cd $PROJECT_PATH
docker-compose down
docker-compose up --build -d
```

## FEAT
Infra 쪽은 거의 완성되어서 개발할 때, django쪽 구현만 신경

### Swagger
* /swagger : API test
* /redoc : API 문서
### API
각 API endpoint마다 django-rest-api 테스트 form 구현
> 이 endpoint 말고 swagger 테스트 추천

### AUTH
`student_id`를 통해 로그인하도록 custom model 구현


다만 custom user model만 만들고 아직 authenticate 모듈은 구현 및 연동 안된 상태
> TODO : `user.view.py`, `user.backends` 수정

### Test
workflow에 push시, test 실행되도록 구현

다만 아직 테스트 코드 구현 X
> TODO : 각 모듈별 `tests.py` 내 테스트 코드 작성 


### CI/CD
#### Docker
배포는 전부 docker container를 통해서 진행
django, nginx, db 이렇게 세개의 container를 통해 배포되는데,

컨테이너 구성 및 네트워크, 볼륨은 아래 compose 파일 확인

`docker-compose.yml` 
#### Git action
`git action` 은 깃허브에서 지원하는 workflow

github으로 코드 push, pr 등의 이벤트를을 트리거삼아 원하는 스크립트 실행 (test, deploy)

[workflow](https://github.com/CSPCLAB/cspc_apply_server/tree/master/.github/workflows) 여기서 실행되는 스크립트 확인가능




## EDITOR SETTING (code style)
vscode 사용 권장

### FORMATTER
* Black Formatter

해당 extension 설치 후 
```json
//settings.json
{
    //...
    "[python]": {
        "editor.formatOnType": true,
        "editor.defaultFormatter": "ms-python.black-formatter"
    },
}
```
