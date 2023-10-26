import argparse
import subprocess

print("[+] Welcome! Your script will be converted to output format\n\n")

parser = argparse.ArgumentParser(description="Print a string")
parser.add_argument('input_string', help='The string to be printed')

args = parser.parse_args()

copyCommand = "cp " + args.input_string + " ./output/code.py"


try:
  output = subprocess.check_output(copyCommand, shell=True, text=True)

  print(output)
  print("[+] Done! your file is in the output folder")
except subprocess.CalledProcessError as e:
  print(f"Error: {e}")
  