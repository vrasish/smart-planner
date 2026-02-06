#!/bin/bash
# Fix npm permissions to install packages without sudo

echo "🔧 Fixing npm permissions..."

# Create directory for global packages
mkdir -p ~/.npm-global

# Configure npm to use it
npm config set prefix '~/.npm-global'

# Add to PATH
if [ -f ~/.zshrc ]; then
    echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.zshrc
    echo "✅ Added to ~/.zshrc"
elif [ -f ~/.bash_profile ]; then
    echo 'export PATH=~/.npm-global/bin:$PATH' >> ~/.bash_profile
    echo "✅ Added to ~/.bash_profile"
fi

# Reload shell config
export PATH=~/.npm-global/bin:$PATH

echo "✅ Done! Now run: npm i -g vercel"
echo "Then restart your terminal or run: source ~/.zshrc"
