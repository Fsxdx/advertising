select billboard_id, price_per_month, size, billboard_address, quality
from advertising.billboards
where (price_per_month > "$min_price" or "$min_price" = '')
  and (price_per_month < "$max_price" or "$max_price" = '')
  and billboard_address like "%. $city,%"
  and (quality > "$min_quality" or "$min_quality" = '')
  and (quality < "$max_quality" or "$max_quality" = '')
  and (size > "$min_size" or "$min_size" = '')
  and (size < "$max_size" or "$max_size" = '');