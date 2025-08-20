class Article:
    all = []
    def __init__(self, author, magazine, title):
        self.author = author
        self.magazine = magazine
        self.title = title

        Article.all.append(self)

    def __setattr__(self, key, value):
        if key == "title":
            if not isinstance(value, str):
                return  
            if hasattr(self, "title"):
                return  
        super().__setattr__(key, value)
        
        
class Author:
    def __init__(self, name):
        self.name = name

    def __setattr__(self, key, value):
        if key == "name":
            if not isinstance(value, str):
                return  
            if hasattr(self, "name"):
                return  
        super().__setattr__(key, value)

    def articles(self):
        return [article for article in Article.all if article.author == self]

    def magazines(self):
        return list({article.magazine for article in self.articles()})

    def add_article(self, magazine, title):
        return Article(self, magazine, title)
    
    def topic_areas(self):
        categories = {article.magazine.category for article in self.articles()}
        if categories:
           return list(categories)
        else:
            return None

class Magazine:
    all = []

    def __init__(self, name, category):
        self.name = name
        self.category = category

        Magazine.all.append(self)

    def __setattr__(self, key, value):
        if key == "name" or key == 'category':
            if not isinstance(value, str):
                return 
            if not 2 <= len(value) <= 16:
                return  
        super().__setattr__(key, value)

    def articles(self):
        return [article for article in Article.all if article.magazine == self]

    def contributors(self):
        authors = [article.author for article in self.articles()]
        return list(set(authors)) if authors else []

    def article_titles(self):
        article_titles = [article.title for article in Article.all if article.magazine == self]
        if article_titles:
            return list(article_titles)

    def contributing_authors(self):
        authors_count = {}

        for article in Article.all:
            if article.magazine == self:
                author = article.author
                authors_count[author] = authors_count.get(author, 0) + 1

        contributing_authors = [author for author, count in authors_count.items() if count > 2]

        return contributing_authors if contributing_authors else None
    
    @classmethod
    def top_publisher(cls):
        if not hasattr(cls, "all") or not cls.all:
            return None

        top_magazine = None
        max_articles = 0

        for magazine in cls.all:
            count = len([article for article in Article.all if article.magazine == magazine])

            if count > max_articles:
                max_articles = count
                top_magazine = magazine

        return top_magazine