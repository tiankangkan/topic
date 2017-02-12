# -*- coding: utf-8 -*-

import scrapy
import urllib
import datetime
import time
import traceback

from .base_spider import BaseSpider


class KMAskSpider(BaseSpider):
    name = "km_ask"
    url = "http://km.oa.com/q?page=1"
    cookie_str = """km_u=7ffa16585f47a6eae1839974975d963241e5ef8375cb533b19824daa8978d6a8c41e239afd2600bd; km_uid=kangtian; pgv_pvi=4734552064; code_user_name=BE420FAD9AFC649C3EE892A1B700DC65; isConventionAlert=true; pgv_pvid=3304542114; t_uid=kangtian; t_u=a379c957bf906798%7Cfa5da23b5b2b837d; CAKEPHP=43kq2sqo7q857u4dg6od5pfgp4; TCOA_TICKET=598E0DBD2CF113F64017462F64491C9497B66ED755378F111C1457DA10FC7F4FE422FE777A5F3E4C12505814F193A8EA82E31AEC6E2123408DFE26888CF960C378CBA48C40CE596D2282C41BB4CB3DF0B693AB52C4A39798D841052643F8D964BD8C8D9CD164BC19F81164194FB0B7769B78B80EA07FED997424700CD1E97A74FC2DE5ABD6782D7491CAAF53737EBA9D6AB89CEC820A545C8FEC91657B7291D2BE9705931647DE57; TCOA=HlOMaxjz5F; pgv_si=s8628081664; is_q_convention_alerted=true; is_alerted=true; KMSID=q0ktk6qrnae7nmhimomqjpkp20"""
    cookie = None
    data = {}
    page = 1

    def start_requests(self):
        self.cookie = self.parse_cookie(self.cookie_str)
        print(self.cookie)
        yield scrapy.Request(self.url, cookies=self.cookie, callback=self.parse)

    def parse(self, response):
        try:
            url = urllib.unquote(response.url)
            host_name = url.split('//')[1].split('/')[0]

            if 'q?page='in url:
                for question in response.css(".q_list .q_list_item"):
                    detail_url = self.format_text(question.css(".q_item_name a::attr(href)").extract_first())
                    if detail_url:
                        detail_url = 'http://' + host_name + detail_url
                        print('[%s]: go to detail: %s' % (self.name, detail_url))
                        yield scrapy.Request(detail_url, cookies=self.cookie, callback=self.parse)

                self.page = int(url.split("=")[-1])
                # print(response.body)
                next_page = self.page + 1
                next_url = "%s=%s" % (url.rsplit("=", 1)[0], next_page)
                yield scrapy.Request(url=next_url, callback=self.parse)
            elif 'q/view' in url:
                question_body = response.css(".q_list ul")
                values = {
                    'title': self.format_text(question_body.css(".q_item_name::text").extract_first()),
                    'time': self.format_text(question_body.css(".q_item_attrs > .answer_time::text").extract()),
                    'author': self.format_text(''.join(question_body.css(".q_item_attrs .question-owner a::text").extract())),
                    'times': self.format_text(question_body.css(".browse-number::text").extract()),
                    'summary': self.format_text(question_body.css(".q_item_question_detail::text").extract_first()),
                    'intro_info': [],
                    'labels': response.css(".q_top_topics_static .topic::text").extract()
                }
                if values['time']:
                    if isinstance(values['time'], list):
                        values['time'] = self.format_text(values['time'][-1])
                    values['time'] = datetime.datetime.strptime(values['time'], "%Y-%m-%d %H:%M")
                if values['times']:
                    if isinstance(values['times'], list):
                        values['times'] = self.format_text(values['times'][-1])
                    values['times'] = int(values['times'].split(u'次')[0])
                for item in question_body.css(".obj_intro .secondary ul li::text"):
                    time.sleep(5)
                    values['intro_info'].append({
                        'from_person': self.format_text(item.css("a:nth-child(1)::text")),
                        'to_person': self.format_text(item.css("a:nth-child(2)::text")),
                        'reason': self.format_text(item.css(".invited-reason::text")),
                    })
                    print('[%s]:values: %s' % (self.name, values))
                yield values
            else:
                yield scrapy.Request(url=self.url.replace('1', str(self.page + 1)), callback=self.parse)
        except:
            print(traceback.format_exc())
            time.sleep(10)
            yield scrapy.Request(url=self.url.replace('1', str(self.page + 1)), callback=self.parse)