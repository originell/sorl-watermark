# sorl-watermark
## This is under heavy development and does not yet support all features mentioned here.
sorl-watermark offers drop-in engines for sorl-thumbnail, which automagically
insert a specified image as watermark on top of the original thumbnail.

Of course everything is configurable, from watermark image to the position and
the opacity.

If you are looking for a sorl engine to dynamically create text watermarks,
you might want to have a look at [zeus/watermark](https://bitbucket.org/zeus/watermarker/overview).

_Note_: This project uses [Semantic Versioning](http://semver.org/) as it's
        versioning scheme.

## Setup
Install sorl-watermark, either by cloning from the [github repository]() or
by installing it via `pip`:

    pip install sorl-watermark

Change sorl's thumbnail engine to the fitting one from sorl-watermark.
See _Engines_ for all available engines. Here is an example using the PIL
engine.

    THUMBNAIL_ENGINE = 'sorl.watermark.engines.pil'

Next up you tell it which image should be used as a watermark. Note that this
file has to live somewhere inside STATIC\_ROOT.

    THUMBNAIL_WATERMARK = 'my_watermark.png'

That's it for a simple setup. The engine will only apply the watermark
if the thumbnail size is big enough. 

See _Advanced Usage_ for ways to dynamically change the watermark itself,
it's size or ways to selectively apply watermarks.

## Engines
sorl-watermark supports two of sorl-thumbnails backends:

* PIL (sorl.watermark.engines.pil)
* GraphicsMagick (Magick++) via pgmagick (sorl.watermark.engines.magick)

## Advanced Usage
sorl-watermark also _enhances_ the default `thumbnail` templatetag with some
more options. (Well, actually it does not really enhance it, since the templatetag
itself passes the options through to the engine itself by default)

By default, the templatetag syntax is:

    {% thumbnail image key1=var1 key2=var2 %}

The following new options are available:

* watermark=imagefile  
  This options takes an ImageFile and uses this one instead of the default
  watermark file, set via THUMBNAIL\_WATERMARK
* watermark\_size=geometry  
  Changes the watermark's size. Takes the same options as the
  THUMBNAIL\_WATERMARK\_SIZE option.
* watermark\_pos=gravity  
  Specifies where the watermark shall be put. Accepts the same options as the
  THUMBNAIL\_WATERMARK\_POSITION setting.
* watermark_alpha=integer
  Sets the watermark's opacity. Has to be a value between 0 and 1.

## Settings Reference
The following settings are available

* THUMBNAIL\_WATERMARK  
  Sets the image to be used as a watermark. The file must live within 
  STATIC\_ROOT.

* THUMBNAIL\_WATERMARK_ALWAYS  
  Stamp a watermark on every image.  
  Default is True.

* THUMBANIL\_WATERMARK\_SIZE  
  Change the size of the watermark. This can either be a geometry string, as
  is usual with sorl-thumbnail ("x200", "200x200"), or a percentage.  
  If given a percentage, the watermark will always be the given percentage
  of the thumbnail size.

* THUMBNAIL\_WATERMARK_OPACITY
  An integer from 0 to 1, specifying the opacity of the watermark.  
  Default is 0 (opaque).

* THUMBNAIL\_WATERMARK\_POSITION  
  Specifies the position of the watermark. You can either pass this a gravity
  like
      * "north"
      * "south"
      * "west"
      * "east"
      * "north east"
      * "south east"
      * "north west"
      * "south west"
      * "center"

  or a tuple (x, y). Default: "south east"

