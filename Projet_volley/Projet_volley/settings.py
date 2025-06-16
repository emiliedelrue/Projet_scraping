# Scrapy settings for Projet_volley project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = "Projet_volley"

SPIDER_MODULES = ["Projet_volley.spiders"]
NEWSPIDER_MODULE = "Projet_volley.spiders"

ADDONS = {}


# Crawl responsibly by identifying yourself (and your website) on the user-agent
#USER_AGENT = "Projet_volley (+http://www.yourdomain.com)"

# Obey robots.txt rules
ROBOTSTXT_OBEY = False

# Configure maximum concurrent requests performed by Scrapy (default: 16)
#CONCURRENT_REQUESTS = 32

# Configure a delay for requests for the same website (default: 0)
# See https://docs.scrapy.org/en/latest/topics/settings.html#download-delay
# See also autothrottle settings and docs
#DOWNLOAD_DELAY = 3
# The download delay setting will honor only one of:
#CONCURRENT_REQUESTS_PER_DOMAIN = 16
#CONCURRENT_REQUESTS_PER_IP = 16

# Disable cookies (enabled by default)
#COOKIES_ENABLED = False

# Disable Telnet Console (enabled by default)
#TELNETCONSOLE_ENABLED = False

# Override the default request headers:
#DEFAULT_REQUEST_HEADERS = {
#    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
#    "Accept-Language": "en",
#}

# Enable or disable spider middlewares
# See https://docs.scrapy.org/en/latest/topics/spider-middleware.html
#SPIDER_MIDDLEWARES = {
#    "Projet_volley.middlewares.ProjetVolleySpiderMiddleware": 543,
#}


# Enable or disable extensions
# See https://docs.scrapy.org/en/latest/topics/extensions.html
#EXTENSIONS = {
#    "scrapy.extensions.telnet.TelnetConsole": None,
#}

DOWNLOADER_MIDDLEWARES = {
    # Middlewares par défaut de Scrapy (désactivés si besoin)
    'scrapy.downloadermiddlewares.useragent.UserAgentMiddleware': None,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': None,
    
    # Nos middlewares personnalisés
    'Projet_volley.middlewares.RotateUserAgentMiddleware': 400,
    'Projet_volley.middlewares.HeadersMiddleware': 500,
    'Projet_volley.middlewares.CustomRetryMiddleware': 550,
    'Projet_volley.middlewares.ThrottleMiddleware': 600,
    'Projet_volley.middlewares.LoggingMiddleware': 650,
    'Projet_volley.middlewares.ResponseSizeMiddleware': 700,
    'Projet_volley.middlewares.ErrorHandlingMiddleware': 750,
    'Projet_volley.middlewares.CacheMiddleware': 800,
}

# Configuration des spider middlewares
SPIDER_MIDDLEWARES = {
    'Projet_volley.middlewares.FFVBScraperSpiderMiddleware': 543,
}

# Configuration des pipelines
ITEM_PIPELINES = {
    'Projet_volley.pipelines.ValidationPipeline': 200,
    'Projet_volley.pipelines.DuplicateFilterPipeline': 300,
    'Projet_volley.pipelines.CSVExportPipeline': 400,
    'Projet_volley.pipelines.JSONExportPipeline': 500,
    'Projet_volley.pipelines.DatabasePipeline': 600,
    'Projet_volley.pipelines.StatisticsPipeline': 700,
    'Projet_volley.pipelines.SimpleFFVBPipeline': 300,
    'Projet_volley.pipelines.FranceFFVBPipeline': 300,
    'Projet_volley.pipelines.FederalFFVBPipeline': 300,
}


# Enable and configure the AutoThrottle extension (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/autothrottle.html
#AUTOTHROTTLE_ENABLED = True
# The initial download delay
#AUTOTHROTTLE_START_DELAY = 5
# The maximum download delay to be set in case of high latencies
#AUTOTHROTTLE_MAX_DELAY = 60
# The average number of requests Scrapy should be sending in parallel to
# each remote server
#AUTOTHROTTLE_TARGET_CONCURRENCY = 1.0
# Enable showing throttling stats for every response received:
#AUTOTHROTTLE_DEBUG = False

# Enable and configure HTTP caching (disabled by default)
# See https://docs.scrapy.org/en/latest/topics/downloader-middleware.html#httpcache-middleware-settings
#HTTPCACHE_ENABLED = True
#HTTPCACHE_EXPIRATION_SECS = 0
#HTTPCACHE_DIR = "httpcache"
#HTTPCACHE_IGNORE_HTTP_CODES = []
#HTTPCACHE_STORAGE = "scrapy.extensions.httpcache.FilesystemCacheStorage"

# Set settings whose default value is deprecated to a future-proof value
FEED_EXPORT_ENCODING = "utf-8"
