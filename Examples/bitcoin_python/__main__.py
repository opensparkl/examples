"""
Copyright (c) 2018 SPARKL Limited. All Rights Reserved.
Author <miklos@sparkl.com> Miklos Duma

Command-line entry point for the Cryptocurrency widget.

Supports Python3 only.
"""

from interface import CryptoGUI


def main():
    """
    Creates an instance of the bitcoin widget
    and starts it.
    """
    root = CryptoGUI()
    root.mainloop()


main()
