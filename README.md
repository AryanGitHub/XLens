# XLens

> [NOTE]
> Development happens on [Gnome GitLab](https://gitlab.gnome.org/Oumuamua/xlens). If you are viewing this on GitHub, please treat this as a read-only mirror and submit all issues and merge requests to the GitLab repository.

A native Optical Character Recognition (OCR) application for the GNOME desktop, built with **GTK4** and **Libadwaita**.

Extract text from images and scanned documents seamlessly with a modern, adaptive user interface.

## Features & Roadmap

* **Modern UI:** Clean, responsive design built specifically for the GNOME ecosystem.
* **Multi-Backend Support (Planned):** Currently building the foundation to support multiple OCR engines (like Tesseract, EasyOCR, and others) so users can choose the best processing backend for their needs.

## Building

XLens can be built and run using standard GNOME build tools (Meson/Ninja) or packaged via Flatpak (Planned).

*(Note: Detailed installation instructions, dependencies, and contribution guidelines will be added as the project grows!)*


## Release Process

This project uses dynamic versioning based on Git tags (`vcs_tag` via Meson). During normal development, the application automatically displays a version string containing the latest commit hash (e.g., `0.1.0-4-g1234abc`).

When it is time to make an official public release without the development hashes, follow these steps in order.

### 1. Update the Base Version

Open the root `meson.build` file and update the `version:` argument inside the `project()` definition to your new release number.

```
project('my-gtk-app',
  version: '1.0.0', # <-- Update this number
  meson_version: '>= 1.7.0'
)

```

### 2. Commit the Version Bump

Stage and commit the `meson.build` change to your Git repository.

```
git add meson.build
git commit -m "chore: bump version to 1.0.0"

```

### 3. Create the Git Tag

This is the most important step. Tag the commit you just made with the exact same version number. Meson will read this tag to generate a clean version string.

```
git tag 1.0.0

```

*(Note: Ensure the tag matches your `meson.build` version exactly so there is no confusion).*

### 4. Push to the Remote Repository

Push your latest commits, and make sure to push the tags as well.

```
git push origin main
git push --tags

```
