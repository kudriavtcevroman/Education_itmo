from pathlib import Path

work = Path.cwd()
my_folder = work / "my_folder"
if not my_folder.exists():
    my_folder.mkdir()
file1 = my_folder / "file1.txt"
file1.touch()
(my_folder / "file2.txt").touch()
my_folder.joinpath("image.png").touch()
(my_folder / "images").mkdir(exist_ok=True)
for f in my_folder.glob('*.png'):
    path_destination = Path(my_folder /"images") / f.name
    f.replace(path_destination)
