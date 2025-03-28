resource "aws_ecs_task_definition" "pg-task-definition" {
  family                   = "invoice-postgres"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "512"
  memory                   = "1024"
  execution_role_arn       = var.ecs_task_execution_role_arn
  container_definitions = jsonencode([
    {
      name      = "invoice-postgres"
      image     = "${var.ecr_repository_url}/postgres-17.2"
      essential = true
      portMappings = [
        {
          name          = "invoice-postgres-port"
          containerPort = 5432
          hostPort      = 5432
          protocol      = "tcp"
        }
      ]
      environment = [
        {
          name  = "POSTGRES_USER"
          value = var.postgres_user
        },
        {
          name  = "POSTGRES_PASSWORD"
          value = var.postgres_password
        },
        {
          name  = "POSTGRES_DB"
          value = var.postgres_db
        }
      ]
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          awslogs-group         = "/ecs/invoice-postgres"
          awslogs-create-group  = "true"
          awslogs-region        = var.aws_region
          awslogs-stream-prefix = "ecs"
        }
      }
    }
  ])
}

resource "aws_ecs_task_definition" "server-task-definition" {
  family                   = "invoice-server"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "512"
  memory                   = "1024"
  execution_role_arn       = var.ecs_task_execution_role_arn
  task_role_arn            = var.invoice_server_role_arn
  container_definitions = jsonencode([
    {
      name      = "invoice-server"
      image     = "${var.ecr_repository_url}/invoice-server"
      essential = true
      portMappings = [
        {
          name          = "invoice-server-port"
          containerPort = 8000
          hostPort      = 8000
          protocol      = "tcp"
        }
      ]
      environment = [
        {
          name  = "FRONT_END_URL"
          value = "*"
        },
        {
          name  = "POSTGRES_USER"
          value = var.postgres_user
        },
        {
          name  = "S3_BUCKET"
          value = var.s3_bucket_name
        },
        {
          name  = "JWT_ALGORITHM"
          value = "HS256"
        },
        {
          name  = "POSTGRES_PASSWORD"
          value = var.postgres_password
        },
        {
          name  = "POSTGRES_DB"
          value = var.postgres_db
        },
        {
          name  = "JWT_SECRET_KEY"
          value = var.jwt_secret_key
        },
        {
          name  = "POSTGRES_SERVER"
          value = "invoice-postgres.invoice-cluster:5432"
        }
      ]
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          awslogs-group         = "/ecs/invoice-server"
          awslogs-create-group  = "true"
          awslogs-region        = var.aws_region
          awslogs-stream-prefix = "ecs"
        }
      }
    }
  ])
}

resource "aws_ecs_task_definition" "ui-task-definition" {
  family                   = "invoice-ui"
  network_mode             = "awsvpc"
  requires_compatibilities = ["FARGATE"]
  cpu                      = "512"
  memory                   = "1024"
  execution_role_arn       = var.ecs_task_execution_role_arn
  container_definitions = jsonencode([
    {
      name      = "invoice-ui"
      image     = "${var.ecr_repository_url}/invoice-ui"
      essential = true
      portMappings = [
        {
          name          = "invoice-ui-port"
          containerPort = 5173
          hostPort      = 5173
          protocol      = "tcp"
        }
      ]
      environment = [
        {
          name  = "VITE_SERVER_API_URL"
          value = "http://${aws_lb.alb.dns_name}/"
        }
      ]
      logConfiguration = {
        logDriver = "awslogs"
        options = {
          awslogs-group         = "/ecs/invoice-ui"
          awslogs-create-group  = "true"
          awslogs-region        = var.aws_region
          awslogs-stream-prefix = "ecs"
        }
      }
    }
  ])
}
