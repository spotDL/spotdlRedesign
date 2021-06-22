# Python Guidelines

<!-- mdformat-toc start --slug=github --maxlevel=6 --minlevel=2 -->

- [Python code standards](#python-code-standards)
- [Suggested Tooling](#suggested-tooling)
- [Docstring formatting](#docstring-formatting)
  - [Functions / Methods](#functions--methods)
  - [Classes](#classes)
  - [Modules](#modules)

<!-- mdformat-toc end -->

## Python code standards<a name="python-code-standards"></a>

1. `mypy` compliance

2. `pylint` score of 9+

3. [McCabe complexity](https://en.wikipedia.org/wiki/Cyclomatic_complexity) \< 10 without
   exception

4. `black` formatted code

5. Docstring's on every method, class and module (using
   [this format](#docstring-formatting))

## Suggested Tooling<a name="suggested-tooling"></a>

1. mypy:

   - `$ mypy ./source`

2. McCabe complexity:

   - `pylint --load-plugins=pylint.extensions.mccabe --limit-inference-results 0 --disable all --enable too-complex`

3. pylint:

   - `$ pylint --limit-inference-results 0 --fail-under 9 ./source`

4. Docstring's:

   - `$ pylint --disable all --limit-inference-results 0 --enable missing-docstring empty-docstring ./source`

5. black:

   - Checking: `$ black --check ./source`

   - Fixing: `$ black ./source`

## Docstring formatting<a name="docstring-formatting"></a>

### Functions / Methods<a name="functions--methods"></a>

The docstring is composed of 5 distinct sections of which 2 are optional:

- __Args__:

  - Non-optional

  - Each input to be formatted as an unordered list:

    `` - $arg_name: `$arg_type`, $description ``

  - If no inputs are taken, none must be specified:

    `- None`

- __Returns__:

  - Non-optional

  - If only a single return type:

    `` - `$return_type`, $description  ``

  - If multiple return types are present:

    `` - `$return_type` if $condition, $description  ``

  - This description should also convey the purpose of the method in brief

  - If nothing is returned, none must be specified:

    `- None`

- __Errors raised__:

  - Non-optional

  - If any custom exceptions are raised or any known errors are left unhandled within the
    function, they must be noted:

    `- $exception_name, $cause `

  - If no known exception are raised or left unhandled, specify none:

    `- None`

- __Function / Notes__:

  - Optional, needed only if:

    - There is a need to expand on the purpose and functioning of the function

    - There are unique design choices to be documented

    - There are special behaviors to look out for

    - There is anything you the author, intend to convey to the user / other devs

    - Any variables or random, out-of-the blue formulas that need a little context

  - No specific format, omit this section if not required

- __Usage__:

  - Optional, needed only if there are quirks to this function's use

  - Write example code in a triple-back-tick (\`\`\`) code block

- __Notes__:

  - Feel free to use markdown formatting, use double-stars for bold and
    single-star/single_underscore for italics, code API documentations are auto-generated
    from these doc strings using pdoc3. NOTE: pdoc3's markdown parser does not accept
    double-underscore for bold (i.e `__this will be in bold__` -> \_\_this will be in
    bold\_\_)

  - You can use LaTeX for mathematical definitions. Enclose LaTeX math between "\\( \\)"
    for inline formulas and in between "$$ $$" for formula blocks. To do this you either
    have to double slash your docstring's (`"\\( $math_goes_here \\)"`) or use raw strings
    (`r"\( $math_goes_here \)"`)

- __A semi-fictional example (for demonstrative purpose only)__:

  ````python
  def get_youtube_link(
      song_name: str, song_artists: typing.List[str],
      song_album: str, song_duration: int) -> typing.Optional[str]:
  """
  ### Args
  - song_name: `str`, name of the song to be found
  - song_artists: `List[str]`, list of contributing artits to the said song
  - song_album: `str`, name of the album to which said song belongs to
  - song_duration: `int`, length of the song in seconds

  ### Returns
  - `str` if a reasonable match is found, the (supposed) best video on YouTube for the said song
  - `None` if all results found are likely to be wrong

  ### Errors raised
  - NoApiReturn, thrown when no results are returned form the YTM API. If all the results are
  likely wrong, `None` is returned, if no results are obtained, this error is thrown.

  ### Function / Notes
  - duration_match =  \\(1 - \\frac{\\Delta time}{15}\\). If the time difference between source
  data and YTM result is greater than 15 seconds, we assume the result is incorrect. The
  \\(\\frac{\\Delta time}{15}\\) is the actual match measure, smaller the better. the
  "1-" part (a) flips this to greater is better to keep inline with the other measures and
  (b) makes duration_match negative if \\(\\Delta time > 15\\), such results with negative match
  values are dumped.

  - album_match is either 0 or 1, no intermediate values. Song results with a perfect
  album match are assigned 1, video results are assigned 0, Song results with an incorrect
  album match are dumped, the idea is that if the album is different, even if the result is
  very close by other metrics, it's definitely not the same Song.

  - name_match = \\(\\frac{\\text{number of common words between song name and result title}}
  {\\text{number of words in the bigger one}}\\), if the value of name_match is less than 0.1,
  the result is dropped. It's common sense, more extra words in the name, farther from the
  actual song it is. The cut-off value of 0.1 was reached after running a sample search of
  100 Songs.

  - artist_match = \\(\\frac{\\text{number of common artists between song and result}}
  {\\text{number of artists in the bigger one}}\\), the cut-off here is 0. This is because,
  YouTube Music supplies the username of the uploader if Song Artists aren't known - there might
  be cases with no common artists.

  - avg_match = average of all the above, this is the deciding factor. The link to the result with
  the highest average match is what is actually returned.

  - The number of common words is slightly fuzzy, *'Vogel Im Kafig'* will be matched against
  *'Vogel Im Käfig'* with a score 3-on-3 in spite of the fact that *'kafig'* is not the exact
  same as *'Käfig'*

  ### Usage
  ```python
  try:
      link = get_youtube_link(
          song_name="Vogel Im Kafig",
          song_album="Attack On Titan OST",
          song_artists=['Hiroyuki Sawano'],
          song_duration=(6*60)+16
      )
      download(link)
  except NoApiReturn:
      print("No results were returned by YouTube Music, check your internet connection...")

  \```
  """
  ````

### Classes<a name="classes"></a>

The docstring is composed of 2 distinct section none of which are optional:

- __Overview__:

  - Describes the purpose of the class on the first line (non-optional)

  - Do not describe quirks in behaviors of any member methods except operator overloads
    (i.e. you can outline quirks in `__eq__` but not in `__init__` and the like)

  - No particular format, prefer bullet points

- __Public attributes__:

  - Each attribute to be formatted as an unordered list:

    `` - $attribute_name: `$attribute_type`, $description  ``

  - If there are no public attributes, none must be specified:

    `- None`

  - Private attributes are not to be specified, you can make note of these as comments
    instead.

- __A fictional example (for demonstrative purpose only)__:

```python
class Song():
   """
   ### Overview
   - Acts as the sole source of truth about a song's details

   ### Public attributes
   - name: `str`, name of the song
   - artists: `List[str]`, names of all contributing artists
   - album: `str`, name of the album to which the song belongs to
   - duration: `int`, length of the song in seconds
   - src: `str`, link to the song on some music streaming platform (usually Spotify)
   - link: `str`, YouTube link to best possible match
   """

   def __init(self, ...):
      ...
```

### Modules<a name="modules"></a>

The docstring is composed of 2 distinct sections one of which is optional:

- The first line should describe the purpose of the module (non-optional)

- Subsequent paragraphs can provide a brief overview of different section of the module
  (optional)

- __A fictional example (for demonstrative purpose only)__:

  (for the search provider from the defaults)

  ```python
  """
  Tools to search YouTube Music for a Song match from available metadata.
  """
  ```
