
#!/usr/bin/env python3
from datetime import datetime, timedelta

class DomainNameRegistry:
  """ A simple domain name registry system """
  def __init__(self, providers, customers):
    # Providers are stored in the form {"provider-name": contact-id} with each 
    # provider having a specific format for contact-id.
    self.providers = providers
    self.customers = customers # customers and their balances, format {"customer-abc":0}
    self.domains = {} # format {"domain.com" : DomainName object}
    self.registration_cost = 40 # $40 for 1 year

  def display_providers(self):
    for provider_name in self.providers.keys():
      print(provider_name)

  def display_domains(self):
    for domain_obj in self.domains.values():
      print(domain_obj)

  def display_customer_balances(self):
    for customer_id, balance in self.customers.items():
      print(f"{customer_id} balance: ${balance}")

  def register_domain(self, request):
    """
    Functionality #1: Domain name registration
    
    ● Request in one of two formats:

    1)
      {
        "domain_name": "domain.com", 
        "period_of_registration": {"years":1, "months":0, "days":0},
        "verification_provider": "provider-abc",
        "contact-id": [contact_id],
        "customer_id": "customer-abc"
      }
        contact_id could be any object, contained within a list to represent that

     or

    2)
      { 
        "domain_name": "gAAAAABdjSdoqn4kx6XMw_fMx5YT2eaeBBCEue3N2F", 
        "period_of_registration": {"years":1, "months":0, "days":0},
        "verification_provider": "provider-ghi",
        "customer_id": "customer-def"
      }

    ● Response (return):
      {
        "domain_name": "domain expiration date"
      }

      or

      "ERROR message"
    """
    domain_name = request["domain_name"]
    period_of_registration = request["period_of_registration"]
    customer_id = request["customer_id"]

    if len(domain_name) < 10:
      return print_and_return(f"ERROR registering {domain_name}: domain_name must be at least 10 characters")

    if request.get("contact-id"):
      contact_id = request.get("contact-id")[0]
    else:
      # request must be of type #2 above, encrypted value for concatenated domain name and contact-id

      # decrypt value, set domain name and contact-id
      domain_and_contact_id = dummy_decrypt(request["domain_name"]).split()
      domain_name = domain_and_contact_id[0]

      if len(request["domain_name"]) < 10:
        return print_and_return("ERROR: domain_name must be at least 10 characters")

      contact_id = domain_and_contact_id[1]

    # Verify provided contact-id matches verification provider
    if not self.providers[request["verification_provider"]] == contact_id:
      return print_and_return(f"ERROR registering {domain_name}: provided contact-id does not match provider")

    # Add domain to registry
    new_domain = DomainName(domain_name, datetime.now(), period_of_registration)
    self.domains.update({domain_name: new_domain})

    # Add charge to customer's account
    self.customers[customer_id] += self.registration_cost * period_of_registration["years"] + \
                                   round(self.registration_cost/12, 2) * period_of_registration["months"] + \
                                   round(self.registration_cost/365, 4) * period_of_registration["days"]

    print(f"{customer_id} registered {domain_name} successfully.")
    
    return {domain_name: new_domain.get_expiration_date()}

  # Functionality 2: Information about domain name
  def get_domain_info(self, domain_name):
    """
    ● Request
      ○ domain name (like "art.software")
    ● Response (return):
      ○ domain name
      ○ domain expiration date
    """
    domain_in_registry = self.domains.get(domain_name)

    if domain_in_registry:
      return print_and_return(domain_in_registry)
    else:
      return print_and_return(f"ERROR getting domain info: domain {domain_name} not in registry")

  # Functionality 3: Renew domain name
  def renew_domain(self, request):
    """
    ● Request
      {
        "domain_name": "domain.com",
        "period_to_extend": {"years":1, "months":0, "days":0},
        "customer_id": "customer-def"
      }
    ● Response:
      ○ domain name
      ○ Domain expiration date
    """
    domain_name = request["domain_name"]
    period_to_extend = request["period_to_extend"]
    customer_id = request["customer_id"]

    domain_in_registry = self.domains.get(domain_name)

    if domain_in_registry:
      # Extend registration period of domain
      for time_unit in domain_in_registry.registration_period.keys():
        domain_in_registry.registration_period[time_unit] += period_to_extend[time_unit]

      # Add charge to customer's account
      self.customers[customer_id] += self.registration_cost * period_to_extend["years"] + \
                                          round(self.registration_cost/12, 2) * period_to_extend["months"] + \
                                          round(self.registration_cost/365, 4) * period_to_extend["days"]
      
      print(f"{customer_id} renewed {domain_name} successfully.")
    else:
      return print_and_return(f"ERROR renewing domain: domain {domain_name} not in registry")

  # Functionality 4: Delete domain name
  def delete_domain(self, domain_name):
    """
    Domain deletion​ :
    ● Request
      ○ domain name (like art.software)
    ● Response:
      ○ N/A - no additional response elements necessary other than standard feedback
        like success or failure.
    """
    if self.domains.get(domain_name):
      del self.domains[domain_name]
      print(f"Domain {domain_name} deleted successfully.")
    else:
      print(f"Domain {domain_name} not found in system.")
    
# Helper function to print and return a message
def print_and_return(message):
  print(message)
  return message

# Dummy function to simulate the process of a verification provider providing an encrypted token
def dummy_decrypt(message):
  return "validdomain.com 2285837176"

class DomainName:
  """ A simple domain name class """
  def __init__(self, name, registration_date, registration_period):

    if len(name) < 10:
      raise ValueError("Domain name must be at least 10 characters long.")
   
    self.name = name
    self.registration_date = registration_date # datetime object
    self.registration_period = registration_period # dictionary in the format {"years":1, "months":0, "days":0}
  
  # String representation for end user
  def __str__(self):
    return f"{self.name}\nExpiration date: {self.get_expiration_date()}"
    
  # Calculate and return expiration date
  def get_expiration_date(self):
    # Convert years and months specified by registration period into days
    # For simplicity's sake we're assuming a month has a 365/12 days
    days_until_expiration = (365 * self.registration_period["years"]) + ((365/12) * self.registration_period["months"]) + self.registration_period["days"]
    
    return self.registration_date + timedelta(days=days_until_expiration)

## Initialized domain name registry with pre-determined providers and contact-id's
def init_domain_name_registry():
  dnr_system = DomainNameRegistry({
    "provider-abc":39838576, "provider-def":"xNOqwuGr", "provider-ghi":"2285837176",
    "provider-jkl":[2891384], "provider-mno":{"gQqkZQnOt": True}, "provider-pqr":29282743,
    "provider-stu":"a e u 7 q x", "provider-vwx":[[[]]], "provider-123":(1, 2, 3),
    "provider-124":"19674649", "provider-125":"xNOqwuGr", "provider-126":39838576,
    "provider-127":93017347, "provider-128":"[[[]]]]]]]", "provider-129":929222922
    },
    {
      "customer-abc":0, "customer-def": 0
    })
  
  return dnr_system


if __name__ == "__main__":
  dnr_system = init_domain_name_registry()
  
  print("*** Providers in system")
  dnr_system.display_providers()
  print()

  print(f"*** Attempting to register domains with cost ${dnr_system.registration_cost} per year..")
  # Successful domain registrations
  dnr_system.register_domain({
    "domain_name": "domaindomain.com", 
    "period_of_registration": {"years":1, "months":0, "days":0},
    "verification_provider": "provider-abc",
    "contact-id": [39838576],
    "customer_id": "customer-abc"
   })

  dnr_system.register_domain({
    "domain_name": "exampletwodomain.com",
    "period_of_registration": {"years":2, "months":6, "days":0},
    "verification_provider": "provider-def",
    "contact-id": ["xNOqwuGr"],
    "customer_id": "customer-def"
   })

  dnr_system.register_domain({
    "domain_name": "threedomain.com", 
    "period_of_registration": {"years":0, "months":0, "days":200},
    "verification_provider": "provider-mno",
    "contact-id": [{"gQqkZQnOt": True}],
    "customer_id": "customer-def"
   })

  print()
  print("*** Attempting registration with dummy encrypted token instead of contact_id..")
  # Request using a dummy encrypted token instead of contact-id
  dnr_system.register_domain({
    "domain_name": "gAAAAABdjSdoqn4kx6XMw_fMx5YT2eaeBBCEue3N2F", 
    "period_of_registration": {"years":1, "months":0, "days":0},
    "verification_provider": "provider-ghi",
    "customer_id": "customer-def"
   })

  print()
  print("*** Registering invalid domains...")
  # Domain names that fail to register
  dnr_system.register_domain({
    "domain_name": "one.com", # Domain name too short
    "period_of_registration": {"years":0, "months":0, "days":200},
    "verification_provider": "provider-mno",
    "contact-id": [{"gQqkZQnOt": True}],
    "customer_id": "customer-abc"
   })

  dnr_system.register_domain({
    "domain_name": "fourfourfour.com", 
    "period_of_registration": {"years":2, "months":12, "days":0},
    "verification_provider": "provider-mno",
    "contact-id": ["invalid contact id"], # Contact_id invalid
    "customer_id": "customer-abc"
   })

  print()
  print("*** Domains in system")
  dnr_system.display_domains()
  print()

  print("*** Getting domain info of non-existent domain")
  dnr_system.get_domain_info("doesntexist.com")
  print()

  print("*** Getting domain info of existing domain")
  dnr_system.get_domain_info("domaindomain.com")
  print()

  print("*** Customers and balances in system")
  dnr_system.display_customer_balances()
  print()

  print("*** Deleting domain 'domaindomain.com'")
  dnr_system.delete_domain("domaindomain.com")
  dnr_system.get_domain_info("domaindomain.com")
  print()

  print("*** Deleting domain that doesn't exist in system")
  dnr_system.delete_domain("nonexistent.com")
  dnr_system.get_domain_info("nonexistent.com")
  print()

  print("*** Renewing domain for 1 year")
  print("Domain info before renew:")
  dnr_system.get_domain_info("validdomain.com")
  print()

  dnr_system.renew_domain({"domain_name": "validdomain.com", "period_to_extend": {"years":1, "months":0, "days":0}, "customer_id": "customer-def"})
  
  print("Domain info after renew:")
  dnr_system.get_domain_info("validdomain.com")
  print()

  print("*** Customers and balances in system")
  dnr_system.display_customer_balances()