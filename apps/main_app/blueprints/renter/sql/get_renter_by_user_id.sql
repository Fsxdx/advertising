select renter_id, first_name, last_name, phone_number, renter_address, business_sphere, user_id
from advertising.renters
where user_id = "%user_id"