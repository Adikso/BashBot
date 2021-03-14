![BashBot](https://i.imgur.com/oHESoVW.png)

BashBot is a Discord bot that provides terminal access via chat.

![](https://i.imgur.com/seKhece.png)

## Features
* Interactive. Works with `nano`, `htop` etc
* Reactions can be used as input keys
* Open/Close/Select/Freeze terminal sessions
* Run terminal session as different user

## Getting Started

These instructions will get you a bot installed and running quickly

### Prerequisites
* Python 3.5+
* `pyte` library (installation instructions below)
* `discord.py` library (installation instructions below)

### Installing

You can download BashBot.zip from [Releases](https://github.com/Adikso/BashBot/releases) 
which contains all required dependencies and continue to "Running" section.

or you can continue with manuall installation:

Type following commands to install dependencies:
```
pip install -r requirements.txt
```

### Running
In order to run bot you have to obtain a bot account. It can be obtained through the [applications page](https://discordapp.com/developers/applications/me#top). 
Later you have to transform your app into app bot user

![Create a Bot User](https://i.imgur.com/98eUWrP.png)

After this operation, copy your bot token using the Copy button

![](https://i.imgur.com/m4L67Hs.png)

And run
```
python bashbot.py
```
or if you downloaded BashBot [release](https://github.com/Adikso/BashBot/releases) 
```
python BashBot.zip
```

Now BashBot should start and show later instructions

### Docker
Copy `config.toml.example` to `config.toml` file. And in the same directory run following command:
```
docker run -v $(pwd)/config.toml:/BashBot/config.toml adikso/bashbot
```
You can add `-d` to run container in background
```
docker run -d -v $(pwd)/config.toml:/BashBot/config.toml adikso/bashbot
```

Now BashBot should start and show later instructions

### Commands
(Every command have to start with prefix. By default it's "$". You can change it in settings. More information about commands after typing "$.help")

Command | Alias | Usage | Description 
------------ | ------------- | ------------- | ------------- 
.about |-|.about|Shows information about project
.open | .o | .open [name] | Opens new terminal session
.close | .c | .close | Closes current terminal session
.freeze | .f | .freeze | Freezes current terminal session
.here | .h | .here | Moves selected terminal below the user message
.select | .s | .select [name] | Sets terminal as selected
.controls |-|.controls add/remove [emoji] [content..] | Manages terminal controls
.repeat | .r | .repeat <n> <string..> | Repeats string n times and sends to the current terminal session
.rename | - | .rename <new_name> | Changes session name
.submit | - | .submit | Toggles auto submit mode
.macro | .m | .macro <macro_name> | Executes macro from "macros" directory
.interactive | .i | .interactive | Enables interactive mode where all messages are sent to terminal
.exec | .e | .exec <command...> | Execute single command
.whitelist | - | .whitelist add/remove <user_tag> | Add/Remove user to/from whitelist. **Bot owner can execute all commands without being on the whitelist**

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
^(key) | CTRL + (key)


## Built With

* [Discord.py](https://github.com/Rapptz/discord.py) - Discord API wrapper for Python
* [Pyte](https://github.com/selectel/pyte) - VTXXX-compatible terminal emulator

## Contributing

Feel free to contribute

## Authors

* **Adam Zambrzycki (Adikso)**

See also the list of [contributors](https://github.com/Adikso/BashBot/contributors) who participated in this project.

## License

This project is licensed under the GNU License - see the [LICENSE](LICENSE) file for details

## Acknowledgments

* Bopke, tomangelo, RhAnjiE for testing
