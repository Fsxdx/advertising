select start_month, start_year, end_month, end_year
from advertising.order_row
where billboard_id = "$billboard_id";