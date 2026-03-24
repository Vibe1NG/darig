import subprocess


def run_cli(args):
    filtered_args = [item for item in args if item is not None]
    # Handle --version separately as it's a top-level flag for darig
    if "--version" in filtered_args:
        result = subprocess.run(["darig", "--version"], capture_output=True, text=True)
    else:
        result = subprocess.run(
            ["darig", "query"] + filtered_args, capture_output=True, text=True
        )
    return result


def test_version_command():
    result = run_cli(["--version"])
    assert result.returncode == 0
    assert "Darig version" in result.stdout
