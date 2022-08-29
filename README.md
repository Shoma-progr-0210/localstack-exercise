# LocalStack Exercise

## 環境

- git
- Docker
- Docker Compose

## 準備

リポジトリ直下に[LocalStack](https://github.com/localstack/localstack)をcloneする

```bash
git clone https://github.com/localstack/localstack.git
```

## LocalStack

### 起動

```bash
docker-compose -f ./localstack/docker-compose.yml up -d
```

### 削除

```bash
docker-compose -f ./localstack/docker-compose.yml down -v
```

## exerciseの実施

`./exercises`にある演習を順番に行う  
ホストからも使用できるが、環境依存を考慮し、exerciseコンテナを使用することを推奨  

### 起動

```bash
docker-compose -f ./exercise_container/docker-compose.yml up -d
```

### コンテナに入る

```bash
docker exec -it exercise /bin/bash
```

### 削除

```bash
docker-compose -f ./exercise_container/docker-compose.yml down -v
```
