<p align="center">
    <img src="docs/logo.png" width="128">
    <p align="center">Maze solving game with randomly generated mazes and raycasting.</p>
</p>

<p align="center">
    <a href="#requirements">Requirements</a> •
  	<a href="#installation">Usage</a> •
	<a href="#controls">Controls</a> •
  	<a href="#license">License</a>
</p>

## Usage

### Running from binary

Download the latest release from the [releases page](https://github.com/exler/mazoku/releases) and run the executable. 

### Running from source

#### Requirements

* Python ^3.11
* [Pyxel ^2.0.9](https://github.com/kitao/pyxel)

#### Commands

```bash
# Install dependencies
$ poetry install

# Run the game
$ poetry run python mazoku.py
```

## Controls

<p align="center">
    <img width="568" src="docs/screen.png">
</p>

* `W/S` - Move forward/backward
* `A/D` - Turn left/right
* `M` - Turn minimap off/on
* `R` - Generate new maze 
* `F10` - Turn debug mode off/on

## License

Copyright (c) 2020 by ***Kamil Marut***

`mazoku` is under the terms of the [MIT License](https://www.tldrlegal.com/l/mit), following all clarifications stated in the [license file](LICENSE).
