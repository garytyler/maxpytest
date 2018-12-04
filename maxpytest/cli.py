from __future__ import print_function
import sys
import argparse
import runner


def parse(args):
    parser = argparse.ArgumentParser(
        prog="maxpytest",
        description="""Command line tool for a friendly testing workflow using the
        Pytest framework in 3ds Max""",
        add_help=False,
        epilog="",
    )
    parser.add_argument(
        "-h",
        "--help",
        action="help",
        default=argparse.SUPPRESS,
        help="Show this help message and exit.",
    )
    parser.add_argument(
        "-m",
        "--max",
        dest="runnerarg",
        nargs="?",
        metavar="YEAR|PATH",
        help="""Can be 3ds Max version by year, path to 3dsmax.exe, or path to
        MXSPyCOM.exe. Default is most recent installed version of 3ds Max. If path to
        MXSPyCOM.exe is provided, currently running 3ds Max instance will be closed and
        relaunched, with unsaved work triggering a save prompt. """,
    )
    parser.add_argument("--cwd", nargs="?", help="Override current working directory")
    parser.add_argument(
        "--no-restart",
        dest="restart",
        action="store_false",
        help="""Do not close and relaunch 3ds Max, running tests on load. This option
        only applies if MXSPyCOM is not configured. If MXSPyCOM is configured, this is
        the default behavior. See README for more info.""",
    )
    parser.add_argument(
        "-py",
        "--pytest",
        dest="pytestargs",
        type=str,
        nargs=argparse.REMAINDER,
        help="Pytest options/args",
    )
    return parser.parse_args(args)


def main():
    pargs = parse(sys.argv[1:])
    runner.runtests(
        cwd=pargs.cwd,
        runnerarg=pargs.runnerarg,
        pytestargs=pargs.pytestargs,
        restart=pargs.restart,
    )
