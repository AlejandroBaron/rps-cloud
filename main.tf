provider "heroku" {}

resource "heroku_app" "rps" {
  name   = "playrps:latest"
  region = "eu"
}

resource "heroku_addon" "postgres" {
  app  = heroku_app.rps.id
  plan = "heroku-postgresql:hobby-dev"
}

resource "heroku_build" "rps" {
  app = heroku_app.rps.id
  #heroku_app.rps.web_url
  source {
    path = "."
  }
}

# Launch the app's web process by scaling-up
resource "heroku_formation" "rps" {
  app        = heroku_app.rps.id
  type       = "web"
  quantity   = var.app_quantity
  size       = "Free"
  depends_on = [heroku_build.rps]
}