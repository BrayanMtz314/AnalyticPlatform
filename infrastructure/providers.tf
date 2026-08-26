terraform {
  required_version = ">= 1.0.0"

  # This empty block tells Terraform to expect an external S3 config
  backend "s3" {}

  required_providers {
    snowflake = {
      source  = "Snowflakedb/snowflake"
      version = "2.20.0" 
    }
  }
}

provider "snowflake" {
  organization_name = var.snowflake_organization
  account_name      = var.snowflake_account
  user              = var.snowflake_user
  role              = var.snowflake_role 
  authenticator     = "SNOWFLAKE_JWT"
  private_key = file(var.snowflake_private_key_path)


  preview_features_enabled = [
    "snowflake_storage_integration_resource",
    "snowflake_file_format_resource",
    "snowflake_stage_resource",
    "snowflake_table_resource",
    "snowflake_table_constraint_resource"
  ]
}