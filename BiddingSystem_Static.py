import random

def timer(func):
    """decorator for evaluation timing"""
    import time
    def wrapper(*args, **kwargs):
        t1 = time.perf_counter()
        result = func(*args, **kwargs)
        t2 = time.perf_counter() - t1
        return (result, t2)
    return wrapper

class Dimension:
    def __init__(self, dimension):
        self.length = self.parse_dimension(dimension)[0]
        self.width = self.parse_dimension(dimension)[1]

    def parse_dimension(self, dimension):
        return dimension.split("x")

    def __hash__(self):
        return hash((self.length, self.width))

    def __eq__(self, other):
        if isinstance(other, Dimension):
            return self.length == other.length and self.width == other.width
        else:
            return False

    def __str__(self):
        return f"length: {self.length} mm / width: {self.width} mm"


class Request:
    pass

class BidRequest(Request):
    def __init__(self, request_id, url, country_of_origin, dimension):
        self.id = request_id
        self.domain = self.parse_url(url)
        self.country = country_of_origin.upper()
        self.dimension = Dimension(dimension)

    def parse_url(self, url):
        from urllib.parse import urlparse
        return urlparse(url).netloc

    def __str__(self):
        return f"{self.id}: Domain - {self.domain}, Country - {self.country}, Dimensions - {self.dimension}"

class Campaign:
    pass

class AdCampaign(Campaign):
    def __init__(self, campaign_id, target_country, domain, dimensions):
        self.id = campaign_id
        self.country = target_country.upper()
        self.domain = domain
        self.dimensions = self.create_Dimensions(dimensions)

    def create_Dimensions(self, dimensions):
        dimension_list = []
        for dimension in dimensions:
            dimension_list.append(Dimension(dimension))
        return dimension_list

    def create_json(self):
        return {"id": self.id,
                "country": self.country,
                "domain": self.domain,
                "dimension": [dimension.__str__() for dimension in self.dimensions]}

    def __str__(self):
        string = f"{self.id}: Domain - {self.domain}, Country - {self.country}, Dimensions - ["
        for i, dimension in enumerate(self.dimensions):
            if i == len(self.dimensions) - 1:
                string += str(dimension)
            else:
                string += str(dimension) + ", "
        return string + "]"

class Generator:
    def generate_urls(self):
        domain = self.pick_domain()
        country = self.pick_country()
        item = random.randint(1, 5000)
        return f"http://{domain}.com/{country}/store?item={item}"

    def pick_country(self):
        countries = ["us", "ca", "it", "au", "bd", "eu", "tu"]
        return random.choice(countries)

    def pick_domain(self):
        domains = ["apple", "amazon", "etsy", "pinterest", "instacart", "hellofresh", "walmart", "metro"]
        return random.choice(domains)

    def generate_dimensions(self):
        length = random.randrange(100, 500, 100)
        width = random.randrange(100, 500, 100)
        return f"{length}x{width}"

    def generate_n_dimensions(self, n):
        dimensions = []
        for _ in range(n):
            dimensions.append(self.generate_dimensions())
        return dimensions

class BidGenerator(Generator):

    def generate_bids(self, no_of_bids):
        bid_requests = []
        for id in range(1, no_of_bids + 1):
            bid_requests.append(BidRequest(id, self.generate_urls(), self.pick_country(), self.generate_dimensions()))
        return bid_requests

class AddGenerator(Generator):

    def generate_AdCampaigns(self, no_of_campaigns):
        campaigns = []
        for id in range(1, no_of_campaigns + 1):
            campaigns.append(AdCampaign(id, self.pick_country(), f"{self.pick_domain()}.com", self.generate_n_dimensions(random.randint(1, 5))))
        return campaigns
