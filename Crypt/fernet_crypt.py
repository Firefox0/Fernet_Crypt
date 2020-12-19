import argparse
import crypt

def main():
    parser = argparse.ArgumentParser()
    subparser = parser.add_subparsers(dest="command")
    encrypt_parser = subparser.add_parser("encrypt", help="encrypt a single file or all files" +
                                                          " at directory including all sub directories")
    encrypt_parser.add_argument("-fp", "--file_path", help="unencrypted file path", required=True)
    encrypt_parser.add_argument("-kp", "--key_path", help="fernet key location", required=True)
    encrypt_parser.add_argument("-r", "--remove", action="store_true", help="remove original file")
    decrypt_parser = subparser.add_parser("decrypt", help="decrypt a single file or all files" +
                                                          " at directory including all sub directories")
    decrypt_parser.add_argument("-fp", "--file_path", help="encrypted file path", required=True)
    decrypt_parser.add_argument("-kp", "--key_path", help="fernet key location", required=True)
    decrypt_parser.add_argument("-p", "--print_only", action="store_true", help="Only print results.")
    new_parser = subparser.add_parser("new", help="create a new encrypted file")
    new_parser.add_argument("-c", "--content", nargs="+", help="file content", required=True)
    new_parser.add_argument("-kp", "--key_path", help="fernet key location", required=True)
    new_parser.add_argument("-o", "--output_path", help="save encrypted file at this path")
    generate_parser = subparser.add_parser("generate", help="generate a fernet key")
    generate_parser.add_argument("-o", "--output_directory", help="create key file at this directory")
    crypt_ = crypt.Crypt()
    args = parser.parse_args()
    if args.command == "encrypt":
        key = crypt_.read_file(args.key_path).decode()
        crypt_.encrypt(args.file_path, key, args.remove)
    elif args.command == "decrypt":
        key = crypt_.read_file(args.key_path).decode()
        crypt_.decrypt(args.file_path, key, args.print_only)
    elif args.command == "new":
        content = "".join(args.content)
        key = crypt_.read_file(args.key_path).decode()
        crypt_.new(content, key, args.output_path)
    elif args.command == "generate":
        crypt_.generate(args.output_directory)
    else:
        parser.error("Need arguments.")

if __name__ == "__main__":
    main()
