# Blue Diamond Medical Staffing — Static Clone

An exact static mirror of [bluediamondmed.com](https://bluediamondmed.com/) (a
WordPress / Elementor site), rebuilt as plain HTML/CSS/JS.

## Pages

| File | Live page |
|------|-----------|
| `index.html` | Home |
| `about-us.html` | About Us |
| `services.html` | Services |
| `healthcare-staffing-services-page.html` | School Staffing |
| `school-staffing.html` | Healthcare Staffing |
| `healthcare-professionals.html` | Healthcare Professionals |
| `teachers-substitute-educators.html` | Teachers & Substitute Educators |
| `cpr-emergency-training-certification.html` | CPR & Emergency Training Certification |
| `teach-in-the-u-s-a-with-blue-diamond-school-staffing.html` | Teach in the U.S.A. |
| `healthcare-staffing.html` | Jobs → Healthcare Staffing |
| `teaching-jobs.html` | Jobs → Teaching Jobs |
| `contact-us.html` | Contact Us |

The full navigation menu (Home, About Us, Services dropdown, Jobs dropdown,
Contact Us) links between these local files.

## Assets

Each page is the site's **real rendered HTML**, so it looks pixel-identical to
the live site. CSS, JS, images and fonts are currently referenced from the
original `bluediamondmed.com` URLs, so the pages render correctly out of the box
in any browser with internet access.

This clone was produced in a sandbox whose network access is locked down, so the
binary assets (images/fonts) could not be copied into the repo here. To make the
clone **100% self-contained**, run the included localizer from any machine with
normal internet access:

```bash
cd bluediamondmed-clone
bash localize.sh
```

It downloads every CSS/JS/image/font into `wp-content/` and `wp-includes/`
(mirroring the site's layout) and rewrites all references to root-relative local
paths.

## Viewing

Open `index.html` directly in a browser (assets load from the live site), or —
recommended, and required after running `localize.sh` — serve the folder:

```bash
cd bluediamondmed-clone
python3 -m http.server 8000
# visit http://localhost:8000
```
