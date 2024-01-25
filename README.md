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

## DEPLOY
git action을 통해 master 브런치에 push or PR merge 시, 자동으로 배포

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

### API



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
