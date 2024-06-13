from pathlib import Path

work = Path.cwd()
test_folder = work / "Test"
print(test_folder)

(test_folder/"text").mkdir(exist_ok=True)
for f in test_folder.glob('*.txt'):
    path_destination = Path(test_folder /"text") / f.name
    f.replace(path_destination)