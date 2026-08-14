git --version
git add .
git commit -m "Auto commit"
git push origin main

:: === Tagging for GitHub Actions Release Build ===
git tag v2.3
git push origin v2.3
pause
