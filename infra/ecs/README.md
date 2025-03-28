# Invoice Manager Infrastructure

This directory groups all Terraform scripts to deploy the application on AWS.

## Infrastructure

The containers are deployed on AWS ECS using Terraform.
Each script represents a part of the infrastructure requiresd by ECS.

## Variables

Variables are stored in the file `variables.tf`.
The value for each is stored in a `terraform.tfvars` file not publicly shared.

## Deploy the infra

To deploy the infrastructure using Terraform, run after creating the `terraform.tfvars` file:

```
terraform apply
```

The AWS permission are not set up yet with Terraform, so you'll need to give the proper permissions to make this command works.

To terminate and delete the entire infrastructure, run:

```
terraform destroy
```

## TODO

* Mount EFS to Postgres container
* Add permissions to Terraform (?)