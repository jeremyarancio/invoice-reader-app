# Notes

## 30/01/2025: ECS setup

### ECS

* Authorize ECS task to use AWS services such as S3: assign a role with *ecs-tasks.amazonaws.com* in **Trust relationships** ([sources](https://repost.aws/knowledge-center/ecs-unable-to-assume-role)):

```
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "",
            "Effect": "Allow",
            "Principal": {
            "Service": "ecs-tasks.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }
    ]
}
```

*  Environment variables can be added by:
    * Adding varibale in plain text in the `task-definition.json` file
    * Storing a *.env* in S3
    * Use AWS Secret Manager

*  To add a role manually into local-dev:
    * Create a user and assign roles you want
    * Create .aws folder with a `config`and `credentials` file with the 

    ```
    # credentials
    [default]
    aws_access_key_id = ...
    aws_secret_access_key = ...
    ```

    ```
    # config
    [default]
    region= ...
    ```
    * Mount volume to Docker Compose in /root ([source](https://stackoverflow.com/questions/49502552/pass-aws-role-supplied-credentials-to-docker-container))

* Easier method: add KEYS as env variables in `.env` file

```bash
$ export AWS_ACCESS_KEY_ID=AKIAIOSFODNN7EXAMPLE
$ export AWS_SECRET_ACCESS_KEY=wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
$ export AWS_DEFAULT_REGION=us-west-2
```

* To connect to Postgres on ECS, allow 0.0.0.0 traffic in **Security Group** => Need to check network good practices


