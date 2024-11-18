# Folder Synchronization Script

This Python script ensures the synchronization of two folders: a `source` folder and a `replica` folder. The `replica` folder is updated to be a complete and identical copy of the `source` folder. Synchronization is performed periodically, with detailed logging of all file operations.

---

## **Features**

- One-way synchronization: Ensures the `replica` matches the `source`.
- Handles:
  - Copying new files and directories from `source` to `replica`.
  - Updating modified files.
  - Removing files and directories in `replica` that no longer exist in `source`.
- Logs all operations to both a file and the console.
- Performs periodic synchronization at a user-defined interval.
- Provides clear error handling and user feedback.
- Allows configuration of paths and intervals via command-line arguments.

---

## **Prerequisites**

- Python 3.6 or higher.

---

## **Installation**

1. Clone this repository:
   ```bash
   git clone https://github.com/yagop27/File-Synchronization-Project.git
   cd File-Synchronization-Project
   
Ensure Python is installed and added to your PATH.

<h3>Usage</h3>

2. Run the script from the command line with the following arguments:

    ```bash
      python sync_folders.py --source <source-folder-path> --replica <replica-folder-path> --interval <sync-interval-seconds> --log <log-file-path>
      
Command-line Arguments:

    --source: The path to the source directory to synchronize from.
    
    --replica: The path to the replica directory to synchronize to.
    
    --interval: The synchronization interval in seconds.
    
    --log: The path to the log file where operations are logged.
  
<h3>Examples:</h3>

Example 1: Basic Synchronization

Synchronize C:\SourceFolder to C:\ReplicaFolder every 10 seconds, logging to C:\Logs\sync.log:

    python sync_folders.py --source C:\SourceFolder --replica C:\ReplicaFolder --interval 10 --log C:\Logs\sync.log

If the replica folder does not exist, the script will create it automatically.

The script logs all actions, including:

  1- Files or directories copied, updated, or deleted.
  
  2- Any errors encountered during the synchronization process.
  
  3- All logs are stored in the specified log file and displayed in the console for real-time feedback.

<h3>Error Handling</h3>

  1- If the source folder does not exist, the script logs an error and stops.
  
  2- If the log file or directory cannot be created due to permission issues, the script logs the issue and exits.
  
Supports graceful exit on Ctrl+C.

License

This project is licensed under the MIT License. See the LICENSE file for more details.

Author
Developed by Yago Oliveira Pais. For any inquiries, feel free to contact me.
