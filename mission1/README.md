# Mission 1: AI/SW 개발 워크스테이션 구축

## 📝 목표
Docker를 활용하여 독립된 개발 환경을 설정하고 컨테이너를 관리합니다.

## 📋 요구사항
- Dockerfile 작성
- 베이스 이미지 설정 (nginx:alpine)
- 환경 변수 및 메타데이터 설정
- 포트 노출 (80)

## 🚀 실행 방법
```bash
docker build -t my-workstation:latest .
docker run -p 80:80 my-workstation:latest
```

## 📂 파일 구조
- `Dockerfile`: Docker 이미지 정의 파일
