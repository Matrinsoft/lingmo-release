#!/bin/bash
cd /home/lingmo/lingmo-release
git init -q
git add -A
git commit -q -m "Initial lingmo-release: Lingmo OS identity, replaces fedora-release"
git remote add origin https://github.com/Matrinsoft/lingmo-release.git
git push -u origin main
echo "push rc=$?"
git log --oneline -1
