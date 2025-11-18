#!/usr/bin/env python3
"""
Version Matrix Test Framework for logic2-automation package.

Tests the package across multiple combinations of Python, protobuf, and gRPC versions

"""

import subprocess
import sys
import tempfile
import json
import csv
import logging
from pathlib import Path
from datetime import datetime
from itertools import product
from typing import Dict, List, Any, Optional, Tuple, Union
from dataclasses import dataclass, asdict
import argparse


# -----------------------------------------
#       Version Configuration
# -----------------------------------------

LATEST_VERSION_STR = 'latest'

PYTHON_VERSIONS = [
    "3.7",
    "3.8",
    "3.9",
    "3.10",
    "3.11",
    "3.12",
    "3.13",
]

PROTOBUF_VERSIONS = [
    "3.20.0", 
    "4.21.0",
    "4.23.4",
    "4.25.0",
    "5.27.0",
    LATEST_VERSION_STR,
]

GRPCIO_VERSIONS = [
    "1.49.0",
    "1.56.0",
    "1.60.0",
    "1.65.0",
    LATEST_VERSION_STR,
]


# -----------------------------------------
#          Data Structures
# -----------------------------------------

@dataclass
class TestResult:
    """Result of testing a specific version combination."""
    python_version: str
    protobuf_version: str
    grpcio_version: str
    success: bool
    skipped: bool
    error: Optional[str]
    step: Optional[str]
    timestamp: str
    duration_seconds: Optional[float]
    log_file: Optional[str]


# -----------------------------------------
#          Test Runner
# -----------------------------------------

def setup_test_logger(log_file: Path, test_name: str) -> logging.Logger:
    """
    Create a logger for a specific test that writes to a file.

    """
    logger = logging.getLogger(test_name)
    logger.setLevel(logging.DEBUG)
    logger.handlers.clear()  # Remove any existing handlers

    # Create file handler
    file_handler = logging.FileHandler(log_file, mode='w')
    file_handler.setLevel(logging.DEBUG)

    # Create formatter
    formatter = logging.Formatter(
        '%(asctime)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    return logger


def run_subprocess(
    cmd: Union[List[str], str],
    timeout: Optional[float] = None,
    logger: Optional[logging.Logger] = None,
    **kwargs: Any
) -> subprocess.CompletedProcess:
    """
    Run a subprocess command and log output.

    Args:
        cmd: Command to run (list or string)
        timeout: Optional timeout in seconds
        logger: Optional logger to write command and output to
        **kwargs: Additional arguments to pass to subprocess.run

    Returns:
        subprocess.CompletedProcess: Result of the command
    """
    cmd_str = ' '.join(cmd) if isinstance(cmd, list) else cmd

    if logger:
        logger.info(f"Running command: {cmd_str}")

    # Always capture output so we can log it
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout, **kwargs)

    # Log the output if logger is provided
    if logger:
        if result.stdout:
            logger.info(f"STDOUT:\n{result.stdout}")
        if result.stderr:
            logger.info(f"STDERR:\n{result.stderr}")
        logger.info(f"Return code: {result.returncode}")

    return result


def test_version_combination(
    python_version: str,
    protobuf_version: str,
    grpcio_version: str,
    logs_dir: Path,
    allow_source_builds: bool = False
) -> TestResult:
    """
    Test a specific combination of Python, protobuf, and gRPC versions.

    Args:
        python_version: Python version (e.g., "3.11")
        protobuf_version: Protobuf version (e.g., "4.23.4")
        grpcio_version: gRPC version (e.g., "1.56.0")
        logs_dir: Directory to store log files
        allow_source_builds: If True, allow building from source; if False, only use binary wheels

    Returns:
        TestResult: Test results with status and details
    """
    start_time = datetime.now()
    timestamp = start_time.isoformat()

    # Setup logging for this specific test
    test_name = f"py{python_version}_pb{protobuf_version}_grpc{grpcio_version}"
    log_file = logs_dir / f"{test_name}.log"
    logger = setup_test_logger(log_file, test_name)

    logger.info(f"Starting test for Python {python_version}, protobuf {protobuf_version}, gRPC {grpcio_version}")
    logger.info(f"Allow source builds: {allow_source_builds}")

    # Create temporary directory for virtual environment
    with tempfile.TemporaryDirectory(prefix=f"uv_test_py{python_version}_") as temp_dir:
        venv_path = Path(temp_dir) / "test_env"

        try:
            # Create virtual environment with specific Python version using uv
            logger.info(f"Creating virtual environment with Python {python_version}")

            cmd = ["uv", "venv", str(venv_path), "--python", python_version]
            proc_result = run_subprocess(cmd, timeout=120, logger=logger)

            if proc_result.returncode != 0:
                logger.error(f"Failed to create virtual environment")
                return TestResult(
                    python_version=python_version,
                    protobuf_version=protobuf_version,
                    grpcio_version=grpcio_version,
                    success=False,
                    skipped=False,
                    error=f"Failed to create uv venv: {proc_result.stderr if hasattr(proc_result, 'stderr') else 'Unknown error'}",
                    step="venv_creation",
                    timestamp=timestamp,
                    duration_seconds=(datetime.now() - start_time).total_seconds(),
                    log_file=str(log_file)
                )

            # Determine python executable in venv
            if sys.platform == "win32":
                python_exe = venv_path / "Scripts" / "python.exe"
                uv_exe = "uv"
            else:
                python_exe = venv_path / "bin" / "python"
                uv_exe = "uv"

            # Install specific versions of dependencies using uv pip
            logger.info("Installing dependencies")
            packages = [
                "protobuf" if protobuf_version == LATEST_VERSION_STR else f"protobuf=={protobuf_version}",
                "grpcio" if grpcio_version == LATEST_VERSION_STR else f"grpcio=={grpcio_version}",
            ]

            for package in packages:
                logger.info(f"Installing package: {package}")

                cmd = ["uv", "pip", "install", "--python", str(python_exe)]

                # Add --only-binary flag if source builds are not allowed
                # Note(Ryan) 2025-11-17 After seeing build failures on linux, unrelated to what this is testing,
                # source builds are disabled by-default to avoid unrelated failures.
                if not allow_source_builds:
                    cmd.extend(["--only-binary", ":all:"])

                cmd.append(package)
                proc_result = run_subprocess(cmd, timeout=300, logger=logger)

                if proc_result.returncode != 0:
                    # Check if failure is due to no binary wheel available or version incompatibility
                    stderr = proc_result.stderr if hasattr(proc_result, 'stderr') else ''
                    if not allow_source_builds and ('no usable wheels' in stderr.lower() or
                                                     'building from source is disabled' in stderr.lower() or
                                                     'no matching distribution' in stderr.lower() or
                                                     'could not find' in stderr.lower() or
                                                     'no binary' in stderr.lower() or
                                                     'does not satisfy python' in stderr.lower()):
                        # Determine the reason
                        if 'does not satisfy python' in stderr.lower():
                            error_msg = f"Python version incompatibility for {package}"
                        else:
                            error_msg = f"No binary wheel available for {package}"

                        logger.warning(f"Skipping test: {error_msg}")
                        return TestResult(
                            python_version=python_version,
                            protobuf_version=protobuf_version,
                            grpcio_version=grpcio_version,
                            success=False,
                            skipped=True,
                            error=error_msg,
                            step="dependency_installation",
                            timestamp=timestamp,
                            duration_seconds=(datetime.now() - start_time).total_seconds(),
                            log_file=str(log_file)
                        )

                    logger.error(f"Failed to install {package}")
                    return TestResult(
                        python_version=python_version,
                        protobuf_version=protobuf_version,
                        grpcio_version=grpcio_version,
                        success=False,
                        skipped=False,
                        error=f"Failed to install {package}: {stderr or 'Unknown error'}",
                        step="dependency_installation",
                        timestamp=timestamp,
                        duration_seconds=(datetime.now() - start_time).total_seconds(),
                        log_file=str(log_file)
                    )

            # Install logic2-automation from local source
            logger.info("Installing logic2-automation from local source")

            package_root = Path(__file__).parent
            python_dir = package_root / "python"

            cmd = ["uv", "pip", "install", "--python", str(python_exe), str(python_dir)]
            proc_result = run_subprocess(cmd, timeout=300, logger=logger)

            if proc_result.returncode != 0:
                logger.error("Failed to install logic2-automation")
                return TestResult(
                    python_version=python_version,
                    protobuf_version=protobuf_version,
                    grpcio_version=grpcio_version,
                    success=False,
                    skipped=False,
                    error=f"Failed to install logic2-automation: {proc_result.stderr if hasattr(proc_result, 'stderr') else 'Unknown error'}",
                    step="package_installation",
                    timestamp=timestamp,
                    duration_seconds=(datetime.now() - start_time).total_seconds(),
                    log_file=str(log_file)
                )

            # Log Python version
            logger.info("Checking Python version")
            cmd = [str(python_exe), "--version"]
            proc_result = run_subprocess(cmd, timeout=30, logger=logger)

            # Log all installed packages
            logger.info("Listing all installed packages")
            cmd = ["uv", "pip", "list", "--python", str(python_exe)]
            proc_result = run_subprocess(cmd, timeout=60, logger=logger)

            # Test import
            logger.info("Testing import of saleae.automation")

            # Test script - extensible for future tests
            test_script = """
try:
    from saleae import automation
    print("SUCCESS: Import successful")
except Exception as e:
    print(f"ERROR: Import failed: {e}")
    import traceback
    traceback.print_exc()
    exit(1)
"""

            cmd = [str(python_exe), "-c", test_script]
            proc_result = run_subprocess(cmd, timeout=60, logger=logger)

            if proc_result.returncode != 0:
                logger.error("Import test failed")
                return TestResult(
                    python_version=python_version,
                    protobuf_version=protobuf_version,
                    grpcio_version=grpcio_version,
                    success=False,
                    skipped=False,
                    error=f"Import test failed: {proc_result.stderr if hasattr(proc_result, 'stderr') else ''}\n{proc_result.stdout if hasattr(proc_result, 'stdout') else ''}",
                    step="import_test",
                    timestamp=timestamp,
                    duration_seconds=(datetime.now() - start_time).total_seconds(),
                    log_file=str(log_file)
                )

            # Success!
            logger.info("Test completed successfully")
            return TestResult(
                python_version=python_version,
                protobuf_version=protobuf_version,
                grpcio_version=grpcio_version,
                success=True,
                skipped=False,
                error=None,
                step="completed",
                timestamp=timestamp,
                duration_seconds=(datetime.now() - start_time).total_seconds(),
                log_file=str(log_file)
            )

        except subprocess.TimeoutExpired as e:
            logger.error(f"Test timed out: {e.cmd}")
            return TestResult(
                python_version=python_version,
                protobuf_version=protobuf_version,
                grpcio_version=grpcio_version,
                success=False,
                skipped=False,
                error=f"Test timed out during {e.cmd}",
                step="timeout",
                timestamp=timestamp,
                duration_seconds=(datetime.now() - start_time).total_seconds(),
                log_file=str(log_file)
            )
        except Exception as e:
            logger.error(f"Unexpected error: {e}")
            return TestResult(
                python_version=python_version,
                protobuf_version=protobuf_version,
                grpcio_version=grpcio_version,
                success=False,
                skipped=False,
                error=f"Unexpected error: {e}",
                step="unexpected_error",
                timestamp=timestamp,
                duration_seconds=(datetime.now() - start_time).total_seconds(),
                log_file=str(log_file)
            )


def generate_test_matrix() -> List[Tuple[str, str, str]]:
    """
    Generate all combinations of Python, protobuf, and gRPC versions to test.

    Returns:
        List of tuples: (python_version, protobuf_version, grpcio_version)
    """
    return list(product(PYTHON_VERSIONS, PROTOBUF_VERSIONS, GRPCIO_VERSIONS))


def print_results_summary(results: List[TestResult]) -> None:
    """Print a summary table of test results to console."""
    print("\n" + "=" * 80)
    print("TEST RESULTS SUMMARY")
    print("=" * 80)

    passed = sum(1 for r in results if r.success)
    skipped = sum(1 for r in results if r.skipped)
    failed = len(results) - passed - skipped

    print(f"\nTotal tests: {len(results)}")
    print(f"Passed: {passed}")
    print(f"Failed: {failed}")
    print(f"Skipped: {skipped} (no binary wheel available)")

    if failed > 0:
        print(f"\n{'='*80}")
        print("FAILED TESTS")
        print(f"{'='*80}")
        print(f"{'Python':<8} {'Protobuf':<10} {'gRPC':<10} {'Step':<20} {'Error'}")
        print("-" * 80)

        for r in results:
            if not r.success and not r.skipped:
                error_preview = (r.error or "Unknown")[:40]
                print(f"{r.python_version:<8} {r.protobuf_version:<10} {r.grpcio_version:<10} {r.step:<20} {error_preview}")

    if skipped > 0:
        print(f"\n{'='*80}")
        print("SKIPPED TESTS (No binary wheel available)")
        print(f"{'='*80}")
        print(f"{'Python':<8} {'Protobuf':<10} {'gRPC':<10}")
        print("-" * 80)

        for r in results:
            if r.skipped:
                print(f"{r.python_version:<8} {r.protobuf_version:<10} {r.grpcio_version:<10}")

    print(f"\n{'='*80}")


def main() -> int:
    """Run the version matrix tests."""
    parser = argparse.ArgumentParser(
        description="Test logic2-automation across multiple Python/protobuf/gRPC versions"
    )
    parser.add_argument(
        "--limit", "-l",
        type=int,
        help="Limit the number of test combinations to run (for quick testing)"
    )
    parser.add_argument(
        "--output-dir", "-o",
        type=Path,
        default=Path("."),
        help="Directory to save result files (default: current directory)"
    )
    parser.add_argument(
        "--allow-source-builds",
        action="store_true",
        help="Allow building packages from source (default: only use binary wheels)"
    )

    args = parser.parse_args()

    # Create timestamped logs directory
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    logs_dir = Path("logs") / f"test_run_{timestamp}"
    logs_dir.mkdir(parents=True, exist_ok=True)

    # Generate test matrix
    test_matrix = generate_test_matrix()

    if args.limit:
        test_matrix = test_matrix[:args.limit]

    print("=" * 80)
    print("VERSION MATRIX TEST")
    print("=" * 80)
    print(f"Logs directory: {logs_dir.absolute()}")
    print(f"\nPython versions: {', '.join(PYTHON_VERSIONS)}")
    print(f"Protobuf versions: {', '.join(PROTOBUF_VERSIONS)}")
    print(f"gRPC versions: {', '.join(GRPCIO_VERSIONS)}")
    print(f"\nBinary wheels only: {not args.allow_source_builds}")
    print(f"Total combinations to test: {len(test_matrix)}")

    if args.limit:
        print(f"(Limited to first {args.limit} combinations)")

    print("\n" + "=" * 80)
    print("RUNNING TESTS")
    print("=" * 80)

    results: List[TestResult] = []

    for i, (py_ver, pb_ver, grpc_ver) in enumerate(test_matrix, 1):
        print(f"\n[{i}/{len(test_matrix)}] Testing: Python {py_ver}, protobuf {pb_ver}, gRPC {grpc_ver}")

        result = test_version_combination(
            py_ver, pb_ver, grpc_ver,
            logs_dir=logs_dir,
            allow_source_builds=args.allow_source_builds
        )
        results.append(result)

        if result.success:
            status = "✓ PASS"
        elif result.skipped:
            status = "○ SKIP"
        else:
            status = "✗ FAIL"

        print(f"  {status} ({result.duration_seconds:.1f}s)")

        if not result.success and not result.skipped:
            assert(result.error is not None)
            print(f"  Error: {result.error[:100]}")

    # Generate output files
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_dir = args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    # Print summary
    print_results_summary(results)

    # Print logs information
    print("\n" + "=" * 80)
    print(f"Detailed logs available in: {logs_dir.absolute()}")
    print("=" * 80)

    # Exit with appropriate code (only count actual failures, not skipped tests)
    failed_count = sum(1 for r in results if not r.success and not r.skipped)
    return 0 if failed_count == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
