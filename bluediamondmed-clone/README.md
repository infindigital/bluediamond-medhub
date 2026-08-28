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

- **CSS / JS** live under `assets/css/` and `assets/js/` where localized.
- **Images and fonts** are referenced from the original `bluediamondmed.com`
  URLs. They are binary files hosted on the live site; because this clone was
  produced without filesystem access to the WordPress server, those assets load
  from the live CDN rather than being copied into the repo. Replace them with
  local copies (under `assets/`) before going fully independent.

## Viewing

Open `index.html` in a browser, or serve the folder:

```bash
cd bluediamondmed-clone
python3 -m http.server 8000
# visit http://localhost:8000
```
