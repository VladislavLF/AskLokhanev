# AskLokhanev
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![Django](https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white) ![MySQL](https://img.shields.io/badge/mysql-4479A1.svg?style=for-the-badge&logo=mysql&logoColor=white) ![Docker](https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white) ![Nginx](https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white) ![Gunicorn](https://img.shields.io/badge/gunicorn-%298729.svg?style=for-the-badge&logo=gunicorn&logoColor=white) ![HTML5](https://img.shields.io/badge/html5-%23E34F26.svg?style=for-the-badge&logo=html5&logoColor=white) ![CSS3](https://img.shields.io/badge/css3-%231572B6.svg?style=for-the-badge&logo=css3&logoColor=white) ![JavaScript](https://img.shields.io/badge/javascript-%23323330.svg?style=for-the-badge&logo=javascript&logoColor=%23F7DF1E)<br /><br />
A fully functional StackOverflow clone with a question and answer system, implemented in Django using modern technologies. <br />

## Peculiarities
- Questions and Answers - posting questions, answers, and comments.
- Rating system - likes/dislikes for questions and answers.
- Tags - categorize questions by topic.
- Search - smart search for questions and answers.
- Authentication - user Registration and Authorization.
- Realtime Updates - centrifugo for real-time updates.
- Caching - memcached for fast performance.
- Pagination - pagination for lists.

## Stack
- Backend: Django 5.1.7, Python 3.11.
- Database: MySQL 8.0.
- Cache: Memcached.
- WebSocket: Centrifugo v4.
- Web Server: Nginx + Gunicorn.
- Container: Docker + Docker Compose.
- Authentication: Django Auth System.
- Real-time: Centrifugo + WebSocket. 
- Task Scheduling: Django-crontab.

## Quick start
### 1. Prerequisites
- Docker
- Git
### 2. Installation and launch
#### 2.1. Clone the repository
`git clone <repository-url>`
`cd AskLokhanev`
#### 2.2. Set up environment variables
`cp .env.production.example .env` or `cp .env.development.example .env`
#### 2.3. Launch the project
`docker-compose --env-file .env up --build`

## Site images
<img width="1859" height="929" alt="image" src="https://github.com/user-attachments/assets/c7b9e2d5-a47e-4dac-a231-975d858cf2da" /><br />
<img width="1874" height="932" alt="image" src="https://github.com/user-attachments/assets/09983e5b-ecb7-4fea-b36d-ef4ff0440325" /><br />
<img width="1858" height="933" alt="image" src="https://github.com/user-attachments/assets/aedb6e2c-4f03-459e-a57c-f6e2c32bbe76" /><br />
<img width="1858" height="933" alt="image" src="https://github.com/user-attachments/assets/036caaec-9d62-4524-bff2-bed7f0ca69c1" /><br />
<img width="1862" height="932" alt="image" src="https://github.com/user-attachments/assets/1f959019-cff2-45ec-9221-84bc46327237" /><br />
<img width="1875" height="929" alt="image" src="https://github.com/user-attachments/assets/b7804d33-015e-4fee-8b20-a50e02327b93" />
