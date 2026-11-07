variable "project_name" {
  description = "Used to name and tag all resources"
  type        = string
  default     = "sre-resiliency"
}

variable "region" {
  description = "AWS region"
  type        = string
  default     = "us-east-2"
}

variable "instance_type" {
  description = "EC2 instance size"
  type        = string
  default     = "t3.micro"
}

variable "public_key_path" {
  description = "Path to your SSH public key"
  type        = string
  default     = "~/.ssh/sre-lab.pub"
}

variable "ssh_cidr" {
  description = "CIDR allowed to SSH. Leave empty to use your current public IP automatically"
  type        = string
  default     = ""
}
