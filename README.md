
# Unidirectional Folder Synchronization Script

This script synchronizes the contents of two folders unidirectionally. It copies the contents from a source folder to a destination folder, ensuring that any changes in the source folder are reflected in the destination folder. However, changes in the destination folder will not affect the source folder.

## Script Target

Task description: [TASK.md](TASK.md)

## Synchronization Rules

- Files created exclusively in the destination folder will not be modified unless they have the same name as files in the source folder. In that case, the files in the destination folder will be overwritten with the corresponding files from the source folder. A warning will be logged for each overwritten file.

- If a file is created inside a folder that has been previously synced from the source, deleting this folder from the source will not delete the folder in the destination.

## Prerequisites

- Python 3

## Usage

To use the script, run the following command:

```bash
python3 sync_script.py -s <source_dir> -d <destination_dir> -u <sync_interval> -l <log_file>
```


Replace `<source_dir>` with the path to the source folder, `<destination_dir>` with the path to the destination folder, `<sync_interval>` with the synchronization interval (in seconds), and `<log_file>` with the path to the log file.

Make sure you have the necessary permissions to read from the source folder and read/write to the destination folder.

## Example

Here's an example command to run the script:

```bash
python3 sync_script.py -u 2 -l /path/to/log_file.txt
```

If an option is not provided it will fall back to the defaults:
- `source_dir`: ./source
- `destination_dir`: ./destination
- `sync_interval`: 1
- `log_file`: ./folder_sync.log 



