# Mission 1: AI/SW 개발 워크스테이션 구축

## 1) 프로젝트 개요
터미널, Docker, Git을 활용하여 재현 가능한 개발 환경을 구축하고, 커스텀 웹 서버 컨테이너를 통해 실행 환경의 격리 및 데이터 영속성을 검증합니다.

## 2) 실행 환경
- **OS**: macOS (Sequoia 15.3.1)
- **Shell**: zsh
- **Docker**: 27.5.1
- **Git**: 2.47.1

## 3) 수행 항목 체크리스트
- [x] 터미널 기본 조작 및 폴더 구성
- [x] 권한 변경 실습
- [x] Docker 설치/점검
- [x] hello-world 실행 및 ubuntu 진입 실습
- [x] Dockerfile 빌드/실행 (커스텀 Nginx 이미지)
- [x] 포트 매핑 접속 확인 (8080:80)
- [x] 볼륨 영속성 검증 (데이터 유지 확인)
- [x] Git 설정 및 GitHub 연동 확인

## 4) 검증 방법 및 결과
### [터미널 조작 및 권한 실습]
```bash
$ pwd
/Users/kangsikseo/Downloads/Codyssey-pre-course
$ mkdir -p mission1/practice
$ cd mission1/practice
$ touch test_file.txt
$ echo "Hello Codyssey" > test_file.txt
$ cp test_file.txt copy_file.txt
$ mv copy_file.txt renamed_file.txt
$ ls -la
total 16
drwxr-xr-x  4 kangsikseo  staff  128 Mar 31 02:25 .
drwxr-xr-x  6 kangsikseo  staff  192 Mar 31 02:25 ..
-rw-r--r--  1 kangsikseo  staff   15 Mar 31 02:25 renamed_file.txt
-rw-r--r--  1 kangsikseo  staff   15 Mar 31 02:25 test_file.txt

# 권한 변경 (chmod)
$ touch perm_test.txt
$ mkdir perm_dir
$ ls -l perm_test.txt
-rw-r--r--  1 kangsikseo  staff  0 Mar 31 02:25 perm_test.txt
$ chmod 644 perm_test.txt
$ chmod 755 perm_dir
$ ls -ld perm_dir
drwxr-xr-x  2 kangsikseo  staff  64 Mar 31 02:25 perm_dir
```

### [Docker 운영 및 빌드]
- **Dockerfile**: [Dockerfile](./Dockerfile)
- **커스텀 이미지 빌드 및 실행**:
```bash
$ docker build -t codyssey-web:1.0 .
$ docker run -d -p 8080:80 --name codyssey-web-server codyssey-web:1.0
$ curl -I http://localhost:8080
HTTP/1.1 200 OK
Server: nginx/1.29.7
...
```

### [볼륨 영속성 검증]
```bash
# 1. 볼륨 생성 및 데이터 쓰기
$ docker volume create codyssey-data
$ docker run --name vol-test -v codyssey-data:/app-data alpine sh -c "echo 'persistence data v2' > /app-data/status.txt"

# 2. 컨테이너 삭제 후 새로운 컨테이너에서 데이터 확인
$ docker run --name vol-test-recovery -v codyssey-data:/app-data alpine cat /app-data/status.txt
persistence data v2
```

### [Git 설정]
```bash
$ git config --list | grep user
user.name=kangsikseo
user.email=********@gmail.com
```

## 5) 트러블슈팅
### Case 1: Docker Daemon 연결 실패
- **문제**: `docker ps` 실행 시 `Cannot connect to the Docker daemon` 에러 발생.
- **원인 가설**: OrbStack(또는 Docker Desktop) 앱이 실행되지 않아 백그라운드 엔진이 구동되지 않음.
- **확인**: `open -a Docker` 명령으로 앱 실행 시도.
- **해결**: 앱 실행 후 몇 초 대기하니 소켓 연결이 정상화되어 명령어 수행 가능해짐.

### Case 2: 볼륨 검증 중 컨테이너 종료로 인한 exec 실패
- **문제**: `docker exec` 수행 시 `container ... is not running` 발생.
- **원인 가설**: `sh -c "echo ..."` 명령이 완료되자마자 컨테이너가 종료(Exited)됨.
- **확인**: `docker ps -a`로 상태 확인 시 `Exited (0)`.
- **해결**: `exec` 대신 컨테이너 실행 시 직접 명령어를 전달하거나(`docker run ... cat ...`), 실행 상태를 유지하도록 구성하여 해결.

---
**학습 포인트**: 이미지와 컨테이너를 분리함으로써 애플리케이션의 재현성을 확보하고, 볼륨을 통해 컨테이너 삭제 후에도 데이터를 유지하는 설계의 중요성을 체득함.
