from pydrive.auth import GoogleAuth
import sys

def main():
    if len(sys.argv) != 2:
        print('Use: python2 gdrive.py <code>')
        sys.exit(1)

    code = sys.argv[1]

    gauth = GoogleAuth()
    gauth.Auth(code)
    print(gauth.credentials.to_json())


if __name__ == '__main__':
    main()
