"""
My first application
"""

import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW
import asyncio
import subprocess


class JarSigner(toga.App):
    def startup(self):
        """Construct and show the Toga application.

        Usually, you would add your application to a main content box.
        We then create a main window (with a name matching the app), and
        show the main window.
        """
        self.keystore_label = toga.Label("No keyfiles selected...")
        self.android_label = toga.Label("No apkfiles selected...")
        self.select_key = toga.Button(
            "Select Key",
            on_press=self.key_action_open_file_dialog,
        )
        self.android_file = toga.Button(
            "Select APK file",
            on_press=self.android_action_open_file_dialog,
        )
        self.alias_name = toga.TextInput(placeholder="Alias")
        self.password = toga.PasswordInput(placeholder="Password")
        signbtn = toga.Button("Sign")
        main_box = toga.Box(
            children=[
                self.keystore_label,
                self.android_label,
                self.select_key,
                self.android_file,
                self.alias_name,
                self.password,
                signbtn,
            ]
        )

        self.main_window = toga.MainWindow(title=self.formal_name)
        self.main_window.content = main_box
        self.main_window.show()

    async def android_action_open_file_dialog(self, widget):
        try:
            self.androidfile = await self.main_window.dialog(
                toga.OpenFileDialog("Open file with Toga", file_types=["apk", "aab"])
            )
            print(self.androidfile)
            if self.androidfile is not None:
                self.android_label.text = f"File to open: {self.androidfile}"
            else:
                self.android_label.text = "No apkfiles selected..."
        except ValueError:
            self.android_label.text = "Open file dialog was canceled"

    async def key_action_open_file_dialog(self, widget):
        try:
            self.keyfile = await self.main_window.dialog(
                toga.OpenFileDialog("Open file with Toga", file_types=["keystore"])
            )
            print(self.keyfile)
            if self.keyfile is not None:
                self.keystore_label.text = f"File to open: {self.keyfile}"
            else:
                self.keystore_label.text = "No keyfiles selected..."
        except ValueError:
            self.keystore_label.text = "Open file dialog was canceled"

    def sign(self):
        try:
            self.cmd = f"jarsigner -verbose -sigalg SHA1withRSA -digestalg SHA1 -keystore {self.keyfile} {self.android_file} {self.alias_name}"
            self.cmd = self.cmd.split(" ")
            subprocess.run(self.cmd)
            print("ready")
        except:
            print("Fail.")


def main():
    return JarSigner()
