#!/bin/bash

# Default values
from_dir_opt=false
name=""

# Parsing command-line options
while getopts ":f:n:" option; do
    case $option in
        f)
            from_dir_opt=true
            ;;
        n)
            name=$OPTARG
            ;;
        *)
            echo "Unknown option: -$OPTARG" >&2
            exit 1
            ;;
    esac
done

create_repo_here() {
    # Get the current directory and its name
    current_dir=$(pwd)
    current_dir_name=$(basename $current_dir)

    # Determine the repository name
    repo=$current_dir_name
    if [ -n "$name" ]; then
        repo=$name
    fi

    echo "Creating repository $repo"
    
    # Create repo on github.com
    gh repo create $repo --public -y

    # Initialize git repo locally
    git init
    git add README.md
    git commit -m "first commit"
    git branch -M main
    git remote add origin "https://github.com/adgedenkers/$repo.git"

    # Push to repo
    echo "Pushing to repo $repo"
    git push -u origin main
}

gh_init() {
    # Get the current directory and its name
    current_dir=$(pwd)
    current_dir_name=$(basename $current_dir)

    echo "Initializing git repo"
    git init
    git add .
    git commit -m "Initial commit"
    git branch -M main
    git remote add origin "https://github.com/adgedenkers/$current_dir_name.git"
}

# Check if the script should create a repo from the current directory or initialize a new git repo
if $from_dir_opt; then
    create_repo
else
    gh_init
fi
