# import pyuac
# from controller import windowsController
from controller import Controller


def main():
    mainprog = Controller()
    mainprog.show_cli()


main()

# if __name__ == "__main__":
#    if not pyuac.isUserAdmin():
#        print("Re-launching as admin!")
#        pyuac.runAsAdmin()
#    else:
#        main()  # Already an admin here.
