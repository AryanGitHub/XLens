# XLens

  

> [NOTE]

> Development happens on [Gnome GitLab](https://gitlab.gnome.org/Oumuamua/XLens). If you are viewing this on GitHub, please treat this as a read-only mirror and submit all issues and merge requests to the GitLab repository.

  

A Optical Character Recognition (OCR) application for the GNOME desktop, built with **GTK4** and **Libadwaita**.

  

Extract text from images and scanned documents seamlessly with a modern, adaptive user interface.

  

## Table of Contents

- [Features & Roadmap](#features--roadmap)

- [How to Build Locally](#how-to-build-locally)

- [How to Build the Flatpak App Locally For Development](#how-to-build-the-flatpak-app-locally-for-development)

- [How to Build the Released Flatpak App](#how-to-build-the-released-flatpak-app)

- [(Incomeplete) How to release new version?](#release-process)

- [(Incomeplete) How to contribute?](#release-process)
  
- [FAQs](#faqs)

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

git clone https://gitlab.gnome.org/Oumuamua/XLens.git

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

# 5. (Optional) Run with trace logging enabled (activates the @debug_log decorator)
XLENS_ENABLE_TRACE_LOGS=true ./build/src/xlens
```

  

Alternatively, you can chain these commands together into a single line:

  

```bash
meson setup build --prefix ~/.local && meson compile -C build && meson install -C build && XLENS_ENABLE_TRACE_LOGS=true ./build/src/xlens
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
## How to Build the Flatpak App Locally For Development

You can build and install XLens as a Flatpak using the official Flatpak Builder Tools. Follow these step-by-step instructions:

### 1. Prepare the build directory

First, create a dedicated directory for the Flatpak build and navigate into it:

```
mkdir -p "./build/flatpak" && cd "./build/flatpak"
```

### 2. Download the Flatpak Builder Tools

Clone the official tools repository to get the `flatpak-pip-generator` script:

```
git clone https://github.com/flatpak/flatpak-builder-tools.git ./.flatpak_builder
```

### 3. Generate the Python dependencies manifest

The generator requires the `requirements-parser` package. Install it, and then run the script against the project's `requirements.txt` to generate the `python3-modules.json` file:

```
# Install the script's required dependency
pip install --user requirements-parser

# Run the generator
python3 .flatpak_builder/pip/flatpak-pip-generator -r ../../requirements.txt -o python3-modules.json
```

### 4. Add the GNOME Nightly Flatpak Repository

To build the development version, you need the GNOME Nightly repository to pull in the required runtime. Please visit the official GNOME Nightly page: <https://nightly.gnome.org/>

Follow the instructions there to install Flatpak and add the `gnome-nightly` remote to your system user before proceeding.
(use the --user flag)

### 5. Build and install the Flatpak

Finally, use `flatpak-builder` to compile the app, pull any missing dependencies from Flathub, and install it to your user environment:

```bash
flatpak-builder --force-clean --user --install-deps-from=gnome-nightly --repo=repo --install builddir --disable-rofiles-fuse ../../flatpak/org.gnome.gitlab.Oumuamua.XLens.Devel.yaml
```

### 6. (Optional) Enable `@debug_log` decorator

Also you can run it with `XLENS_ENABLE_TRACE_LOGS=true` environment variable, to enable trace logging via `@debug_log` decorator.
```bash
XLENS_ENABLE_TRACE_LOGS=true flatpak run org.gnome.gitlab.Oumuamua.XLens
```


### 7. Uninstalling

```bash
flatpak uninstall org.gnome.gitlab.Oumuamua.XLens
```

---

## How to Build the Released Flatpak App 

You can build and install XLens as a Flatpak using the official Flatpak Builder Tools. Follow these step-by-step instructions:

### 1. Prepare the build directory

First, create a dedicated directory for the Flatpak build and navigate into it:

```
mkdir -p "./build/flatpak" && cd "./build/flatpak"
```

### 2. Download the Flatpak Builder Tools

Clone the official tools repository to get the `flatpak-pip-generator` script:

```
git clone https://github.com/flatpak/flatpak-builder-tools.git ./.flatpak_builder
```

### 3. Generate the Python dependencies manifest

The generator requires the `requirements-parser` package. Install it, and then run the script against the project's `requirements.txt` to generate the `python3-modules.json` file:

```
# Install the script's required dependency
pip install --user requirements-parser

# Run the generator
python3 .flatpak_builder/pip/flatpak-pip-generator -r ../../requirements.txt -o python3-modules.json
```

### 4. Lint the Flatpak manifest

Before building, verify your manifest against Flathub standards using the [flatpak-builder-lint](https://github.com/flathub-infra/flatpak-builder-lint) tool. It can be installed directly via Flathub.

Once installed, run this command to check your manifest:

```
flatpak run --command=flatpak-builder-lint org.flatpak.Builder manifest ../../flatpak/org.gnome.gitlab.Oumuamua.XLens.yaml
```

### 5. Build and install the Flatpak

Use `flatpak-builder` to compile the app, pull any missing dependencies from Flathub, and install it to your user environment:

```
flatpak-builder --force-clean --user --install-deps-from=flathub --repo=repo --install builddir --disable-rofiles-fuse ../../flatpak/org.gnome.gitlab.Oumuamua.XLens.yaml
```

### 6. Lint the built repository

After the build completes successfully, lint the generated repository:

```
flatpak run --command=flatpak-builder-lint org.flatpak.Builder repo ./repo
```

### 7. Uninstalling

If you need to remove the installed application, run:

```
flatpak uninstall org.gnome.gitlab.Oumuamua.XLens
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

## 5. Update the Flatpak Manifest

To ensure build reproducibility and satisfy Flathub requirements, you must pin the Flatpak manifest to the exact Git tag and commit hash you just created.

1. **Get the full commit hash** for your new tag by running:

   ```
   git rev-parse 1.0.0
   ```

2. **Update the manifest:** Open `org.gnome.gitlab.Oumuamua.XLens.yaml` and add the `tag` and `commit` under the `xlens` module sources:

   ```
   modules:
     - name: xlens
       buildsystem: meson 
       builddir: true
       sources:
         # use type git for release
         - type: git
           url: "https://gitlab.gnome.org/Oumuamua/XLens"
           tag: "1.0.0"                           # <-- Your new tag
           commit: "INSERT_FULL_COMMIT_HASH_HERE" # <-- The hash from step 1
   ```
---

## FAQs

**Q: Why are there two Flatpak manifest files?**
This project uses two separate manifest files to follow Flatpak best practices, keeping local development entirely isolated from the stable release.

* **Production Manifest (`org.gnome.gitlab.Oumuamua.xlens.yaml`):** This is the official stable version intended for Flathub. It builds against a stable GNOME runtime (e.g., version 51) and pulls strictly version-controlled source code.
* **Development Manifest (`org.gnome.gitlab.Oumuamua.xlens.Devel.yaml`):** This is used for local testing. It builds against GNOME Nightly (the `master` branch) to test against upcoming GNOME features and compiles your local, uncommitted directory changes instantly.
Also run it with `XLENS_ENABLE_TRACE_LOGS=true` environment variable, to enable trace logging via `@debug_log` decorator.



**Q: How do I use the `@debug_log` decorator for debugging?**

The `@debug_log` decorator logs function arguments and return values. For performance reasons, it is disabled by default. 

To enable it, set the `XLENS_ENABLE_TRACE_LOGS` environment variable to `true` (or `TRUE`) when launching the app:

```bash
XLENS_ENABLE_TRACE_LOGS=true ./build/src/xlens
```

**Q: What is the `@async_handler` decorator and when should I use it?**

The `@async_handler` decorator safely runs asynchronous functions in the background, preventing Python's garbage collector from destroying the task before it finishes.
It wraps your function in an `asyncio.create_task()`.

**How to use it:**
It is highly recommended for UI development. Use it to wrap async functions that are activated like when pressing a button or triggering other UI events, so the tasks run smoothly without freezing the interface.

```python
from . import app_utils
# Attach this to your GTK button's "clicked" signal


@app_utils.async_handler
async def on_button_clicked(button):
    # Safely await background operations
    await fetch_data_from_network()
```