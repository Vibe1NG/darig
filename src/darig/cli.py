"""
Darig Unified CLI
"""

import argparse
import cmd
import logging
import sys
from typing import Any

from darig.common.utils import darig_version
from darig.query.engine import YaqlEngine
from darig.schema import check_paths, check_schema


class YaqlShell(cmd.Cmd):
    intro = "Welcome to the YAQL shell.   Type help or ? to list commands.\n"
    prompt = "(yaql) "

    def __init__(self, engine: YaqlEngine):
        super().__init__()
        self.engine = engine
        self.log = logging.getLogger(__name__)

    def do_load_schema(self, arg):
        """
        Load a YASL schema definition.
        Usage: load_schema <path_to_yasl_file_or_dir>
        """
        if not arg:
            self.log.error("❌ Please provide a file path or directory.")
            return

        self.log.info(f"Loading schema from: {arg}")
        if self.engine.load_schema(arg):
            self.log.info("✅ Schema loaded successfully.")
        else:
            self.log.error("❌ Failed to load schema.")

    def do_load_data(self, arg):
        """
        Load YAML data files.
        Usage: load_data <path_to_yaml_file_or_dir>
        """
        if not arg:
            self.log.error("❌ Please provide a file path or directory.")
            return

        self.log.info(f"Loading data from: {arg}")
        count = self.engine.load_data(arg)
        self.log.info(f"✅ Loaded {count} data records.")

    def do_export_data(self, arg):
        """
        Export the current database contents to YAML files.
        Usage: export_data <path_to_output_dir> [min]

        Options:
            min     If specified, writes all records of a type to a single file separated by '---'.
        """
        if not arg:
            self.log.error("❌ Please provide an output directory.")
            return

        args = arg.split()
        path = args[0]
        min_mode = False

        if len(args) > 1 and args[1] == "min":
            min_mode = True

        self.log.info(f"Exporting data to: {path} (min_mode={min_mode})")
        count = self.engine.export_data(path, min_mode=min_mode)
        self.log.info(f"✅ Exported {count} data files.")

    def do_sql(self, arg):
        """
        Execute a SQL query against the in-memory database.
        Usage: sql <query>
        """
        if not arg:
            self.log.error("❌ Please provide a SQL query.")
            return

        try:
            results = self.engine.execute_sql(arg)
            self._print_results(results)

        except Exception as e:
            self.log.error(f"❌ SQL Error: {e}")

    def _print_results(self, results: list[dict[str, Any]] | None):
        if results is None:
            self.log.info("Query executed successfully.")
        elif len(results) == 0:
            self.log.info("Query executed successfully (no results).")
        else:
            # Basic table printing
            headers = list(results[0].keys())
            print(" | ".join(headers))
            print("-" * (sum(len(h) for h in headers) + 3 * len(headers)))
            for row in results:
                print(" | ".join(str(v) for v in row.values()))

    def do_exit(self, arg):
        """Exit the YAQL shell."""
        self.log.info("Goodbye!")
        return True

    def do_quit(self, arg):
        """Exit the YAQL shell."""
        return self.do_exit(arg)


def get_parser():
    parser = argparse.ArgumentParser(
        prog="darig",
        description="Darig - Unified YAML Advanced Scripting & Querying CLI",
    )

    parser.add_argument(
        "--version", action="store_true", help="Show version information and exit"
    )
    parser.add_argument(
        "--quiet", action="store_true", help="Suppress output except for errors"
    )
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    parser.add_argument(
        "--output",
        choices=["text", "json", "yaml"],
        default="text",
        help="Set output format (text, json, yaml). Default is text.",
    )

    subparsers = parser.add_subparsers(
        title="commands", dest="command", help="Available commands"
    )

    # Command: check
    check_parser = subparsers.add_parser(
        "check", help="Check mixed YASL schemas and YAML data"
    )
    check_parser.add_argument(
        "paths",
        nargs="+",
        help="List of files or directories containing schemas and data",
    )
    check_parser.add_argument(
        "--model",
        dest="model_name",
        help="Specific YASL schema type name to validate data against (optional)",
    )

    # Command: schema
    schema_parser = subparsers.add_parser(
        "schema", help="Check the validity of a YASL schema file"
    )
    schema_parser.add_argument(
        "schema",
        help="YASL schema file or directory",
    )

    # Command: query
    query_parser = subparsers.add_parser(
        "query", help="Query YAML data using SQL (YAQL)"
    )
    query_parser.add_argument(
        "--sql",
        help="Execute a single SQL query and exit",
    )
    query_parser.add_argument(
        "--interactive",
        action="store_true",
        help="Start interactive YAQL shell (default if no --sql provided)",
    )
    query_parser.add_argument(
        "--schema",
        help="Path to a YASL schema file or directory to load on startup",
    )
    query_parser.add_argument(
        "--data",
        help="Path to a YAML data file or directory to load on startup",
    )

    return parser


def main():
    parser = get_parser()
    args = parser.parse_args()

    if args.version:
        print(f"Darig version {darig_version()}")
        sys.exit(0)

    if args.verbose and args.quiet:
        print("❌ Cannot use both --quiet and --verbose.")
        sys.exit(1)

    # Configure logging based on global flags
    log_level = logging.INFO
    if args.verbose:
        log_level = logging.DEBUG
    elif args.quiet:
        log_level = logging.ERROR

    logging.basicConfig(level=log_level, format="%(message)s")

    if args.command == "check":
        success = check_paths(
            args.paths,
            model_name=args.model_name,
            disable_log=False,
            quiet_log=args.quiet,
            verbose_log=args.verbose,
            output=args.output,
        )
        sys.exit(0 if success else 1)

    elif args.command == "schema":
        valid = check_schema(
            args.schema,
            disable_log=False,
            quiet_log=args.quiet,
            verbose_log=args.verbose,
            output=args.output,
        )
        sys.exit(0 if valid else 1)

    elif args.command == "query":
        # Validate schema/data args
        if args.data and not args.schema:
            print("❌ Cannot load data without a schema. Please provide --schema.")
            sys.exit(1)

        engine = YaqlEngine()

        # Load initial schema if provided
        if args.schema:
            if not args.quiet:
                print(f"Loading schema from: {args.schema}")
            if engine.load_schema(args.schema):
                if not args.quiet:
                    print("✅ Schema loaded successfully.")
            else:
                print("❌ Failed to load schema.")
                if args.data:
                    sys.exit(1)

        # Load initial data if provided (and schema succeeded)
        if args.data and args.schema:
            if not args.quiet:
                print(f"Loading data from: {args.data}")
            count = engine.load_data(args.data)
            if not args.quiet:
                print(f"✅ Loaded {count} data records.")

        if args.sql:
            try:
                results = engine.execute_sql(args.sql)
                shell = YaqlShell(engine)
                shell._print_results(results)
                sys.exit(0)
            except Exception as e:
                # Error is already logged by engine.execute_sql
                sys.exit(1)
        else:
            # Interactive mode
            shell = YaqlShell(engine)
            try:
                shell.cmdloop()
            except KeyboardInterrupt:
                print("\nInterrupted. Exiting...")
                sys.exit(1)

    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
