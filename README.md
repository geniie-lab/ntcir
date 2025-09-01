# MkDocs Starter Kit

## Enabled Settings and Extensions

(See `docs/index.md`)

- Material theme
- Copyright and Social Media Icons
- Abbreviations and Snippets
- Admonition
- Code Hilighting and Line Number
- Math
- Footnote
- Keys
- Tabs
- Mermaid
- Emoji

## Getting Started

- Clone the repo

```
$ git clone https://github.com/hideojoho/mkdocs-starter-kit-en.git
```

- Create `venv`

```
$ cd mkdocs-starter-kit-en
$ python -m venv venv
```

- Activate

(Mac/Linux)
```
$ source venv/bin/activate
```

(Windows)
```
$ venv\Scripts\activate
```

- Install python modules

```
(venv) $ python -m pip install -U pip
(venv) $ python -m pip install -r requirements.txt
```

- Run the server for a local access (http://localhost:8000/)

```
(venv) $ mkdocs serve
```

- Run the server for a remote access

```
(venv) $ mkdocs serve --dev-addr=remote-server-ip:8000
```

- Build your static pages to `./site`

```
(venv) $ mkdocs build
```

- Edit `mkdocs.yml` to customise your website

## Publish to GitHub Pages

Build the source files in the `main` branch and automatically save the generated html files into the `gh-pages` branch using GitHub Actions.

- Create a folder

```
$ mkdir -p .github/workflows
```

- Create a GitHub Action config file [gh-pages.yaml](https://github.com/marketplace/actions/github-pages-action#%EF%B8%8F-static-site-generators-with-python) in the folder
- (Option) If you need to use a private repository in `requirements.txt`
  - Replace the requirement part of `gh-pages.yaml` with the following code
    ```
    - name: Install dependencies
      run: |
        git config --global url."https://${{ secrets.ACCESS_TOKEN }}@github".insteadOf https://github
        python3 -m pip install -r ./requirements.txt
    ```
  - [Set a repository secret using a personal access token](https://stackoverflow.com/questions/64715544/install-private-repository-in-build-stage-on-github-actions)
- (Option) If you use a non-main (or master) branch to keep mkdocs files
  - Replace the Branch and Deploy parts of `gh-pages.yaml` with the follwing code (A branch `v2.0` is used as an example)
    ```
    on:
      push:
        branches:
        - v2.0
    ```
    ```
    if: ${{ github.ref == 'refs/heads/v2.0' }}
    ```
- Commit the change. This triggers the build in GitHub. Takes a whlie to complete the build.
- Go to Settings > GitHub Pages and select `gh-pages` as the source. Save.
  - You should see a message: `Your site is published at [URL]`
  - Takes a while to appear the website at the first time.


## URLs

- https://squidfunk.github.io/mkdocs-material/
- https://github.com/marketplace/actions/github-pages-action
