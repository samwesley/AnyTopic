import datetime

today = str(datetime.date.today())
folderName = str(today)

categories = {"sr": "space_robotics",
              "st": "space_tech",
              "cr": "chicago_river",
              "cm": "chuck_malk",
              "wm": "wild_mile",
              "w": "wildmile",
              "cdn": "chicago_disctrict_news",
              "ure": "urban_river_ecology",
              "ftw": "floating_treatment_wetlands",
              "fi": "floating_islands",
              "fii": "floating_islands_international",
              "bw": "biomatrix_water",
              "awh": "artificial_wildlife_habitat",
              "ur": "urban_rivers",
              "urp": "urban_river_project",
              "np": "naru_project",
              "rr": "river_rehabilitation",
              "br": "bioremediation_river",
              "fw": "floating_wetland"}

categoryNames = {"sr": "Space Robotics",
                 "st": "Space Technology",
                 "cr": "Chicago River",
                 "cm": "chuck malk",
                 "wm": "wild mile",
                 "w": "wildmile",
                 "cdn": "Chicago Disctrict News",
                 "ure": "urban river ecology",
                 "ftw": "floating treatment wetlands",
                 "fi": "floating islands",
                 "fii": "floating islands international",
                 "bw": "biomatrix water",
                 "awh": "artificial wildlife habitat",
                 "ur": "urban rivers",
                 "urp": "urban river project",
                 "np": "naru project",
                 "rr": "River rehabilitation",
                 "br": "bioremediation river",
                 "fw": "floating wetland"}

titleTags = ["title"]
# ordered by least to most specific area to find article content
articleTags = ["p", "article", 'id="article-body"', 'class_="caas-body"', 'itemprop="articleBody"']
filterList = ["Attention Required! | Cloudflare", "403 Forbidden"]

urls = {"sr": "https://www.google.com/alerts/feeds/04179049431026736918/16094280887727195819",
        "st": "https://www.google.com/alerts/feeds/04179049431026736918/10352800335472653504",
        "cr": "https://www.google.com/alerts/feeds/04179049431026736918/13632024569597942229",
        "cm":"https://www.google.com/alerts/feeds/09250651260953586917/18048113753386306616",
        "wm":"https://www.google.com/alerts/feeds/09250651260953586917/6775137044205405918",
        "w":"https://www.google.com/alerts/feeds/09250651260953586917/6775137044205405416",
        "cdn":"https://www.lrc.usace.army.mil/DesktopModules/ArticleCS/RSS.ashx?ContentType=21&Site=464&isdashboardselected=0&max=20",
        "ure":"https://www.google.com/alerts/feeds/00141647403121360786/14569334214809738282",
        "ftw":"https://www.google.com/alerts/feeds/00141647403121360786/3777413808972477893",
        "fi":"https://www.google.com/alerts/feeds/00141647403121360786/12341478358814264785",
        "fii":"https://www.google.com/alerts/feeds/00141647403121360786/7745654336954776598",
        "bw":"https://www.google.com/alerts/feeds/00141647403121360786/13925161882465971883",
        "awh":"https://www.google.com/alerts/feeds/00141647403121360786/3777413808972480282",
        "ur":"https://www.google.com/alerts/feeds/00141647403121360786/16394135660641242900",
        "urp":"https://www.google.com/alerts/feeds/00141647403121360786/2473140282316406995",
        "np":"https://www.google.com/alerts/feeds/00141647403121360786/16900800042481686209",
        "rr":"https://www.google.com/alerts/feeds/00141647403121360786/334295087509496198",
        "br":"http://google.com/alerts/feeds/00141647403121360786/8523717045299115071",
        "fw":"https://www.google.com/alerts/feeds/00141647403121360786/3252336291101328349"}

firstFieldOption = ["date", "category"]
secondFieldOption = ["link", "title", "html"]
thirdFieldOptions = ["htmlTag", "block", "prompt", "summary", "blockWordCount"]
