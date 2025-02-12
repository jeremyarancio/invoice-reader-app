# Notes

## 05/02/2025: ECS & VPC

* Struggled for days to make the PG DB available. For PG, we need to remove the HTTP protocole in task definition!
* Service connect enables connection between services:
    * Client-side: only send request (Front-end)
    * Client-Server: send and receive requests (Server, PG)
* Assign LogCreate to IAM role (ECSTaskexecution or custom role to log)
* Enable logging in task definition (use log collection stupid!)
* Error DNS from Front-End because even if UI container is in the VPC, the browser send the requests, therefore outside of the VPC, resulting in a DNS error. Recommended: Load [balancing](https://repost.aws/questions/QUAwiyQWEuTlGNKKV8tyYdUw/ecs-service-connect-not-able-to-connect-to-backend-from-frontend-application)
    * **To solve the issue with service connect and the browser, we use load balancer for both UI & SERVER and add a rule to the ALB to redirect requests: check Terraform solution**
* The ALB listen to port 80, and target group the front end port (5173)
* To enable container to perform tasks such as pulling image from ecr or docker hub, the ip needs to be public (in the video, I turns off the public, so I don't know how does he do)
    * Configure with **VPS endpoint**
* Use cloudformation to iac feature from AWS
* Use API Gateway in proxy with lambda to host the backend: cheaper solution in the future.
 

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


