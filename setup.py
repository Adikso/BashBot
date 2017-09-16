from setuptools import setup

setup(
    name="bashbot",
    version="1.0",
    packages=["bashbot", "bashbot.commands"],
    install_requires=['pyte', 'discord.py'],
    author="Adam Zambrzycki (Adikso)",
    author_email="me@adikso.net",
    description="BashBot is a Discord bot that provides terminal access via chat",
    license="MIT",
    keywords="bot discord bash terminal",
    url="https://github.com/Adikso/BashBot",
    package_data={'': ['*.json']},
    entry_points={
        "console_scripts": [
            "bashbot = bashbot.main:main",
        ]
    }
)
