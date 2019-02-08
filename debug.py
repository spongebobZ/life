import tools

r=tools.query_es_by_match('xfy','order_count',{'order_date':'2019-01-06'},'order_count','order_date1')
print(type(r))