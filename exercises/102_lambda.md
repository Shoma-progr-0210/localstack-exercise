# 102 Lambda

LocalStackにLambdaを作成する  
Lambdaを実行して動作を確認する  

## 事前準備

|環境変数名|説明|
|:-:|:-:|
|LAMBDA_FUNCTION_NAME|Lambdaの関数名|

```bash
export LAMBDA_FUNCTION_NAME=test-lambda
```

## 関数の作成

`test_lambda.py`をzip化したソースコードで`test-lambda`関数を作成する　　
※ロール(`--role`)は適当でよい  

```bash
aws lambda create-function \
    --function-name $LAMBDA_FUNCTION_NAME \
    --runtime python3.9 \
    --zip-file fileb:///exercise/appendix/test_lambda.zip \
    --role test-role \
    --handler test_lambda.lambda_handler \
    --endpoint-url=$ENDPOINT_URL --profile localstack
```

関数の一覧を確認する  
`test-lambda`が作成されていることを確認する  

```bash
aws lambda list-functions --endpoint-url=$ENDPOINT_URL --profile localstack
```

## 動作確認

`lambda_input.json`を使用して動作確認を行う  

```bash
aws lambda invoke \
    --function-name $LAMBDA_FUNCTION_NAME \
    --payload file:///exercise/appendix/lambda_input.json /tmp/exercise/result.txt \
    --cli-binary-format raw-in-base64-out \
    --endpoint-url=$ENDPOINT_URL --profile localstack
```

`/tmp/exercise/result.txt`に関数の戻り値が出力されるので、内容を確認する  
※ホストの`./tmp`でも確認できる  

```bash
cat /tmp/exercise/result.txt
```
