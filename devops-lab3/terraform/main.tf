# Lab 3 - provision scalable infrastructure with Terraform (docker provider)
terraform {
  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "~> 3.0"
    }
  }
}

provider "docker" {}

variable "replicas" {
  description = "Number of web container replicas"
  type        = number
  default     = 2
}

resource "docker_image" "web" {
  name = "nginx:alpine"
}

resource "docker_container" "web" {
  count = var.replicas
  name  = "lab3-web-${count.index + 1}"
  image = docker_image.web.image_id

  ports {
    internal = 80
    external = 8082 + count.index
  }
}

output "container_names" {
  value = [for c in docker_container.web : c.name]
}

output "container_urls" {
  value = [for c in docker_container.web : "http://localhost:${c.ports[0].external}"]
}
