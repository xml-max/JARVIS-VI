import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import os
import shutil
import requests
import subprocess

class SetupWizard:
    def __init__(self, root):
        self.root = root
        self.root.title("Setup Wizard")
        self.root.geometry("600x400")

        self.current_step = 0
        self.setup_steps = [
            self.step_download_exe,
            self.step_copy_to_system32,
            self.step_download_framework,
            self.step_install_framework,
            self.step_install_additional_components,
            self.step_activate_jarvis,
            self.step_finish
        ]

        self.create_widgets()

    def create_widgets(self):
        self.frame = ttk.Frame(self.root)
        self.frame.pack(pady=20)

        self.label = ttk.Label(self.frame, text="Welcome to the Setup Wizard!", font=("Helvetica", 16))
        self.label.pack(pady=20)

        self.button_next = ttk.Button(self.frame, text="Next", command=self.next_step)
        self.button_next.pack(pady=20)

    def next_step(self):
        self.current_step += 1
        if self.current_step < len(self.setup_steps):
            self.setup_steps[self.current_step]()
        else:
            self.finish_installation()

    def step_download_exe(self):
        self.clear_frame()

        self.label = ttk.Label(self.frame, text="Step 1: Downloading Executable", font=("Helvetica", 14))
        self.label.pack(pady=20)

        # Replace with your executable file URL
        exe_url = "https://example.com/path/to/your/executable.exe"

        # Replace with your desired download directory
        download_dir = os.path.join(os.path.expanduser('~'), 'Downloads')

        self.progress_label = ttk.Label(self.frame, text=f"Downloading executable from:\n{exe_url}")
        self.progress_label.pack(pady=20)

        try:
            # Download the file with requests (streaming)
            filename = os.path.basename(exe_url)
            destination_file = os.path.join(download_dir, filename)

            with requests.get(exe_url, stream=True) as r:
                r.raise_for_status()
                total_size = int(r.headers.get('content-length', 0))
                chunk_size = 1024  # Adjust chunk size as needed

                self.progress_bar = ttk.Progressbar(self.frame, orient=tk.HORIZONTAL, length=300, mode='determinate')
                self.progress_bar.pack(pady=20)

                downloaded_size = 0
                with open(destination_file, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=chunk_size):
                        if chunk:
                            f.write(chunk)
                            f.flush()  # Ensure data is written to disk
                            downloaded_size += len(chunk)

                            # Update progress bar
                            self.progress_bar["value"] = (downloaded_size / total_size) * 100
                            self.progress_bar.update()

                self.progress_label.config(text=f"Executable downloaded to:\n{destination_file}")
                self.button_next.config(text="Next")
        except Exception as e:
            self.progress_label.config(text=f"Error downloading executable:\n{str(e)}")
            self.button_next.config(state=tk.DISABLED)
            messagebox.showerror("Download Error", f"Error downloading executable:\n{str(e)}")

        # Display warning about file size
        if total_size > 500 * 1024 * 1024:  # 500 MB
            messagebox.showwarning("File Size Warning", "This file is large. It may take a while to download.")

    def step_copy_to_system32(self):
        self.clear_frame()

        self.label = ttk.Label(self.frame, text="Step 2: Copying to System32 Directory", font=("Helvetica", 14))
        self.label.pack(pady=20)

        try:
            # Replace with actual destination directory for System32
            system32_dir = os.path.join(os.environ['SystemRoot'], 'System32')

            # Replace with downloaded executable path
            source_file = os.path.join(os.path.expanduser('~'), 'Downloads', 'executable.exe')

            # Copy the file to System32 (requires admin rights)
            shutil.copy2(source_file, system32_dir)

            self.progress_label = ttk.Label(self.frame, text=f"Executable copied to:\n{system32_dir}")
            self.progress_label.pack(pady=20)

            self.button_next.config(text="Next")
        except Exception as e:
            self.progress_label.config(text=f"Error copying executable:\n{str(e)}")
            self.button_next.config(state=tk.DISABLED)
            messagebox.showerror("Copy Error", f"Error copying executable:\n{str(e)}")

    def step_download_framework(self):
        self.clear_frame()

        self.label = ttk.Label(self.frame, text="Step 3: Downloading Framework Installer", font=("Helvetica", 14))
        self.label.pack(pady=20)

        # Replace with your framework installer URL
        framework_url = "https://example.com/path/to/your/framework_installer.exe"

        # Replace with your desired download directory
        download_dir = os.path.join(os.path.expanduser('~'), 'Downloads')

        self.progress_label = ttk.Label(self.frame, text=f"Downloading framework installer from:\n{framework_url}")
        self.progress_label.pack(pady=20)

        try:
            # Download the file with requests (streaming)
            filename = os.path.basename(framework_url)
            destination_file = os.path.join(download_dir, filename)

            with requests.get(framework_url, stream=True) as r:
                r.raise_for_status()
                total_size = int(r.headers.get('content-length', 0))
                chunk_size = 1024  # Adjust chunk size as needed

                self.progress_bar = ttk.Progressbar(self.frame, orient=tk.HORIZONTAL, length=300, mode='determinate')
                self.progress_bar.pack(pady=20)

                downloaded_size = 0
                with open(destination_file, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=chunk_size):
                        if chunk:
                            f.write(chunk)
                            f.flush()  # Ensure data is written to disk
                            downloaded_size += len(chunk)

                            # Update progress bar
                            self.progress_bar["value"] = (downloaded_size / total_size) * 100
                            self.progress_bar.update()

                self.progress_label.config(text=f"Framework installer downloaded to:\n{destination_file}")
                self.button_next.config(text="Next")
        except Exception as e:
            self.progress_label.config(text=f"Error downloading framework installer:\n{str(e)}")
            self.button_next.config(state=tk.DISABLED)
            messagebox.showerror("Download Error", f"Error downloading framework installer:\n{str(e)}")

        # Display warning about file size
        if total_size > 500 * 1024 * 1024:  # 500 MB
            messagebox.showwarning("File Size Warning", "This file is large. It may take a while to download.")

    def step_install_framework(self):
        self.clear_frame()

        self.label = ttk.Label(self.frame, text="Step 4: Installing Framework", font=("Helvetica", 14))
        self.label.pack(pady=20)

        try:
            # Replace with downloaded framework installer path
            framework_installer = os.path.join(os.path.expanduser('~'), 'Downloads', 'framework_installer.exe')

            # Example: Run framework installer (modify as per your installer requirements)
            subprocess.run([framework_installer, '/silent', '/norestart'])

            # Optional: Check if framework is installed (example command)
            framework_installed = os.path.exists("check_framework_installed.exe")

            if framework_installed:
                self.progress_label = ttk.Label(self.frame, text="Framework installed successfully!")
                self.progress_label.pack(pady=20)
                self.button_next.config(text="Next")
            else:
                messagebox.showerror("Installation Error", "Framework installation failed.")
                self.button_next.config(state=tk.DISABLED)
        except Exception as e:
            self.progress_label.config(text=f"Error installing framework:\n{str(e)}")
            self.button_next.config(state=tk.DISABLED)
            messagebox.showerror("Installation Error", f"Error installing framework:\n{str(e)}")

    def step_install_additional_components(self):
        self.clear_frame()

        self.label = ttk.Label(self.frame, text="Step 5: Installing Additional Components", font=("Helvetica", 14))
        self.label.pack(pady=20)

        try:
            # Replace with command to install additional components
            subprocess.run(["install_additional_components.exe", "/silent"])

            self.progress_label = ttk.Label(self.frame, text="Additional components installed successfully!")
            self.progress_label.pack(pady=20)
            self.button_next.config(text="Next")
        except Exception as e:
            self.progress_label.config(text=f"Error installing additional components:\n{str(e)}")
            self.button_next.config(state=tk.DISABLED)
            messagebox.showerror("Installation Error", f"Error installing additional components:\n{str(e)}")

    def step_activate_jarvis(self):
        self.clear_frame()

        self.label = ttk.Label(self.frame, text="Step 6: Activating JARVIS", font=("Helvetica", 14))
        self.label.pack(pady=20)

        try:
            # Replace with command to activate JARVIS
            os.system("jarvis")

            self.progress_label = ttk.Label(self.frame, text="JARVIS activated successfully!")
            self.progress_label.pack(pady=20)
            self.button_next.config(text="Next")
        except Exception as e:
            self.progress_label.config(text=f"Error activating JARVIS:\n{str(e)}")
            self.button_next.config(state=tk.DISABLED)
            messagebox.showerror("Activation Error", f"Error activating JARVIS:\n{str(e)}")

    def step_finish(self):
        self.clear_frame()

        self.label = ttk.Label(self.frame, text="Setup Complete!", font=("Helvetica", 16))
        self.label.pack(pady=20)

        self.button_next.config(text="Finish", command=self.finish_installation)

    def finish_installation(self):
        messagebox.showinfo("Installation Complete", "Installation finished successfully!")
        self.root.destroy()

    def clear_frame(self):
        for widget in self.frame.winfo_children():
            widget.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    setup_wizard = SetupWizard(root)
    root.mainloop()
