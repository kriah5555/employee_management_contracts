1) Create database named indii_2_0_backend

Initialization: Run "flask db init" to set up the migration environment. This creates a migrations directory and other necessary files.


after running command "flask db init" migration folder will be created goto migration folder and add "[alembic]
sqlalchemy.url = postgresql://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@localhost/{DATABASE_NAME}" in alembic.ini file


Generate Migrations: Run "flask db migrate" to auto-generate migration scripts based on changes to your models.

run command "flask db migrate -m "Initial migration"

--> "flask db": This is a command provided by Flask-Migrate to perform database-related operations.

--> "migrate": This is a sub-command used to generate a new migration.

--> -m "Initial migration": The -m option is used to specify a message for the migration. In this case, "Initial migration" is a human-readable description of the changes introduced by the migration. It's good practice to provide a meaningful message to describe the purpose of the migration.

Apply Migrations: Run "flask db upgrade" to apply the generated migrations to the database.

If you want to reset your database and start fresh, you can drop and recreate the database manually or use a migration command with "flask db downgrade" to rollback the migrations.

migrations doc = https://flask-migrate.readthedocs.io/en/latest/