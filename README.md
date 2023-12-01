# Jotter: A note-taking app for Django

A note-taking app similar to Evernote or Joplin.

## Features

- Notes are organized into notebooks
- Notes can have tags for filtering and searching
- Notes are stored in HTML
- WYSIWYG editor for note text
- Notes are private by default but can be published
- Full text search
- Bookmarklet to add web snippets as Notes

## Design

Evernote has a separate Home page, and a sidebar with top-level categories that include
Home, Notebooks, Shortcuts, Notes, Tasks. The Home page displays modules including
Shortcuts, Pinned Notes, Notes, Notebooks, and Tags.

Joplin opens with the standard 3-column display, Column 1 is Notebooks, Column 2 is
Notes, Column 3 is Note Editor. This is similar to Evernote's view when a Notebook is
selected in Column 1.

## Note Model

- uuid primary key (prevent conflicts when syncing)
- title
- body
- link
- description
- tags
- image
- created datetime
- modified datetime

## Notebook Model

- title
- description
- icon
- image
- created datetime
- modified datetime

## Dependency Management

This project includes [pip-tools](https://pypi.org/project/pip-tools/) for dependency
management. There are two requirements files: `requirements.in` provides the acceptable
ranges of packages to install in a production environment (or any other environment);
`requirements-dev.in` provides packages to install in development environments. Both of
these have corresponding "pin" files: `requirements.txt` and `requirements-dev.txt`.

To add a new dependency, add it to the correct `.in` file, and then run
`manage.py pipsync` to regenerate the pin files and synchronize your current virtual
environment with the new pin files.

Any arguments passed to `manage.py pipsync` will be passed through to the underlying
`pip-compile` command. For example, to bump to the latest Django patch release use
`manage.py pipsync --upgrade-package django`. See the
[pip-tools docs](https://pypi.org/project/pip-tools/) for complete details.

The pin files are not included in the template repository, but will be generated when
you run `manage.py devsetup`. This ensures you will get the latest version of Django and
related packages when starting a new project.
