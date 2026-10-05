# Leo Tsou — personal website

A Traditional Chinese personal website built with Jekyll 3.10 and the genuine Minimal Mistakes 4.28.1 theme.

Site: https://leotsouo.github.io

## Development

Use Ruby 3.3 and Bundler 2.5.22:

```sh
bundle install
bundle exec jekyll serve --host 127.0.0.1
```

## Production checks

```sh
JEKYLL_ENV=production bundle exec jekyll build --strict_front_matter
python3 scripts/verify_site.py
```

The build verifies generated HTML pages, internal links, language metadata, expected routes, source-file exclusions, and no automatically loaded external resources.

## Content

- `_config.yml`: identity and build settings
- `index.html`: homepage
- `_pages/`: about, projects, and notes
- `_data/projects.yml`: project descriptions and links
- `_posts/`: dated notes
- `assets/css/main.scss`: responsive visual styling

## Deployment

In repository Settings → Pages, select GitHub Actions. Then run **Build and publish Jekyll site** for `main` in Actions. Publication is manual; ordinary pushes do not deploy automatically.

## Theme and license

The real Minimal Mistakes gem provides the base layouts and Sass. Local includes and styles customize the navigation, typography, and content. The upstream MIT license is preserved in `LICENSE`; see `THIRD_PARTY_NOTICES.md`.
