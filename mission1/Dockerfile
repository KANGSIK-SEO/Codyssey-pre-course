# 1. 베이스 이미지 설정
FROM nginx:alpine

# 2. 메타데이터 추가
LABEL maintainer="Seo Kangsik"
LABEL title="My AI Dev Workstation"

# 3. 환경 변수 설정 (제약사항 반영)
ENV APP_ENV=dev

# 4. 로컬의 파일을 컨테이너로 복사 (로컬에 index.html이 있어야 함)
# COPY ./index.html /usr/share/nginx/html/index.html

# 5. 포트 노출
EXPOSE 80
