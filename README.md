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
python3 scripts/verify_navigation.py
python3 scripts/verify_content.py
python3 scripts/test_content_templates.py
```

The build verifies generated HTML pages, internal links, language metadata, expected routes, source-file exclusions, and no automatically loaded external resources.

## Design and screenshots

The homepage presents research and selected software projects using a warm editorial layout. Project images are screenshots of the public Taste Compare and QuestNote websites, captured on 2026-10-06. They are lossless PNG crops, not generated interface mockups; local copies keep the website independent of third-party image requests. Images are limited to 580 CSS pixels to avoid enlargement. Product links open their respective public websites.

## Content

- `_config.yml`: identity and build settings
- `index.html`: homepage
- `_pages/`: about, projects, papers, and notes
- `_papers/`: reading records and bibliographic metadata
- `_projects/`: individual project pages
- `_data/profile.yml`: public contact and optional CV/education
- `_data/projects.yml`: project descriptions and links
- `_posts/`: dated notes
- `assets/css/main.scss`: responsive visual styling

## Deployment

In repository Settings → Pages, select GitHub Actions. Then run **Build and publish Jekyll site** for `main` in Actions. Publication is manual; ordinary pushes do not deploy automatically.

## Theme and license

The real Minimal Mistakes gem provides the base layouts and Sass. Local includes and styles customize the navigation, typography, and content. The upstream MIT license is preserved in `LICENSE`; see `THIRD_PARTY_NOTICES.md`.
