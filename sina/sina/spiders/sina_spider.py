'''
Author: error: git config user.name & please set dead value or install git
Date: 2025-07-13 23:20:19
LastEditors: yinchao
LastEditTime: 2025-07-15 23:22:14
Description: 
'''
from typing import Any
import scrapy
from scrapy.http import Request
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import os
from sina.items import SinaItem




class SinaSpiderSpider(scrapy.Spider):
    name = "sina_spider"
    
    def __init__(self, name: str | None = None, **kwargs: Any):
        self.start_urls = ['https://news.sina.com.cn/china/'] 
        
        # 配置Chrome选项
        self.option = webdriver.ChromeOptions()
        
        # 指定Chrome浏览器路径（macOS标准路径）
        chrome_path = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
        if os.path.exists(chrome_path):
            self.option.binary_location = chrome_path
        
        # 添加稳定性选项
        self.option.add_argument('--no-sandbox')
        self.option.add_argument('--disable-dev-shm-usage')
        self.option.add_argument('--headless')  # 无头模式
        self.option.add_argument('--disable-gpu')
        self.option.add_argument('--disable-web-security')
        self.option.add_argument('--disable-features=VizDisplayCompositor')
        self.option.add_argument('--blink-settings=imagesEnabled=false')
        self.option.add_argument('--disable-extensions')
        self.option.add_argument('--disable-plugins')
        self.option.add_argument('--disable-background-timer-throttling')
        self.option.add_argument('--disable-backgrounding-occluded-windows')
        self.option.add_argument('--disable-renderer-backgrounding')
        self.option.add_argument('--disable-software-rasterizer')
        self.option.add_argument('--disable-ipc-flooding-protection')
        
        # 指定chromedriver路径，避开selenium-manager
        chromedriver_path = "/usr/local/bin/chromedriver"
        service = Service(chromedriver_path) if os.path.exists(chromedriver_path) else None
        
        # 初始化webdriver实例（只创建一次）
        try:
            if service:
                self.driver = webdriver.Chrome(service=service, options=self.option)
            else:
                self.driver = webdriver.Chrome(options=self.option)
            self.driver.set_page_load_timeout(30)
            print("WebDriver初始化成功")
        except Exception as e:
            print(f"初始化webdriver失败: {e}")
            self.driver = None
    
    def start_requests(self):
        for url in self.start_urls:
            yield Request(url, callback=self.parse)
    
    def parse(self, response):
        if not self.driver:
            print("WebDriver未初始化，跳过此请求")
            return
            
        try:
            self.driver.get(response.url)
            title_elements = self.driver.find_elements(By.XPATH, "//h2[@class='undefined']/a[@target='_blank']")
            time_elements = self.driver.find_elements(By.XPATH, "//h2[@class='undefined']/../div[@class='feed-card-a feed-card-clearfix']/div[@class='feed-card-time']")
            
            for i in range(len(title_elements)):
                # 创建SinaItem实例
                item = SinaItem()
                item['title'] = title_elements[i].text
                item['time'] = time_elements[i].text if i < len(time_elements) else ""
                
                # 输出到控制台（可选）
                print(f'标题：{item["title"]}')
                print(f'时间：{item["time"]}')
                
                # yield item给pipeline处理
                yield item
                
        except Exception as e:
            print(f"解析页面时出错: {e}")
    
    def closed(self, reason):
        """爬虫关闭时清理webdriver"""
        if hasattr(self, 'driver') and self.driver:
            self.driver.quit()
            print("WebDriver已关闭")
        