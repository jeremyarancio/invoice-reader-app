# Notes

## Docker React Vite
* Super tricky, Vite is not configured to run on Docker natively. The solution: `npm run dev -- --host`

## Refresh token
* Cookie is sent to from the Server, but the GET or POST method from the Front-End should include {withCredentials: true}
* Cookie can only be shared under the same domain => put everything under Traefik
```
const response = await api.post("users/signin/", formData, {
        withCredentials: true,
    });
```
* Finally, the solution was to use local domain name (for WSL, change `/mnt/c/Windows/System32/drivers/etc/hosts`). Here's the cookie set up in Fastapi:

```python
response.set_cookie(
    key="refresh_token",
    value=refresh_token,
    httponly=True,
    secure=False,
    samesite="lax",
    domain="localdev.test",
    max_age=1800,
)
```

## Monitoring
### Prometheus Grafana
* `rate(http_requests_total{handler!~"/|/metrics|/openapi.json|none"}[1m])` --> Calculate the number of requests per seconds for everything except {} in average in a 1 minute range.

## 04/04/2025
### Exception handler
* Error handler: HTTPException returns {"detail": <error message>} by default. But by using exception_handler in fastAPI, we can custom how the HTTPException, or any other exception is returned
* This can lead to removing all httpexception from all route, making the code lighter
* On the FE side, Axios stores the custom error message behind: (error) => error.response.data.message. Error.message represents the default status code error.

## 28/03/2025
* When deploying on GKE, every step needs more time for the deployment. Be patient.
* Pushing to the ghcr.io is private by default.

## 26/03/2025
* Minikube can be quite buggy: `minikube delete --all --purge`
* Enable minikube to access local images: `eval $(minikube docker-env)`. Now all docker command will run inside minikube (build docker images)
* Silent failure from the UI due to Typescript errors during build
* Also, missed set -e in the entrypoint
* VITE can cache, leading to weird behaviours. Force fresh start: `npm run dev -- --force`

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


