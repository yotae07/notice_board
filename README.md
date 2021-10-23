구현한 방법: DRF와 sqlite, oauth2를 활용하여 회원가입, 로그인, 게시판 CRUD 구현

실행방법
```
git clone git@github.com:yotae07/notice_board.git
requirements.txt가 있는 곳으로 이동
pip install -r requirements.txt
python manage.py createsuperuser로 슈퍼 유저 생성후
서버실행: python manage.py runserver 127.0.0.1:8000 or 0.0.0.0:8000
서버 실행후 localhost:8000/admin/ 접속 후 로그인
localhost:8000/o/applications/ 접속 후
name=아무거나, client type=confidential, authorizaion grant type=resource owner password-based 입력 후 저장
발급 받은 client_id, client_secret를 settings 파일안 CLIENT_ID, CLIENT_SECRET에 복사 붙여넣기
테스트코드 실행: manage.pt가 있는 곳에서 pytest
```

endpoint
```
signup
curl -i POST -H "Authorization:Bearer {로그인시 받은 토큰}" -H "Content-Type: application/json" -d '{"username":"{username}"}", "name":"{name}", "phone":"{phone}", "email":"{email}", "password":"{passowrd}"}' http://localhost:8000/users/

request
- username: str, 5~32, 영어, 숫자, _, .만 가능 띄어쓰기 불가, 중복불가
- name: str, 1~30, 한국어만 가능
- phone: str, 1~20, 숫자만 가능
- email: str, @, .com 필수 입력
- password: str, 8~20

response
- id: int, pk
- username: request와 동일 
- name: request와 동일
- phone: request와 동일
- email: request와 동일
- role: Admin, General, Manager 중 하나
- created_at: 생성 시간
- updated_at: 수정 시간
```
```
login
curl -i POST -d 'grant_type=password&username={user_name}&password={password}&scope=read write' -u'client_id:client_secret' http://localhost:8000/o/token/

request
- username: str, 5~32, 영어, 숫자, _, .만 가능 띄어쓰기 불가, 중복불가
- password: str, 8~20

response
- access_token: str, 토큰
- expires_in: int, 만료시간 초단위
- token_type: str
- scope: str, 토큰 권한
- refresh_token: str, 재발급 토큰
```
```
create post
curl -i POST -H "Authorization: Bearer {로그인시 받은 토큰}" -H "Content-Type: application/json" -d '{"title":"{title}", "content":"{content}", "writer":"{user_id}"}' http://localhost:8000/posts/

request
- title: str, 1~50
- content: str, 1~1000
- writer: int, user pk

response
- id: int, pk
- title: request와 동일
- content: request와 동일
- created_at: 생성시간
- updated_at: 수정시간
```
```
read post
token: curl -i GET -H "Authorization:Bearer {로그인시 받은 토큰}" http://localhost:8000/posts/
curl -i GET http://localhost:8000/posts/

request

response
- count: 총 게시글 개수
- next: 
- previous: 
- result: array, {
    - id: int, pk
    - title: request와 동일
    - content: request와 동일
    - created_at: 생성시간
    - updated_at: 수정시간
}, 25개
```
```
retrieve post
token: curl -i GET -H "Authorization:Bearer {로그인시 받은 토큰}" http://localhost:8000/posts/post_id/ 
curl -i GET http://localhost:8000/posts/post_id/

request

response
- id: int, pk
- title: request와 동일
- content: request와 동일
- created_at: 생성시간
- updated_at: 수정시간
```
```
patch post
curl -X PATCH -H "Authorization: Bearer {로그인시 받은 토큰}" -H "Content-Type: application/json" -d '{"title":"{title}", "content":"{content}"}' http://localhost:8000/posts/post_id/

request
- title: str, 1~50
- content: str, 1~1000

response
- id: int, pk
- title: request와 동일
- content: request와 동일
- created_at: 생성시간
- updated_at: 수정시간
```
```
delete post
curl -X DELETE -H "Authorization: Bearer {로그인시 받은 토큰}" http://localhost:8000/posts/post_id/

reqeust

response
```