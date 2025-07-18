import jieba
import jieba.analyse
 
 
class Model(object):
    def __init__(self):
        pass
 
    def process_text(self, text):
        words_list = jieba.cut(text)
        words_list = ' '.join(words_list)
        return words_list
 
    def get_keyword(self, words_list, param, use_pos=True):
        if use_pos:
            # 选定部分词性
            allow_pos = ('n', 'nr', 'nr1', 'nr2', 'ns', 'nsf', 'nt', 'nz', 'nl', 'ng', 'nr', 'vn')
        else:
            allow_pos = ()
        if param == 'tfidf':
            tfidf_keywords = jieba.analyse.extract_tags(words_list, topK=10, withWeight=False, allowPOS=allow_pos)
            return tfidf_keywords
        elif param == 'textrank':
            textrank_keywords = jieba.analyse.textrank(words_list, topK=10, withWeight=False, allowPOS=allow_pos)
            return textrank_keywords
 
    def keyword_interact(self, tfidf_keyword, textrank_keyword):
        return list(set(tfidf_keyword).intersection(set(textrank_keyword)))
 
    def keyword_topk(self, tfidf_keyword, textrank_keyword, k):
        combine = list(tfidf_keyword[:k])
        for word in textrank_keyword[:k]:
            combine.append(word)
        return list(set(combine))
 
 
if __name__ == "__main__":
    model = Model()
    text = '北京时间5月28日消息，据《北京青年报》官微透露，北京中赫国安归化球员李可将入选新一期国家队的大名单。而他将成为国足历史首位归化国脚，目前相关手续应该已经得到落实，意味着李可具备代表中国队参赛的资格。北京时间5月28日消息，据《北京青年报》官微透露，北京中赫国安归化球员李可将入选新一期国家队的大名单。而他将成为国足历史首位归化国脚，目前相关手续应该已经得到落实，意味着李可具备代表中国队参赛的资格。'
    words_list = model.process_text(text)
    tfidf_keyword = model.get_keyword(words_list, param='tfidf')
    print('tfidf_keyword', tfidf_keyword)
    textrank_keyword = model.get_keyword(words_list, param='textrank')
    print("textrank_keyword", textrank_keyword)
    keyword_interact = model.keyword_interact(tfidf_keyword, textrank_keyword)
    print('keyword_interact', keyword_interact)
    keyword_topk = model.keyword_topk(tfidf_keyword, textrank_keyword, 3)
    print('keyword_topk', keyword_topk)
 