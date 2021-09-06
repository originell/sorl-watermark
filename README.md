# sorl-watermark

sorl-watermark adds support for watermarking to [sorl-thumbnail](https://github.com/jazzband/sorl-thumbnail).

## Features

- Everything configurable: watermark image, position, opacity and watermark size etc.
- Engines for all sorl-thumbnail engines: Pillow, ImageMagick, PIL, Wand, pgmagick, and vipsthumbnail
- sorl-thumbnail 12.4 to 12.7
- Django 2.2, 3.1 and 3.2 following the [Django supported versions policy](https://www.djangoproject.com/download/#supported-versions)

## Quick Start

1. Install

    ```sh
    $ pip install sorl-watermark
    ```

2. Swap out your sorl-thumbnail engine with one from sorl-watermark:
    * Pillow (PIL) based engine:

       ```python
       THUMBNAIL_ENGINE = 'sorl_watermarker.engines.pil_engine.Engine'
      ```
    * Wand based engine:

      ```python
      THUMBNAIL_ENGINE = 'sorl_watermarker.engines.wand_engine.Engine'
      ```
   * pgmagick based engine:

     ```python
     THUMBNAIL_ENGINE = 'sorl_watermarker.engines.pgmagick_engine.Engine'
     ```
    * ImageMagick/GraphicsMagick engine:
    
      ```python
      THUMBNAIL_ENGINE = 'sorl_watermarker.engines.convert_engine.Engine'
      ```
      
      When using this engine, remember to also set the ``THUMBNAIL_WATERMARK_COMPOSITE``
      setting. See the reference at the bottom.
    * vips (libvips) engine. This 

      ```python
      THUMBNAIL_ENGINE = 'sorl_watermarker.engines.vips_engine.Engine'
      ```
        
      This engine has some important things to know:
    
      1. Requires libvips 8.7.0. Ideally 8.8.0, as that includes some speedups for the 
         used `vips composite` command.
      3. When using this engine, remember to also set the ``THUMBNAIL_WATERMARK_VIPS``
         setting. See the reference at the bottom.
      4. This engine, just like sorl-thumbnail, uses the vips command line. Not the
         library. Hence, performance might not be stellar for all usecases. The best
         example here is that `THUMBNAIL_WATERMARK_POSITION="tile"` is terribly slow in
         comparison to other engines. That's because we can't pipe and have to write 
         multiple images to disk before assembling the final one.

3. Configure the watermark image. Note that this file has to live somewhere
   inside `STATIC_ROOT`.

    ```python
    THUMBNAIL_WATERMARK = 'my_watermark.png'
    ```

That's it for a simple setup. Note that the watermark will only appear if your thumbnail
size is big enough.

See _Advanced Usage_ for ways to dynamically change all sort of aspects of the
watermark. Refer to the _Settings Reference_ at the bottom to get a good overview over
all the possibilities.

## Advanced Usage

sorl-watermark adds additional options to the `{% thumbnail %}` templatetag, so you can
customize the watermarking dynamically.

The following new options are available:

* `watermark=imagefile`  
  This options takes an ImageFile and uses it instead of the
  default `THUMBNAIL_WATERMARK`.
* `watermark_size="x200"`  
  Changes the watermark's size. Takes the same options as the `THUMBNAIL_WATERMARK_SIZE`
  option.
* `watermark_pos="north east"`  
  Specifies where the watermark should be put. Accepts the same options as
  the `THUMBNAIL_WATERMARK_POSITION` setting.
* `watermark_alpha=0.9`
  Sets the watermark's opacity. See the `THUMBNAIL_WATERMARK_OPACITY` setting.

### Example

Let's say you have a gallery. You don't want the small thumbnails to have any
watermarks. So you set `THUMBNAIL_WATERMARK_ALWAYS = False`. However, the fullscreen
images in your gallery should have a watermark. Centered and with 20 percent opacity:

```jinja2
{# Your preview image, no watermark. %}
{% thumbnail item.image "100x100" crop="center" as preview_thumb %}
    <img 
      src="{{ preview_thumb.url }}" 
      width="{{ preview_thumb.width }}" 
      height="{{ preview_thumb.height }}"
    >
{% endthumbnail %}

{# Your fullscreen image, with a nice watermark. %}
{% thumbnail item.image "3840x2160" crop="center" watermark_alpha=0.2 watermark_pos="center" as full_image %}
    <img 
      src="{{ full_image.url }}" 
      width="{{ full_image.width }}" 
      height="{{ full_image.height }}"
    >
{% endthumbnail %}
```

## Settings Reference

The following settings are available:

* `THUMBNAIL_WATERMARK`  
  Sets the image to be used as a watermark. The file must live within `STATIC_ROOT`.
* `THUMBNAIL_WATERMARK_ALWAYS` (default: `True`)  
  Stamp a watermark on every image.
* `THUMBNAIL_WATERMARK_SIZE`  
  Change the size of the watermark. This can either be a geometry string, as is usual
  with sorl-thumbnail (`x200`, `200x200`,…), or a percentage. If given a percentage,
  the watermark will always be the given percentage of the thumbnail size.
* `THUMBNAIL_WATERMARK_OPACITY` (default: `0.0`, meaning fully transparent)  
  A float from 0.0 to 1.0, specifying the opacity of the watermark.
* `THUMBNAIL_WATERMARK_POSITION` (default: `"south east"`, so right-bottom corner)  
  Specifies the position of the watermark. There are multiple ways to set position:

    - Using words:
      * `"north"` - top
      * `"south"` - bottom
      * `"west"` - left
      * `"east"` - right
      * `"north east"` - top right corner
      * `"north west"` - top left corner
      * `"south east"` - bottom right corner
      * `"south west"` - bottom left corner
      * `"center"` - well, the middle of the image.
      * **Special**: `"tile"` - will plaster your watermark all over the thumbnail.
    - Using pixels:

      You can change position with a pair of padding values (in pixels). E.g. "20 20"
      will place the watermark near the left-top corner, "-20 -20" - near the right-bottom
      corner. 
* `THUMBNAIL_WATERMARK_COMPOSITE` (default: `'composite'`).  
  Path to composite command, use `'gm composite'` for GraphicsMagick. Only applicable 
  for the convert Engine.
* `THUMBNAIL_WATERMARK_VIPS` (default: `'vips'`).  
  Path to vips command. Only applicable for the Vips Engine.
