resource "aws_service_discovery_http_namespace" "namespace" {
  name        = "invoice-cluster"
  description = "Invoice application namespace to connect services"
}