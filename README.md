# grace.py

grace.py is a python based commandline audio player. It supports
play|stop|next|prev and was mainly built as a smarter alternative to:

```bash
$ case $(uname) in
$   "Darwin") PLAYER="afplay";;
$   "Linux") PLAYER="mplayer";;
$ esac
$ IFS="
$ "
$ for f in $(ls -1 "$1"); do
$   "$PLAYER" "$1/$f"
$ done
```

## Usage

```bash
$ ./grace.py ~/Music
$ # Or
$ ./grace.py "$HOME/Music/In Flames/Whoracle (Reissue 2014)"
```

## Trivia

grace.py was named after my cat, who in turn was named after Grace Hopper.

## License

See [LICENSE](LICENSE.md)

