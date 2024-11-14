import board
import terminalio
import displayio
import time
import wifi
from helper import TDeck
import adafruit_connection_manager
import adafruit_requests
import parser
from paging_terminal import HighlightTerminal



def wrap_text(text, max_width):
    lines = []
    line = []
    current_width = 0
    for chunk in text:
        name = chunk[0]
        content = chunk[1]
        print(f"wrapping [{name}] {content}")
        if name == 'h1':
            name = 'header'
        if name == 'h2':
            name = 'header'
        if name == 'h3':
            name = 'header'
        if name == 'a':
            name = 'link'
        if name == 'p':
            name = 'plain'
        if current_width + len(content) > max_width:
            print(f"SPLIT: {content}")
            words = content.split()
            before = ""
            for word in words:
                if current_width + len(before) > max_width:
                    print(f"BREAK at word '{word}'",)
                    line.append([before,name])
                    print("LINE:",line)
                    lines.append(line)
                    line = []
                    before = ""
                    current_width = 0
                before += word + " "
            line.append([before,name])
            current_width += len(before)
            continue
        if name == 'header':
            print("LINE:",line)
            # lines.append(line)
            lines.append([content,name])
            line = []
            current_width = 0
            continue
        line.append([content,name])
        current_width += len(content)
        # current_width += 1 # account for spaces
    print("LINE:",line)
    lines.append(line)
    return lines


# init tdeck
tdeck = TDeck()
display = board.DISPLAY
splash = displayio.Group()
display.root_group = splash


COLCOUNT = 50
ROWCOUNT = 20

# init highlighter
term = HighlightTerminal(ROWCOUNT,COLCOUNT)
splash.append(term.group)

term.print_line(["Loading...","plain"])

# Initalize Wifi, Socket Pool, Request Session
print("initting wifi objects")
pool = adafruit_connection_manager.get_radio_socketpool(wifi.radio)
ssl_context = adafruit_connection_manager.get_radio_ssl_context(wifi.radio)
requests = adafruit_requests.Session(pool, ssl_context)


# fetch the page
def fetch_url():
    ssid = "JEFF22G"
    # ssid = "JEFF22"
    password = "Jefferson2022"
    # TEXT_URL = "https://joshondesign.com/c/writings"
    text_url = "https://joshondesign.com/2023/07/25/circuitpython-watch"
    try:
        print("connecting to", ssid)
        wifi.radio.connect(ssid, password)
        print("Connected to", ssid)
        print("fetching",text_url)
        with requests.get(text_url) as response:
            # print(response.text)
            print("got the page",text_url)
            print(f"{len(response.text)} bytes")
            chunks = parser.process_html(response.text)

            slice = chunks[1:50]
            print("==== chunks ====")
            for chunk in slice:
                print(chunk)
            return wrap_text(slice,COLCOUNT-8)
    except OSError as e:
        print("Failed to connect to", ssid, e)
        return

# parse into chunks
# print chunks to stdout
# wrap chunks into lines
# display first N lines to the highlighting terminal

output_lines = fetch_url()
print("==== output lines ====")
for line in output_lines:
    print(line)
#     term.print_line(line)

start_line = 0
def paginate():
    end_line = min(start_line+ROWCOUNT, len(output_lines))
    print("line count",len(output_lines), start_line,"to",end_line)

    for i in range(start_line,end_line):
        li = output_lines[i]
        term.print_line(li)

paginate()

# handle input events
while True:
    time.sleep(0.01)
    keypress = tdeck.get_keypress()
    if keypress:
        print("keypress-", keypress,"-")
        if keypress == ' ':
            start_line += ROWCOUNT
            paginate()