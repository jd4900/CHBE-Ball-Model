from setuptools import setup, find_packages

setup(
    name='ball-model',
    version='0.1',
    packages=find_packages(),
    install_requires=[
        'flake8',
        'autopep8',
        'docutils',
        'pygments',
        'pypiwin32',
        'kivy_deps.sdl2 == 0.1.*',
        'kivy_deps.glew == 0.1.*',
        'kivy_deps.gstreamer == 0.1.*',
        'kivy == 1.11.1'
    ],
)
