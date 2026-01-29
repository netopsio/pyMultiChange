#!/usr/bin/env python
"""Main script for making mass changes to network devices."""

import argparse
import logging
import queue
import sys
import threading
from pathlib import Path

from netlib.conn_type import SSH, Telnet
from netlib.user_keyring import KeyRing

from pymultichange.models import Arguments, Credentials, DeviceSettings, Protocol


logger = logging.getLogger(__name__)


def setup_logging(verbose: bool = False) -> None:
    """Configure logging for the application."""
    level = logging.DEBUG if verbose else logging.INFO
    logging.basicConfig(
        level=level,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )


def log_failure(device_name: str, log_file: str = "failure.log") -> None:
    """Log failed device connections to a file."""
    log_path = Path(log_file)
    mode = "a" if log_path.exists() else "w"
    with log_path.open(mode) as f:
        f.write(f"{device_name}\n")
    logger.warning(f"Connection to {device_name} failed. Logged to {log_file}")


def device_connection(device_settings: DeviceSettings) -> None:
    """
    Connect to a device and execute commands.

    Args:
        device_settings: Configuration for the device connection
    """
    device_name = device_settings.device_name
    protocol = device_settings.protocol
    logger.info(f"Attempting to connect to {device_name} via {protocol.value.upper()}")

    try:
        if protocol == Protocol.SSH:
            connection = SSH(
                device_name=device_name,
                username=device_settings.username,
                password=device_settings.password,
                delay=device_settings.delay,
                buffer=device_settings.buffer,
            )
        elif protocol == Protocol.TELNET:
            connection = Telnet(
                device_name=device_name,
                username=device_settings.username,
                password=device_settings.password,
                delay=device_settings.delay,
            )
        else:
            logger.error(f"Unknown protocol: {protocol}")
            sys.exit(1)

        connection.connect()
        logger.debug(f"Successfully connected to {device_name}")

        connection.set_enable(device_settings.enable_password)
        connection.disable_paging()

        for command in device_settings.commands:
            logger.debug(f"Executing command on {device_name}: {command}")
            output = connection.command(command)
            if device_settings.command_output:
                print(f"\n--- {device_name}: {command} ---")
                print(output)

        logger.debug(f"Closing connection to {device_name}")
        connection.close()
        logger.info(f"Successfully completed commands on {device_name}")

    except Exception as e:
        logger.error(f"Error connecting to {device_name} via {protocol.value}: {e}")
        log_failure(device_name)


def connection_queue_worker(devices_queue: queue.Queue) -> None:
    """
    Worker function to process device connections from a queue.

    Args:
        devices_queue: Queue containing DeviceSettings objects
    """
    while True:
        try:
            device_settings = devices_queue.get(timeout=5)
        except queue.Empty:
            break

        device_connection(device_settings)
        devices_queue.task_done()


def parse_arguments() -> Arguments:
    """Parse and validate command-line arguments."""
    description = "Managing network devices with Python"
    parser = argparse.ArgumentParser(description=description)

    parser.add_argument("-u", "--username", help="Specify your username.", required=True)
    parser.add_argument(
        "--delete-creds",
        help="Delete credentials from keyring.",
        nargs="?",
        const=True,
        dest="delete_creds",
    )
    parser.add_argument(
        "--set-creds",
        help="Set keyring credentials.",
        nargs="?",
        const=True,
        dest="set_creds",
    )
    parser.add_argument("-d", "--devices", help="Specifies a host file")
    parser.add_argument("-c", "--commands", help="Specifies a commands file")
    parser.add_argument(
        "-s", "--ssh", help="Default: Use the SSH protocol", nargs="?", const="ssh"
    )
    parser.add_argument(
        "-t", "--telnet", help="Use the Telnet protocol", nargs="?", const="telnet"
    )
    parser.add_argument(
        "-o", "--output", help="Verbose command output", nargs="?", const=True
    )
    parser.add_argument(
        "-v", "--verbose", help="Debug script output", nargs="?", const=True
    )
    parser.add_argument(
        "--delay", help="Change the default delay exec between commands", default="2"
    )
    parser.add_argument(
        "--buffer", help="Change the default SSH output buffer", default="8192"
    )
    parser.add_argument(
        "--threaded", help="Enable process threading", nargs="?", const=True
    )
    parser.add_argument(
        "-m", "--maxthreads", help="Define the maximum number of threads", default="10"
    )

    args_dict = vars(parser.parse_args())

    # Determine protocol
    if args_dict.get("telnet"):
        args_dict["protocol"] = Protocol.TELNET
    else:
        args_dict["protocol"] = Protocol.SSH

    return Arguments(**args_dict)


def read_file_lines(file_path: str, file_type: str) -> list[str]:
    """
    Read lines from a file.

    Args:
        file_path: Path to the file
        file_type: Type of file for error messages (e.g., "hosts", "commands")

    Returns:
        List of stripped lines from the file

    Raises:
        SystemExit: If file doesn't exist
    """
    path = Path(file_path)
    if not path.is_file():
        logger.error(f"Invalid {file_type} file: {file_path}")
        sys.exit(1)

    logger.debug(f"Reading {file_type} from {file_path}")
    with path.open("r") as f:
        return [line.strip() for line in f if line.strip()]


def main() -> None:
    """Main entry point for the application."""
    args = parse_arguments()
    setup_logging(verbose=bool(args.verbose))

    logger.debug("Starting pyMultiChange")

    # Handle keyring operations
    user_keys = KeyRing(username=args.username)

    if args.set_creds:
        logger.debug("Setting credentials in keyring")
        user_keys.set_creds()

    if args.delete_creds:
        logger.debug("Deleting credentials from keyring")
        user_keys.del_creds()
        return

    # Get credentials
    logger.debug("Obtaining credentials from keyring")
    creds_dict = user_keys.get_creds()
    creds = Credentials(**creds_dict)

    # Read hosts and commands
    if not args.devices or not args.commands:
        logger.error("Both --devices and --commands are required for operations")
        sys.exit(1)

    hosts = read_file_lines(args.devices, "hosts")
    commands = read_file_lines(args.commands, "commands")

    if not hosts:
        logger.error("No hosts found in devices file")
        sys.exit(1)

    if not commands:
        logger.error("No commands found in commands file")
        sys.exit(1)

    # Build device settings
    host_settings: list[DeviceSettings] = []
    for host in hosts:
        if not host:
            continue

        settings = DeviceSettings(
            device_name=host,
            protocol=args.protocol,
            username=creds.username,
            password=creds.password,
            enable_password=creds.enable,
            delay=int(args.delay),
            buffer=int(args.buffer),
            commands=commands,
            command_output=bool(args.output),
        )
        host_settings.append(settings)

    logger.info(f"Processing {len(host_settings)} devices with {len(commands)} commands")

    # Execute on devices
    if not args.threaded:
        logger.debug("Running in sequential mode")
        for settings in host_settings:
            device_connection(settings)
    else:
        logger.debug(f"Running in threaded mode with max {args.maxthreads} threads")
        try:
            device_queue: queue.Queue = queue.Queue()
            threads: list[threading.Thread] = []

            for settings in host_settings:
                device_queue.put(settings)

            max_threads = int(args.maxthreads)
            for _ in range(max_threads):
                thread = threading.Thread(target=connection_queue_worker, args=[device_queue])
                thread.start()
                threads.append(thread)

            for thread in threads:
                thread.join()

            logger.info("All devices processed successfully")

        except KeyboardInterrupt:
            logger.warning("Operation cancelled by user")
            sys.exit(1)


if __name__ == "__main__":
    main()
