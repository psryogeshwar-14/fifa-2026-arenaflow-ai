#!/bin/bash

# ArenaFlow AI Deployment Helper Script

echo "🏟️ ArenaFlow AI Deployment Helper"
echo "---------------------------------"

# Check if git remote is already added
if ! git remote | grep -q "origin"; then
    echo "Enter your GitHub username:"
    read -r username
    echo "Enter your repository name (e.g., fifa-2026-arenaflow-ai):"
    read -r repo_name

    git remote add origin "https://github.com/$username/$repo_name.git"
    echo "✅ Remote origin added: https://github.com/$username/$repo_name.git"
else
    echo "✅ Remote origin already exists:"
    git remote -v
fi

echo ""
echo "Attempting to push to GitHub main branch..."
echo "Note: If prompted, please enter your GitHub Personal Access Token (PAT)."
echo ""

git branch -M main
if git push -u origin main; then
    echo "✅ Successfully pushed to GitHub!"
    echo ""
    echo "Next Steps to Deploy on Streamlit Community Cloud:"
    echo "1. Visit https://share.streamlit.io/"
    echo "2. Log in with your GitHub account."
    echo "3. Click 'New app' and select this repository."
    echo "4. Set Main file path to 'app.py'."
    echo "5. (Optional) In Advanced settings -> Secrets, add:"
    echo "   GEMINI_API_KEY = \"your_gemini_api_key_here\""
    echo "6. Click 'Deploy'!"
else
    echo "❌ Push failed. Please verify that you created the repository on GitHub and that your credentials are correct."
fi
