import subprocess
import sys
import argparse

def run_migrations(command="upgrade", revision="head", message=None, autogenerate=False):
    cmd = ["alembic", "-c", "src/alembic.ini", command]
    
    if command == "revision":
        if message:
            cmd.extend(["-m", message])
        if autogenerate:
            cmd.append("--autogenerate")
    elif command in ["upgrade", "downgrade"]:
        cmd.append(revision)
        
    try:
        subprocess.run(cmd, check=True)
        print(f"Successfully ran: {' '.join(cmd)}")
    except subprocess.CalledProcessError as e:
        print(f"Error running migration: {e}")
        sys.exit(1)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Alembic migrations helper.")
    subparsers = parser.add_subparsers(dest="action", required=True)

    # Upgrade
    parser_upgrade = subparsers.add_parser("upgrade", help="Upgrade to a later version")
    parser_upgrade.add_argument("revision", nargs="?", default="head", help="Revision to upgrade to (default: head)")

    # Downgrade
    parser_downgrade = subparsers.add_parser("downgrade", help="Revert to a previous version")
    parser_downgrade.add_argument("revision", help="Revision to downgrade to")

    # Revision (create new migration)
    parser_revision = subparsers.add_parser("revision", help="Create a new migration file")
    parser_revision.add_argument("-m", "--message", required=True, help="Message string to use with 'revision'")
    parser_revision.add_argument("--autogenerate", action="store_true", help="Populate revision script with candidate migration operations")

    args = parser.parse_args()

    if args.action == "upgrade":
        run_migrations("upgrade", revision=args.revision)
    elif args.action == "downgrade":
        run_migrations("downgrade", revision=args.revision)
    elif args.action == "revision":
        run_migrations("revision", message=args.message, autogenerate=args.autogenerate)
