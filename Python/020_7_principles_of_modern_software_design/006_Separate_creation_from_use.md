# Separate creation from use

> Source: https://academy.arjancodes.com/products/the-software-designer-mindset/categories/2150444017/posts/2153274140

As a continuation of cohesion topic, where we want to split responsibilities we can go one step ahead and split 
creating an object from using them. Factory pattern is a good way to do so.

## Factory pattern

The main point of Factory pattern is that we have a class that is responsible for creating objects.

### Before

`main` function is responsible for - receiving a user choice for video quality, creating Exporter objects and using selected Exporter objects,

```python
def main() -> None:

    # read the desired export quality
    export_quality = read_choice(
        "What output quality do you want", ["low", "high", "master"]
    )

    # create the video and audio exporters
    video_exporter: VideoExporter
    audio_exporter: AudioExporter
    if export_quality == "low":
        video_exporter = H264BPVideoExporter()
        audio_exporter = AACAudioExporter()
    elif export_quality == "high":
        video_exporter = H264Hi422PVideoExporter()
        audio_exporter = AACAudioExporter()
    else:
        # default: master quality
        video_exporter = LosslessVideoExporter()
        audio_exporter = WAVAudioExporter()

    # prepare the export
    video_exporter.prepare_export("placeholder_for_video_data")
    audio_exporter.prepare_export("placeholder_for_audio_data")

    # do the export
    folder = Path("/usr/tmp/video")
    video_exporter.do_export(folder)
    audio_exporter.do_export(folder)
```

### After

Instead of creating objects in `main` functions, the one of Exporter classes (which are factories) is responsible to do so.

Factory for particular choice is stored in constant `FACTORIES` dictionary. It's picked via separate `read_factory` function.

Created objects are used in separate `do_export` function.

```python
class ExporterFactory(Protocol):
    """
    Factory that represents a combination of video and audio codecs.
    The factory doesn't maintain any of the instances it creates.
    """

    def create_video_exporter(self) -> VideoExporter:
        """Returns a new video exporter belonging to this factory."""
        ...

    def create_audio_exporter(self) -> AudioExporter:
        """Returns a new audio exporter belonging to this factory."""
        ...


class FastExporter:
    """Factory aimed at providing a high speed, lower quality export."""

    def create_video_exporter(self) -> VideoExporter:
        return H264BPVideoExporter()

    def create_audio_exporter(self) -> AudioExporter:
        return AACAudioExporter()


class HighQualityExporter:
    """Factory aimed at providing a slower speed, high quality export."""

    def create_video_exporter(self) -> VideoExporter:
        return H264Hi422PVideoExporter()

    def create_audio_exporter(self) -> AudioExporter:
        return AACAudioExporter()


class MasterQualityExporter:
    """Factory aimed at providing a low speed, master quality export."""

    def create_video_exporter(self) -> VideoExporter:
        return LosslessVideoExporter()

    def create_audio_exporter(self) -> AudioExporter:
        return WAVAudioExporter()


FACTORIES: dict[str, ExporterFactory] = {
    "low": FastExporter(),
    "high": HighQualityExporter(),
    "master": MasterQualityExporter(),
}


def read_factory() -> ExporterFactory:
    """Constructs an exporter factory based on the user's preference."""

    while True:
        export_quality = input(
            f"Enter desired output quality ({', '.join(FACTORIES)}): "
        )
        try:
            return FACTORIES[export_quality]
        except KeyError:
            print(f"Unknown output quality option: {export_quality}.")


def do_export(fac: ExporterFactory) -> None:
    """Do a test export using a video and audio exporter."""

    # retrieve the exporters
    video_exporter = fac.create_video_exporter()
    audio_exporter = fac.create_audio_exporter()

    # prepare the export
    video_exporter.prepare_export("placeholder_for_video_data")
    audio_exporter.prepare_export("placeholder_for_audio_data")

    # do the export
    folder = Path("/usr/tmp/video")
    video_exporter.do_export(folder)
    audio_exporter.do_export(folder)


def main() -> None:
    # create the factory
    factory = read_factory()

    # perform the exporting job
    do_export(factory)
```