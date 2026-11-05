# Upload this project to GitHub

> **GitHub does not extract ZIP archives uploaded through the browser.** Uploading the ZIP itself would store just one downloadable file, not your Python project.

## Fastest browser method

1. **Extract** the downloaded ZIP on your computer.
2. Open the extracted `Python_Learning_Chatbot` folder.
3. Sign in to [github.com](https://github.com) and select **New repository**.
4. Name it `Python_Learning_Chatbot`. Choose **Public** (or **Private** if you prefer). Don't initialize it with a README, `.gitignore`, or license: those files already exist here.
5. Create the repository, choose **uploading an existing file** (or **Add file → Upload files**).
6. Drag or select the **contents inside** the extracted folder, not the ZIP archive. Keep the folders `scripts/`, `tests/`, and `data/` intact. Include the hidden `.gitignore` file.
7. Enter the commit message `Initial commit: Python Learning Chatbot` and click **Commit changes**.

## Alternative: Git command line

From the extracted project folder:

```bash
git init
git add .
git commit -m "Initial commit: Python Learning Chatbot"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/Python_Learning_Chatbot.git
git push -u origin main
```

If you use this command-line method, first create an **empty** repository on GitHub and replace `YOUR_USERNAME` with your real GitHub username. Authenticate when Git requests it.

**Before making the repository public:** confirm you have the rights to publish all source code. Faculty PowerPoints and Python cache files were intentionally excluded from this package.
