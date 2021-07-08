# AWS SAM Lambda Deployment Steps

First, set up AWS CLI and configure a profile to be used.

```
aws configure --profile PROFILE_NAME
```

After making changes to the serverless apps, build it
```
sam build
```

To test locally, you need to configure `local_env.json` from the `local_env.sample.json`
```
sam local invoke BinanceCrawlerFunction --env-vars local_env.json
```

Deploy to AWS.  **IMPORTANT** Do not set `PGPASSLOCAL`, it is only used for local invoke testing due to lack of parameter store support.  The lambda functions require `PGPASSLOCAL` to be blank to look for the password in parameter store.

First time (or new env vars required):
```
sam deploy --guided --profile PROFILE_NAME
```

Thereafter:
```
sam deploy
```


# Documenting Some Past Issues

1. Need to `chmod 755` or there is insufficient permissions to access the files
2. VPC and role configuration (maybe?) is not done in `template.yaml`, do that after new lambdas are created if needed
3. Parameter store is not supported locally, so configure `local_env.json` to test and ensure to not deploy passwords
4. Do NOT manually remove things created by SAM

# Other Note

* Test not implemented

# Resources

* See the [AWS SAM developer guide](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/what-is-sam.html) for an introduction to SAM specification, the SAM CLI, and serverless application concepts.
* Next, you can use AWS Serverless Application Repository to deploy ready to use Apps that go beyond hello world samples and learn how authors developed their applications: [AWS Serverless Application Repository main page](https://aws.amazon.com/serverless/serverlessrepo/)
