import webbrowser
import capabilities

settings = {
    "print": {
        "type":"os",
        "value": "firefox"
    },
    "power": {
        "type":"os",
        "value": "firefox"
    },
    "browser": {
        "type":"python",
        "value": {
            "browser_name": "firefox"
            },
        "function" : capabilities.open_browser
    },
    "chrome": {
        "type":"python",
        "value": "chrome",
        "function" : capabilities.open_browser
    },
    "email": {
        "type": "browser",
        "value": "https://mail.google.com"
    },
    "facebook": {
        "type": "browser",
        "value": "https://facebook.com"
    },
    "github": {
        "type": "browser",
        "value": "https://github.com"
    }
}



# trigger_commands = {
# 	"open":open_program,
# 	"sleep":,
# 	"poweroff":,
# 	"reset network":,
# 	"update":,
# 	"paste":,
# }

#commands that are meant to be directly executed in terminal
terminal_commands = {

}

#commands that require some implicit arguments passed in voice messages
argurment_commands = {
	"google",
	"stack overflow",
}


def google():
    pass

def watch():
	#Interface with youtube
    pass

def stack_overflow():
	#take the error in the clipboard and search it on stackoverflow
    pass


