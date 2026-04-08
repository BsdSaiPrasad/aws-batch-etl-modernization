variable "aws_region" {
  description = "AWS region for resources"
  type        = string
}

variable "project_name" {
  description = "Project name prefix"
  type        = string
}

variable "environment" {
  description = "Environment name"
  type        = string
}

variable "alerts_email" {
  description = "Email for SNS alerts"
  type        = string
}

variable "alerts_topic_name" {
  description = "SNS topic name for alerts"
  type        = string
}

variable "step_function_name" {
  description = "Step Functions state machine name"
  type        = string
}

variable "state_machine_alarm_name" {
  description = "CloudWatch alarm name for failed executions"
  type        = string
}

variable "source_check_lambda_name" {
  description = "Source check Lambda function name"
  type        = string
}

variable "curated_check_lambda_name" {
  description = "Curated check Lambda function name"
  type        = string
}
