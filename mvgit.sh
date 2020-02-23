#!/bin/bash

if [ -d $1 ]; then
  cd $1
  echo '---------------------> enter $1...'  

  # 签出所有远程分支到本地分支
  git branch -r | grep -v '\->' | while read r; do git branch --track "${r#origin/}" "$r"; done
  # 记录当前的远程地址
  origin_url=`git remote -v | grep  "origin" | grep "push" | awk '{print $2}'`
  echo $origin_url
  # 将origin设置为新的地址
  git remote set-url origin $2
  # 将所有分支推送到新的远程地址
  git push origin --all
  # 恢复原来的分支
  git remote set-url origin $origin_url
  echo '---------------------> leave $1...'  
else
  echo "$1 directory not found! exit..."
  exit;
fi;
