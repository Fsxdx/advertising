select $db_columns
from advertising.$table
where year = "$year"
  and month = "$month";