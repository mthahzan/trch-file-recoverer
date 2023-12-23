# File Recoverer

This is a tool you can use to recover files from partition images. It is a very simple tool, but it can be useful in some cases where you need to recover files from a partition image.

## Pre-requisites

You must install The Sleuth Kit (TSK) to use this tool. To install it on Ubuntu, run the following command:

```bash
sudo apt-get install sleuthkit
```

To install on other Linux distributions, please refer to the [TSK website](https://www.sleuthkit.org/sleuthkit/download.php). To install on a Mac, you can use [Homebrew](https://brew.sh/):

```bash
brew install sleuthkit
```

## Installation

To install this tool, you can use the following command:

```bash
pip install trch-file-recoverer
```

## Usage

To use this tool, you must first create a partition image. You can do this using the `dd` command. For example, to create an image of the first partition on a disk, you can run the following command:

```bash
dd if=/dev/sda1 of=sda1.img
```

Once you have created the image, you can run the tool as follows:

```bash
file-recoverer sda1.img
```
