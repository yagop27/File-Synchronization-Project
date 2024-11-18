import os
import filecmp
import shutil
import logging
import argparse
import time


def setup_logging(log_file_path):
    """Set up logging configuration."""
    log_dir = os.path.dirname(log_file_path)
    if not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)-8s %(message)s',
        datefmt='%a, %d %b %Y %H:%M:%S',
        handlers=[
            logging.FileHandler(log_file_path, mode='a'),
            logging.StreamHandler()
        ]
    )


def comparison_check(source_path, replica_path, files, comparison):

    """This function handles the synchronization of the source and replica files. It copies, updates, or deletes files
    and directories as needed."""

    for file in files:

        source_file = os.path.join(source_path, file)
        replica_file = os.path.join(replica_path, file)

        # Checking for subdirectories that exist only on source or replica
        if os.path.isdir(source_file) or os.path.isdir(replica_file):

            if file in comparison.left_only:  # If the sub exists only on source it is copied to replica
                shutil.copytree(source_file, replica_file)
                logging.info(f"Copied directory: {source_file} to {replica_file}")

            elif file in comparison.right_only:  # If it exists only in the replica, it will be deleted.
                shutil.rmtree(replica_file)
                logging.info(f"Removed directory: {replica_file}")

            elif file in comparison.common_dirs and file not in comparison.same_files:  # If the subs exist in both it's going to recurse into them
                new_source_path = os.path.join(source_path, file)
                new_replica_path = os.path.join(replica_path, file)

                new_comparison = filecmp.dircmp(new_source_path, new_replica_path)
                new_files = (
                        new_comparison.left_only
                        + new_comparison.right_only
                        + new_comparison.common
                )
                comparison_check(new_source_path, new_replica_path, new_files, new_comparison)

        elif file in comparison.right_only:  # Files that aren't on source anymore are deleted from replica
            os.remove(replica_file)
            logging.info(f"Removed file: {replica_file}")

        elif file in comparison.left_only:  # Files that are on source only are copied to replica
            shutil.copy2(source_file, replica_file)
            logging.info(f"Copied file: {source_file} to {replica_file}")

        elif file in comparison.diff_files:  # Files that have the same name but have different os.stats() are updated
            shutil.copy2(source_file, replica_file)
            logging.info(f"Updated file: {source_file} to {replica_file}")


def main(source_path, replica_path, sync_interval, log_file_path):
    """This function will configure the log file, and it will synchronize the source and replica files periodically
     unless an error occurs or the user stops it."""

    # Setting up the log config
    try:
        setup_logging(log_file_path)
    except PermissionError:
        logging.error(f"Unable to create log file at {log_file_path}")
        raise PermissionError(f"Unable to create log file at {log_file_path}")

    # Checking if the source and replica paths are valid
    if not os.path.exists(source_path):
        logging.error(f"Source path does not exist: {source_path}")
        raise FileNotFoundError(f"Source path does not exist: {source_path}")

    if not os.path.exists(replica_path):
        os.makedirs(replica_path, exist_ok=True)
        logging.info(f"Replica path does not exist. Creating: {replica_path}")

    try:
        while True:
            # Create the comparison object between the directories
            comparison = filecmp.dircmp(source_path, replica_path)

            # Gather all the files names in a list for looping
            all_files = comparison.left_only + comparison.right_only + comparison.common

            # Start comparison check
            comparison_check(source_path, replica_path, all_files, comparison)

            # It puts the code on standby so it can run again after the given interval
            print(f"Waiting for {sync_interval} seconds before restarting...")
            time.sleep(sync_interval)

    except KeyboardInterrupt:
        # Exists the program on Ctrl+C
        logging.info("Synchronization stopped by the user.")
    except Exception as e:
        # Log unexpected errors
        logging.error(f"An error occurred: {e}")


# Setting up the argument parser
parser = argparse.ArgumentParser(description='Sync folders and log the activity.')
parser.add_argument('--source', required=True, help='Path to the source directory.')
parser.add_argument('--replica', required=True, help='Path to the destination directory.')
parser.add_argument('--interval', type=int, required=True, help='Synchronization interval in seconds.')
parser.add_argument('--log', required=True, help='Path to the log file.')

# Parse the command line arguments
args = parser.parse_args()

# Access the provided arguments
src_path = args.source
rep_path = args.replica
interval = args.interval
log_path = args.log

main(src_path, rep_path, interval, log_path)


