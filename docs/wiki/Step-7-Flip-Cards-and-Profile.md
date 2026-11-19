**English** · [Dansk](Step-7-Flip-Cards-and-Profile-da) · [Bahasa Malaysia](Step-7-Flip-Cards-and-Profile-ms)

# Step 7: Flip cards and profile

## What this step builds

Each project is a flip card. The front shows the project's picture, name and description. The back shows the link to the source code, the tags and the skills the project shows. The card turns on hover, on keyboard focus and on a tap. The about page links to the owner's LinkedIn profile and shows the owner's profile photo, or a round avatar with the initials when no photo is set. The build copies every image from the data folder into the site.

![The front of a project card](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/083-assignment-website-portfolio/raw/branch/main/docs/images/step-07-flip-card-front.png)

![The back of a project card](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/083-assignment-website-portfolio/raw/branch/main/docs/images/step-07-flip-card-back.png)

![The about page with the LinkedIn link and the profile photo](https://git.tirsystem.com/Tirsvad-Udemy-100-days-of-code/083-assignment-website-portfolio/raw/branch/main/docs/images/step-07-about-page.png)

## What we gained

- A 3D flip is plain CSS (`transform-style: preserve-3d` and `backface-visibility: hidden`), no JavaScript.
- Accessibility: the card can be reached with the keyboard, and visitors who prefer reduced motion get no animation.
- A new kind of file, binary images, needed a new port for reading files and a way for the site writer to write bytes, and the same path checks as for text keep a bad path from escaping the folder.
- The sample projects are real work that shows real skills, not course exercises: the data file is the portfolio.

## Try it

Edit `data/projects.json` to add `tags` and `skills` to a project, put your photo in `data/images/` and set `"photo"` in `data/profile.json`, then build again.
