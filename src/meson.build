pkgdatadir = get_option('prefix') / get_option('datadir') / meson.project_name()
moduledir = pkgdatadir / 'xlens'
gnome = import('gnome')

gnome.compile_resources('xlens',
  'xlens.gresource.xml',
  gresource_bundle: true,
  install: true,
  install_dir: pkgdatadir,
)

python = import('python')

conf = configuration_data()
conf.set('PYTHON', python.find_installation('python3').full_path())
conf.set('VERSION', meson.project_version())
conf.set('localedir', get_option('prefix') / get_option('localedir'))
conf.set('pkgdatadir', pkgdatadir)

configure_file(
  input: 'xlens.in',
  output: 'xlens',
  configuration: conf,
  install: true,
  install_dir: get_option('bindir'),
  install_mode: 'rwxr-xr-x'
)

xlens_sources = [
  '__init__.py',
  'main.py',
  'window.py',
  'appLogger.py',
  'ConfigManager.py',
  'constants.py',
  'ImageProcessingContext.py',
  'OutputViewer.py',
  'PreferencesPage.py',
  'FromURLPage.py'
]

install_data(xlens_sources, install_dir: moduledir)
