

# Custom domain setup for the API Gateway HTTP API
#
# This file connections four resources to expose the API at
# https://<subdomain>.<domain_name> with a valid TLS certificate:
#
# 1. aws_acm_certificate — requests a TLS certificate from AWS Certificate
#    Manager for the custom domain using DNS validation. Terraform outputs
#    the required CNAME record; it is added to the DNS provider manually
#
# 2. aws_acm_certificate_validation — waits until ACM confirms the
#    certificate has been issued. Only completes onces the validation
#    CNAME has been added to the DNS provider manually
#
# 3. aws_apigatewayv2_domain_name — registers the custom domain with API
#    Gateway and attaches the validated certificate. Produces a hostname 
#    (e.g. d-xxxxx.execute-api.ca-central-1.amazonaws.com) to point the 
#    CNAME to from the third party.
#
# 4. aws_apigatewayv2_api_mapping — connects the custom domain to the
#    $default stage of the HTTP API so that requests arriving at the custom
#    domain are routed to the Lambda function.
#
#  This is hacked together and maybe a mess.


locals {
  api_subdomain = "${var.subdomain}.${var.domain_name}"
}

# ACM certificate for the custom domain. Validation is done via DNS
resource "aws_acm_certificate" "api" {
  domain_name       = local.api_subdomain
  validation_method = "DNS"

  lifecycle {
    create_before_destroy = true
  }
}

# Waits until ACM confirms the certificate has been issued.
resource "aws_acm_certificate_validation" "api" {
  certificate_arn = aws_acm_certificate.api.arn
}

# Custom domain name in API Gateway backed by the validated certificate.
resource "aws_apigatewayv2_domain_name" "api" {
  domain_name = local.api_subdomain

  domain_name_configuration {
    certificate_arn = aws_acm_certificate.api.arn
    endpoint_type   = "REGIONAL"
    security_policy = "TLS_1_2"
  }

  depends_on = [aws_acm_certificate_validation.api]
}

# Maps the custom domain to the $default stage of the HTTP API.
resource "aws_apigatewayv2_api_mapping" "api" {
  api_id      = module.lambda_api.api_id
  domain_name = aws_apigatewayv2_domain_name.api.id
  stage       = "$default"
}
