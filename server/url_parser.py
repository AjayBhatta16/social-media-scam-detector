import re 
import json

sites = {
    'facebook': r'^(?:https?:\/\/)?(?:www\.)?facebook\.com\/([a-zA-Z0-9.]+)',
    'twitter': r'^(?:https?:\/\/)?(?:www\.)?twitter\.com\/([a-zA-Z0-9_]+)',
    'instagram': r'^(?:https?:\/\/)?(?:www\.)?instagram\.com\/([a-zA-Z0-9_.]+)'
}

def parse(url):
    for platform, exp in sites.items():
        match = re.search(exp, url)
        if re.search(exp, url):
            username = match.group(1)
            if platform=="instagram" and username=="p":
                return {
                    "status": 400,
                    "message": "Cannot scan post"
                }
            return {
                "status": 200,
                "platform": platform,
                "username": username
            }
    return {
        "status": 400,
        "message": "Invalid Profile URL"
    }

testUrls = [
    "https://instagram.com/ajaybhatta49",
    "https://instagram.com/redjugpub?igshid=NTc4MTIwNjQ2YQ==",
    "instagram.com/clickhole",
    "reddit.com/ajaybhatta49",
    "https://twitter.com/ScammerPayback?s=20",
    "twitter.com/gangstakittle",
    "",
    "randomlettersandstuff",
    "https://www.facebook.com/ajay.bhatta.49",
    "https://www.instagram.com/p/BmZd2UTFErHKIbh-Xizyx1k9i4hK5xvDTXo9yw0/",
    "https://twitter.com/Kitboga/status/1658118112481271810",
    "instagram.com/"
]
def test():
    for url in testUrls:
        result = parse(url)
        print(json.dumps(result))

# Uncomment the following line to run test cases:
# test()