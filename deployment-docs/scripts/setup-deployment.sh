#!/bin/bash

# Deployment Setup Script
# This script helps you quickly set up deployment configuration for your project

set -e

echo "🚀 Deployment Setup Script"
echo "=========================="

# Check if we're in a project directory
if [ ! -f "package.json" ] && [ ! -f "go.mod" ] && [ ! -f "main.py" ]; then
    echo "⚠️  Warning: No package.json, go.mod, or main.py found in current directory"
    echo "Make sure you're in your project root directory"
    read -p "Continue anyway? (y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 1
    fi
fi

# Detect project type
echo "🔍 Detecting project type..."
if [ -f "go.mod" ]; then
    PROJECT_TYPE="go"
    echo "✅ Go project detected"
elif [ -f "package.json" ]; then
    if grep -q "next" package.json; then
        PROJECT_TYPE="nextjs"
        echo "✅ Next.js project detected"
    else
        PROJECT_TYPE="node"
        echo "✅ Node.js project detected"
    fi
elif [ -f "main.py" ] || [ -f "requirements.txt" ]; then
    PROJECT_TYPE="python"
    echo "✅ Python project detected"
elif [ -f "Cargo.toml" ]; then
    PROJECT_TYPE="rust"
    echo "✅ Rust project detected"
elif [ -f "pom.xml" ] || [ -f "build.gradle" ]; then
    PROJECT_TYPE="java"
    echo "✅ Java project detected"
else
    echo "❌ Could not detect project type"
    echo "Please choose manually:"
    echo "1) Go"
    echo "2) Python"
    echo "3) Node.js"
    echo "4) Next.js"
    echo "5) Rust"
    echo "6) Java"
    read -p "Enter choice (1-6): " choice
    case $choice in
        1) PROJECT_TYPE="go" ;;
        2) PROJECT_TYPE="python" ;;
        3) PROJECT_TYPE="node" ;;
        4) PROJECT_TYPE="nextjs" ;;
        5) PROJECT_TYPE="rust" ;;
        6) PROJECT_TYPE="java" ;;
        *) echo "❌ Invalid choice"; exit 1 ;;
    esac
fi

# Get app name
read -p "Enter app name (default: $(basename $(pwd))): " APP_NAME
APP_NAME=${APP_NAME:-$(basename $(pwd))}

# Get registry info
read -p "Enter registry host (e.g., registry.example.com:5000): " REGISTRY_HOST
if [ -z "$REGISTRY_HOST" ]; then
    echo "⚠️  No registry specified, using localhost:5000"
    REGISTRY_HOST="localhost:5000"
fi

# Get remote server info
read -p "Enter remote server user (e.g., deploy): " REMOTE_USER
read -p "Enter remote server host (e.g., prod-server): " REMOTE_HOST

echo ""
echo "📋 Configuration Summary:"
echo "  App Name: $APP_NAME"
echo "  Project Type: $PROJECT_TYPE"
echo "  Registry: $REGISTRY_HOST"
echo "  Remote: $REMOTE_USER@$REMOTE_HOST"
echo ""

read -p "Continue with setup? (y/n): " -n 1 -r
echo
if [[ ! $REPLY =~ ^[Yy]$ ]]; then
    echo "Setup cancelled."
    exit 0
fi

# Copy files based on project type
echo ""
echo "📦 Copying template files..."

# Copy Makefile
cp deployment-docs/templates/Makefile.template Makefile
echo "✅ Makefile"

# Copy Dockerfile
case $PROJECT_TYPE in
    go)
        cp deployment-docs/templates/Dockerfile.go Dockerfile
        ;;
    python)
        cp deployment-docs/templates/Dockerfile.python Dockerfile
        # Create requirements.txt if it doesn't exist
        if [ ! -f "requirements.txt" ]; then
            pip freeze > requirements.txt 2>/dev/null || echo "# Add your dependencies here" > requirements.txt
        fi
        ;;
    node)
        cp deployment-docs/templates/Dockerfile.node-pm2 Dockerfile
        cp deployment-docs/templates/ecosystem.config.js ecosystem.config.js
        ;;
    nextjs)
        cp deployment-docs/templates/Dockerfile.nextjs-nginx Dockerfile
        mkdir -p docker/nginx
        cp deployment-docs/templates/nginx.conf.template docker/nginx/
        cp deployment-docs/templates/nginx.entrypoint.sh docker/nginx/
        chmod +x docker/nginx/entrypoint.sh
        ;;
    rust)
        cp deployment-docs/templates/Dockerfile.rust Dockerfile
        ;;
    java)
        cp deployment-docs/templates/Dockerfile.java Dockerfile
        ;;
esac
echo "✅ Dockerfile ($PROJECT_TYPE)"

# Copy docker-compose files
cp deployment-docs/templates/docker-compose.local.yaml.template docker-compose.local.yaml
cp deployment-docs/templates/docker-compose.test.yaml.template docker-compose.test.yaml
cp deployment-docs/templates/docker-compose.yaml.template docker-compose.yaml
echo "✅ Docker Compose files"

# Update Makefile with user configuration
echo ""
echo "⚙️  Updating Makefile configuration..."

# Use sed to update the configuration (works on both macOS and Linux)
if [[ "$OSTYPE" == "darwin"* ]]; then
    sed -i '' "s/APP_NAME ?= your-app-name/APP_NAME ?= $APP_NAME/" Makefile
    sed -i '' "s/REGISTRY_HOST = registry.example.com:5000/REGISTRY_HOST = $REGISTRY_HOST/" Makefile
    sed -i '' "s/REMOTE_USER = deploy/REMOTE_USER = $REMOTE_USER/" Makefile
    sed -i '' "s/REMOTE_HOST = prod-server/REMOTE_HOST = $REMOTE_HOST/" Makefile
else
    sed -i "s/APP_NAME ?= your-app-name/APP_NAME ?= $APP_NAME/" Makefile
    sed -i "s/REGISTRY_HOST = registry.example.com:5000/REGISTRY_HOST = $REGISTRY_HOST/" Makefile
    sed -i "s/REMOTE_USER = deploy/REMOTE_USER = $REMOTE_USER/" Makefile
    sed -i "s/REMOTE_HOST = prod-server/REMOTE_HOST = $REMOTE_HOST/" Makefile
fi

# Update docker-compose files
for file in docker-compose.local.yaml docker-compose.test.yaml docker-compose.yaml; do
    if [[ "$OSTYPE" == "darwin"* ]]; then
        sed -i '' "s/image: registry.example.com:5000\/app/image: $REGISTRY_HOST\/$APP_NAME/" $file
        sed -i '' "s/container_name: app/container_name: $APP_NAME/" $file
    else
        sed -i "s/image: registry.example.com:5000\/app/image: $REGISTRY_HOST\/$APP_NAME/" $file
        sed -i "s/container_name: app/container_name: $APP_NAME/" $file
    fi
done

echo "✅ Configuration updated"

# Make Makefile executable
chmod +x Makefile

echo ""
echo "🎉 Setup complete!"
echo ""
echo "📋 Next steps:"
echo "  1. Review and edit Makefile if needed"
echo "  2. Review and edit Dockerfile if needed"
echo "  3. Review and edit docker-compose files if needed"
echo "  4. Test locally: make test"
echo "  5. Build and push: make push"
echo "  6. Deploy: make remote-deploy"
echo ""
echo "📖 For more help:"
echo "  - Read deployment-docs/README.md"
echo "  - Use @deployment-skill in Claude Code"
echo ""
echo "🚀 Happy deploying!"