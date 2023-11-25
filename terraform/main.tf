resource "azurerm_resource_group" "group" {
  name     = "unigpt-assist"
  location = "westeurope"
}

resource "azurerm_container_group" "server" {
  name                = "server"
  resource_group_name = azurerm_resource_group.group.name
  location            = azurerm_resource_group.group.location
  ip_address_type     = "Public"
  os_type             = "Linux"
  dns_name_label      = "unigpt-assist"

  image_registry_credential {
    server   = var.registry_server
    username = var.registry_username
    password = var.registry_password
  }

  container {
    name   = "server"
    image  = var.server_image
    cpu    = 1
    memory = 5

    ports {
      port = 80
    }
  }
}
