from common import signin_index_valid
import random
import time

if __name__ == '__main__':
    firstname_list = [
        '赵', '钱', '孙', '李', '周', '吴', '郑', '王', '冯', '陈', '褚', '卫', '蒋', '沈', '韩', '杨', '朱', '秦', '尤', '许',
        '何', '吕', '施', '张', '孔', '曹', '严', '华', '金', '魏', '陶', '姜', '戚', '谢', '邹', '喻', '柏', '水', '窦', '章',
        '云', '苏', '潘', '葛', '奚', '范', '彭', '郎', '鲁', '韦', '昌', '马', '苗', '凤', '花', '方', '俞', '任', '袁', '柳',
        '酆', '鲍', '史', '唐', '费', '廉', '岑', '薛', '雷', '贺', '倪', '汤', '滕', '殷', '罗', '毕', '郝', '邬', '安', '常',
        '乐', '于', '时', '傅', '皮', '卞', '齐', '康', '伍', '余', '元', '卜', '顾', '孟', '平', '黄', '和', '穆', '萧', '尹',
        '姚', '邵', '堪', '汪', '祁', '毛', '禹', '狄', '米', '贝', '明', '臧', '计', '伏', '成', '戴', '谈', '宋', '茅', '庞',
        '熊', '纪', '舒', '屈', '项', '祝', '董', '梁']
    lastname_list = ['雅婷', '雅雯', '怡婷', '雅惠', '心怡', '佳蓉', '静怡', '雅玲', '俊宏', '怡伶', '俊杰', '怡如', '静宜', '冠宇', '诗婷', '承翰',
                     '佳慧',
                     '宜君', '雅文', '韵如', '俊贤', '淑芬', '家铭', '冠廷', '怡萱', '婷婷', '淑娟', '威廷', '淑惠', '哲玮', '淑婷', '佳桦', '嘉玲',
                     '雅芳',
                     '慧君', '俊豪', '哲维', '家瑜', '宜静', '佳琪', '淑君', '冠宏', '惠君', '嘉宏', '雅筑', '慧玲', '欣颖', '惠如', '明哲', '孟儒',
                     '俊宇',
                     '欣宜', '志鸿', '宗霖', '俊毅', '玮婷', '美君', '建良', '建铭', '志强', '佳雯', '仁杰', '志铭', '智凯', '思妤', '士杰', '建宇',
                     '淑萍',
                     '伟哲', '文杰', '博文', '淑华', '郁涵', '志远', '嘉慧', '宇轩', '玉玲', '思婷', '雅芬', '莉婷', '志明', '淑贞', '家宏', '明宏',
                     '舒婷',
                     '书玮', '冠霖', '俊铭', '雅如', '佩颖', '姿吟', '家维', '凯文', '建文', '怡秀', '佳容', '宗颖', '婉君', '智杰', '凯婷', '世伟',
                     '俊彦',
                     '彦儒', '蕙如', '琼文', '俊玮', '哲豪', '芳如', '家伟', '佩桦', '圣文', '郁文', '秀玲', '嘉伟', '馨慧', '英杰', '怡萍', '美惠',
                     '振宇',
                     '家慧', '文彬', '宜臻', '明宪', '家庆', '姿莹', '姿伶', '佩怡', '佳静', '欣洁', '柏廷', '盈如', '慧婷', '子翔', '淑芳', '柏宇',
                     '佳惠',
                     '慧珊', '彦良', '晓雯', '建中', '子轩', '俊德', '宗贤', '彦伶', '建安', '哲铭', '育如', '志文', '怡臻', '佩芳', '宜真', '庭玮',
                     '君豪',
                     '孟颖', '威宇', '俊达', '美芳', '伟诚', '嘉鸿', '家华', '志杰', '舒涵', '志忠', '雯婷', '秀娟', '家弘', '政达', '佩真', '意婷',
                     '育贤',
                     '慧敏', '宜洁', '冠伶', '佳燕', '孟洁', '惠萍', '淑雯', '雅菁', '惠敏', '珮珊', '嘉雯', '国豪', '志贤', '静如', '佩琪', '明勳',
                     '晓君',
                     '佳琳', '明慧', '怡桦', '子杰', '宛儒', '冠儒', '伟翔', '逸群', '家祥', '博仁', '念慈', '柏翔', '玫君', '竹君', '于庭', '雅淳',
                     '晓薇',
                     '家贤', '宛真', '佳芸', '玮伦', '钰雯', '丽娟', '维哲', '伟杰', '莉雯', '淑真', '伟铭', '佳宜', '思洁', '仁豪', '玉珊', '玮玲',
                     '柏钧',
                     '政宪', '耀文', '建华', '姿仪', '欣瑜', '佩雯', '佳勳', '韵婷', '佳纯', '建佑', '珮琪', '蕙君', '婉菁', '雅欣', '彦文', '婉玲',
                     '育德',
                     '欣慧', '政霖', '倩如', '彦志', '建兴', '明达', '子扬', '馨文', '柏凯', '彦甫', '雅晴', '彦宇', '美华', '俊翰', '文贤', '怡蓉',
                     '子涵',
                     '慧真', '思贤', '晓菁', '婉茹', '思莹', '鸿文', '俊荣', '欣儒', '郁珊', '佩儒', '育民', '明贤', '琼仪', '耀仁', '育铭', '依璇',
                     '孟桦',
                     '静芬', '俊颖', '思桦', '育瑄', '玟君', '文正', '健铭', '俊仁', '诗怡', '家琪', '彦勳', '宗哲', '俊维', '智钧', '郁翔',
                     '俊安', '冠华', '俊明', '佳瑜', '家欣', '景翔', '怡颖', '育萱', '秉勳', '峻玮', '柏元', '宗达', '佳璇', '致远', '淑卿', '晓萍',
                     '香君',
                     '钰涵', '耀德', '冠中', '诗雅', '冠豪', '峻豪', '志祥', '家纬', '筱君', '依萍', '逸凡', '慧芳', '宛臻', '书维', '淑珍', '婉甄',
                     '慧珍',
                     '伟智', '晓琪', '心瑜', '丽如', '昱宏', '郁芳', '政哲', '靖雅', '佩伶', '怡祯', '俊吉', '宏达', '雅钧', '玟伶', '宜芬', '婷',
                     '柏青',
                     '佳臻', '佳吟', '庭瑜', '玉雯', '文斌', '嘉琳', '郁欣', '馨莹', '彦婷', '宗桦', '育豪', '怡妏', '明德', '耀中', '启宏', '建明',
                     '雅莉',
                     '宜颖', '淑怡', '静慧', '惠琪', '雅娟', '志翔', '俊儒', '国伟', '俊宪', '慧文', '志仁', '美琪', '安妮', '博凯', '凤仪', '博元',
                     '俊雄',
                     '维真', '伟志', '淑美', '珮瑄', '宗祐', '彦博', '裕仁', '铭鸿', '俊龙', '建璋', '士弘', '力玮', '奕君', '博钧', '宏仁', '哲安',
                     '瑞鸿',
                     '怡玲', '诗雯', '嘉骏', '政儒', '智强', '昆霖', '文龙', '胜杰', '俐伶', '育廷', '怡贞', '凯雯', '家宁', '于真', '晋嘉', '佩萱',
                     '嘉芸',
                     '虹君', '玉菁', '秀芬', '懿萱', '奕安', '伟民', '秀婷', '承勳', '建忠', '建男', '妍伶', '宏文', '信良', '鼎钧', '佩容', '宜珍',
                     '淑仪',
                     '美吟', '智勇', '玉洁', '育儒', '巧雯', '明宗', '欣蓓', '嘉仁', '怡珍', '婉萍', '世贤', '彦佑', '柏儒', '明璋', '宜轩', '建纬',
                     '孟娟',
                     '珊珊', '佳盈', '佳翰', '仁宏', '信安', '思嘉', '惠芳', '文心', '雅琴', '瑞祥', '慧怡', '建甫', '政颖', '明君', '孟芳', '凯伦',
                     '宛玲',
                     '玉琳', '美仪', '佳音', '明修', '宜蓉', '昱辰', '政伟', '自强', '丽华', '婉真', '柏辰', '伟婷', '宛庭', '家源', '玉华', '品洁',
                     '子维',
                     '晓岚', '子婷', '宛婷', '婉琪', '惠美', '圣哲', '明鸿', '柏村', '珮玲', '薇如', '依静', '美秀', '志平', '韦翔', '柏贤', '晋玮',
                     '家骏',
                     '俊仪', '雅琦', '宛谕', '柏任', '钰珊', '书婷', '信杰', '慧慈']

    while True:
        firstname = random.sample(firstname_list, 1)
        lastname = random.sample(lastname_list, 1)
        name = ''.join(firstname + lastname)
        password = random.randint(1000, 9998)
        signin_index_valid(name, password, password)
        time.sleep(random.randint(1, 10))
