"""CPU-composed product advert with original illustrative assets; no video model/audio."""
import hashlib
import json
import re
import shutil
import subprocess
import textwrap
import uuid
from copy import deepcopy
from dataclasses import dataclass
from pathlib import Path

from ..contracts import DomainError

LABEL = "Template-composed MP4; fictional product, no video model or audio used."
MAX_BYTES = 20 * 1024 * 1024
ASSET_ROOT = Path(__file__).resolve().parent.parent / "assets" / "advert"


def digest(value):
    return hashlib.sha256(value).hexdigest()


def script_digest(script):
    return digest(json.dumps(script, sort_keys=True, ensure_ascii=False, separators=(",", ":")).encode())


def failed(code="MEDIA_GENERATION_FAILED"):
    return DomainError("Template video could not be generated or verified. No review-ready media is claimed.",
                       503, code)


@dataclass(frozen=True)
class VideoConfig:
    ffmpeg: str
    ffprobe: str
    font: str
    output_dir: str
    timeout_seconds: int = 120

    @classmethod
    def load(cls, path):
        path = Path(path).resolve()
        values = json.loads(path.read_text(encoding="utf-8-sig"))
        config = cls(**values)
        if type(config.timeout_seconds) is not int or not 1 <= config.timeout_seconds <= 300:
            raise ValueError("Video timeout must be an integer from 1 to 300 seconds.")
        for field in ("ffmpeg", "ffprobe", "font", "output_dir"):
            value = getattr(config, field)
            if not isinstance(value, str) or not value.strip():
                raise ValueError("Supply explicit local video tool, font and output paths.")
            local = Path(value)
            values[field] = str((local if local.is_absolute() else path.parent/local).resolve())
        # Missing binaries are checked at generation time and retained as a failed campaign.
        return cls(**values)


class TemplateVideo:
    template_video = True

    def __init__(self, config):
        self.config = config
        self.root = Path(config.output_dir).resolve()

    def run(self, executable, arguments, cwd):
        return subprocess.run([executable, *arguments], cwd=cwd, check=True, capture_output=True,
                              timeout=self.config.timeout_seconds,
                              creationflags=getattr(subprocess, "CREATE_NO_WINDOW", 0))

    def generate(self, script):
        try:
            if any(not Path(p).is_file() for p in (self.config.ffmpeg, self.config.ffprobe, self.config.font)):
                raise failed("MEDIA_UNAVAILABLE")
            frames = deepcopy(script["storyboard"])
            if len(frames) != 3:
                raise failed("MEDIA_CONTENT_REJECTED")
            for i, frame in enumerate(frames):
                if (set(frame) != {"shot", "duration", "caption", "direction"}
                        or type(frame["shot"]) is not int or frame["shot"] != i+1
                        or frame["duration"] != ("0–5 s", "5–10 s", "10–15 s")[i]
                        or any(not isinstance(frame[k], str) or not frame[k].strip()
                               or len(frame[k]) > limit for k, limit in (("caption", 120), ("direction", 140)))):
                    raise failed("MEDIA_CONTENT_REJECTED")
            # Fixed bundled illustrations only, never caller-selected files/URLs.
            # Packaging is fictional art, not evidence of a real product's appearance.
            vessel = "pump" if "cleanser" in frames[0]["caption"].casefold() else "jar"
            assets = {"studio.png": ASSET_ROOT / "studio.png", "product.png": ASSET_ROOT / (vessel + ".png")}
            if any(not path.is_file() for path in assets.values()):
                raise failed("MEDIA_UNAVAILABLE")
            self.root.mkdir(parents=True, exist_ok=True)
            artifact_id = uuid.uuid4().hex
            job = self.root/artifact_id
            job.mkdir(exist_ok=False)
            shutil.copyfile(self.config.font, job/"font.ttf")
            for filename, source in assets.items():
                shutil.copyfile(source, job / filename)
            style = script.get("textPlan", {}).get("style", "CALM")
            accent, speed = {"CALM": ("0x45624b", .35), "ENERGETIC": ("0xa45532", .8),
                             "INFORMATIVE": ("0x354d5b", .2)}.get(style, ("0x45624b", .35))
            baseline = 280 if vessel == "pump" else 330
            filters = [f"[0:v]scale=744:1322,crop=720:1280:x='12+8*sin(t*.25)':y='21+10*sin(t*.2)',setsar=1[studio]",
                       "[1:v]format=rgba,scale=w='600*(1+.035*sin(PI*t/15))':h=-1:eval=frame:flags=lanczos[product]",
                       f"[studio][product]overlay=x='(W-w)/2+8*sin(t*{speed})':"
                       f"y='{baseline}-(h-720)*.85+5*sin(t*{speed})':eval=frame:shortest=1[composed]"]
            finishing = ["drawbox=x=56:y=119:w=608:h=1:color=0x40583d@0.25:t=fill",
                         f"drawbox=x=56:y=154:w=28:h=3:color={accent}:t=fill",
                         "drawbox=x=0:y=1140:w=720:h=140:color=0x273e30@0.94:t=fill"]

            def text(filename, value, size, y, when=None, color="0x273e30", x="56"):
                with (job/filename).open("w", encoding="utf-8", newline="\n") as output:
                    output.write(value)
                f = (f"drawtext=fontfile=font.ttf:textfile={filename}:expansion=none:fontsize={size}:"
                     f"fontcolor={color}:line_spacing=12:x='{x}'")
                if when:
                    start, end = when
                    # Only fixed numeric timing enters the filter language; all copy is textfile data.
                    f += (f":y='{y}+14*(1-min(1,max(0,(t-{start})/.5)))':"
                          f"alpha='if(lt(t,{start}),0,if(lt(t,{start}+.4),(t-{start})/.4,"
                          f"if(lt(t,{end}-.3),1,if(lt(t,{end}),({end}-t)/.3,0))))'")
                else:
                    f += f":y={y}"
                finishing.append(f)

            text("header.txt", "BEAUTY COMPANY", 25, 66)
            text("studio.txt", "CONTENT STUDIO", 12, 75, x="w-text_w-56")
            text("watermark.txt", "FICTIONAL PACKAGING  /  SILENT TEMPLATE", 17, 1171, color="0xf0f1df")
            text("review.txt", "DRAFT  /  FOUNDER REVIEW REQUIRED", 15, 1205, color="0xc3cfb9")
            for i, frame in enumerate(frames):
                when = (i*5, (i+1)*5)
                text(f"stage-{i}.txt", ("01  /  THE PRODUCT", "02  /  THE DETAILS", "03  /  EXPLORE")[i],
                     15, 176, when, color=accent)
                caption = frame["caption"]
                text(f"caption-{i}.txt", "\n".join(textwrap.wrap(caption, width=25)),
                     45 if len(caption) < 65 else 33, 232, when)
            finishing.extend(["fade=t=in:st=0:d=0.4", "fade=t=out:st=14.6:d=0.4", "format=yuv420p"])
            graph = ";\n".join(filters + ["[composed]" + ",".join(finishing) + "[out]"])
            (job / "render.ffgraph").write_text(graph, encoding="utf-8")
            # Pass the fixed graph as one argv item; FFmpeg 9 removed -filter_complex_script.
            # Captions remain textfile data, never interpolated into the filter language.
            self.run(self.config.ffmpeg, ["-nostdin", "-v", "error", "-n", "-filter_complex_threads", "1",
                "-loop", "1", "-framerate", "24", "-i", "studio.png", "-loop", "1", "-framerate", "24", "-i", "product.png",
                "-filter_complex", graph, "-map", "[out]", "-t", "15", "-r", "24", "-an", "-c:v", "libx264",
                "-preset", "veryfast", "-crf", "21", "-pix_fmt", "yuv420p", "-movflags", "+faststart", "draft.mp4"], job)
            probe = json.loads(self.run(self.config.ffprobe, ["-v", "error", "-show_streams", "-show_format",
                                                             "-of", "json", "draft.mp4"], job).stdout)
            streams = probe["streams"]
            if (len(streams)!=1 or streams[0]["codec_type"]!="video" or streams[0]["codec_name"]!="h264"
                    or streams[0]["width"]!=720 or streams[0]["height"]!=1280
                    or streams[0]["pix_fmt"]!="yuv420p" or int(streams[0]["nb_frames"])!=360
                    or abs(float(probe["format"]["duration"])-15)>0.05):
                raise failed("MEDIA_CONTENT_REJECTED")
            self.run(self.config.ffmpeg, ["-nostdin", "-v", "error", "-xerror", "-i", "draft.mp4", "-f", "null", "-"], job)
            file = job/"draft.mp4"
            if not 0 < file.stat().st_size <= MAX_BYTES:
                raise failed("MEDIA_CONTENT_REJECTED")
            media = {"kind": "TEMPLATE_VIDEO", "simulated": False, "modelGenerated": False,
                     "label": LABEL, "frames": frames, "artifactId": artifact_id,
                     "sha256": digest(file.read_bytes()), "scriptSha256": script_digest(script),
                     "bytes": file.stat().st_size, "mime": "video/mp4", "durationSeconds": 15,
                     "width": 720, "height": 1280, "fps": 24, "audio": False}
            (job/"manifest.json").write_text(json.dumps(media, ensure_ascii=False, indent=2), encoding="utf-8")
            return media
        except DomainError:
            raise
        except subprocess.TimeoutExpired:
            raise failed("MEDIA_TIMEOUT") from None
        except (OSError, subprocess.CalledProcessError, ValueError, TypeError, KeyError, IndexError):
            raise failed() from None

    def read(self, media):
        """Only opaque, saved artifact identifiers; never accept a caller path or URL."""
        try:
            artifact_id = media["artifactId"]
            if not isinstance(artifact_id, str) or not re.fullmatch(r"[0-9a-f]{32}", artifact_id):
                raise ValueError()
            job = self.root/artifact_id
            if job.resolve().parent != self.root or (job/"draft.mp4").resolve().parent != job.resolve():
                raise ValueError()
            file = job/"draft.mp4"
            if not 0 < file.stat().st_size <= MAX_BYTES:
                raise ValueError()
            manifest = json.loads((job/"manifest.json").read_text(encoding="utf-8"))
            raw = file.read_bytes()
            if manifest != media or len(raw)!=media["bytes"] or digest(raw)!=media["sha256"]:
                raise ValueError()
            return raw
        except (OSError, ValueError, TypeError, KeyError):
            raise failed("MEDIA_ARTIFACT_UNAVAILABLE") from None

    def validate(self, media, script):
        if (not isinstance(media, dict) or media.get("kind")!="TEMPLATE_VIDEO" or media.get("simulated") is not False
                or media.get("modelGenerated") is not False or media.get("label")!=LABEL
                or media.get("frames")!=script["storyboard"] or media.get("scriptSha256")!=script_digest(script)):
            raise failed("MEDIA_CONTENT_REJECTED")
        self.read(media)
