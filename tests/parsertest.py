import pprint
import unittest
from parser import HtmlParser



class BasicParsing(unittest.TestCase):
    def simple_element(self,text,name,content):
        parser = HtmlParser()
        chunks = list(parser.parse(text))
        print(chunks,len(chunks))
        self.assertEqual(len(chunks),1)
        self.assertEqual(chunks[0][0], name)
        self.assertEqual(chunks[0][1], content)

    # def test_elements(self):
    #     self.simple_element("<h1>some html</h1>","h1","some html")
    #     self.simple_element("<h1 extra>some html</h1>","h1","some html")
    #     self.simple_element("<a>some html</a>","a","some html")
    #     self.simple_element("<b>some html</b>","b","some html")
    #     self.simple_element("<i>some html</i>","i","some html")
    #     self.simple_element('<a href="foo">some html</a>',"a","some html")
    #     self.simple_element('<a\n href="foo">some html</a>',"a","some html")
        # self.simple_element('<img\n src="foo" alt="z" />',"img",'')
        # self.simple_element("<li>some html</li>","li","some html")

    # def test_whitespace_removal(self):
    #     self.simple_element("  <h1>   some html  </h1>  ","h1","some html")
    #     self.simple_element("  <a>   some html  </a>  ","a","some html")
    # def test_entity_replacement(self):
    #     self.simple_element('<a href="foo">foo & bar</a>  ', "a", "foo & bar")
    #     self.simple_element('<a href="foo">foo &amp; bar</a>  ', "a", "foo & bar")
    #     self.simple_element('<a href="foo">foo &#x27; bar</a>  ', "a", "foo ' bar")


    def test_link(self):
        self.assertEqual(
            [
                ['p',{},['a',{'href':'https://google.com/'},['text','a link to google']]]
            ],
            list(HtmlParser().parse(
            '<p><a href="https://google.com/">a link to google</a></p>')),
        )
    def test_plain_text(self):
        self.assertEqual(list(HtmlParser().parse('middle')), [
            ['block',['text','middle']]
        ])
    def test_para_with_styles(self):
        self.assertEqual(
            [
                ['p', {},
                    ['text', 'before'],
                    ['b',{},['text', 'middle']],
                    ['text', 'after']
                ],
            ],
            list(HtmlParser().parse('<p> before <b>middle</b> after </p>')),
        )
    def test_extra_text(self):
        self.assertEqual(
            [
                ['block',['text','cool text']],
                ['p', {},
                    ['text', 'text']
                ],
                ['block',['text','after text']]
            ],
            list(HtmlParser().parse('cool text <p>text</p> after text')),
        )
    def test_complex_text(self):
        self.assertEqual(
            [
                ['h1',{}, ['text', 'HTML Test']],
                ['p', {},
                 ['text', 'One of my original']
                ],
            ],
            list(HtmlParser().parse('<html>'
                                    '<body>'
                                    '<h1>HTML Test</h1>'
                                    '<p>'
                                    'One of my original'
                                    '</p>'
                                    '</body>'
                                    '</html>')),
        )
        self.assertEqual(
            [
                ['p', {},
                    ['text', 'One of my original IdealOS front page'],
                ],
            ],
            list(HtmlParser().parse('<p>One of my original IdealOS\n     front page</p>')),
        )

    # def test_live(self):
    #     with open("test.html", "r") as txt:
    #         html = txt.read()
    #         # print("opened the file", html)
    #         parser = HtmlParser()
    #         chunks = list(parser.parse(html))
    #         chunks = list(filter(lambda x: len(x[1].strip())>0,chunks))
    #         for chunk in chunks:
    #             print(chunk)
    #         self.assertEqual(len(chunks),5)
    #
    def test_bigger_html_local(self):
        with open("test.html", "r") as txt:
            html = txt.read()
            blocks = list(HtmlParser().parse(html))
            pprint.pp(blocks)
            self.assertEqual(len(blocks),6)
    def test_strip_whitespace(self):
        with open("test.html", "r") as txt:
            html = txt.read()
            blocks = list(HtmlParser().parse(html))
            pprint.pp(blocks)
            self.assertEqual(len(blocks),6)
    def test_blog_local(self):
        with open("blog.html", "r") as txt:
            html = txt.read()
            blocks = list(HtmlParser().parse(html))
            print("blocks==========")
            for block in blocks:
                print(block)
            self.assertEqual(len(blocks),29)
            self.assertEqual(blocks[0][0],'h1')
            self.assertEqual(blocks[1][0],'li')

            self.assertEqual(blocks[22][0],'p')
            self.assertEqual(blocks[22][2][1],'Posted July 25th, 2023')

    # def test_blog_remote(self):
    #     text_url = "https://joshondesign.com/2023/07/25/circuitpython-watch"
    #     with requests.get(text_url) as response:
    #         print("got the page",text_url)
    #         print(f"{len(response.text)} bytes")
    #         html = response.text
    #         parser = HtmlParser()
    #         chunks = list(parser.parse(html))
    #         slice = chunks[1:50]
    #         # chunks = list(filter(lambda x: len(x[1].strip())>0,chunks))
    #         print("==== chunks ====")
    #         for chunk in slice:
    #             print(chunk)
    #         self.assertEqual(len(chunks),57)


if __name__ == '__main__':
    unittest.main()
