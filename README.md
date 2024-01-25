# cspc_apply_server
## DEV (local)
로컬에서 개발할 때 가이드 

로컬에서 개발할때는, sqlite3 local DB를 사용함 (배포용 DB와 별도)

### 소스코드 다운로드
```bash
git clone https://github.com/CSPCLAB/cspc_apply_server.git
```

### 가상환경 세팅
```bash
cd ./app
conda activate env # 가상환경 세팅
pip install -r requirements

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

다만 웬만해서 PR을 통해 test후 배포하는 것을 권장

직접 배포해야 하는 상황이 있다면 (ex DB migration 충돌)
```bash
cd $PROJECT_PATH
docker-compose down
docker-compose up --build -d
```

## FEAT
작성중...
### Swagger
* /swagger : API test
* /redoc : API 문서
### API
각 API endpoint마다 django-rest-api 테스트 form 구현(다만 swagger로 테스트하는 걸 추천)

### AUTH
`student_id`를 통해 로그인하도록 custom backend 구현

다만 계정 생성, 로그인 API 수정하는 걸 추천 
> TODO : `user.view.py` 수정

### Test
workflow에 push시, test 실행되도록 구현

다만 아직 테스트 코드 구현 X
> TODO : 각 모듈별 `tests.py` 내 테스트 코드 작성 

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
