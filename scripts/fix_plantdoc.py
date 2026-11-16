"""Copy PlantDoc images from the downloaded Git clone using Windows-safe names."""

from pathlib import Path, PurePosixPath
from subprocess import PIPE, Popen, check_output


def main():
    data = Path.cwd() / "data"
    clone = data / "PlantDoc-Dataset-clone"
    destination = data / "PlantDoc-Dataset"
    git = ["git", "-C", str(clone)]

    if not clone.is_dir():
        raise SystemExit(
            "Run this from LeafShift-main with the downloaded clone at "
            "data/PlantDoc-Dataset-clone."
        )

    entries = check_output(
        [*git, "ls-tree", "-r", "-z", "HEAD", "--", "train", "test"]
    ).split(b"\0")
    count = 0

    with Popen([*git, "cat-file", "--batch"], stdin=PIPE, stdout=PIPE) as blobs:
        try:
            for entry in filter(None, entries):
                metadata, raw_path = entry.split(b"\t", 1)
                _, kind, object_id = metadata.split()
                if kind != b"blob":
                    continue

                source = PurePosixPath(raw_path.decode("utf-8"))
                blobs.stdin.write(object_id + b"\n")
                blobs.stdin.flush()
                header = blobs.stdout.readline().split()
                if len(header) != 3 or header[1] != b"blob":
                    raise RuntimeError(f"Git could not read {source}")

                size = int(header[2])
                content = blobs.stdout.read(size)
                if len(content) != size or blobs.stdout.read(1) != b"\n":
                    raise RuntimeError(f"Incomplete Git data for {source}")

                count += 1
                folder = destination.joinpath(*source.parts[:-1])
                folder.mkdir(parents=True, exist_ok=True)
                (folder / f"{count:04d}{source.suffix.lower()}").write_bytes(content)
        finally:
            blobs.stdin.close()

        if blobs.wait() != 0:
            raise SystemExit("Git could not finish reading the clone.")

    print(f"Extracted {count} files into data/PlantDoc-Dataset.")


if __name__ == "__main__":
    main()
