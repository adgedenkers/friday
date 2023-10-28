#!/bin/bash

while getops "from_dir" option; do
    case $option in
        from_dir) 
            from_dir_opt=True
            ;;
        name) 
            name=$OPTARG
            ;;
    esac
done



create_repo() {
    # get current directory
    current_dir = $(pwd)
    current_dir_name = $(basename $current_dir)

    

    if [ $from_dir_opt ]; then

        echo "creating repository from this directory"
        $repo = 
    fi

    local new_folder = $1

    # create repo on github.com
    echo "Creating repo $current_dir_name"
    repo = $current_dir_name
    gh repo create $repo --public -y

    # initialize git repo locally
    git init
    git add README.md
    git commit -m "first commit"
    git branch -M main
    git remote add origin "https://github.com/adgedenkers/$repo.git"

    # push to repo
    echo "Pushing to repo $repo"
    git push -u origin main
}

link_to_repo() {

}

create_repo --where

gh_init() {

    # get current directory
    current_dir = $(pwd)
    current_dir_name = $(basename $current_dir)

    echo "Initializing git repo"
    git init
    git add .
    git commit -m "Initial commit"
    git branch -M main
    git remote add origin current_dir_name
}
git init
git add README.md
git commit -m "first commit"
git branch -M main
git remote add origin https://github.com/adgedenkers/friday.git

git push -u origin main