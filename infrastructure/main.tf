# 1. Create the Database
resource "snowflake_database" "analytics_db" {
  name = "ANALYTICS_PLATFORM_DB"
}

# 2. Create the Schema
resource "snowflake_schema" "analytics_schema" {
  database = snowflake_database.analytics_db.name
  name     = "API_DATA"
}

# 3. Create the Compute Warehouse
resource "snowflake_warehouse" "analytics_wh" {
  name           = "ANALYTICS_WH"
  warehouse_size = "X-SMALL"
  auto_suspend   = 60
  auto_resume    = true
}

# 4. Create a specific Role for the application
resource "snowflake_account_role" "fastapi_role" {
  name = "FASTAPI_APP_ROLE"
}

# 5. Grant Warehouse Usage to the new Role
resource "snowflake_grant_privileges_to_account_role" "wh_usage" {
  privileges        = ["USAGE"]
  account_role_name = snowflake_account_role.fastapi_role.name
  
  on_account_object {
    object_type = "WAREHOUSE"
    object_name = snowflake_warehouse.analytics_wh.name
  }
}