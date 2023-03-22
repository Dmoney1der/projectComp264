from math import ceil
from chalicelib.business_card import BusinessCard

class BusinessCardList:
    
    def __init__(self, search_result, page, pagesize):
        
        self.raw_result = search_result
        self.cards = []
        self.page = int(page)
        self.pagesize = int(pagesize)
        self.count = 0
        self.numpages = 0

        # Create card object list
        self.__build_list()

    def __build_list(self):
    
        items = self.raw_result['Items']
        self.count = int(self.raw_result['Count'])

        # Extract card information
        for item in items:

            c = BusinessCard()

            if item.__contains__('card_id'):
                c.card_id = item['card_id']['S']

            if item.__contains__('user_id'):
                c.user_id = item['user_id']['S']

            if item.__contains__('card_names'):
                c.names = item['card_names']['S']

            if item.__contains__('telephone_numbers'):
                c.telephone_numbers = item['telephone_numbers']['SS']

            if item.__contains__('email_addresses'):
                c.email_addresses = item['email_addresses']['SS']

            if item.__contains__('company_name'):
                c.company_name = item['company_name']['S']

            if item.__contains__('company_website'):
                c.company_website = item['company_website']['S']

            if item.__contains__('company_address'):
                c.company_address = item['company_address']['S']

            self.cards.append(c)

        # Sort cards by person name
        self.cards.sort(key=lambda x: x.names)

        # Calculate indexes for pagination in sorted results
        start_index = 0
        end_index = 0

        if self.pagesize > self.count:
            self.pagesize = self.count

        if self.pagesize and self.pagesize > 0:
            numpages = ceil(self.count/self.pagesize)
            self.numpages = numpages
            if self.page > numpages or self.page == 0:
                self.page = 1

            end_index = (self.pagesize * self.page)
            if end_index > self.count:
                end_index = self.count
            start_index = (self.pagesize * (self.page-1))

        # Retrieve elements by index bounds
        self.cards = self.cards[start_index:end_index]

        # print(start_index, ' ', end_index)


    def get_list(self):
       
        return self.cards

    def get_count(self):
       
        return self.count

    def get_numpages(self):
       
        return self.numpages