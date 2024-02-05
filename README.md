[![CI](https://github.com/Aineopintojen-harjoitustyo-Algoritmit-j/miinaharava/actions/workflows/auto.yml/badge.svg)](https://github.com/Aineopintojen-harjoitustyo-Algoritmit-j/miinaharava/actions/workflows/auto.yml)
[![codecov](https://codecov.io/gh/Aineopintojen-harjoitustyo-Algoritmit-j/miinaharava/graph/badge.svg?token=KK71RE0U3O)](https://codecov.io/gh/Aineopintojen-harjoitustyo-Algoritmit-j/miinaharava)
# miinaharava
Miinaharava ratkaisijalla

## Dokumentit:
- [määrittelydokumentti](doc/m%C3%A4%C3%A4rittelydokumentti.pdf)
- [toteutusdokumentti](doc/toteutusdokumentti.pdf)

### Viikkoraportit
- [viikko 1](doc/viikkoraportti1.pdf)
- [viikko 2](doc/viikkoraportti2.pdf)
- [viikko 3](doc/viikkoraportti3.pdf)
  
## Ohjeet:

### Asenna
`mkdir miinaharava && wget -O - https://github.com/Aineopintojen-harjoitustyo-Algoritmit-j/miinaharava/archive/refs/tags/v0.1-alpha.tar.gz | tar xz --strip-components=1 --directory=miinaharava`

### Pelaa
`python3 miinaharava`

### Käyttöohjeet
`python3 miinaharava -h`

### Automaattipelaa hidastettuna keskivaikea lauta
`python3 miinaharava -i -aa -d 30`

### Automaattipelaa 10 peliä
`python3 miinaharava -c 10`

### Pelaa kentät tiedostosta
`python3 miinaharava -f miinaharava/tests/data/beginner_3win.txt`
