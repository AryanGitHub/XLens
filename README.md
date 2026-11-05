# XLens

  

> [NOTE]

> Development happens on [Gnome GitLab](https://gitlab.gnome.org/Oumuamua/xlens). If you are viewing this on GitHub, please treat this as a read-only mirror and submit all issues and merge requests to the GitLab repository.

  

A Optical Character Recognition (OCR) application for the GNOME desktop, built with **GTK4** and **Libadwaita**.

  

Extract text from images and scanned documents seamlessly with a modern, adaptive user interface.

  

## Table of Contents

- [Features & Roadmap](#features--roadmap)

- [How to Build Locally](#how-to-build-locally)

- [How to Build the Flatpak App Locally](#how-to-build-the-flatpak-app)

- [(Incomeplete) How to release new version?](#release-process)

- [(Incomeplete) How to contribute?](#release-process)
  

---

  
  

## Features & Roadmap

  

* **Modern UI:** Clean, responsive design built specifically for the GNOME ecosystem.

* **Multi-Backend Support (Planned):** Currently building the foundation to support multiple OCR engines (like Tesseract, EasyOCR, and others) so users can choose the best processing backend for their needs.

---

## Building

  

XLens can be built and run using standard GNOME build tools (Meson/Ninja) or packaged via Flatpak.

  

## How to Build Locally

  

### 1. Install System Dependencies

  

Before setting up the project, install the necessary development tools and libraries. For Fedora/RHEL-based distributions, run the following command:

  

```bash

sudo dnf install meson python3-gobject gettext glib-compile-resources gtk-update-icon-cache update-desktop-database gtk4-devel libadwaita-devel libportal-devel libportal-gtk4-devel tesseract
```

  

### 2. Cloning the Repository

  

Once the dependencies are installed, clone the project to your local machine and navigate into the project directory:

  

```bash

git clone https://gitlab.gnome.org/Oumuamua/xlens.git

cd xlens
```

  

### 3. Setting up the Python Virtual Environment

  

It is recommended to use a local virtual environment (`.venv`) to manage Python dependencies without interfering with your system packages.

  

1. **Create the virtual environment** (allowing access to system site-packages):

```bash
python -m venv --system-site-packages .venv
```

  

2. **Activate the virtual environment**:

```bash
source .venv/bin/activate
```

  

3. **Install dependencies**:

Install the standard project requirements:

```bash
pip install -r requirements.txt
```

For development purposes, also install the development requirements:

```bash
pip install -r requirements-dev.txt
```

  

4. **Deactivate the virtual environment**:

When you are done working on the project, you can easily exit the virtual environment by running:

```bash
deactivate
```

  

### 4. Setting up Pre-commit Hooks

  

To ensure code quality and consistent formatting, we use `pre-commit`.

  

Once your virtual environment is active and you have installed the development requirements, initialize the pre-commit tool in your local repository:

  

```bash
# Install the git hook scripts
pre-commit install

# (Optional) Run against all files manually to test it
pre-commit run --all-files
```

With this installed, the pre-commit checks will automatically run every time you make a `git commit`.

  

### 5. Building and Running

  

XLens uses the Meson build system. You can set up the build directory, compile, install to your local user directory (`~/.local`), and run the application step-by-step.

  

You can execute the following steps one by one:

  

```bash

# 1. Setup the build directory
meson setup build --prefix ~/.local

# 2. Compile the project
meson compile -C build

# 3. Install locally
meson install -C build

# 4. Run the application
./build/src/xlens
```

  

Alternatively, you can chain these commands together into a single line:

  

```bash
meson setup build --prefix ~/.local && meson compile -C build && meson install -C build && ./build/src/xlens
```

  

### 6. Uninstalling

  

If you need to remove the locally installed files from your system, use `ninja` to trigger the uninstall target from your build directory:

  

```bash
ninja -C build uninstall
```

Also you can remove the build folder:

```bash
rm -rf ./build
```

---


## How to Build the Flatpak App

You can build and install XLens as a Flatpak using the official Flatpak Builder Tools. Follow these step-by-step instructions:

### 1. Prepare the build directory**  
First, create a dedicated directory for the Flatpak build and navigate into it:
```bash
mkdir -p "./build/flatpak" && cd "./build/flatpak"
```

### 2. Download the Flatpak Builder Tools**  
Clone the official tools repository to get the `flatpak-pip-generator` script:
```bash
git clone https://github.com/flatpak/flatpak-builder-tools.git ./.flatpak_builder
```

### 3. Generate the Python dependencies manifest**  
The generator requires the `requirements-parser` package. Install it, and then run the script against the project's `requirements.txt` to generate the `python3-modules.json` file:
```bash
# Install the script's required dependency
pip install --user requirements-parser

# Run the generator
python3 .flatpak_builder/pip/flatpak-pip-generator -r ../../requirements.txt -o python3-modules.json
```

### 4. Build and install the Flatpak**  
Finally, use `flatpak-builder` to compile the app, pull any missing dependencies from Flathub, and install it to your user environment:
```bash
flatpak-builder --force-clean --user --install-deps-from=flathub --repo=repo --install builddir --disable-rofiles-fuse ../../flatpak/org.gnome.gitlab.oumuamua.XLens.yaml
```

### 5. Uninstalling
```bash
flatpak uninstall org.gnome.gitlab.oumuamua.XLens
```

---

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