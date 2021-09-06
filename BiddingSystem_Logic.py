from BiddingSystem_Static import Campaign, AdCampaign, Request, BidRequest, Generator, AddGenerator, BidGenerator, timer
import json
from collections import defaultdict

class Evaluation:
    def __init__(self, ad_campaigns, bid_requests):
        self.ad_campaigns = ad_campaigns
        self.bid_requests = bid_requests

    def load_AdCampaigns(self):
        ad_table = {}
        for ad_campaign in self.ad_campaigns:
            if ad_campaign.domain not in ad_table:
                ad_table[ad_campaign.domain] = {}
            if ad_campaign.country not in ad_table[ad_campaign.domain]:
                ad_table[ad_campaign.domain][ad_campaign.country] = defaultdict(list)
            for dimension in ad_campaign.dimensions:
                ad_table[ad_campaign.domain][ad_campaign.country][dimension] += [ad_campaign.id]

        return ad_table

    @timer
    def evaluate(self):
        """The evaluate method returns a dictionary with the bid request id as the key and list of add campaign ids
        as the values which match the criteria of bid request made"""

        evaluation_results = {}
        ad_table = self.load_AdCampaigns()
        for bid_request in self.bid_requests:
            try:
                ad_ids = ad_table[bid_request.domain][bid_request.country][bid_request.dimension]
                if ad_ids:
                    evaluation_results[bid_request.id] = ad_ids
            except:
                continue
        return evaluation_results

    def evaluataion_results(self):
        """This method returns a json object of existing ad campaigns to evaluate bid requests against,
        evaluation results with bid request IDs and matching ad campaign IDs,
        number of bid requests processed and
        the time to run the evaluation"""

        evaluation_results = self.evaluate()
        defined_campaigns = []
        for ad_campaign in self.ad_campaigns:
            defined_campaigns.append(ad_campaign.create_json())
        bid_requests_processed = len(self.bid_requests)
        return json.dumps({
            "defined campaigns": defined_campaigns,
            "evaluation results": evaluation_results[0],
            "bid requests processed": bid_requests_processed,
            "evaluation time": evaluation_results[1]
        }, indent=2)


def main():
    bids = BidGenerator().generate_bids(100)
    adds = AddGenerator().generate_AdCampaigns(10)

    evaluation_results = Evaluation(adds, bids).evaluataion_results()
    print(evaluation_results)
    return evaluation_results

if __name__ == "__main__":
    main()