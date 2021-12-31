provider "heroku" {}

resource "heroku_app" "rps" {
  name   = "alexbaronrps"
  region = "us"
}

resource "heroku_addon" "postgres" {
  app  = heroku_app.rps.id
  plan = "heroku-postgresql:hobby-dev"
}

resource "heroku_build" "rps" {
  app = heroku_app.rps.id
  source {
    path = "."
  }
}
variable "app_quantity" {
  default     = 1
  description = "Number of dynos in your Heroku formation"
}
# Launch the app's web process by scaling-up
resource "heroku_formation" "rps" {
  app        = heroku_app.rps.id
  type       = "web"
  quantity   = var.app_quantity
  size       = "Free"
  depends_on = [heroku_build.rps]
}