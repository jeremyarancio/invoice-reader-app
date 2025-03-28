resource "aws_lb" "alb" {
  name               = "invoice-alb"
  internal           = false
  load_balancer_type = "application"
  security_groups    = [aws_security_group.alb_sg.id]
  subnets            = data.aws_subnets.default.ids
}

resource "aws_lb_target_group" "ui-target-group" {
  name        = "invoice-ui-tg"
  port        = 5173
  protocol    = "HTTP"
  vpc_id      = data.aws_vpc.default.id
  target_type = "ip"

  health_check {
    path = "/"
  }
}

resource "aws_lb_target_group" "server-target-group" {
  name        = "invoice-server-tg"
  port        = 8000
  protocol    = "HTTP"
  vpc_id      = data.aws_vpc.default.id
  target_type = "ip"

  health_check {
    path = "/"
  }
}

resource "aws_lb_listener" "ui" {
  load_balancer_arn = aws_lb.alb.arn
  port              = "80"
  protocol          = "HTTP"

  default_action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.ui-target-group.arn
  }
}

resource "aws_lb_listener_rule" "server" {
  listener_arn = aws_lb_listener.ui.arn

  action {
    type             = "forward"
    target_group_arn = aws_lb_target_group.server-target-group.arn
  }

  condition {
    path_pattern {
      values = ["/api/*"]
    }
  }
}