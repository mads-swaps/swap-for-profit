# AWS Setup

This is a documentation of the steps take for AWS setup.

## Account and IAM Setup

IAM accounts are created for each member of the team with limited IAM policies.

1. AWS Root account creation
2. IAM accounts created for other members of the capstone team
    1. Include IAM policy for RDS access

## RDS Setup

RDS is used for PostgreSQL database.  Additional user accounts are required for connection to the PostgreSQL server.

1. Create RDS database with Easy Create wizard
    1. PostgreSQL engine
    2. Free tier option (scale up later if needed)
2. Configure master user and password
3. Setup additional user accounts and tables according to SQL files in `./rds/` directory
4. Inbound traffic to RDS is blocked by default, VPC -> Security Group
    1. Create new security group
    2. Add inbound rule for the PostgreSQL port (5432), allowing a range of source IPs
    3. Set RDS to use the newly created security group

## Parameter Store Setup

SecretString from the System Manager Parameter Store is one of many way to store passwords and sensitive configuration without exposing them in code on AWS.  We need this to allow Lambda to connect to the database.  We choose it because it was simple to setup.

1. Go to AWS System Manager > Parameter Store
2. Create new parameter and select Standard + SecretString option, with your secret as value

## Lambda Setup

Lambda is used to fetch the latest klines data from Binance and store it in the database.  We use Lambda instead of EC2 due to very sparse computational needs (<1 second every 15 minutes).

1. Go to Lambda, create function from scratch
    1. Runtime: Python 3.8
    2. Permissions -> Execution role: Create a new role with basic Lambda permissions
    3. Advanced Settings -> Network -> VPC: Selecting default VPC is OK here
2. Copy the code from `lambda_function.py` and replace it
3. Copy these files https://github.com/jkehler/awslambda-psycopg2/tree/master/psycopg2-3.8 to `psycopg2` folder.
4. Other configurations:
    1. Increase timeout to 10 seconds, as 3 seconds may be too short
    2. Environment variables: `pg_host`, `pg_db`, `pg_user`
    3. VPC changes to allow connection to internet: https://blog.theodo.com/2020/01/internet-access-to-lambda-in-vpc/
    4. Add `ssm:GetParameter` policy to the created Lambda role to access Parameter Store
5. Setup scheduled triggers for automatic data fetching
    1. Go to AWS EventBridge -> Rules
    2. Create Rule, Schedule with cron expression `1-59/15 * * * ? *`
    3. Select the Lambda function as target
