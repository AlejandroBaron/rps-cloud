terraform {
  required_providers {
    heroku = {
      source  = "heroku/heroku"
      version = "~> 4.8.0"
    }
  }

  required_version = ">= 0.14"
}