BYLD LOGO PACK  ·  Buildd From Ideas  ·  v1.0, November 2026
==============================================================

Start with BYLD-Brand-Guide.pdf.
The logo is white with a sky-blue arrow and ALWAYS sits on a dark background.

QUICK PICKS
  Slides, docs, email signature ...... png/byld-logo-on-dark-1200.png  (dark background built in)
  On a dark slide or web page ........ png/byld-logo-1200.png          (transparent)
  Tees, banners, signs ............... svg/byld-logo.svg or pdf/
  Embroidery / one colour ............ svg/byld-logo-white.svg
  Profile pictures, app stores ....... png/byld-icon-1024.png
  Website tab ........................ favicon/

FOLDERS
  svg/      Master artwork. Vector, outlined paths (no fonts, no strokes).
  pdf/      Vector PDFs. byld-logo-on-dark.pdf shows the background;
            byld-logo-transparent.pdf is white artwork for printers (looks blank on white screens).
  png/      600, 1200 and 2400 px wide. Transparent, except the on-dark set.
  favicon/  favicon.ico (16/32/48), favicon.svg, apple-touch-icon.png (180 px).
  source/   build_logo.py -> svg/, render.js -> png/ pdf/ and the guide, finish.py -> .ico + zip.

COLOURS
  Night  #12163A  rgb(18 22 58)    background   CMYK 90 80 30 70 (proof it)
  White  #FFFFFF                   letters
  Sky    #5CC0FF  rgb(92 192 255)  arrow        CMYK 55 10 0 0 (proof it)

SPECS
  Logo viewBox 0 -24 394 124 (3.18:1), cropped tight.
  On-dark viewBox -50 -74 494 224: background + clear space (half the letter height) built in.
  Icon viewBox 0 0 200 200, corner radius 56. Minimums: logo 100 px / 25 mm, icon 32 px / 8 mm.

REBUILD
  cd source && python3 build_logo.py && node render.js && python3 finish.py
