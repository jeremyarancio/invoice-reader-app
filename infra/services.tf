resource "aws_ecs_cluster" "invoice-cluster" {
  name = "invoice-cluster"
}

resource "aws_ecs_service" "server-service" {
  name            = "invoice-server"
  cluster         = aws_ecs_cluster.invoice-cluster.id
  task_definition = aws_ecs_task_definition.server-task-definition.arn
  desired_count   = 1
  launch_type     = "FARGATE"

  deployment_circuit_breaker {
    enable   = true
    rollback = false
  }

  network_configuration {
    subnets          = data.aws_subnets.default.ids
    security_groups  = [aws_security_group.sg.id]
    assign_public_ip = true
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.server-target-group.arn
    container_name   = "invoice-server"
    container_port   = 8000
  }

  service_connect_configuration {
    enabled   = true
    namespace = aws_service_discovery_http_namespace.namespace.arn
  }
}

resource "aws_ecs_service" "ui_service" {
  name            = "invoice-ui"
  cluster         = aws_ecs_cluster.invoice-cluster.id
  task_definition = aws_ecs_task_definition.ui-task-definition.arn
  desired_count   = 1
  launch_type     = "FARGATE"

  network_configuration {
    subnets          = data.aws_subnets.default.ids
    security_groups  = [aws_security_group.sg.id]
    assign_public_ip = true
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.ui-target-group.arn
    container_name   = "invoice-ui"
    container_port   = 5173
  }

  deployment_circuit_breaker {
    enable   = true
    rollback = false
  }
}

resource "aws_ecs_service" "pg_service" {
  name            = "invoice-pg"
  cluster         = aws_ecs_cluster.invoice-cluster.id
  task_definition = aws_ecs_task_definition.pg-task-definition.arn
  desired_count   = 1
  launch_type     = "FARGATE"

  network_configuration {
    subnets          = data.aws_subnets.default.ids
    security_groups  = [aws_security_group.sg.id]
    assign_public_ip = true
  }

  service_connect_configuration {
    enabled   = true
    namespace = aws_service_discovery_http_namespace.namespace.arn
    service {
      client_alias {
        port = 5432
      }
      discovery_name = "invoice-postgres"
      port_name      = "invoice-postgres-port"
    }
  }

  deployment_circuit_breaker {
    enable   = true
    rollback = false
  }
}
