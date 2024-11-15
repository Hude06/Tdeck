import re
paraTags = ["h1","h2","h3","h4","p","li","td"]
solo_tags = ['img']
ignore_tags = ['meta','link', "!DOCTYPE",'script','title','head','html','body']

MAX_TEXT = 2500_0
class HtmlParser:
    def __init__(self):
        self.stack = []
        self.run = ""
        self.runs = []
        self.n = 0

    def parse(self, text):
        # print("processing text",text[0:MAX_TEXT])
        self.n = 0
        self.runs = []
        self.run = ""

        while self.n < len(text) and self.n < MAX_TEXT:
            if text[self.n:self.n+len("</")] == "</":
                self.end_tag(text,self.n)
                self.run = ""
                continue
            if text[self.n] == "<":
                self.slurp_tag(text,self.n)
                continue

            ch = text[self.n]
            if ch == '\n':
                ch = ""
            self.run += ch
            self.n += 1
            # print(self.run)
        self.save_run()
        return self.runs

    def slurp_tag(self, text, n):
        self.save_run()
        end_index = text.find(">",n+1)
        space_index = text.find(' ',n+1,end_index)
        name = text[n+1:end_index]
        # print(f"slurping tag '{name}'")
        if space_index >= 0:
            name = text[n+1:space_index]
        name = name.strip()
        if  not (name in ignore_tags):
            atts = text[n+1:end_index]
            # print(f"pushing tag '{name}':'{atts}'")
            self.stack.append([name,atts])
        if name in solo_tags:
            res = self.stack.pop()
            # print(f"popping solo tag '{res[0]}'", text[n+1:end_index])
            self.runs.append([res[0],''])
        self.n = end_index+1

    def end_tag(self,text,n):
        end_index = text.find(">",n+1)
        name = text[n+2:end_index]
        if name in ignore_tags:
            # print("should ignore",name)
            self.n = end_index+1
            return
        res = self.stack.pop()
        # print("pop",res[0])
        if name != res[0]:
            print("pop mismatch", text[n+2:end_index],'vs',res)
        txt = self.run.strip()
        if len(txt) > 0:
            self.append_content(name,txt)
        self.n = end_index+1

    def save_run(self):
        txt = self.run.strip()
        if len(txt) > 0:
            # print(f"saving run: '{txt}'")
            name = 'plain'
            if len(self.stack) > 0 and self.stack[-1]:
                name = self.stack[-1][0]
            self.append_content(name,txt)

    def append_content(self, name, content):
        # print("appending",content)
        content = re.sub(r"&amp;", '&', content)
        content = re.sub(r"&#x27;", "'", content)
        self.runs.append([name,content])
        self.run = ""


def process_html(html):
    parser = HtmlParser()
    chunks = parser.parse(html)
    return chunks


