output "public_ip" {
  description = "Public IP of the API server"
  value       = aws_instance.api.public_ip
}

output "api_url" {
  description = "Base URL of the deployed API"
  value       = "http://${aws_instance.api.public_ip}"
}

output "ssh_command" {
  description = "SSH into the server"
  value       = "ssh -i ~/.ssh/sre-lab ec2-user@${aws_instance.api.public_ip}"
}
