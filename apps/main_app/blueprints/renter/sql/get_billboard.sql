select billboard_id, price_per_month, size, billboard_address, mount_date, quality, owner_id
from advertising.billboards
where billboard_id="$billboard_id";