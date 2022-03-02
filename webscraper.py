import scrapy

# def string_cleaner(rouge_text):
#         return ("".join(rouge_text.strip()).encode('cp865', 'ignore').decode("cp865"))
furl = 'https://vcnewsdaily.com/{}'
surl = 'https://vcnewsdaily.com/access/{}'
class WebCrawler(scrapy.Spider):
    name = 'webscraper'
    start_urls = ['https://vcnewsdaily.com/archive.php',]

    def parse(self,response):
        for link in response.css('div.col-xl-9 a::attr(href)'):
            correct_link = furl.format(link.get())
            yield response.follow(correct_link, callback = self.first_link)

    def first_link(self,response):
        tem = response.css('div.row')
        temp = tem[2]
        for link in temp.css('a::attr(href)'):
            correct_link = surl.format(link.get())
            yield response.follow(correct_link, callback = self.second_link)
        
    def second_link(self,response):
        rr = response.css('div.row')
        rs = rr[2]
        data = rs.css('::text').getall()

        title = []
        for i in range(2,len(data),9):
            title.append(data[i])

        date = []
        for i in range(4,len(data),9):
            date.append(data[i])

        article_desc = []
        for i in range(6,len(data),9):
            article_desc.append(data[i])

        article_link = []

        data2 = rs.css('a::attr(href)').getall()
        for i in range(1,len(data2),2):
            article_link.append(data2[i])

        for (dt,tit,art_li,art_des) in zip(date,title,article_link,article_desc):
            yield {
                'date':dt,
                'title':tit,
                'article_link':art_li,
                'article_desc':art_des
            }





        
    

'''
a.css('tr.data-table_row__2w7Kn')
a.css('tr.data-table_row__2w7Kn td.data-table_cell__2OGzJ section a.cells_link__2252j::text').getall()
len(a.css('tr.data-table_row__2w7Kn td.data-table_cell__2OGzJ p::text').getall())
a.css('tr.data-table_row__2w7Kn td.data-table_cell__2OGzJ span::text').getall()
a.css('tr.data-table_row__2w7Kn td.data-table_cell__2OGzJ div.cells_cell-3__1_fE_ ::text').getall()

'''