class Config():

    def __init__(self):

        self.diretorioarcom = "c:\\Arcom"

        self.chocolateypath = "c:\\ProgramData\\chocolatey\\choco.exe"

        self.filestringspark = """passwordSaved=true
        server=arcompbx.gotdns.com
        hostAndPort=false
        DisableHostnameVerification=true
        """
        self.programas = {
            "Adobe Reader": "adobereader",
            "Adobe Air": "adobeair",
            "Java": "javaruntime --x86SteamSteam",
                    "Spark": "spark",
                    "Teamviewer": "teamviewer",
                    "Anydesk": "anydesk.install",
                    "Google Chrome": "googlechrome",
                    "Firefox": "firefox"
        }
        self.allusersdesktop = "c:\\Users\\Public\\Desktop"
        self.userdesktop = "%USERPROFILE%\\Desktop"
