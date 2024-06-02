# Chat em Tempo Real com FastAPI e Redis

Este projeto é um chat em tempo real implementado com FastAPI e Redis. FastAPI é utilizado para criar as rotas e gerenciar as conexões WebSocket, enquanto o Redis é usado para armazenar as mensagens de chat.

## Requisitos

- Python 3.8 ou superior
- Redis
- pip install fastapi uvicorn redis


## Redis
- sudo apt-get install redis-server
- sudo service redis-server start

## FAST-API
 - uvicorn app.main:app --reload
