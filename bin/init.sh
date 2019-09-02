export APP=test
export BUCKET=arln-lambdas
export RUNTME=python3
export HANDLER=main.lambda_handler
#Todo: create role here!
export ROLE=arn:aws:iam::113585188124:role/Lambda-Dynamo

mkdir target
touch ${APP}.zip
aws lambda create-function --function-name ${APP} --region us-east-1 --handler ${HANDLER} --runtime python3.7 --role ${ROLE}
