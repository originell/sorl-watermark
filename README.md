# sorl-watermark

sorl-watermark adds support for adding watermarks to sorl-thumbnail.

Tested with:

* Django 1.8, 1.9, 1.10, 1.11, 2.0, 2.1, 2.2, 3.0, 3.1 and 3.2.
* [sorl-Thumbnail](https://github.com/jazzband/sorl-thumbnail) 12.4, 12.5, 12.6 and 12.7.
* Pillow 5, 6, 7 and 8.
* Python 2.7, 3.5, 3.6, 3.7, 3.8 and 3.9.

Of course everything is configurable, from the watermark image to position and
opacity.

sorl-watermark does not ship with support for generating text-based watermarks.

## Setup

Install via pip

    $ pip install sorl-watermark

Change sorl's thumbnail engine to one from sorl-watermark. PIL and imagemagick are
supported.

PIL:

```python
# PIL is the most well tested backend.
THUMBNAIL_ENGINE = 'sorl_watermarker.engines.pil_engine.Engine'
```

Pgmagick:

```python
# PIL is the most well tested backend.
THUMBNAIL_ENGINE = 'sorl_watermarker.engines.pgmagick_engine.Engine'
```

Next up, you tell it which image should be used as a watermark. Note that this file
has to live somewhere inside `STATIC_ROOT`.

```python
THUMBNAIL_WATERMARK = 'my_watermark.png'
```

That's it for a simple setup. The engine will only apply the watermark if the
thumbnail size is big enough.

See _Advanced Usage_ for ways to dynamically change the watermark itself, it's size
or ways to selectively apply watermarks.

## Advanced Usage

sorl-watermark adds additional options to the `{% thumbnail %}` templatetag.

The following new options are available:

* `watermark=imagefile`
  This options takes an ImageFile and uses this one instead of the default
  watermark file, set via `THUMBNAIL_WATERMARK`
* `watermark_size="x200"`
  Changes the watermark's size. Takes the same options as the
  `THUMBNAIL_WATERMARK_SIZE` option.
* `watermark_pos="north east"`
  Specifies where the watermark shall be put. Accepts the same options as the
  `THUMBNAIL_WATERMARK_POSITION` setting.
* `watermark_alpha=0.9`
  Sets the watermark's opacity. Has to be a value between 0 and 1.

## Settings Reference

The following settings are available

* `THUMBNAIL_WATERMARK`
  Sets the image to be used as a watermark. The file must live within `STATIC_ROOT`.

* `THUMBNAIL_WATERMARK_ALWAYS`
  Stamp a watermark on every image.
  Default is `True`.

* `THUMBNAIL_WATERMARK_SIZE`
  Change the size of the watermark. This can either be a geometry string, as is usual
  with sorl-thumbnail ("x200", "200x200"), or a percentage. If given a percentage,
  the watermark will always be the given percentage of the thumbnail size.

* `THUMBNAIL_WATERMARK_OPACITY`
  An integer from 0 to 1, specifying the opacity of the watermark.
  Default is `0` (opaque).

* `THUMBNAIL_WATERMARK_POSITION`
  Specifies the position of the watermark. You can specify the position with a pair
  of padding values (in pixels) Ex. "20 20" will place watermark near the left-top
  corner, "-20 -20" - near the right-bottom corner.
  Either you can specify the position as:

    * "north"
    * "south"
    * "west"
    * "east"
    * "north east"
    * "south east"
    * "north west"
    * "south west"
    * "center"

  Default: `"south east"` (right-bottom corner)

  If you want to tile your image completely with a watermark, you should set:

    ```python
    THUMBNAIL_WATERMARK_POSITION = 'tile'
    ```
