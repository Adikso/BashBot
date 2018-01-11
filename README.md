![BashBot](https://i.imgur.com/oHESoVW.png)

![Python 3.5](https://img.shields.io/badge/python-3.5-orange.svg) ![Discord.py](https://img.shields.io/badge/discord.py-0.16.11-green.svg) ![Discord.py](https://img.shields.io/badge/pyte-0.7.0_dev-blue.svg)

BashBot is a Discord bot that provides terminal access via chat.

![](https://i.imgur.com/seKhece.png)

## Features
* Interactive. Works with `nano`, `htop` etc
* Reactions can be used as input keys
* Permissions system (per channel/server/group)
* Open/Close/Select/Freeze terminal sessions
* Run terminal session as different user

## Getting Started

These instructions will get you a bot installed and running quickly

### Prerequisites
* Python 3.5+
* `pyte` library (installation instructions below)
* `discord.py` library (installation instructions below)

### Installing

In order to install BashBot you have to clone this repository

```
git clone https://github.com/Adikso/BashBot.git
cd BashBot
```

Then type following command to install:
```
sudo python setup.py install
```
(Your settings and permissions files will be in ~/.bashbot)

**or install dependencies manually and run bot from directory**

Type following commands to install libraries:
```
pip3 install pyte
pip3 install discord.py
```
(Your settings and permissions files will be in cloned repository directory)

### Running
In order to run bot you have to obtain a bot account. It can be obtained through the [applications page](https://discordapp.com/developers/applications/me#top). 
Later you have to transform your app into app bot user

![Create a Bot User](https://i.imgur.com/DaloaLN.png)

After this operation reveal your token and copy it

![](https://i.imgur.com/V2IE9uP.png)

And run
```
python bashbot.py
```

or (if installed with `setup.py`)
```
bashbot
```

Now BashBot should start and show later instructions

### Security
If you want your BashBot to be secure and want to use permissions system, you have to fill `user` field in `settings.json` with user credentials for user that will run terminal sessions and block read and write access to BashBot files and configuration files from that user. Otherwise users will be able to modify files such as `permissions.json` or stole your bot `token` from `settings.json` using terminal tools such as `nano`, `vim`, `cat` etc.

### Commands
(Every command have to start with prefix. By default it's "$". You can change it in settings. More information about commands after typing "$.help")

Command | Alias | Usage | Description 
------------ | ------------- | ------------- | ------------- 
.about |-|.about|Shows information about project
.help |-|.help [name] | Shows help
.settings |.setting|.settings <name> [value] or .settings save | Get/Set bot settings
.permission | .p, .permissions |.permission <user> <permission_name> [new_value] or .permission list | Manage permissions
.open | .o | .open [name] | Opens new terminal session
.close | .c | .close [name] | Closes terminal session
.freeze | .f | .freeze [name] | Freezes terminal session
.here | .h | .here | Moves selected terminal below the user message
.select | .s | .select [name] | Sets terminal as selected
.controls |-|.controls add/remove [emoji] [content..] | Manages terminal controls
.repeat | .r | .repeat <n> <string..> | Repeats string n times and sends to the current terminal session
.sessions | .session | .sessions or .sessions kill <name> or .sessions killall | Manage sessions
.rename | - | .rename <new_name> | Changes session name

### Shortcuts
Shortcut | Description
------------ | ------------- |
[UP] | Arrow up
[DOWN] | Arrow down
[LEFT] | Arrow left
[RIGHT] | Arrow right
[ESC] | Escape
[TAB] or [T] | Horizontal tab
[F1]...[F12]|
[<] | Clears entire input line
\a|Bell (BEL)
\b|Backspace (BS)
\f|Formfeed (FF)
\n|Linefeed(Newline) (LF)
\r|Carriage Return (CR)
\t|Horizontal Tab (TAB)
\v|Vertical Tab (VT)


## Built With

* [Discord.py](https://github.com/Rapptz/discord.py) - Discord API wrapper for Python
* [Pyte](https://github.com/selectel/pyte) - VTXXX-compatible terminal emulator

## Contributing

Feel free to contribute

## Authors

* **Adam Zambrzycki (Adikso)**

See also the list of [contributors](https://github.com/Adikso/BashBot/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Bopke, tomangelo, RhAnjiE for testing
