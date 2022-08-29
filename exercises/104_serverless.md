# 104 Serverless Architecture

## 事前準備

|環境変数名|説明|
|:-:|:-:|
|SQS_QUEUE_NAME|SQSのキュー名|
|SQS_QUEUE_URL|SQSのキューのURL|
|SQS_QUEUE_ARN|SQSのキューのARN|
|S3_BUCKET_NAME|S3のバケット名|
|LAMBDA_FUNCTION_NAME|Lambdaの関数名|
|CLOUDWATCH_LOG_GROUP_NAME|Lambdaのログが記録されるCloudWatchロググループ名|

```bash
export SQS_QUEUE_NAME=words-queue
export SQS_QUEUE_URL=$ENDPOINT_URL/000000000000/$SQS_QUEUE_NAME
export SQS_QUEUE_ARN=arn:aws:sqs:ap-northeast-1:000000000000:$SQS_QUEUE_NAME
export S3_BUCKET_NAME=words-bucket
export LAMBDA_FUNCTION_NAME=words-lambda
export CLOUDWATCH_LOG_GROUP_NAME=/aws/lambda/$LAMBDA_FUNCTION_NAME
```

## メッセージを管理するSQSキューの作成

### Question. SQSで`words-queue`キューを作成する

※103 SQSで行った内容を参考にすること

<details>
<summary>Answer</summary>

```bash
aws sqs create-queue --queue-name $SQS_QUEUE_NAME --endpoint-url=$ENDPOINT_URL --profile localstack
```
</details>

## Lambdaで処理した内容を保存するS3バケットの作成

### Question. S3で`words-bucket`バケットを作成する

※101 S3で行った内容を参考にすること

<details>
<summary>Answer</summary>

```bash
aws s3 mb s3://$S3_BUCKET_NAME --endpoint-url=$ENDPOINT_URL --profile localstack
```
</details>

## SQSのメッセージを受信するLambda関数の作成

### Question. Lambdaで`words-lambda`関数を作成する

※102 Lambdaで行った内容を参考にすること  
条件  
- ソースコードのzipファイルは`/exercise/appendix/process_messages.zip`を使用する  
- ハンドラーは`process_messages.lambda_handler`とする
- 追加のオプションとして、環境変数を設定するオプション`--environment "Variables={AWS_ACCESS_KEY_ID=dummy,AWS_SECRET_ACCESS_KEY=dummy,REGION_NAME=ap-northeast-1,ENDPOINT_URL=$ENDPOINT_URL,BUCKET_NAME=$S3_BUCKET_NAME}"`を使用する


<details>
<summary>Answer</summary>

```bash
aws lambda create-function \
    --function-name $LAMBDA_FUNCTION_NAME \
    --runtime python3.9 \
    --zip-file fileb:///exercise/appendix/process_messages.zip \
    --role test-role \
    --handler process_messages.lambda_handler \
    --environment "Variables={AWS_ACCESS_KEY_ID=dummy,AWS_SECRET_ACCESS_KEY=dummy,REGION_NAME=ap-northeast-1,ENDPOINT_URL=$ENDPOINT_URL,BUCKET_NAME=$S3_BUCKET_NAME}" \
    --endpoint-url=$ENDPOINT_URL --profile localstack
```
</details>

## Lambdaのイベントソースマッピング作成

### SQSキューのメッセージをポーリングしてイベントとして受け取って処理するため、SQSとLambdaをマップする

これにより、SQSにキューを送信すると、Lambdaで処理されることになる  
`--batch-size`は各Lambdaがポーリング時にキューを受信する数である  

```bash
aws lambda create-event-source-mapping \
    --function-name $LAMBDA_FUNCTION_NAME \
    --batch-size 2 \
    --event-source-arn $SQS_QUEUE_ARN \
    --endpoint-url=$ENDPOINT_URL --profile localstack
```

## 動作確認

SQSキューに3件メッセージを送信して、Lambdaで正常に処理されて結果がS3に保存されることを確認する

### Question. SQSの`words-queue`キューにメッセージを3件送信する

※103 SQSで行った内容を参考にすること   
条件  
- 送信する`--message-body`は、以下の3つ
  - /exercise/appendix/sqs_input_msg_001.json 
  - /exercise/appendix/sqs_input_msg_002.json 
  - /exercise/appendix/sqs_input_msg_003.json 

<details>
<summary>Answer</summary>

```bash
aws sqs send-message --queue-url $SQS_QUEUE_URL --message-body file:///exercise/appendix/sqs_input_msg_001.json --endpoint-url=$ENDPOINT_URL --profile localstack
aws sqs send-message --queue-url $SQS_QUEUE_URL --message-body file:///exercise/appendix/sqs_input_msg_002.json --endpoint-url=$ENDPOINT_URL --profile localstack
aws sqs send-message --queue-url $SQS_QUEUE_URL --message-body file:///exercise/appendix/sqs_input_msg_003.json --endpoint-url=$ENDPOINT_URL --profile localstack
```
</details>

### Lambda関数が正常に動作したかをCloudWatch Logsから確認する

ロググループ一覧を表示する

```bash
aws logs describe-log-groups --endpoint-url=$ENDPOINT_URL --profile localstack
```

Lambdaのログが記録されているロググループを確認する  

```bash
aws logs describe-log-groups --log-group-name $CLOUDWATCH_LOG_GROUP_NAME --endpoint-url=$ENDPOINT_URL --profile localstack
```

特定のロググループのログストリームの一覧を表示する  

```bash
aws logs describe-log-streams --log-group-name $CLOUDWATCH_LOG_GROUP_NAME --endpoint-url=$ENDPOINT_URL --profile localstack
```

特定のロググループのログストリームの内容を表示する  
`CLOUDWATCH_LOG_STREAM_NAME`は、ログストリーム一覧から選択すること  

```bash
export CLOUDWATCH_LOG_STREAM_NAME=2022/08/29/[LATEST]d8731ea4
aws logs get-log-events --log-group-name $CLOUDWATCH_LOG_GROUP_NAME --log-stream-name $CLOUDWATCH_LOG_STREAM_NAME --endpoint-url=$ENDPOINT_URL --profile localstack
```

### Question. LambdaからS3にアップロードされたファイルをダウンロードする

※101 S3で行った内容を参考にすること  
条件  
- ダウンロードするファイルパスは`s3://$S3_BUCKET_NAME/`
- 再帰的に処理するオプション`--recursive`を使用する
- ダウンロード先は`/tmp/exercise/`

<details>
<summary>Answer</summary>

```bash
aws s3 cp s3://$S3_BUCKET_NAME/ /tmp/exercise/ --recursive --endpoint-url=$ENDPOINT_URL --profile=localstack
```
</details>

ダウンロードしたファイルのJSONに`sentence`フィールドがあること

```json
{"id": "001", "name": "Alice", "word": "What's up?", "sentence": "Alice said, \"What's up?\""}
{"id": "002", "name": "Bob", "word": "Hello.", "sentence": "Bob said, \"Hello.\""}
{"id": "003", "name": "Charlie", "word": "Hi!", "sentence": "Charlie said, \"Hi!\""}
```
