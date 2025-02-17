from setuptools import setup

setup(
    name="asciimation",
    version="1.0",
    py_modules=["main"],
    install_requires=[
        "opencv-python",
        "pydub",
        "fpstimer",
        "yt-dlp",
    ],
    entry_points={
        "console_scripts": [
            "asciimation=main:main",
        ],
    },
)