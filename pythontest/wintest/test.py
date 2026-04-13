import win32com.client
GUID = "{4234d49b-0245-4df3-b780-3893943456e1}"
shell = win32com.client.Dispatch("Shell.Application")
apps = shell.NameSpace(f"shell:::{GUID}")

print

for item in apps.Items():
    print(item.Name)
    print(item.Path)
    if item.Name == "Microsoft Teams":
        print(item.Application)
    print(type(item))
    print([n for n in dir(item) if not n.startswith("_")][:20])
    print(dir(item))
    print(item._oleobj_.GetTypeInfo())
    
