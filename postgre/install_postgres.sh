#!/bin/bash

# Update package index
sudo apt update

# Install PostgreSQL and related packages
sudo apt install -y postgresql postgresql-contrib

# Enable and start PostgreSQL service
sudo systemctl enable postgresql
sudo systemctl start postgresql

echo "PostgreSQL installation completed."
