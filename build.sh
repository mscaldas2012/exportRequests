### Variables
export APP=ExportRequests
export BUCKET=arln-lambdas

##Prepare build env
mkdir target
rm -f target/${APP}.zip

#Make sure all dependencies are available
#Manually delete packages if you're removing dependencies
pip3 install -r requirements.txt --target packages --upgrade
#Create Artifact
zip -r9 ./target/${APP}.zip main.py
zip -r9 ./target/${APP}.zip packages

#Upload Artifact to S3
aws s3 cp ./target/${APP}.zip s3://${BUCKET}/${APP}.zip

#Deploy Fucntion
#aws lambda create-function --function-name ${APP} --zip-file fileb://${APP}.zip --handler main.lambda_handler --runtime python3.7 --role arn:aws:iam::113585188124:role/Lambda-Dynamo
aws lambda update-function-code --function-name ${APP} --region us-east-1 --s3-bucket ${BUCKET} --s3-key ${APP}.zip