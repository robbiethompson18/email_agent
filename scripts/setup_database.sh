#!/bin/bash

# Database setup script for Email Unsubscribe Agent
# Run this script to set up PostgreSQL and create the database

set -e  # Exit on any error

echo "🗄️  Setting up PostgreSQL database..."
echo "this script was written by claude, and I think it only works on mac (ie it uses brew). sorry..."

# Check if PostgreSQL is installed
if ! command -v brew &> /dev/null; then
    echo "❌ Homebrew is required but not installed. Please install Homebrew first:"
    echo "   /bin/bash -c \"\$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)\""
    exit 1
fi

# Install PostgreSQL if not already installed
if ! brew list postgresql@15 &> /dev/null; then
    echo "📦 Installing PostgreSQL 15..."
    brew install postgresql@15
else
    echo "✅ PostgreSQL 15 is already installed"
fi

# Start PostgreSQL service
echo "🚀 Starting PostgreSQL service..."
brew services start postgresql@15

# Wait a moment for service to start
sleep 2

# Create database if it doesn't exist
DB_NAME="email_unsubscribe_db"
USERNAME=$(whoami)

echo "🏗️  Creating database '$DB_NAME'..."
if /opt/homebrew/opt/postgresql@15/bin/psql -lqt | cut -d \| -f 1 | grep -qw $DB_NAME; then
    echo "✅ Database '$DB_NAME' already exists"
else
    /opt/homebrew/opt/postgresql@15/bin/createdb $DB_NAME
    echo "✅ Database '$DB_NAME' created successfully"
fi

# Test connection
echo "🔍 Testing database connection..."
if /opt/homebrew/opt/postgresql@15/bin/psql -d $DB_NAME -c "SELECT version();" > /dev/null 2>&1; then
    echo "✅ Database connection successful!"
else
    echo "❌ Database connection failed"
    exit 1
fi

echo ""
echo "🎉 Database setup complete!"
echo ""
echo "Add this to your .env file:"
echo "DATABASE_URL=\"postgresql://$USERNAME@localhost:5432/$DB_NAME\""
echo ""
echo "To stop PostgreSQL later: brew services stop postgresql@15"