#SNOWFLAKE
variable "snowflake_organization" {
  type = string
}

variable "snowflake_account" {
  type = string
}

variable "snowflake_user" {
  type = string
}

variable "snowflake_private_key_path" {
  type        = string
  description = "Path to the RSA private key file"
}


variable "snowflake_role" {
  type = string
  description = "The role used to run Terraform (e.g., ACCOUNTADMIN)"
  default = "ACCOUNTADMIN"
}