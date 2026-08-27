# 1. Create the Database
resource "snowflake_database" "analytics_db" {
  name = "ANALYTICS_PLATFORM_DB"
}

# 2. Create the Schema
resource "snowflake_schema" "analytics_schema" {
  database = snowflake_database.analytics_db.name
  name     = "API_DATA"
}
