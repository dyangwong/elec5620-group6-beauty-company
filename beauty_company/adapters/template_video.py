"""Opt-in CPU FFmpeg template renderer. No diffusion, product photos, voice or publishing."""
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
            self.root.mkdir(parents=True, exist_ok=True)
            artifact_id = uuid.uuid4().hex
            job = self.root/artifact_id
            job.mkdir(exist_ok=False)
            shutil.copyfile(self.config.font, job/"font.ttf")
            palette = {"CALM": "0xeaf0e5", "ENERGETIC": "0xffe6ce", "INFORMATIVE": "0xe8edf3"}
            color = palette.get(script.get("textPlan", {}).get("style"), "0xeaf0e5")
            filters = ["drawbox=x=42:y=40:w=636:h=1200:color=white:t=fill",
                       "drawbox=x=70:y=220:w=580:h=4:color=0x426356:t=fill"]

            def text(filename, value, size, y, when=None, color="0x203b31"):
                with (job/filename).open("w", encoding="utf-8", newline="\n") as output:
                    output.write(value)
                f = (f"drawtext=fontfile=font.ttf:textfile={filename}:expansion=none:fontsize={size}:"
                     f"fontcolor={color}:line_spacing=16:x=70:y={y}")
                filters.append(f + (f":enable='gte(t,{when[0]})*lt(t,{when[1]})'" if when else ""))

            text("header.txt", "BEAUTY COMPANY\nCONTENT STUDIO", 26, 100)
            text("watermark.txt", "TEMPLATE VIDEO / SILENT\nFICTIONAL PRODUCT\nDRAFT - FOUNDER REVIEW", 20, 1080)
            for i, frame in enumerate(frames):
                if set(frame) != {"shot", "duration", "caption", "direction"} or frame["shot"] != i+1:
                    raise failed("MEDIA_CONTENT_REJECTED")
                caption, direction = frame["caption"], frame["direction"]
                if not isinstance(caption, str) or not isinstance(direction, str) or len(caption)>120 or len(direction)>140:
                    raise failed("MEDIA_CONTENT_REJECTED")
                when = (i*5, (i+1)*5)
                text(f"shot-{i}.txt", f"SHOT {i+1:02d} / 03", 24, 300, when)
                text(f"caption-{i}.txt", "\n".join(textwrap.wrap(caption, width=23)), 45, 420, when)
                text(f"direction-{i}.txt", "\n".join(textwrap.wrap(direction, width=33)), 24, 790, when)
            filters.extend(["fade=t=in:st=0:d=0.3", "fade=t=out:st=14.7:d=0.3"])
            self.run(self.config.ffmpeg, ["-nostdin", "-v", "error", "-n", "-f", "lavfi", "-i",
                f"color=c={color}:s=720x1280:r=24:d=15", "-vf", ",".join(filters), "-an", "-c:v", "libx264",
                "-preset", "veryfast", "-crf", "23", "-pix_fmt", "yuv420p", "-movflags", "+faststart", "draft.mp4"], job)
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
