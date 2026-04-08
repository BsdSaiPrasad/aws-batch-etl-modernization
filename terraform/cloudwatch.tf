resource "aws_cloudwatch_metric_alarm" "stepfunctions_failed" {
  alarm_name          = var.state_machine_alarm_name
  alarm_description   = "Alarm when Step Functions executions fail"
  comparison_operator = "GreaterThanOrEqualToThreshold"
  evaluation_periods  = 1
  threshold           = 1
  metric_name         = "ExecutionsFailed"
  namespace           = "AWS/States"
  period              = 300
  statistic           = "Sum"

  dimensions = {
    StateMachineArn = "arn:aws:states:${var.aws_region}:720800607159:stateMachine:${var.step_function_name}"
  }

  alarm_actions = [aws_sns_topic.alerts.arn]

  tags = {
    Project     = var.project_name
    Environment = var.environment
  }
}
