import os
import platform
import site
import subprocess
import sys
import importlib
import time


class OneClick:
    script_dir = os.path.dirname(os.path.abspath(__file__))

    env_path = os.environ.get(
        "INSTALL_ENV_DIR", os.path.join(script_dir, "installer_files", "env")
    )
    app_model_path = os.path.join(script_dir, "model")

    @classmethod
    def configure_runtime_paths(cls):
        install_dir = os.path.join(cls.script_dir, "installer_files")
        temp_dir = os.path.join(install_dir, "tmp")
        hf_home = os.path.join(cls.app_model_path, ".hf_cache")
        hf_hub_cache = os.path.join(hf_home, "hub")
        runtime_env = {
            "HOME": os.path.join(install_dir, "home"),
            "TMP": temp_dir,
            "TEMP": temp_dir,
            "TMPDIR": temp_dir,
            "XDG_CACHE_HOME": os.path.join(install_dir, "xdg-cache"),
            "XDG_CONFIG_HOME": os.path.join(install_dir, "xdg-config"),
            "XDG_DATA_HOME": os.path.join(install_dir, "xdg-data"),
            "XDG_STATE_HOME": os.path.join(install_dir, "xdg-state"),
            "GRADIO_TEMP_DIR": os.path.join(install_dir, "gradio"),
            "STANZA_RESOURCES_DIR": os.path.join(cls.app_model_path, "stanza"),
            "HF_HOME": hf_home,
            "HF_HUB_CACHE": hf_hub_cache,
            "HUGGINGFACE_HUB_CACHE": hf_hub_cache,
            "TRANSFORMERS_CACHE": hf_hub_cache,
            "MODELSCOPE_CACHE": os.path.join(cls.app_model_path, ".modelscope_cache"),
            "UV_CACHE_DIR": os.path.join(install_dir, "uv-cache"),
            "PIP_CACHE_DIR": os.path.join(install_dir, "uv-cache"),
            "UV_PYTHON_INSTALL_DIR": os.path.join(install_dir, "uv-python"),
            "MPLCONFIGDIR": os.path.join(install_dir, "matplotlib"),
            "TORCH_HOME": os.path.join(cls.app_model_path, ".torch"),
            "TORCH_EXTENSIONS_DIR": os.path.join(
                cls.app_model_path, ".torch_extensions"
            ),
            "CACHED_PATH_CACHE_DIR": os.path.join(cls.app_model_path, ".cached_path"),
            "NUMBA_CACHE_DIR": os.path.join(install_dir, "numba-cache"),
            "TRITON_CACHE_DIR": os.path.join(cls.app_model_path, ".triton"),
            "CUDA_CACHE_PATH": os.path.join(
                cls.app_model_path, ".nv", "ComputeCache"
            ),
        }
        os.environ.update(runtime_env)
        for path in set(runtime_env.values()):
            if os.path.isabs(path) or path.startswith(cls.script_dir):
                os.makedirs(path, exist_ok=True)

    print("Info: Start 1-click ...")

    @classmethod
    def is_linux(cls):
        return sys.platform.startswith("linux")

    @classmethod
    def is_x86_64(cls):
        return platform.machine() == "x86_64"

    @classmethod
    def torch_version(cls):
        site_packages_path = None
        for sitedir in site.getsitepackages():
            if "site-packages" in sitedir and cls.env_path in sitedir:
                site_packages_path = sitedir
                break

        if site_packages_path:
            torch_version_file = (
                open(os.path.join(site_packages_path, "torch", "version.py"))
                .read()
                .splitlines()
            )
            torver = (
                [line for line in torch_version_file if line.startswith("__version__")][
                    0
                ]
                .split("__version__ = ")[1]
                .strip("'")
            )
        else:
            from torch import __version__ as torver

        return torver

    @classmethod
    def update_pytorch(cls):
        cls.oc_print_big_message("Checking for PyTorch updates")
        torver = cls.torch_version()
        is_cuda = "+cu" in torver if torver else False

        if is_cuda:
            install_pytorch = "uv pip install --upgrade torch==2.5.1+cu124 torchvision==0.20.1+cu124 torchaudio==2.5.1+cu124 --extra-index-url https://download.pytorch.org/whl/cu124"
        else:
            install_pytorch = "uv pip install --upgrade torch==2.5.1 torchvision==0.20.1 torchaudio==2.5.1"

        cls.oc_run_cmd(f"{install_pytorch}", assert_success=True, environment=True)

    @classmethod
    def oc_is_installed(cls):
        # Check if key packages are installed to verify installation is complete
        site_packages_path = None
        for sitedir in site.getsitepackages():
            if "site-packages" in sitedir and cls.env_path in sitedir:
                site_packages_path = sitedir
                break

        if site_packages_path:
            # Check if at least torch and a couple other key packages exist
            torch_exists = os.path.isfile(
                os.path.join(site_packages_path, "torch", "__init__.py")
            )
            json5_exists = os.path.isfile(
                os.path.join(site_packages_path, "json5", "__init__.py")
            )
            gradio_exists = os.path.isfile(
                os.path.join(site_packages_path, "gradio", "__init__.py")
            )

            # If packages don't exist, definitely not installed
            if not (torch_exists and json5_exists and gradio_exists):
                return False

            # Additional check: Try to actually import torch to verify it works
            # This catches cases where torch is installed but broken
            try:
                test_cmd = "python -c \"import sys; sys.path.insert(0, ''); import torch; assert hasattr(torch, '_C') or hasattr(torch, '__version__')\""
                return cls.oc_run_cmd(test_cmd, environment=True, capture_output=True)
            except:
                return False
        else:
            return False

    @classmethod
    def oc_check_env(cls):
        os.chdir(cls.script_dir)
        cls.configure_runtime_paths()
        # Verify a virtual environment is active
        if not os.environ.get("VIRTUAL_ENV"):
            print("Error: No virtual environment active. Run start.sh first. Exiting...")
            sys.exit(1)

        # Check if we're in a PyTorch source directory (can cause import issues)
        current_dir = os.getcwd()
        torch_source_dir = os.path.join(current_dir, "torch")
        if os.path.exists(torch_source_dir) and os.path.exists(
            os.path.join(torch_source_dir, "_C")
        ):
            print("=" * 70)
            print("WARNING: PyTorch source directory detected in current path!")
            print(f"Current directory: {current_dir}")
            print(f"Found: {torch_source_dir}")
            print("This can cause PyTorch import errors.")
            print("=" * 70)
            print("Solution options:")
            print("1. Remove or rename the 'torch' directory in the current path")
            print("2. Run the script from a different directory")
            print("=" * 70)

        # Ensure PYTHONPATH doesn't interfere with installed packages
        # Clear any torch-related paths that might cause conflicts
        pythonpath = os.environ.get("PYTHONPATH", "")
        if pythonpath:
            paths = pythonpath.split(os.pathsep)
            filtered_paths = [
                p for p in paths if not os.path.exists(os.path.join(p, "torch", "_C"))
            ]
            if len(filtered_paths) != len(paths):
                print(
                    "Warning: Removed PyTorch source paths from PYTHONPATH to avoid conflicts"
                )
                os.environ["PYTHONPATH"] = (
                    os.pathsep.join(filtered_paths) if filtered_paths else ""
                )

    @classmethod
    def clear_cache(cls):
        print("clear_cache?? no...")
        # uv cache prune

    @classmethod
    def oc_print_big_message(cls, message):
        message = message.strip()
        lines = message.split("\n")
        print("\n\n*******************************************************************")
        for line in lines:
            print("*", line)

        print("*******************************************************************\n\n")

    @classmethod
    def oc_run_cmd(
        cls,
        cmd,
        assert_success=False,
        environment=False,
        capture_output=False,
        env=None,
    ):
        # venv is already activated by start.sh; environment flag is a no-op kept for compat
        cls.configure_runtime_paths()
        process_env = os.environ.copy()
        if env:
            process_env.update(env)
        try:
            result = subprocess.run(
                cmd,
                shell=True,
                capture_output=capture_output,
                env=process_env,
                cwd=cls.script_dir,
            )

            if assert_success and result.returncode != 0:
                print(
                    f"Command '{cmd}' failed with exit status code '{str(result.returncode)}'.\n\nExiting now.\nTry running the start/update script again."
                )
                sys.exit(1)

            return result.returncode == 0
        except Exception as e:
            print(f"Command: '{cmd}' failed with {e}")
            return False

    @classmethod
    def get_user_choice(cls, question, options_dict):
        print()
        print(question)
        print()

        for key, value in options_dict.items():
            print(f"{key}) {value}")

        print()

        choice = input("Input> ").upper()
        while choice not in options_dict.keys():
            print("Invalid choice. Please try again.")
            choice = input("Input> ").upper()

        return choice

    @classmethod
    def oc_install_webui(cls, app_name: str, is_update=False):
        # Ask the user for the GPU vendor
        if "GPU_CHOICE" in os.environ:
            choice = os.environ["GPU_CHOICE"].upper()
            cls.oc_print_big_message(
                f'Selected GPU choice "{choice}" based on the GPU_CHOICE environment variable.'
            )
        else:
            choice = cls.get_user_choice(
                "What is your GPU?",
                {
                    "G": "NVIDIA GTX, RTX, Tesla",
                    "C": "CPU (I want to run models in CPU mode)",
                },
            )

        gpu_choice_to_name = {
            "G": "NVIDIA",
            "C": "CPU",
        }

        selected_gpu = gpu_choice_to_name[choice]

        # Install build tools (ninja) via uv pip
        cls.install_build_tools()

        if is_update:
            cls.update_pytorch()

        # Install the webui requirements
        cls.install_requirements(app_name, is_update, selected_gpu)

        cls.clear_cache()

    @classmethod
    def check_package_installed(cls, package_name):
        try:
            importlib.import_module(package_name)
            return True
        except ImportError:
            return False

    @classmethod
    def install_requirements(cls, app_name, is_update=False, selected_gpu="NVIDIA"):
        requirements_file = (
            f"requirements-{app_name}-gpu.txt"
            if selected_gpu == "NVIDIA"
            else f"requirements-{app_name}-cpu.txt"
        )
        cls.oc_print_big_message(
            f"Install/Update webui requirements from file: {requirements_file}"
        )

        cmd = f"uv pip install -r {requirements_file}"
        cmd = cmd + " --upgrade" if is_update else cmd
        cls.oc_run_cmd(cmd, assert_success=True, environment=True)

        # Install PyTorch via pip for CPU builds
        if selected_gpu == "CPU":
            if not cls.check_package_installed("torch"):
                cls.oc_print_big_message("Installing PyTorch via uv pip")
                cls.oc_run_cmd(
                    "uv pip install torch==2.5.1 torchvision==0.20.1 torchaudio==2.5.1",
                    assert_success=True,
                    environment=True,
                )

    @classmethod
    def install_build_tools(cls):
        cls.oc_print_big_message("Installing build tools (ninja)")
        max_retries = 3
        retry_count = 0
        success = False
        while retry_count < max_retries and not success:
            if retry_count > 0:
                print(
                    f"Retrying ninja installation (attempt {retry_count + 1}/{max_retries})..."
                )
                time.sleep(5)
            success = cls.oc_run_cmd(
                "uv pip install ninja", assert_success=False, environment=True
            )
            retry_count += 1

        if not success:
            print("WARNING: Failed to install ninja. Continuing anyway...")

    @classmethod
    def launch_webui(cls, app_file):
        print("Start the program...")
        cls.oc_run_cmd(f"python {app_file}", environment=True)
