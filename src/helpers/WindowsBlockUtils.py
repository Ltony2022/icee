from src.helpers.blockutils import BlockUtils


class WindowsBlockUtils(BlockUtils):
    """
    Windows block utils.
    """

    def __init__(self):
        print(dir(self))
        self.trackingSites = [
            ["DOMAINS", "STATUS", "DURATION", "POSITION", "ID"]]
        # Change the host_path to your host file path
        self.host_path = "C:/Windows/System32/drivers/etc/hosts"
        # Local host IP
        self.redirect = "127.0.0.1"
        self.dict_trackingSites = {}

    def display_all_blocked_sites(self):
        # Display all blocked sites
        col_width = max(len(word)
                        for row in self.trackingSites for word in row) + 2
        for row in self.trackingSites:
            print("".join(word.ljust(col_width) for word in row))

    def return_all_blocked_sites(self):
        # Return all blocked sites
        return self.trackingSites

    def add_block_site(self, site, duration=None):
        # interacting with file
        with open(self.host_path, "r+") as f:
            content = f.read()
            domainPositionOnTheFile = len(content.split("\n"))
            numberOnTheList = len(self.trackingSites)
            if site in content:
                f.close()
                return print("(AddBlockSite) ", site, " is already blocked")
            else:
                # Adding site to the list
                self.trackingSites.append(
                    [
                        site,
                        "BLOCKED",
                        duration,
                        domainPositionOnTheFile - 1,
                        numberOnTheList,
                    ]
                )
                f.write(self.redirect + " " + site + "\n")
                self.dict_trackingSites[site] = self.trackingSites[
                    numberOnTheList
                ]

    def remove_block_site(self, site):
        # Find the site in the list
        if site in self.dict_trackingSites:
            # Get the position of the domain in the file
            domainPosition = self.dict_trackingSites[site][3]
            with open(self.host_path, "r+") as f:
                content = f.readlines()
                print("Removing site ", site, "...")
                content[domainPosition] = ""
                f.truncate(0)
                f.seek(0)
                f.writelines(content)

                # remove object from the list
                self.dict_trackingSites.pop(site)
                self.trackingSites.remove(site)
        else:
            print("", site, " is not blocked")

    def enable_block_site(self, site, duration=None):
        with open(self.host_path, "r+") as f:
            content = f.readlines()
            if site not in self.dict_trackingSites:
                f.close()
                return print("(EnableBlockSite) ", site, " is not available in the block list")
            elif self.dict_trackingSites[site][1] == "ENABLED":
                f.close()
                return print("(EnableBlockSite) ", site, " is already enabled")

            if site in self.dict_trackingSites:
                # verbose mode only
                print("(EnableBlockSite) The site information: ",
                      self.dict_trackingSites[site])
                domainPosition = self.dict_trackingSites[site][3]
                print(
                    "(EnableBlockSite) Position of the domain in the file: ", domainPosition)
                # end of verbose mode
                print("Enabling site...")
                line = content[domainPosition].replace("# ", "")
                content[domainPosition] = line
                f.seek(0)
                f.writelines(content)
                self.dict_trackingSites[site][1] = "ENABLED"

    def disable_block_site(self, site, duration=None):
        with open(self.host_path, "r+") as f:
            content = f.readlines()
            if site not in self.dict_trackingSites:
                f.close()
                return print("(DisableBlockSite) ", site, " is not on the block list")
            elif self.dict_trackingSites[site][1] == "DISABLED":
                f.close()
                return print("(DisableBlockSite) ", site, " is already disabled")

            if site in self.dict_trackingSites:
                domainPosition = self.dict_trackingSites[site][3]
                # verbose mode only
                print(
                    "(DisableBlockSite) Position of the domain in the file: ", domainPosition)
                # End of verbose mode
                print("Disabling site...")
                line = "# " + content[domainPosition]
                content[domainPosition] = line
                f.seek(0)
                f.writelines(content)
                self.dict_trackingSites[site][1] = "DISABLED"
