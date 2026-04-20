[sund.site](https://sund.site)

This project is auto deployed by Github Action.

Dependencies:

- Hugo version >= v0.113.0+extended

## Installation

Refer to <https://gohugo.io/installation/>

### Build

```bash
hugo mod get -u
hugo
```

## Get Started

### New Post

```bash
hugo new posts/{current-year}/{post-title}.md
```

### Category

The article category is choosen based on `CATEGORIES.md`.

### Preview

```bash
hugo serve
```

### Publish

This repo has set up github actions. Just push the commit to master branch, this will auto trigger page publish process.
