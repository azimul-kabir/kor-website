# Kor website

The website for [Kor (কর)](https://github.com/azimul-kabir/kor), an offline Android app for Bangladesh personal income tax, in English with Bangla as an option, at [kor.azimulkabir.com](https://kor.azimulkabir.com).

| Address | What |
| --- | --- |
| `/` | Home page in English, with the hero |
| `/bn/` | Home page in Bangla |
| `/privacy/` | The app's privacy policy, English first, then Bangla |

It is plain static HTML and CSS: no JavaScript, no trackers, no requests to other sites (both fonts are self-hosted), and it follows the visitor's light or dark setting and reduced-motion preference. It is hosted on Cloudflare Pages, as the Sotorko site is. All links between pages are relative, so it also works under any other address, such as a preview URL.

## Editing

Everything you read on the site lives in [`content.py`](content.py), in English and Bangla side by side. Edit the words there, then rebuild:

```bash
python3 build.py        # needs only Python 3, no packages
```

`build.py` writes `index.html`, `bn/index.html`, `privacy/index.html`, `404.html`, `sitemap.xml` and `robots.txt`. **Commit the generated files**: they are what gets published, and CI fails if they are stale. The build refuses to run if the two languages have different keys or a different number of list items.

Look at it locally with `python3 -m http.server` and open http://localhost:8000.

Keep the claims true to the app: the "works today" and "not yet" lists follow the status table in the app's README (the app repository is private). The site links to no repository and makes no claim about the app's licence, and `scripts/check_site.py` fails the build if a GitHub link or a GPL mention appears. There is no download button until the app has a release: the call to action is an email to kor@azimulkabir.com.

### The privacy policy

The text of the policy belongs to the app (Settings, then Privacy policy, in both languages), so it is written in the app repository and copied here as data:

```bash
python3 scripts/sync_privacy.py ../kor     # reads the app's string resources
python3 build.py
```

Never edit `data/privacy.json` or `privacy/index.html` by hand.

### Screenshots

The pictures are real screenshots of the app in English and Bangla, with made-up figures for a made-up taxpayer ("Nusrat Jahan", TIN 123456789012; no real data), as small WebP files in `assets/shots/`. `assets/shots/manifest.json` records their sizes for the pages. They go stale when the app's screens change, so refresh them then:

```bash
# 1. In the app, enter the sample figures (profile, salary 14,40,000, rent 1,80,000, DPS 60,000 and savings
#    certificates 2,00,000, tax paid 30,000, expenses 4,00,000, assets 19,90,000, last year's net wealth
#    8,00,000) on an emulator or phone, once in English and once in Bangla.
# 2. Use the demo status bar so the clock and battery are tidy:
#    adb shell settings put global sysui_demo_allowed 1
#    adb shell am broadcast -a com.android.systemui.demo -e command enter
#    adb shell am broadcast -a com.android.systemui.demo -e command clock -e hhmm 0941
# 3. Capture 1080x2340 PNGs into raw/en and raw/bn as 01-home, 02-home-tiles, 04-tax-detail,
#    06-wealth-assets, 07-ereturn and 09-calculator (adb exec-out screencap -p > raw/en/01-home.png).
python3 scripts/optimize_shots.py /path/to/raw      # needs Pillow: pip install pillow
python3 build.py && python3 scripts/check_site.py
```

English and Bangla captures must be the same size. The check script fails the build if an image lacks alt text or fixed dimensions.

### Share image

`assets/og.png` (1200x630) is the picture shown when a page is shared on WhatsApp, Facebook and the like. It is drawn from the same raw screenshots:

```bash
python3 scripts/make_og.py /path/to/raw /path/to/Inter.ttf     # needs Pillow; any Inter .ttf will do
```

### Fonts

`assets/fonts/` holds Inter (Latin) and Noto Sans Bengali, both under the SIL Open Font License 1.1 (see `assets/fonts/OFL.txt`). Each is a subset of the original (Latin or Bengali characters only), converted to WOFF2, and is a variable font so one file covers every weight.

## Deploying to Cloudflare

The site is hosted on **Cloudflare Pages**, as the Sotorko site is. `scripts/stage.py` fills `_site/` with exactly what the site publishes (build scripts, data and docs stay out) and copies `_headers` and `_redirects` into it, which Pages applies. The `_headers` file sets a strict Content-Security-Policy: nothing but this site's own images, stylesheet and fonts can load, and inline styles and scripts are not allowed.

### One-time setup in the Cloudflare dashboard

1. **Workers & Pages, Create, Pages, Connect to Git**, and pick `azimul-kabir/kor-website`.
2. Production branch: `main`. Framework preset: **None**. Root directory: `/`.
3. **Build command:** `npm run build`. This rebuilds the pages, runs the checks and stages `_site/`, and fails the deploy if anything is stale or broken.
4. **Build output directory:** `_site`.
5. No environment variables are needed. Save and deploy: every push to `main` then publishes, and other branches and pull requests get a preview URL, with a Cloudflare check on the commit.
6. **Custom domain:** in the project, **Custom domains, Set up a domain**, `kor.azimulkabir.com`. A domain can belong to only one project, so remove it from any earlier Worker or Pages project first.

The build needs Python 3 (no packages) and Node, both in the Pages build image; `package-lock.json` pins `wrangler`, which is only used for local previews. `wrangler.jsonc` is the Workers form of the same site (static assets from `_site/`) and is there for `npm run deploy`; Pages does not need it.

### From your own machine

```bash
npm install          # once; only wrangler
npm run build        # build, check and stage into _site/
npm run preview      # build, then serve it locally with wrangler
npm run deploy       # build, then deploy to a Worker with wrangler (needs `wrangler login`); not used for Pages
```

CI (`.github/workflows/check.yml`) runs the same checks on every push and pull request, so a problem shows up on GitHub as well as in the Cloudflare build.

## Not done yet

- The Bangla text is a first draft and needs a read by a native speaker.
- There is no download or Play Store link, because the app has no release yet; the call to action is an email.
