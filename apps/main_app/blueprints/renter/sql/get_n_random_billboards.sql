SELECT billboard_id, price_per_month, size, billboard_address, mount_date, quality, owner_id
  FROM advertising.billboards
 ORDER BY RAND()
 LIMIT 6;
