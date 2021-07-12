# senapaislist-aws-lambda

![senpaiXlambda](https://raw.githubusercontent.com/harrisonwjs/images/main/senpaiXlambda.png)

## Creating a new AWS function (with runtime dependencies)
### Create the deployment package
```bash
# Inside the $(lambda-function-name) directory...

###########################
### Implement something ###
###########################

# Install the runtime dependencies into a seperate directory 
pip install --target ./package $(package-name)
# Create the package
cd package
zip -r ../$(deployment-package-name).zip .
cd ..
zip -g $(deployment-package-name).zip $(lambda_file_name).py
```
### Create the Lambda function
```bash
# Inside the $(lambda-function-name) directory...
aws lambda create-function --function-name $(lambda-function-name) --zip-file fileb://$(deployment-package-name).zip --handler $(lambda_file_name).$(lambda_handler_name) --runtime python3.8 --role $(arn)

# $(lambda_handler_name) is the function name inside $(lambda_file_name).py
# arn can be found under the role summary in AWS IAM
```

## Updating an existing AWS function (with runtime dependencies)
### Repeat the zipping process from when you had to create a new function
```bash
# Inside the $(lambda-function-name) directory... 
zip -r ../$(deployment-package-name).zip .
zip -g $(deployment-package-name).zip $(lambda_file_name).py
# Update
aws lambda update-function-code --function-name senpaislist-broadcast-times --zip-file fileb://broadcast-times-deployment-package.zip
```

## Invoke the Lambda function
```bash
aws --cli-read-timeout 0 lambda invoke \
  --function-name $(lambda-function-name) \
      --cli-binary-format raw-in-base64-out \
          --payload '{"key1": "value1", "key2": "value2", "key3": "value3"}' output.txt
```

## Environment variables
### ADD
**_This will replace the entire Variables structure. To retain existing environment variables when you add a new one, include all existing values in your request_**
```bash
aws lambda update-function-configuration --function-name $(lambda-function-name) \
    --environment "Variables={KEY1=value1,KEY2=value2,...}"
```
### Get
```bash
aws lambda get-function-configuration --function-name $(lambda-function-name)
```

## Timeout
**_The default timeout is 3 seconds so if you are creating a new function, change the config to maximum of 900 seconds_**
```bash
aws lambda update-function-configuration --function-name $(lambda-function-name) \
    --timeout 900
```

## Premade Commands for functions
**senapaislist-broadcast-times:**
update
```bash
# update packages
cd package
zip -r ../broadcast-times-deployment-package.zip .
cd ..
# update codes
zip -g broadcast-times-deployment-package.zip get_broadcast_times.py utils/*
# update function
aws lambda update-function-code --function-name senpaislist-broadcast-times --zip-file fileb://broadcast-times-deployment-package.zip
```
invoke
```bash
aws --cli-read-timeout 0 lambda invoke \
  --function-name senpaislist-broadcast-times \
      --cli-binary-format raw-in-base64-out \
          --payload '{"key1": "value1", "key2": "value2", "key3": "value3"}' output.txt
```

## Note
- The **package directories** and the **deployment zip files** will be excluded from the repository, so run:
```bash
mkdir package
pip install --target ./package -r requirements.txt

# Then follow the above steps for the zip file
```


## References
[Deploy Python Lambda functions with .zip file archives](https://docs.aws.amazon.com/lambda/latest/dg/python-package.html)

[Lambda update-function-configuration](https://docs.aws.amazon.com/cli/latest/reference/lambda/update-function-configuration.html)
