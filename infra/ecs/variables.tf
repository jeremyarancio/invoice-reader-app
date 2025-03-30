variable "aws_region" {
  description = "The AWS region to deploy resources"
  type        = string
}

variable "postgres_user" {
  description = "Username for the PostgreSQL database"
  type        = string
  sensitive   = true
}

variable "postgres_password" {
  description = "Password for the PostgreSQL database"
  type        = string
  sensitive   = true
}

variable "postgres_db" {
  description = "Name of the PostgreSQL database"
  type        = string
  sensitive   = true
}

variable "jwt_secret_key" {
  description = "Secret key for JWT encoding"
  type        = string
  sensitive   = true
}

variable "jwt_algorithm" {
  description = "JWT algorithm"
  type        = string
  sensitive   = true
}

variable "s3_bucket_name" {
  description = "Name of the S3 bucket for the application"
  type        = string
  sensitive   = true
}

variable "ecr_repository_url" {
  description = "URL of the ECR repository"
  type        = string
  sensitive   = true
}

variable "ecs_task_execution_role_arn" {
  description = "ARN of the ECS task execution role"
  type        = string
  sensitive   = true
}

variable "invoice_server_role_arn" {
  description = "ARN of the role for the invoice server"
  type        = string
  sensitive   = true
}