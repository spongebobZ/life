class Config:
    class ConfigError(TypeError): pass

    def __setattr__(self, key, value):
        if key in self.__dict__:
            raise self.ConfigError('can not update exist key')
        self.__dict__[key] = value


cnf = Config()
cnf.t_rourou = './data/rourou.csv'
cnf.t_wallet = './data/wallet.csv'
cnf.t_rou_wallet = './data/rou_wallet.csv'
cnf.t_seller = './data/seller.csv'
cnf.t_orders = './data/orders.csv'
cnf.t_product_prior = './data/product_prior.csv'
cnf.t_product = './data/product.csv'
cnf.es_host = 'master'
cnf.es_port = 9200
# es offline type
cnf.es_type_order_count = 'order_count'
cnf.es_type_topn_product = 'topn_products'
cnf.es_type_reg = 'reg'
cnf.es_type_dau = 'login'
# es online index
cnf.es_index_today_order_count = 'today_order_count'
cnf.es_index_today_topn_product = 'today_topn_product'
cnf.es_index_today_reg = 'today_reg'
cnf.es_index_today_dau = 'today_dau'
